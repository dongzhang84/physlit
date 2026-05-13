"""v0.2 data loaders for disagree cases and structural-judge verdicts.

All loaders read existing files committed at `prereg-v0.1-locked` (for
v0.1 content judgments) or written by v0.2's own scripts (for
structural judgments).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Stages on the content axis. Stage 4 (meta over-claim) is intentionally
# excluded from v0.2 content-axis processing (the prereg inherits Stage 4
# verdicts verbatim from v0.1).
CONTENT_STAGES: tuple[str, ...] = ("induction", "formulation", "prediction")


def _normalised_verdict(parsed: dict[str, Any]) -> str | None:
    """Extract a normalised PASS/FAIL from a parsed_verdict dict.

    Stage 3 content-judge files use ``overall_verdict``; Stages 1-2 and
    all v0.2 output schemas use ``verdict``. Returns the upper-case
    string, or ``None`` if neither key resolves to a recognized value.
    """
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    upper = raw.strip().upper()
    if upper not in {"PASS", "FAIL"}:
        return None
    return upper


@dataclass(frozen=True)
class ContentDisagreeCase:
    """One v0.1 content-axis disagree case identified for Agent 1 to resolve."""

    model_id: str
    trial_index: int
    stage: str  # "induction" / "formulation" / "prediction"
    trial_path: Path
    response_text: str
    judge_a_parsed: dict[str, Any]  # Anthropic judge's parsed_verdict
    judge_b_parsed: dict[str, Any]  # OpenAI judge's parsed_verdict
    judge_a_path: Path
    judge_b_path: Path


@dataclass(frozen=True)
class StructuralVerdictBundle:
    """Both structural judges' verdicts for one trial."""

    model_id: str
    trial_index: int
    judge_a_parsed: dict[str, Any] | None
    judge_b_parsed: dict[str, Any] | None
    judge_a_path: Path | None
    judge_b_path: Path | None

    @property
    def both_present(self) -> bool:
        return self.judge_a_parsed is not None and self.judge_b_parsed is not None

    @property
    def joint_verdict(self) -> str:
        """Return "PASS" | "FAIL" | "DISAGREE" | "MISSING"."""
        if not self.both_present:
            return "MISSING"
        assert self.judge_a_parsed is not None
        assert self.judge_b_parsed is not None
        a = _normalised_verdict(self.judge_a_parsed)
        b = _normalised_verdict(self.judge_b_parsed)
        if a is None or b is None:
            return "MISSING"
        if a == b:
            return a
        return "DISAGREE"


def find_content_disagree_cases(
    results_root: Path,
    model_ids: tuple[str, ...],
    n_trials: int,
) -> list[ContentDisagreeCase]:
    """Scan v0.1 content-judge verdicts; return one entry per content
    DISAGREE (Stage 1 / 2 / 3, both judges produced a verdict and they
    differ on PASS/FAIL).

    The v0.1 audit recorded 5 + 7 + 5 = 17 such cases. This function
    reconstructs that set from the committed `results/<model>/judgments/`
    directories.
    """
    cases: list[ContentDisagreeCase] = []
    for model_id in model_ids:
        judgments_dir = results_root / model_id / "judgments"
        if not judgments_dir.is_dir():
            continue
        by_key: dict[tuple[int, str, str], tuple[dict[str, Any], Path]] = {}
        for path in sorted(judgments_dir.glob("*.json")):
            data = json.loads(path.read_text())
            stage = data.get("stage")
            if stage not in CONTENT_STAGES:
                continue
            trial_path = Path(data["trial_path"])
            trial_filename = trial_path.name
            if not trial_filename.startswith("trial_"):
                continue
            trial_index = int(trial_filename.split("_")[1])
            judge_family = data["judge_family"]
            by_key[(trial_index, stage, judge_family)] = (
                data.get("parsed_verdict", {}) or {},
                path,
            )

        for trial_index in range(n_trials):
            for stage in CONTENT_STAGES:
                key_a = (trial_index, stage, "anthropic")
                key_b = (trial_index, stage, "openai")
                if key_a not in by_key or key_b not in by_key:
                    continue
                parsed_a, path_a = by_key[key_a]
                parsed_b, path_b = by_key[key_b]
                v_a = _normalised_verdict(parsed_a)
                v_b = _normalised_verdict(parsed_b)
                if v_a is None or v_b is None:
                    continue
                if v_a == v_b:
                    continue
                # DISAGREE — load the trial response.
                trial_path = Path(json.loads(path_a.read_text())["trial_path"])
                trial_data = json.loads(trial_path.read_text())
                cases.append(
                    ContentDisagreeCase(
                        model_id=model_id,
                        trial_index=trial_index,
                        stage=stage,
                        trial_path=trial_path,
                        response_text=trial_data["response_text"],
                        judge_a_parsed=parsed_a,
                        judge_b_parsed=parsed_b,
                        judge_a_path=path_a,
                        judge_b_path=path_b,
                    )
                )
    return cases


def load_structural_verdicts(
    results_root: Path,
    model_ids: tuple[str, ...],
    n_trials: int,
) -> dict[tuple[str, int], StructuralVerdictBundle]:
    """Load every structural-judge verdict written by
    `scripts/run_structural_judging.py` and bundle by (model_id, trial_index).

    Returns a dict from (model_id, trial_index) → StructuralVerdictBundle.
    Missing trials map to a bundle with both judges = None.
    """
    out: dict[tuple[str, int], StructuralVerdictBundle] = {}
    for model_id in model_ids:
        for trial_index in range(n_trials):
            out[(model_id, trial_index)] = StructuralVerdictBundle(
                model_id=model_id,
                trial_index=trial_index,
                judge_a_parsed=None,
                judge_b_parsed=None,
                judge_a_path=None,
                judge_b_path=None,
            )

    for model_id in model_ids:
        structural_dir = results_root / model_id / "01_aristotelian" / "structural"
        if not structural_dir.is_dir():
            continue
        # Each verdict file lives at structural_dir/<filename>.json and
        # records its trial in the parsed_verdict / trial_path fields.
        for path in sorted(structural_dir.glob("*.json")):
            data = json.loads(path.read_text())
            trial_path = Path(data.get("trial_path", ""))
            trial_filename = trial_path.name
            if not trial_filename.startswith("trial_"):
                continue
            trial_index = int(trial_filename.split("_")[1])
            judge_family = data["judge_family"]
            current = out[(model_id, trial_index)]
            parsed = data.get("parsed_verdict", {}) or {}
            if judge_family == "anthropic":
                out[(model_id, trial_index)] = StructuralVerdictBundle(
                    model_id=current.model_id,
                    trial_index=current.trial_index,
                    judge_a_parsed=parsed,
                    judge_b_parsed=current.judge_b_parsed,
                    judge_a_path=path,
                    judge_b_path=current.judge_b_path,
                )
            elif judge_family == "openai":
                out[(model_id, trial_index)] = StructuralVerdictBundle(
                    model_id=current.model_id,
                    trial_index=current.trial_index,
                    judge_a_parsed=current.judge_a_parsed,
                    judge_b_parsed=parsed,
                    judge_a_path=current.judge_a_path,
                    judge_b_path=path,
                )
    return out


def load_trial_response(trial_path: Path) -> str:
    """Read the `response_text` from a trial JSON file."""
    data = json.loads(trial_path.read_text())
    return str(data["response_text"])
