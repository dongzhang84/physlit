"""Anthropic / Claude runner.

Pins ``claude-opus-4-7-20260101`` per ``CLAUDE.md`` (no aliases). Each
``call_model`` constructs a fresh ``anthropic.Anthropic`` client; do not
refactor toward a shared client without revisiting the methodology.
"""

from __future__ import annotations

import os

import anthropic

from physlit.runners.base import TestedModelRunner

CLAUDE_MODEL_ID = "claude-opus-4-7-20260101"

# Approximate Anthropic Opus 4.7 token pricing (USD per million tokens).
# These are estimates for the cost log only — Anthropic's invoice is
# authoritative. Update if pricing changes; do not silently re-tune.
CLAUDE_INPUT_PRICE_PER_MTOK = 15.0
CLAUDE_OUTPUT_PRICE_PER_MTOK = 75.0

# Char-to-token approximation. English text is ~4 characters per token
# on Claude's tokenizer. Off by ~20% in either direction is fine for
# budget gating.
_CHARS_PER_TOKEN = 4


class ClaudeRunner(TestedModelRunner):
    """Single Anthropic Opus 4.7 call. No retry, no caching, no streaming."""

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
    ) -> tuple[str, str]:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set (check .env.local or shell env)")
        client = anthropic.Anthropic(api_key=api_key)  # FRESH per call
        msg = client.messages.create(
            model=self.model_id,
            max_tokens=max_tokens,
            temperature=temperature,
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
        return response_text, msg.model

    def estimate_cost(self, prompt: str, response: str) -> float:
        in_tok = max(1, len(prompt) // _CHARS_PER_TOKEN)
        out_tok = max(1, len(response) // _CHARS_PER_TOKEN)
        return (
            in_tok * CLAUDE_INPUT_PRICE_PER_MTOK / 1_000_000
            + out_tok * CLAUDE_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )
