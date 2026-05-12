"""N11 LLM layer — detects smuggled mechanism that regex misses.

Uses Anthropic Haiku (cheap, fast, strong at structured-JSON
instructions). Per the v0.1 prereg-derived hard rule: fresh client per
call, no cross-call state. The class is a thin wrapper; the prompt and
parsing are the substantive content.

Cost: ~$0.001 per Stage-1 trial (one call per trial, ~1k input + ~200
output tokens). For 60 v0.1 trials over Stages 1+2 = 120 calls ~$0.12.
The bulk of the calibration spend is on Agent 1 (disagree resolver),
not this layer.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from typing import Any

from .models import FlagTier, StructuralFlag

DEFAULT_LLM_MODEL = "claude-haiku-4-5-20251001"

LLM_SMUGGLE_PROMPT = """\
You are auditing a Stage-1 induction response from a frontier LLM that was \
asked to propose rules for an Aristotelian-mechanics world, using only \
concepts derivable from these 12 observations:

{observations}

The response below proposed a set of rules. Your job is to identify any \
**smuggled mechanism** — a thing that acts on motion, position, or shape \
in a way that is NOT supported by any of the 12 observations. Smuggled \
mechanisms are usually borrowed from modern physics (friction, buoyancy, \
vector decomposition, energy transfer) but worded so that no banned word \
literally appears.

Examples of smuggling (FAIL):
- "The road and air rob motion from the cart" — observations never describe \
  road or air as motion-removers.
- "Lighter bodies are surface-supported in water" — no observation introduces \
  any 'support' mechanism.
- "The downward and forward components combine to give the trajectory" — no \
  observation introduces component / vector decomposition.

NOT smuggling (PASS):
- "Heavier things tend toward their natural place" — natural-place language \
  is permitted Aristotelian vocabulary.
- "The arrow continues because the air helps to bear it forward" — antiperistasis \
  is permitted (it's a real Aristotelian / medieval mechanism).
- "The medium resists passage" — medium-resistance is in observation 9.

Respond with a single JSON object, no prose, in this exact shape:

{{
  "smuggled": [
    {{"quote": "<verbatim quote from the response>", "explanation": "<one sentence>"}}
  ]
}}

If no smuggling is found, return `{{"smuggled": []}}`.

---

RESPONSE TO AUDIT:

{response_text}
"""


@dataclass(frozen=True)
class SmuggleHit:
    """One LLM-detected smuggled-mechanism instance."""

    quote: str
    explanation: str


class SmuggleDetectorLLM:
    """N11 LLM-layer detector. Fresh Anthropic client per call."""

    def __init__(
        self,
        model: str = DEFAULT_LLM_MODEL,
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self._api_key = api_key

    def detect(self, response_text: str, observations_text: str) -> list[SmuggleHit]:
        """Single API call. Returns parsed smuggle hits.

        Returns ``[]`` on parse failure (the regex layer remains the
        primary signal; LLM is supplementary).
        """
        from anthropic import Anthropic  # local import to avoid load-cost at module import

        client = Anthropic(api_key=self._api_key) if self._api_key else Anthropic()
        prompt = LLM_SMUGGLE_PROMPT.format(
            observations=observations_text,
            response_text=response_text,
        )
        _session_id = str(uuid.uuid4())  # bookkeeping per the fresh-session contract
        msg = client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = "".join(block.text for block in msg.content if block.type == "text")
        return _parse_smuggle_response(raw)

    def detect_as_flags(
        self,
        response_text: str,
        observations_text: str,
    ) -> list[StructuralFlag]:
        """Convenience: run detect() and return StructuralFlag objects directly."""
        hits = self.detect(response_text, observations_text)
        return [
            StructuralFlag(
                criterion="N11",
                tier=FlagTier.TIER_2,
                layer="llm",
                evidence=f"…{hit.quote}…",
                explanation=hit.explanation,
            )
            for hit in hits
        ]


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_smuggle_response(raw: str) -> list[SmuggleHit]:
    match = _JSON_OBJECT_RE.search(raw)
    if match is None:
        return []
    try:
        parsed: Any = json.loads(match.group(0))
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, dict):
        return []
    smuggled = parsed.get("smuggled", [])
    if not isinstance(smuggled, list):
        return []
    hits: list[SmuggleHit] = []
    for item in smuggled:
        if not isinstance(item, dict):
            continue
        quote = item.get("quote", "")
        explanation = item.get("explanation", "")
        if isinstance(quote, str) and isinstance(explanation, str) and quote:
            hits.append(SmuggleHit(quote=quote, explanation=explanation))
    return hits
