"""Apply human audit verdicts to v0.1 dual-judge data; recompute P1 / P3.

The dual-judge production run on Aristotelian Mechanics produced an
overall judge-disagreement rate of 36.67 %, which exceeds the 25 %
threshold that triggers a prereg-mandated human audit (see
``predictions/v0_1_prereg.md`` and ``CLAUDE.md`` "Inter-rater
reliability"). The human auditor reviewed all 22 DISAGREE cases and
recorded verdicts in ``analysis/v0_1_audit_human_review.md``.

This script:

1. Loads original dual-judge verdicts from ``results/<model>/judgments/``
   (the source of truth produced by ``scripts/judge_v0_1.py``).
2. Resolves every DISAGREE row using the corresponding audit verdict
   below (hard-coded so this script is self-auditing; the same
   verdicts are visible in the canonical audit file).
3. Recomputes P1 and P3 from the audit-resolved classifications.
4. Appends a "## Post-audit findings" block to
   ``analysis/v0_1_findings.md`` (does NOT overwrite the pre-audit
   block — both stay on the record).

Does NOT modify:

- ``predictions/v0_1_prereg.md`` (prereg-locked; SHA-256 protected).
- ``frameworks/01_aristotelian/*.md`` (frozen at the locked tag).
- ``prompts/stage*.md`` (frozen at the locked tag).
- Original trial JSONs or judge verdict JSONs under ``results/``.

Usage: ``uv run python scripts/apply_audit.py``
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from physlit.judges.aggregate import (
    IRRStats,
    TrialClassification,
    load_trial_verdicts,
)

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
ANALYSIS = REPO / "analysis"
FINDINGS_PATH = ANALYSIS / "v0_1_findings.md"

MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
N_TRIALS = 5

# All 22 audit verdicts from analysis/v0_1_audit_human_review.md, keyed
# by (model_id, trial_index, stage). Values:
#   - Stage 1-3:  "PASS" | "FAIL"
#   - Stage 4:    "yes" | "no" | "vacuous"
# These overrides apply ONLY to rows where the dual-judge consensus
# was DISAGREE; non-DISAGREE rows are untouched.
AUDIT_VERDICTS: dict[tuple[str, int, str], str] = {
    # Stage 1 (induction) — Cases 1-5
    ("claude-opus-4-7", 2, "induction"): "FAIL",  # Case 1
    ("claude-opus-4-7", 3, "induction"): "FAIL",  # Case 2
    ("gpt-5.5-2026-04-23", 1, "induction"): "FAIL",  # Case 3
    ("gpt-5.5-2026-04-23", 3, "induction"): "FAIL",  # Case 4
    ("gemini-3.1-pro-preview", 4, "induction"): "FAIL",  # Case 5
    # Stage 2 (formulation) — Cases 6-12
    ("claude-opus-4-7", 2, "formulation"): "FAIL",  # Case 6
    ("claude-opus-4-7", 3, "formulation"): "FAIL",  # Case 7
    ("claude-opus-4-7", 4, "formulation"): "FAIL",  # Case 8
    ("gpt-5.5-2026-04-23", 3, "formulation"): "FAIL",  # Case 9
    ("gemini-3.1-pro-preview", 0, "formulation"): "FAIL",  # Case 10
    ("gemini-3.1-pro-preview", 3, "formulation"): "FAIL",  # Case 11
    ("gemini-3.1-pro-preview", 4, "formulation"): "FAIL",  # Case 12
    # Stage 3 (prediction) — Cases 13-17
    ("claude-opus-4-7", 3, "prediction"): "FAIL",  # Case 13
    ("gpt-5.5-2026-04-23", 1, "prediction"): "PASS",  # Case 14
    ("gpt-5.5-2026-04-23", 2, "prediction"): "PASS",  # Case 15
    ("gpt-5.5-2026-04-23", 3, "prediction"): "FAIL",  # Case 16
    ("gemini-3.1-pro-preview", 3, "prediction"): "PASS",  # Case 17
    # Stage 4 (meta over-claim) — Cases 18-22
    ("claude-opus-4-7", 3, "meta"): "yes",  # Case 18
    ("claude-opus-4-7", 4, "meta"): "no",  # Case 19
    ("gpt-5.5-2026-04-23", 1, "meta"): "yes",  # Case 20
    ("gpt-5.5-2026-04-23", 3, "meta"): "yes",  # Case 21
    ("gemini-3.1-pro-preview", 0, "meta"): "yes",  # Case 22
}


def _stage_consensus(parsed_c: dict[str, Any], parsed_o: dict[str, Any], stage: str) -> str:
    """Return the dual-judge consensus label for one (trial, stage) pair.

    "PASS" / "FAIL" / "DISAGREE" / "MISSING" for Stage 1-3;
    "yes" / "no" / "vacuous" / "DISAGREE" / "MISSING" for Stage 4.
    """

    def _label_s13(p: dict[str, Any]) -> str:
        if not p:
            return ""
        raw = p.get("verdict") or p.get("overall_verdict") or ""
        return str(raw).upper()

    def _label_meta(p: dict[str, Any]) -> str:
        if not p:
            return ""
        return str(p.get("over_claim", "")).lower()

    label = _label_meta if stage == "meta" else _label_s13
    cv = label(parsed_c)
    ov = label(parsed_o)
    if not cv or not ov:
        return "MISSING"
    if cv == ov:
        return cv
    return "DISAGREE"


def _audited_label(consensus: str, model: str, trial_index: int, stage: str) -> str:
    """Resolve DISAGREE rows via AUDIT_VERDICTS; pass through others."""
    if consensus == "DISAGREE":
        return AUDIT_VERDICTS.get((model, trial_index, stage), "DISAGREE")
    return consensus


def build_audited_classifications(
    verdicts: dict[tuple[str, int, str, str], dict[str, Any]],
) -> tuple[list[TrialClassification], IRRStats, IRRStats]:
    """Build TrialClassification rows from audit-resolved verdicts.

    Returns ``(classifications, pre_audit_irr, post_audit_irr)``.

    The pre-audit IRR is computed from raw dual-judge agreement (so
    we can publish "the original IRR that triggered the audit"). The
    post-audit IRR counts each audit-resolved row as agreement (since
    the audit is the prereg-mandated tie-breaker). Both numbers are
    surfaced in the appended findings block for transparency.
    """
    classifications: list[TrialClassification] = []
    pre_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    post_counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])

    for model in MODELS:
        for trial_index in range(N_TRIALS):
            stage_verdicts: dict[str, str] = {}
            for stage in ("induction", "formulation", "prediction"):
                pc = verdicts.get((model, trial_index, stage, "anthropic"), {})
                po = verdicts.get((model, trial_index, stage, "openai"), {})
                consensus = _stage_consensus(pc, po, stage)
                audited = _audited_label(consensus, model, trial_index, stage)
                stage_verdicts[stage] = audited
                if consensus != "MISSING":
                    pre_counts[stage][0] += 1
                    if consensus == "DISAGREE":
                        pre_counts[stage][1] += 1
                if audited != "MISSING":
                    post_counts[stage][0] += 1
                    if audited == "DISAGREE":
                        post_counts[stage][1] += 1
            pc_meta = verdicts.get((model, trial_index, "meta", "anthropic"), {})
            po_meta = verdicts.get((model, trial_index, "meta", "openai"), {})
            meta_consensus = _stage_consensus(pc_meta, po_meta, "meta")
            meta_audited = _audited_label(meta_consensus, model, trial_index, "meta")
            if meta_consensus != "MISSING":
                pre_counts["meta"][0] += 1
                if meta_consensus == "DISAGREE":
                    pre_counts["meta"][1] += 1
            if meta_audited != "MISSING":
                post_counts["meta"][0] += 1
                if meta_audited == "DISAGREE":
                    post_counts["meta"][1] += 1

            has_failure = any(
                stage_verdicts.get(s) == "FAIL" for s in ("induction", "formulation", "prediction")
            )
            classifications.append(
                TrialClassification(
                    model_id=model,
                    trial_index=trial_index,
                    stage1_verdict=stage_verdicts.get("induction", "MISSING"),
                    stage2_verdict=stage_verdicts.get("formulation", "MISSING"),
                    stage3_verdict=stage_verdicts.get("prediction", "MISSING"),
                    overclaim=meta_audited,
                    has_any_stage_failure=has_failure,
                )
            )

    def _irr(counts: dict[str, list[int]]) -> IRRStats:
        return IRRStats(
            stage1_total=counts["induction"][0],
            stage1_disagree=counts["induction"][1],
            stage2_total=counts["formulation"][0],
            stage2_disagree=counts["formulation"][1],
            stage3_total=counts["prediction"][0],
            stage3_disagree=counts["prediction"][1],
            meta_total=counts["meta"][0],
            meta_disagree=counts["meta"][1],
        )

    return classifications, _irr(pre_counts), _irr(post_counts)


def audited_p1(classifications: list[TrialClassification]) -> dict[str, object]:
    """P1 verdict computed from audit-resolved Stage 1 labels."""
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
    verdict = "confirmed" if confirmed else ("partially confirmed" if partial else "refuted")
    return {
        "verdict": verdict,
        "pass": dict(pass_count),
        "fail": dict(fail_count),
        "disagree": dict(disagree_count),
    }


def audited_p3(classifications: list[TrialClassification]) -> dict[str, object]:
    """P3 verdict computed from audit-resolved Stage 1-3 + over-claim labels."""
    failure_trials = [c for c in classifications if c.has_any_stage_failure]
    overclaim_trials = [c for c in failure_trials if c.overclaim == "yes"]
    denom = len(failure_trials)
    num = len(overclaim_trials)
    if denom == 0:
        return {
            "verdict": "vacuous",
            "failure_trials": 0,
            "overclaim_trials": 0,
            "overclaim_rate": 0.0,
        }
    rate = num / denom
    if rate >= 0.30:
        verdict = "confirmed"
    elif rate >= 0.15:
        verdict = "partially confirmed"
    else:
        verdict = "refuted"
    return {
        "verdict": verdict,
        "failure_trials": denom,
        "overclaim_trials": num,
        "overclaim_rate": rate,
    }


def _format_block(
    classifications: list[TrialClassification],
    pre_irr: IRRStats,
    post_irr: IRRStats,
    p1: dict[str, object],
    p3: dict[str, object],
) -> str:
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    lines: list[str] = []
    lines.append("\n## Post-audit findings\n")
    lines.append(
        f"_Generated `{ts}` by `scripts/apply_audit.py` from the audit\n"
        f"verdicts in [`v0_1_audit_human_review.md`](./v0_1_audit_human_review.md).\n"
        f"The pre-audit findings block above is preserved as the original\n"
        f"dual-judge output; this block represents the prereg-mandated\n"
        f"human-audit resolution of the 22 DISAGREE rows. The locked\n"
        f"`predictions/v0_1_prereg.md` (and its SHA-256) is unchanged._\n"
    )

    lines.append("### IRR (judge disagreement rate)\n")
    lines.append("**Pre-audit** (the rate that triggered the audit):\n")
    lines.append(
        f"- Stage 1: {pre_irr.stage1_disagree}/{pre_irr.stage1_total} = "
        f"{(pre_irr.stage1_disagree / max(1, pre_irr.stage1_total)):.2%}\n"
        f"- Stage 2: {pre_irr.stage2_disagree}/{pre_irr.stage2_total} = "
        f"{(pre_irr.stage2_disagree / max(1, pre_irr.stage2_total)):.2%}\n"
        f"- Stage 3: {pre_irr.stage3_disagree}/{pre_irr.stage3_total} = "
        f"{(pre_irr.stage3_disagree / max(1, pre_irr.stage3_total)):.2%}\n"
        f"- Meta:    {pre_irr.meta_disagree}/{pre_irr.meta_total} = "
        f"{(pre_irr.meta_disagree / max(1, pre_irr.meta_total)):.2%}\n"
        f"- Overall: {pre_irr.overall_disagree_rate:.2%}\n\n"
    )
    lines.append(
        "Per the prereg, this overall rate exceeded the 25 % threshold; "
        "the audit was the prereg-mandated tie-breaker.\n\n"
    )

    lines.append("**Post-audit** (after applying the 22 audit verdicts):\n")
    lines.append(
        f"- Stage 1: {post_irr.stage1_disagree}/{post_irr.stage1_total} "
        f"= {(post_irr.stage1_disagree / max(1, post_irr.stage1_total)):.2%}\n"
        f"- Stage 2: {post_irr.stage2_disagree}/{post_irr.stage2_total} "
        f"= {(post_irr.stage2_disagree / max(1, post_irr.stage2_total)):.2%}\n"
        f"- Stage 3: {post_irr.stage3_disagree}/{post_irr.stage3_total} "
        f"= {(post_irr.stage3_disagree / max(1, post_irr.stage3_total)):.2%}\n"
        f"- Meta:    {post_irr.meta_disagree}/{post_irr.meta_total} "
        f"= {(post_irr.meta_disagree / max(1, post_irr.meta_total)):.2%}\n"
        f"- Overall: {post_irr.overall_disagree_rate:.2%}\n\n"
    )

    lines.append("### P1 — Induction failure under training-data conflict\n")
    lines.append(f"**Audit-resolved verdict: {str(p1['verdict']).upper()}**\n\n")
    lines.append(f"- Per-model Stage 1 PASS counts: `{p1['pass']}`\n")
    lines.append(f"- Per-model Stage 1 FAIL counts: `{p1['fail']}`\n")
    lines.append(
        f"- Per-model residual-DISAGREE counts: `{p1['disagree']}` (should be empty post-audit)\n\n"
    )

    lines.append("### P3 — Meta-cognitive miscalibration\n")
    lines.append(f"**Audit-resolved verdict: {str(p3['verdict']).upper()}**\n\n")
    lines.append(
        f"- Failure-containing trials (any Stage 1-3 audit-FAIL): {p3['failure_trials']}\n"
    )
    lines.append(
        f"- Over-claim trials among them (audit-resolved 'yes'): {p3['overclaim_trials']}\n"
    )
    rate_val = p3.get("overclaim_rate", 0.0)
    rate_float = float(rate_val) if isinstance(rate_val, (int, float)) else 0.0
    lines.append(f"- Over-claim rate: {rate_float:.2%}\n\n")

    lines.append("### Per-trial classification matrix (audit-resolved)\n\n")
    lines.append("| Model | Trial | S1 | S2 | S3 | Over-claim | Any failure |\n")
    lines.append("|---|---|---|---|---|---|---|\n")
    for c in classifications:
        lines.append(
            f"| `{c.model_id}` | {c.trial_index} | "
            f"{c.stage1_verdict} | {c.stage2_verdict} | {c.stage3_verdict} | "
            f"{c.overclaim} | {'yes' if c.has_any_stage_failure else 'no'} |\n"
        )
    lines.append(
        "\n_Resolved-from-DISAGREE rows are bolded in the audit file_"
        "_(see [`v0_1_audit_human_review.md`](./v0_1_audit_human_review.md))_"
        "_; this matrix presents the operational classifications used to_"
        "_compute the P1 and P3 verdicts above._\n"
    )

    return "".join(lines)


def main() -> int:
    if not FINDINGS_PATH.exists():
        print(f"missing {FINDINGS_PATH}; cannot append audit findings", file=sys.stderr)
        return 1

    all_verdicts: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for model in MODELS:
        verdicts_dir = RESULTS / model / "judgments"
        if not verdicts_dir.exists():
            continue
        all_verdicts.update(load_trial_verdicts(verdicts_dir))

    classifications, pre_irr, post_irr = build_audited_classifications(all_verdicts)
    p1 = audited_p1(classifications)
    p3 = audited_p3(classifications)
    block = _format_block(classifications, pre_irr, post_irr, p1, p3)

    with FINDINGS_PATH.open("a") as fh:
        fh.write(block)

    rate_val = p3.get("overclaim_rate", 0.0)
    rate_float = float(rate_val) if isinstance(rate_val, (int, float)) else 0.0
    print(
        f"Appended post-audit findings to {FINDINGS_PATH}.\n"
        f"  P1: {str(p1['verdict']).upper()}\n"
        f"  P3: {str(p3['verdict']).upper()}\n"
        f"  P1 fail counts: {p1['fail']}\n"
        f"  P3: {p3['overclaim_trials']}/{p3['failure_trials']} = {rate_float:.2%}\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
