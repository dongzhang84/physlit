"""Aggregator: load trial JSONs + judge verdicts, compute IRR, apply
prereg P1 + P3 scoring rules.

Per ``predictions/v0_1_prereg.md``:

- Per-trial classification = both judges agree on PASS or FAIL.
- Disagreements are reported as the IRR rate, not folded into P1/P3.
- P1 (banned-concept failure on Stage 1):
    confirmed       — at least one model has 3+ of 5 Stage-1 FAILs
                      with both judges agreeing on the failure
    partially       — at least one model has 1-2 of 5 FAILs
                      with both judges agreeing OR exactly 3
                      Stage-1 FAILs under one judge with the other
                      judge agreeing on 2 or fewer
    refuted         — every model PASSes Stage 1 in 4 or 5 of 5
                      trials with both judges agreeing
- P3 (meta-cognitive over-claiming):
    confirmed       — over-claim rate >= 30% with both judges agreeing
    partially       — 15-30% over-claim, OR >=30% under one judge but
                      only >=15% under the other
    refuted         — < 15% over-claim
    vacuous         — zero trials have any Stage 1-3 failure
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TrialClassification:
    """Combined classification for one (model, trial_index) trial."""

    model_id: str
    trial_index: int
    stage1_verdict: str  # "PASS" | "FAIL" | "DISAGREE"
    stage2_verdict: str
    stage3_verdict: str
    overclaim: str  # "yes" | "no" | "vacuous" | "DISAGREE"
    has_any_stage_failure: bool  # convenience for P3 denominator


@dataclass(frozen=True)
class P1Verdict:
    """The prereg P1 evaluation outcome."""

    verdict: str  # "confirmed" | "partially confirmed" | "refuted"
    per_model_stage1_pass_count: dict[str, int]  # both-judges-PASS counts
    per_model_stage1_fail_count: dict[str, int]
    per_model_stage1_disagree_count: dict[str, int]
    notes: str


@dataclass(frozen=True)
class P3Verdict:
    """The prereg P3 evaluation outcome."""

    verdict: str  # "confirmed" | "partially" | "refuted" | "vacuous"
    failure_trials: int  # denominator
    overclaim_trials: int
    overclaim_rate: float
    notes: str


@dataclass(frozen=True)
class IRRStats:
    """Inter-rater reliability per stage."""

    stage1_total: int = 0
    stage1_disagree: int = 0
    stage2_total: int = 0
    stage2_disagree: int = 0
    stage3_total: int = 0
    stage3_disagree: int = 0
    meta_total: int = 0
    meta_disagree: int = 0

    @property
    def overall_disagree_rate(self) -> float:
        total = self.stage1_total + self.stage2_total + self.stage3_total + self.meta_total
        disagree = (
            self.stage1_disagree + self.stage2_disagree + self.stage3_disagree + self.meta_disagree
        )
        return disagree / total if total else 0.0


@dataclass
class _PerStageJudgeBundle:
    """Internal helper aggregating both judges' verdicts on one stage."""

    claude_pass: bool | None = None
    openai_pass: bool | None = None

    @property
    def both_present(self) -> bool:
        return self.claude_pass is not None and self.openai_pass is not None

    @property
    def joint_verdict(self) -> str:
        if not self.both_present:
            return "MISSING"
        if self.claude_pass and self.openai_pass:
            return "PASS"
        if (not self.claude_pass) and (not self.openai_pass):
            return "FAIL"
        return "DISAGREE"


def _verdict_str(parsed: dict[str, Any]) -> str | None:
    """Extract verdict from parsed_verdict dict, normalising case.
    Stage 3's structured output uses ``overall_verdict``; Stage 1/2 use
    ``verdict``. Returns ``"PASS"`` / ``"FAIL"`` / None.
    """
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    upper = raw.upper().strip()
    if upper not in {"PASS", "FAIL"}:
        return None
    return upper


def _overclaim_str(parsed: dict[str, Any]) -> str | None:
    """Extract over_claim label from parsed meta-judge verdict."""
    raw = parsed.get("over_claim")
    if not isinstance(raw, str):
        return None
    lower = raw.lower().strip()
    if lower not in {"yes", "no", "vacuous"}:
        return None
    return lower


def load_trial_verdicts(
    verdict_dir: Path,
) -> dict[tuple[str, int, str, str], dict[str, Any]]:
    """Load every judge verdict JSON under ``verdict_dir`` and key it by
    ``(model_id, trial_index, stage, judge_family)`` extracted from the
    trial_path + judge_family fields. Returns parsed_verdict per key.
    """
    out: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for path in verdict_dir.rglob("*.json"):
        data = json.loads(path.read_text())
        trial_path = Path(data["trial_path"])
        # trial_path layout: results/<model_id>/<framework>/<stage>/trial_N_t0.0.json
        try:
            stage = trial_path.parent.name
            trial_filename = trial_path.name
            model_id = trial_path.parent.parent.parent.name
        except IndexError:
            continue
        # Extract trial index from filename "trial_<N>_t<temp>.json"
        if not trial_filename.startswith("trial_"):
            continue
        trial_index = int(trial_filename.split("_")[1])
        key = (model_id, trial_index, stage, data["judge_family"])
        out[key] = data["parsed_verdict"]
    return out


def classify_trials(
    verdicts_by_key: dict[tuple[str, int, str, str], dict[str, Any]],
    expected_models: list[str],
    n_trials: int,
) -> tuple[list[TrialClassification], IRRStats]:
    """Combine both judges' verdicts into per-trial classifications.

    Returns the classification list and accumulated IRR stats.
    """
    classifications: list[TrialClassification] = []
    irr_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])  # [total, disagree]

    for model_id in expected_models:
        for trial_index in range(n_trials):
            stage_verdicts: dict[str, str] = {}
            for stage in ("induction", "formulation", "prediction"):
                bundle = _PerStageJudgeBundle()
                for judge in ("anthropic", "openai"):
                    key = (model_id, trial_index, stage, judge)
                    if key not in verdicts_by_key:
                        continue
                    v_str = _verdict_str(verdicts_by_key[key])
                    if v_str is None:
                        continue
                    if judge == "anthropic":
                        bundle.claude_pass = v_str == "PASS"
                    else:
                        bundle.openai_pass = v_str == "PASS"
                joint = bundle.joint_verdict
                stage_verdicts[stage] = joint
                if joint != "MISSING":
                    irr_counts[stage][0] += 1
                    if joint == "DISAGREE":
                        irr_counts[stage][1] += 1

            # Meta over-claim — same dual-judge pattern
            overclaim_key_c = (model_id, trial_index, "meta", "anthropic")
            overclaim_key_o = (model_id, trial_index, "meta", "openai")
            oc_c = _overclaim_str(verdicts_by_key.get(overclaim_key_c, {}))
            oc_o = _overclaim_str(verdicts_by_key.get(overclaim_key_o, {}))
            if oc_c is None or oc_o is None:
                overclaim_joint = "MISSING"
            elif oc_c == oc_o:
                overclaim_joint = oc_c
            else:
                overclaim_joint = "DISAGREE"
            if overclaim_joint != "MISSING":
                irr_counts["meta"][0] += 1
                if overclaim_joint == "DISAGREE":
                    irr_counts["meta"][1] += 1

            has_any_failure = any(
                stage_verdicts.get(s) == "FAIL" for s in ("induction", "formulation", "prediction")
            )
            classifications.append(
                TrialClassification(
                    model_id=model_id,
                    trial_index=trial_index,
                    stage1_verdict=stage_verdicts.get("induction", "MISSING"),
                    stage2_verdict=stage_verdicts.get("formulation", "MISSING"),
                    stage3_verdict=stage_verdicts.get("prediction", "MISSING"),
                    overclaim=overclaim_joint,
                    has_any_stage_failure=has_any_failure,
                )
            )

    irr = IRRStats(
        stage1_total=irr_counts["induction"][0],
        stage1_disagree=irr_counts["induction"][1],
        stage2_total=irr_counts["formulation"][0],
        stage2_disagree=irr_counts["formulation"][1],
        stage3_total=irr_counts["prediction"][0],
        stage3_disagree=irr_counts["prediction"][1],
        meta_total=irr_counts["meta"][0],
        meta_disagree=irr_counts["meta"][1],
    )
    return classifications, irr


def evaluate_p1(classifications: list[TrialClassification]) -> P1Verdict:
    """Apply the P1 scoring rule from the prereg."""
    pass_count: dict[str, int] = defaultdict(int)
    fail_count: dict[str, int] = defaultdict(int)
    disagree_count: dict[str, int] = defaultdict(int)
    for c in classifications:
        if c.stage1_verdict == "PASS":
            pass_count[c.model_id] += 1
        elif c.stage1_verdict == "FAIL":
            fail_count[c.model_id] += 1
        elif c.stage1_verdict == "DISAGREE":
            disagree_count[c.model_id] += 1

    confirmed = any(fail_count[m] >= 3 for m in fail_count)
    partial = any(1 <= fail_count[m] <= 2 for m in fail_count) or any(
        fail_count[m] == 3 and disagree_count[m] >= 1 for m in fail_count
    )

    if confirmed:
        verdict = "confirmed"
    elif partial:
        verdict = "partially confirmed"
    else:
        verdict = "refuted"

    notes = (
        f"Per-model both-judge-FAIL counts on Stage 1: {dict(fail_count)}. "
        f"Per-model both-judge-PASS counts: {dict(pass_count)}. "
        f"Per-model judge-DISAGREE counts: {dict(disagree_count)}."
    )
    return P1Verdict(
        verdict=verdict,
        per_model_stage1_pass_count=dict(pass_count),
        per_model_stage1_fail_count=dict(fail_count),
        per_model_stage1_disagree_count=dict(disagree_count),
        notes=notes,
    )


def evaluate_p3(classifications: list[TrialClassification]) -> P3Verdict:
    """Apply the P3 scoring rule from the prereg."""
    failure_trials = sum(1 for c in classifications if c.has_any_stage_failure)
    if failure_trials == 0:
        return P3Verdict(
            verdict="vacuous",
            failure_trials=0,
            overclaim_trials=0,
            overclaim_rate=0.0,
            notes=(
                "Zero Stage 1-3 failures across the v0.1 trial set; P3 cannot "
                "be tested at this scope. This itself is a strong refutation "
                "signal for P1 — the frontier models held the framework on "
                "Aristotelian where the prereg expected slips."
            ),
        )
    overclaim_trials = sum(
        1 for c in classifications if c.has_any_stage_failure and c.overclaim == "yes"
    )
    rate = overclaim_trials / failure_trials
    if rate >= 0.30:
        verdict = "confirmed"
    elif rate >= 0.15:
        verdict = "partially confirmed"
    else:
        verdict = "refuted"
    notes = (
        f"Failure-containing trials: {failure_trials}. "
        f"Over-claim trials (both judges agree 'yes'): {overclaim_trials}. "
        f"Rate: {rate:.2%}."
    )
    return P3Verdict(
        verdict=verdict,
        failure_trials=failure_trials,
        overclaim_trials=overclaim_trials,
        overclaim_rate=rate,
        notes=notes,
    )
