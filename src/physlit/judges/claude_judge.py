"""Claude as v0.1 judge — same model class as the tested ClaudeRunner."""

from __future__ import annotations

import os

import anthropic

from physlit.judges.judge_base import JudgeBase
from physlit.runners.claude import (
    CLAUDE_INPUT_PRICE_PER_MTOK,
    CLAUDE_MODEL_ID,
    CLAUDE_OUTPUT_PRICE_PER_MTOK,
)


class ClaudeJudge(JudgeBase):
    """Claude Opus 4.7 acting as judge. Same model id as the tested
    runner; the methodology rationale is that one of the two judges
    being structurally identical to one of the tested models is a
    feature — it surfaces self-evaluation bias as part of the IRR
    signal rather than hiding it."""

    @property
    def judge_family(self) -> str:
        return "anthropic"

    @property
    def judge_model(self) -> str:
        return CLAUDE_MODEL_ID

    def call_judge(self, prompt: str, max_tokens: int) -> tuple[str, int, int]:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        client = anthropic.Anthropic(api_key=api_key)  # FRESH per call
        msg = client.messages.create(
            model=self.judge_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        # Strict pin: judge response must come from the pinned model
        if msg.model != self.judge_model:
            raise RuntimeError(
                f"Claude judge identity mismatch: configured {self.judge_model!r}, "
                f"API returned {msg.model!r}"
            )
        parts: list[str] = []
        for block in msg.content:
            text = getattr(block, "text", None)
            if isinstance(text, str):
                parts.append(text)
        text = "".join(parts)
        in_tok = int(getattr(msg.usage, "input_tokens", 0)) if msg.usage else 0
        out_tok = int(getattr(msg.usage, "output_tokens", 0)) if msg.usage else 0
        return text, in_tok, out_tok

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * CLAUDE_INPUT_PRICE_PER_MTOK / 1_000_000
            + output_tokens * CLAUDE_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )
