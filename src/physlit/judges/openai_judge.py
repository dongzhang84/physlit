"""GPT-5.5 as v0.1 judge — same model class as the tested OpenAIRunner."""

from __future__ import annotations

import os

import openai

from physlit.judges.judge_base import JudgeBase
from physlit.runners.openai import (
    OPENAI_INPUT_PRICE_PER_MTOK,
    OPENAI_MODEL_ID,
    OPENAI_OUTPUT_PRICE_PER_MTOK,
)


class OpenAIJudge(JudgeBase):
    """GPT-5.5 acting as judge. Same model id as the tested runner."""

    @property
    def judge_family(self) -> str:
        return "openai"

    @property
    def judge_model(self) -> str:
        return OPENAI_MODEL_ID

    def call_judge(self, prompt: str, max_tokens: int) -> tuple[str, int, int]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        client = openai.OpenAI(api_key=api_key)  # FRESH per call
        try:
            response = client.chat.completions.create(
                model=self.judge_model,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=max_tokens,
                reasoning_effort="none",
            )
        except TypeError:
            response = client.chat.completions.create(
                model=self.judge_model,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=max_tokens,
            )
        if response.model != self.judge_model:
            raise RuntimeError(
                f"OpenAI judge identity mismatch: configured {self.judge_model!r}, "
                f"API returned {response.model!r}"
            )
        choice = response.choices[0]
        text = choice.message.content or ""
        usage = response.usage
        in_tok = int(usage.prompt_tokens) if usage else 0
        out_tok = int(usage.completion_tokens) if usage else 0
        return text, in_tok, out_tok

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * OPENAI_INPUT_PRICE_PER_MTOK / 1_000_000
            + output_tokens * OPENAI_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )
