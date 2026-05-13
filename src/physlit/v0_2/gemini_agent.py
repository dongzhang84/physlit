"""Gemini 2.5 Pro as v0.2.1 disagree-resolver agent.

Used for both Agent 1 (content-axis disagree resolution) and Agent 2
(structural-axis disagree resolution). Per the v0.2.1 prereg, both
agents are the *same model* — the difference is which prompt template
the runner passes in.

Methodologically a stateless JSON-out evaluator, so this class
subclasses ``JudgeBase`` to reuse ``judge_one`` orchestration + the
``JudgeVerdict`` save format. The `judge_family` field in the saved
verdict is set to `"google"`; the `stage` field is set to
`"agent1_content"` or `"agent2_structural"` to disambiguate the role
the agent was playing on a given call.

Model history:
- v0.2 (prereg-v0.2-locked): `gemini-3.1-pro-preview` — preview tier,
  retired after sustained `503 UNAVAILABLE` throttle on 2026-05-13.
- v0.2.1 (prereg-v0.2.1-locked, current): `gemini-2.5-pro` — GA tier,
  one generation behind. See `predictions/v0_2_1_prereg.md` §0 for the
  deviation rationale.

Reproducers of v0.2 (the original locked tag) should `git checkout
prereg-v0.2-locked`, which keeps the file at its v0.2 state.
"""

from __future__ import annotations

import os
import time

from google import genai
from google.genai import types as genai_types

from physlit.judges.judge_base import JudgeBase

# Per the v0.2.1 prereg envelope. Reverting to `gemini-3.1-pro-preview`
# (v0.2) requires a new prereg version, not an in-place edit.
GEMINI_AGENT_MODEL_ID = "gemini-2.5-pro"

# Approximate Gemini 2.5 Pro pricing (USD per million tokens),
# placeholder for the audit cost_usd_estimate field. Google's invoice
# is authoritative. As of 2026-05-13, public list price for 2.5 Pro is
# $1.25/M input / $5.00/M output (≤200K context).
GEMINI_INPUT_PRICE_PER_MTOK = 1.25
GEMINI_OUTPUT_PRICE_PER_MTOK = 5.00

# Anthropic / OpenAI judges accept up to 2048 max_tokens by convention.
# Agent verdicts are structured JSON with rationale — match the
# allowance, with room for the slightly larger N11 evidence quotes
# that Agent 2 may emit.
DEFAULT_AGENT_MAX_TOKENS = 2048

# Retry policy for transient Gemini API failures (e.g. 503 UNAVAILABLE
# from "high demand" capacity throttling). Mirrors
# `runners/gemini.py`'s convention; each retry constructs a fresh
# client, so "fresh API client per call" still holds. Non-transient
# failures (auth, quota, identity mismatch) propagate unchanged.
_RETRY_BACKOFF_SECONDS = (5, 10, 20)
_RETRYABLE_TOKENS = ("503", "unavailable", "high demand")


class GeminiAgent(JudgeBase):
    """Gemini 3.1 Pro Preview acting as a v0.2 resolver agent."""

    @property
    def judge_family(self) -> str:
        return "google"

    @property
    def judge_model(self) -> str:
        return GEMINI_AGENT_MODEL_ID

    def call_judge(self, prompt: str, max_tokens: int) -> tuple[str, int, int]:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY / GOOGLE_API_KEY not set (check .env.local or shell env)"
            )

        config = genai_types.GenerateContentConfig(max_output_tokens=max_tokens)

        response = None
        last_exc: Exception | None = None
        for attempt, backoff_s in enumerate((0, *_RETRY_BACKOFF_SECONDS)):
            if backoff_s:
                time.sleep(backoff_s)
            client = genai.Client(api_key=api_key)  # FRESH per call (including retries)
            try:
                response = client.models.generate_content(
                    model=self.judge_model,
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
                f"Gemini agent retry exhausted after {len(_RETRY_BACKOFF_SECONDS) + 1} "
                f"attempts: {last_exc}"
            )

        # Strict pin: agent response must come from the pinned model.
        returned = getattr(response, "model_version", None) or getattr(response, "model", None)
        if returned and returned != self.judge_model:
            raise RuntimeError(
                f"Gemini agent identity mismatch: configured {self.judge_model!r}, "
                f"API returned {returned!r}"
            )

        text = response.text or ""
        usage = getattr(response, "usage_metadata", None)
        in_tok = int(getattr(usage, "prompt_token_count", 0)) if usage else 0
        out_tok = int(getattr(usage, "candidates_token_count", 0)) if usage else 0
        return text, in_tok, out_tok

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * GEMINI_INPUT_PRICE_PER_MTOK / 1_000_000
            + output_tokens * GEMINI_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )
