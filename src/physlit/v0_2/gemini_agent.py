"""Gemini 3.1 Pro as v0.2 disagree-resolver agent.

Used for both Agent 1 (content-axis disagree resolution) and Agent 2
(structural-axis disagree resolution). Per the prereg, both agents
are the *same model* — the difference is which prompt template the
runner passes in.

Methodologically a stateless JSON-out evaluator, so this class
subclasses ``JudgeBase`` to reuse ``judge_one`` orchestration + the
``JudgeVerdict`` save format. The `judge_family` field in the saved
verdict is set to `"google"`; the `stage` field is set to
`"agent1_content"` or `"agent2_structural"` to disambiguate the role
the agent was playing on a given call.
"""

from __future__ import annotations

import os

from google import genai
from google.genai import types as genai_types

from physlit.judges.judge_base import JudgeBase
from physlit.runners.gemini import (
    GEMINI_INPUT_PRICE_PER_MTOK,
    GEMINI_MODEL_ID,
    GEMINI_OUTPUT_PRICE_PER_MTOK,
)

# Per the v0.2 prereg, the resolver model is pinned to the same
# identifier verified in v0.1's Phase 1.5 dry-run paper trail.
GEMINI_AGENT_MODEL_ID = GEMINI_MODEL_ID

# Anthropic / OpenAI judges accept up to 2048 max_tokens by convention.
# Agent verdicts are structured JSON with rationale — match the
# allowance, with room for the slightly larger N11 evidence quotes
# that Agent 2 may emit.
DEFAULT_AGENT_MAX_TOKENS = 2048


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
        client = genai.Client(api_key=api_key)  # FRESH per call

        response = client.models.generate_content(
            model=self.judge_model,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                max_output_tokens=max_tokens,
            ),
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
