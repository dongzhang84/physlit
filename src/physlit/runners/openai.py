"""OpenAI / GPT-5.5 runner.

Pins ``gpt-5.5-2026-04-23`` per ``predictions/v0_1_prereg.md`` lock at
2026-05-09. Each ``call_model`` constructs a fresh ``openai.OpenAI``
client.

GPT-5.5 is a reasoning model; the v0.1 protocol requests
``reasoning_effort="none"`` to keep behaviour comparable to the other
two vendors (which run at default sampling). Token counts come from
the ``response.usage`` block.
"""

from __future__ import annotations

import os

import openai

from physlit.runners.base import CallResult, TestedModelRunner

OPENAI_MODEL_ID = "gpt-5.5-2026-04-23"

# Approximate GPT-5.5 token pricing (USD per million tokens), placeholder.
# OpenAI's invoice is authoritative. These constants are wrong-by-some-factor
# but only feed into the ``cost_usd_estimate`` audit field; the v0.1 budget
# gate is not enforced through this number.
OPENAI_INPUT_PRICE_PER_MTOK = 5.0
OPENAI_OUTPUT_PRICE_PER_MTOK = 20.0


class OpenAIRunner(TestedModelRunner):
    """Single GPT-5.5 call. No retry, no caching, no streaming.

    The runner sets ``reasoning_effort="none"`` because the v0.1
    protocol uses default sampling across all three vendors and
    ``"none"`` is the closest-to-non-reasoning level GPT-5.5 supports.
    """

    @property
    def model_family(self) -> str:
        return "openai"

    @property
    def model_id(self) -> str:
        return OPENAI_MODEL_ID

    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> CallResult:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set (check .env.local or shell env)")
        client = openai.OpenAI(api_key=api_key)  # FRESH per call
        del temperature  # GPT-5.5 reasoning model uses reasoning_effort instead

        # Reasoning_effort: GPT-5.5 supports {none, low, medium, high, xhigh}.
        # The v0.1 protocol uses "none" to match the other vendors' default
        # sampling. If the SDK in use doesn't expose the kwarg yet (older
        # version), fall back to omitting it.
        try:
            response = client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=max_tokens,
                reasoning_effort="none",
            )
        except TypeError:
            response = client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=max_tokens,
            )

        choice = response.choices[0]
        response_text = choice.message.content or ""

        # R1(a) audit: capture all OpenAI identity fields. response.model is
        # the primary; system_fingerprint identifies the underlying serving
        # build (changes when OpenAI deploys new infra without bumping
        # the model id).
        identity_fields: dict[str, str] = {
            "response_model": str(response.model),
            "system_fingerprint": str(response.system_fingerprint or ""),
        }

        usage = response.usage
        input_tokens = int(usage.prompt_tokens) if usage else 0
        output_tokens = int(usage.completion_tokens) if usage else 0

        return CallResult(
            response_text=response_text,
            primary_id=str(response.model),
            identity_fields=identity_fields,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return (
            input_tokens * OPENAI_INPUT_PRICE_PER_MTOK / 1_000_000
            + output_tokens * OPENAI_OUTPUT_PRICE_PER_MTOK / 1_000_000
        )
