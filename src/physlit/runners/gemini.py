"""Google / Gemini 3.1 Pro Preview runner.

Pins ``gemini-3.1-pro-preview`` (the **specific ID**, not the family
alias ``gemini-3-pro-preview``) per ``predictions/v0_1_prereg.md``
lock at 2026-05-09. The alias was rejected because at ping time on
2026-05-09 it was found to auto-resolve to ``gemini-3.1-pro-preview``
— pinning the alias would have hidden underlying-model drift behind
a strict-equality check that always passes; see
``analysis/dryrun_findings.md`` §8 for the paper trail.

R1(a) per-call identity capture (per
``docs/v0_1_runner_requirements.md``) is implemented by recording
every model-identity field the SDK exposes and surfacing them on the
``CallResult.identity_fields`` dict. The base class ``run_trial``
performs the strict equality check and halts the run on mismatch.
"""

from __future__ import annotations

import os
import time

from google import genai
from google.genai import types as genai_types

from physlit.runners.base import CallResult, TestedModelRunner

# Retry policy for transient Gemini API failures (e.g. 503 UNAVAILABLE
# from "high demand" capacity throttling, observed 2026-05-09 during
# calibration). Methodology: a retry that succeeds is still one trial
# under the prereg's "fresh API client per call" rule, because each
# retry constructs a new ``genai.Client``. Non-transient failures
# (e.g. authentication, quota exhaustion, identity drift) propagate
# unchanged.
_RETRY_BACKOFF_SECONDS = (5, 10, 20)
_RETRYABLE_TOKENS = ("503", "unavailable", "high demand")

GEMINI_MODEL_ID = "gemini-3.1-pro-preview"

# Approximate Gemini 3.1 Pro pricing (USD per million tokens), placeholder.
# Google's invoice is authoritative; placeholder constants only feed into
# the audit ``cost_usd_estimate`` field.
GEMINI_INPUT_PRICE_PER_MTOK = 5.0
GEMINI_OUTPUT_PRICE_PER_MTOK = 20.0


class GeminiRunner(TestedModelRunner):
    """Single Gemini 3.1 Pro Preview call. No retry, no caching, no streaming.

    The vendor identity dict captures ``response.model_version`` plus
    any per-candidate identity field the SDK surfaces, supporting R1(a)
    audit. The base ``run_trial`` raises if ``response.model_version``
    differs from :data:`GEMINI_MODEL_ID`, halting the run before a
    drifted model can contaminate subsequent trials.
    """

    @property
    def model_family(self) -> str:
        return "google"

    @property
    def model_id(self) -> str:
        return GEMINI_MODEL_ID

    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> CallResult:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY / GOOGLE_API_KEY not set (check .env.local or shell env)"
            )
        del temperature  # v0.1 uses default sampling across all vendors
        config = genai_types.GenerateContentConfig(max_output_tokens=max_tokens)

        # Retry transient 503 / UNAVAILABLE errors with exponential backoff.
        # Each attempt constructs a fresh ``genai.Client``, preserving the
        # "fresh API client per call" methodology rule.
        last_exc: Exception | None = None
        response = None
        for attempt, backoff_s in enumerate((0, *_RETRY_BACKOFF_SECONDS)):
            if backoff_s:
                time.sleep(backoff_s)
            client = genai.Client(api_key=api_key)
            try:
                response = client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=config,
                )
                break
            except Exception as exc:
                last_exc = exc
                msg = str(exc).lower()
                retryable = any(token in msg for token in _RETRYABLE_TOKENS)
                if not retryable or attempt >= len(_RETRY_BACKOFF_SECONDS):
                    raise
        if response is None:
            raise RuntimeError(
                f"Gemini retry exhausted after {len(_RETRY_BACKOFF_SECONDS) + 1} "
                f"attempts: {last_exc}"
            )

        # Extract text from the first candidate. google-genai exposes a
        # convenience .text property that concatenates text parts; if it
        # is missing, fall back to manual concatenation.
        response_text = ""
        text_attr = getattr(response, "text", None)
        if isinstance(text_attr, str) and text_attr:
            response_text = text_attr
        elif response.candidates:
            parts: list[str] = []
            for candidate in response.candidates:
                content = getattr(candidate, "content", None)
                if content is None:
                    continue
                for part in getattr(content, "parts", []) or []:
                    text = getattr(part, "text", None)
                    if isinstance(text, str):
                        parts.append(text)
            response_text = "".join(parts)

        # R1(a) audit: capture every model-identity field the SDK surfaces.
        # As of google-genai at v0.1 build, the primary one is
        # ``response.model_version``; we also record any per-candidate
        # identifiers that may be present.
        identity_fields: dict[str, str] = {}
        primary = getattr(response, "model_version", None)
        if isinstance(primary, str):
            identity_fields["response_model_version"] = primary
        # Some SDK versions expose ``response.model``; capture if present
        alt_model = getattr(response, "model", None)
        if isinstance(alt_model, str):
            identity_fields["response_model"] = alt_model
        # Per-candidate identity fields (deployment id, etc.)
        for i, candidate in enumerate(response.candidates or []):
            for attr in ("deployment_id", "model_version", "model"):
                value = getattr(candidate, attr, None)
                if isinstance(value, str):
                    identity_fields[f"candidate_{i}_{attr}"] = value

        usage = getattr(response, "usage_metadata", None)
        input_tokens = int(getattr(usage, "prompt_token_count", 0) or 0)
        output_tokens = int(getattr(usage, "candidates_token_count", 0) or 0)

        primary_id = identity_fields.get("response_model_version") or self.model_id
        return CallResult(
            response_text=response_text,
            primary_id=primary_id,
            identity_fields=identity_fields,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * GEMINI_INPUT_PRICE_PER_MTOK / 1_000_000
            + output_tokens * GEMINI_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )

    def r1b_post_run_ping(self) -> dict[str, str]:
        """R1(b) post-trial-set re-ping. Sends one minimal request and
        captures the same identity fields as a regular call would. The
        orchestrator compares the result to the lock-time identifier
        and writes the disclosure into ``analysis/v0_1_findings.md``.

        Mirrors the parameters of ``scripts/discover_model_versions.py``
        (``"hi"``, ``max_output_tokens=16``).
        """
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY / GOOGLE_API_KEY not set for R1(b) re-ping")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=self.model_id,
            contents="hi",
            config=genai_types.GenerateContentConfig(max_output_tokens=16),
        )
        out: dict[str, str] = {}
        primary = getattr(response, "model_version", None)
        if isinstance(primary, str):
            out["response_model_version"] = primary
        alt_model = getattr(response, "model", None)
        if isinstance(alt_model, str):
            out["response_model"] = alt_model
        return out
