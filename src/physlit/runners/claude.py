"""Anthropic / Claude runner.

Pins ``claude-opus-4-7`` per ``predictions/v0_1_prereg.md`` lock at
2026-05-09. Anthropic has not yet published a date-stamped 4.7
variant; the bare alias *is* the most-specific identifier the API
exposes. Each ``call_model`` constructs a fresh ``anthropic.Anthropic``
client; do not refactor toward a shared client without revisiting the
methodology.
"""

from __future__ import annotations

import os

import anthropic

from physlit.runners.base import CallResult, TestedModelRunner

CLAUDE_MODEL_ID = "claude-opus-4-7"

# Approximate Anthropic Opus 4.7 token pricing (USD per million tokens).
# These are estimates for the cost log only — Anthropic's invoice is
# authoritative. Update if pricing changes; do not silently re-tune.
CLAUDE_INPUT_PRICE_PER_MTOK = 15.0
CLAUDE_OUTPUT_PRICE_PER_MTOK = 75.0


class ClaudeRunner(TestedModelRunner):
    """Single Anthropic Opus 4.7 call. No retry, no caching, no streaming.

    Opus 4.7 has deprecated the ``temperature`` parameter; the runner
    accepts a ``temperature`` argument and records the requested value
    on the ``TrialRecord``, but does not pass it to the API. See
    ``analysis/dryrun_findings.md`` §4.1 for the methodology footnote.
    """

    @property
    def model_family(self) -> str:
        return "anthropic"

    @property
    def model_id(self) -> str:
        return CLAUDE_MODEL_ID

    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> CallResult:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set (check .env.local or shell env)")
        client = anthropic.Anthropic(api_key=api_key)  # FRESH per call
        del temperature  # API rejects this param on Opus 4.7
        msg = client.messages.create(
            model=self.model_id,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        # Concatenate text from any text blocks. Some response types may
        # contain non-text blocks (tool use, thinking, etc.) — those are
        # skipped here. We don't enable any of those for v0.1.
        parts: list[str] = []
        for block in msg.content:
            text = getattr(block, "text", None)
            if isinstance(text, str):
                parts.append(text)
        response_text = "".join(parts)

        # R1(a) audit: Anthropic exposes a single identity field on the
        # response. Capture it explicitly so future SDK changes that add
        # additional identifiers can be merged into this dict.
        identity_fields: dict[str, str] = {"response_model": str(msg.model)}

        usage_in = int(getattr(msg.usage, "input_tokens", 0)) if msg.usage else 0
        usage_out = int(getattr(msg.usage, "output_tokens", 0)) if msg.usage else 0
        return CallResult(
            response_text=response_text,
            primary_id=str(msg.model),
            identity_fields=identity_fields,
            input_tokens=usage_in,
            output_tokens=usage_out,
        )

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * CLAUDE_INPUT_PRICE_PER_MTOK / 1_000_000
            + output_tokens * CLAUDE_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )
