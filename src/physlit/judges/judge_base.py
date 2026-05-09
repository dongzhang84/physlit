"""Base for v0.1 dual-judge LLM judges.

Each judge is an LLM (Claude or OpenAI) that scores tested-model
responses against the prereg-locked criteria. Per
``predictions/v0_1_prereg.md`` Scoring procedure, each Stage 1-3
trial is scored by two independent judges; per-trial verdict =
both judges agree, disagreements are reported as IRR rate.

Judges produce structured JSON verdicts. The base class handles
parsing + retries on malformed output. Subclasses implement the
single-call API binding.
"""

from __future__ import annotations

import json
import re
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class JudgeVerdict:
    """One judge's verdict on one (trial, stage) pair, persisted to JSON."""

    trial_path: str  # path to the tested-model trial JSON judged
    judge_family: str  # "anthropic" / "openai"
    judge_model: str  # full version string
    judge_session_id: str
    judge_timestamp_utc: str
    stage: str  # "induction" / "formulation" / "prediction" / "meta"
    raw_response: str  # the judge LLM's full reply, verbatim
    parsed_verdict: dict[str, Any] = field(default_factory=dict)
    parse_error: str | None = None
    cost_usd_estimate: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0


# Regex to extract the first JSON object from a judge response. We are
# permissive about leading/trailing prose because some judges add
# preamble despite our "JSON only" instruction.
_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_verdict_json(raw: str) -> tuple[dict[str, Any] | None, str | None]:
    """Best-effort JSON extraction.

    Returns ``(parsed, error)`` where exactly one is None.
    """
    match = _JSON_OBJECT_RE.search(raw)
    if match is None:
        return None, "no JSON object found in judge response"
    blob = match.group(0)
    try:
        parsed = json.loads(blob)
    except json.JSONDecodeError as exc:
        return None, f"JSON decode error: {exc}"
    if not isinstance(parsed, dict):
        return None, f"JSON top-level must be object, got {type(parsed).__name__}"
    return parsed, None


class JudgeBase(ABC):
    """Abstract base for one judge LLM. Subclasses bind to vendor SDK."""

    @property
    @abstractmethod
    def judge_family(self) -> str:
        """``"anthropic"`` / ``"openai"``."""

    @property
    @abstractmethod
    def judge_model(self) -> str:
        """Pinned full version string for this judge."""

    @abstractmethod
    def call_judge(self, prompt: str, max_tokens: int) -> tuple[str, int, int]:
        """Single API call. Returns ``(text, input_tokens, output_tokens)``.
        Constructs a fresh client per call (same hard rule as testers)."""

    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Approximate USD cost of one judge call."""

    def judge_one(
        self,
        *,
        trial_path: Path,
        stage: str,
        prompt: str,
        max_tokens: int = 2048,
    ) -> JudgeVerdict:
        """Judge one (trial, stage) pair. The stage label is just a
        bookkeeping field — the prompt itself encodes which criteria to
        apply."""
        session_id = str(uuid.uuid4())
        raw, in_tok, out_tok = self.call_judge(prompt, max_tokens)
        parsed, err = parse_verdict_json(raw)
        return JudgeVerdict(
            trial_path=str(trial_path),
            judge_family=self.judge_family,
            judge_model=self.judge_model,
            judge_session_id=session_id,
            judge_timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            stage=stage,
            raw_response=raw,
            parsed_verdict=parsed or {},
            parse_error=err,
            cost_usd_estimate=self.estimate_cost(in_tok, out_tok),
            input_tokens=in_tok,
            output_tokens=out_tok,
        )

    @staticmethod
    def save_verdict(verdict: JudgeVerdict, output_dir: Path) -> Path:
        """Write the verdict to
        ``<output_dir>/<judge_family>_<stage>_<sha>.json``."""
        output_dir.mkdir(parents=True, exist_ok=True)
        # Use last 8 chars of session id for stable, sortable filenames
        suffix = verdict.judge_session_id[-8:]
        filename = f"{verdict.judge_family}_{verdict.stage}_{suffix}.json"
        out_file = output_dir / filename
        out_file.write_text(json.dumps(asdict(verdict), indent=2, sort_keys=True))
        return out_file
