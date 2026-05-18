"""02_fmv dual-judge orchestrator + P1-P4 aggregator.

Written and committed **before** any 02_fmv production trial lands, so
the scoring logic is fixed in advance of seeing data (a methodology
hygiene requirement: judging must not be tuned to the results).

For every Stage 1-4 trial JSON under ``results/<model>/02_fmv/``:

- Stages 1-3: dispatch to two content judges (Claude + GPT-5.5), each
  given the framework-specific judge prompt + the frozen criteria.
- Stage 4: build a Stage 1-3 failure summary, dispatch the meta judge.
- Save every verdict to ``results/<model>/02_fmv/judgments/``.

Then aggregate, per the locked ``predictions/02_fmv_prereg.md`` §2-§3:

- IRR  = dual-judge disagreement over the 45 Stage 1-3 judged units.
- P1   = # Stage 1 FAIL trials (>= 8 of 15 -> Confirmed).
- P2   = over-claiming rate among failure-containing trials (>= 50 %).
- P3   = IRR below 25 % -> Confirmed.
- P4   = direction-correct / ratio-leaked share of the 45 quantitative
         Stage 3 predictions (Scenarios 1, 2, 4; >= 30 % -> Confirmed).

DISAGREE cases (the two judges split) are flagged, not silently
resolved: per the prereg they go to human audit. While unresolved they
are excluded from the FAIL / leak counts, so P1 / P2 / P4 are reported
as **preliminary lower bounds** whenever any DISAGREE remains.

This runner does not modify run_v0_1.py, judge_v0_1.py, or any library
code; the v0.1 and 02_fmv experiments are independent.

Usage:
    uv run python scripts/judge_02_fmv.py [options]

Options:
    --models <csv>     Subset of model ids to judge. Default: all three.
    --n-trials <int>   Trials per model expected on disk. Default: 5.
    --skip-stage <csv> Stages to skip (induction|formulation|prediction|meta).
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from physlit.judges import ClaudeJudge, JudgeBase, JudgeVerdict, OpenAIJudge
from physlit.prompts import PromptTemplate

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "02_fmv"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
JUDGE_PROMPTS_DIR = FRAMEWORK_DIR / "prompts"
RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"
FINDINGS_PATH = ANALYSIS_DIR / "02_fmv_findings.md"

DEFAULT_MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
JUDGE_MAX_TOKENS = 8192  # reasoning judges burn thinking tokens; keep headroom
QUANT_SCENARIOS = (1, 2, 4)  # Scenarios with a binding ratio (prereg P4)

# Prereg-locked thresholds (predictions/02_fmv_prereg.md §2).
P1_CONFIRM, P1_PARTIAL_LOW = 8, 5  # >=8 confirm; 5-7 partial; <=4 refute
P2_CONFIRM, P2_PARTIAL_LOW = 0.50, 0.30
P3_CONFIRM, P3_PARTIAL_HIGH = 0.25, 0.3667
P4_CONFIRM, P4_PARTIAL_LOW = 0.30, 0.15


def _load_dotenv() -> None:
    env_path = REPO_ROOT / ".env.local"
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


# --- Transient-error retry (same contract as run_02_fmv.py) -------------
_TRANSIENT_MARKERS = (
    "overload",
    "rate limit",
    "rate_limit",
    "unavailable",
    "timeout",
    "timed out",
    "try again",
    "503",
    "529",
)


def _is_transient(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None)
    if status in (408, 409, 429, 500, 502, 503, 504, 529):
        return True
    text = f"{type(exc).__name__} {exc}".lower()
    return any(marker in text for marker in _TRANSIENT_MARKERS)


def _judge_with_retry(
    judge: JudgeBase,
    *,
    trial_path: Path,
    stage: str,
    prompt: str,
    max_attempts: int = 6,
) -> JudgeVerdict:
    """``judge.judge_one`` with exponential-backoff retry on transient
    API errors."""
    delay = 4.0
    for attempt in range(1, max_attempts + 1):
        try:
            return judge.judge_one(
                trial_path=trial_path,
                stage=stage,
                prompt=prompt,
                max_tokens=JUDGE_MAX_TOKENS,
            )
        except Exception as exc:
            if not _is_transient(exc) or attempt == max_attempts:
                raise
            print(
                f"      [retry {attempt}/{max_attempts - 1}] transient API "
                f"error ({type(exc).__name__}); waiting {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
    raise AssertionError("unreachable")  # pragma: no cover


# --- Criteria files (read once; injected whole into the judge prompts) --
def _criteria() -> dict[str, str]:
    return {
        "ideal_induction_md": (FRAMEWORK_DIR / "ideal_induction.md").read_text(),
        "pass_fail_criteria_md": (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text(),
        "prediction_tests_md": (FRAMEWORK_DIR / "prediction_tests.md").read_text(),
    }


def _build_stage1_prompt(c: dict[str, str], stage1_response: str) -> str:
    return PromptTemplate(JUDGE_PROMPTS_DIR / "judge_stage1.md").render(
        ideal_induction_md=c["ideal_induction_md"],
        stage1_response=stage1_response,
    )


def _build_stage2_prompt(c: dict[str, str], s1: str, s2: str) -> str:
    return PromptTemplate(JUDGE_PROMPTS_DIR / "judge_stage2.md").render(
        pass_fail_criteria_md=c["pass_fail_criteria_md"],
        ideal_induction_md=c["ideal_induction_md"],
        stage1_response=s1,
        stage2_response=s2,
    )


def _build_stage3_prompt(c: dict[str, str], s2: str, s3: str) -> str:
    return PromptTemplate(JUDGE_PROMPTS_DIR / "judge_stage3.md").render(
        prediction_tests_md=c["prediction_tests_md"],
        pass_fail_criteria_md=c["pass_fail_criteria_md"],
        ideal_induction_md=c["ideal_induction_md"],
        stage2_response=s2,
        stage3_response=s3,
    )


def _build_meta_prompt(c: dict[str, str], failure_summary: str, s4: str) -> str:
    return PromptTemplate(JUDGE_PROMPTS_DIR / "judge_meta.md").render(
        pass_fail_criteria_md=c["pass_fail_criteria_md"],
        stage_failures_summary=failure_summary,
        stage4_response=s4,
    )


def _load_trial(p: Path) -> dict[str, Any]:
    data: Any = json.loads(p.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"trial JSON {p} is not a dict")
    return data


def _verdict_of(parsed: dict[str, Any]) -> str | None:
    """PASS / FAIL from a judge verdict dict (Stage 3 uses overall_verdict)."""
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _consensus(va: str | None, vb: str | None) -> str:
    if va is None or vb is None:
        return "MISSING"
    if va == vb:
        return va
    return "DISAGREE"


def _summarise_failures(stage_verdicts: dict[str, str]) -> str:
    """Plain-text Stage 1-3 failure summary fed to the meta judge."""
    lines: list[str] = []
    for label, key in (
        ("Stage 1", "induction"),
        ("Stage 2", "formulation"),
        ("Stage 3", "prediction"),
    ):
        v = stage_verdicts.get(key, "MISSING")
        if v == "FAIL":
            lines.append(f"- {label}: FAIL.")
        elif v == "PASS":
            lines.append(f"- {label}: PASS.")
        elif v == "DISAGREE":
            lines.append(f"- {label}: judges split (treat as a possible failure).")
        else:
            lines.append(f"- {label}: no verdict available.")
    return "\n".join(lines)


# === Dispatch ===========================================================
def _judgments_dir(model_id: str) -> Path:
    return RESULTS_ROOT / model_id / FRAMEWORK_ID / "judgments"


def dispatch(
    models: list[str],
    n_trials: int,
    skip: set[str],
    judges: list[tuple[str, JudgeBase]],
) -> float:
    """Run both judges over every trial on disk. Returns total judge cost."""
    c = _criteria()
    total_cost = 0.0

    for model_id in models:
        model_root = RESULTS_ROOT / model_id / FRAMEWORK_ID
        if not model_root.is_dir():
            print(f"[skip] {model_id}: no trials at {model_root}")
            continue
        out_dir = _judgments_dir(model_id)
        out_dir.mkdir(parents=True, exist_ok=True)

        for t in range(n_trials):
            paths = {s: model_root / s / f"trial_{t}_t0.0.json" for s in (*CONTENT_STAGES, "meta")}
            missing = [s for s, p in paths.items() if not p.exists()]
            if missing:
                print(f"  [skip] {model_id} trial {t}: missing {missing}")
                continue
            print(f"--- {model_id} trial {t} ---")
            trials = {s: _load_trial(p) for s, p in paths.items()}

            prompts = {
                "induction": _build_stage1_prompt(c, trials["induction"]["response_text"]),
                "formulation": _build_stage2_prompt(
                    c, trials["induction"]["response_text"], trials["formulation"]["response_text"]
                ),
                "prediction": _build_stage3_prompt(
                    c, trials["formulation"]["response_text"], trials["prediction"]["response_text"]
                ),
            }

            consensus: dict[str, str] = {}
            for stage in CONTENT_STAGES:
                if stage in skip:
                    continue
                pv: dict[str, str | None] = {}
                for jfam, judge in judges:
                    v = _judge_with_retry(
                        judge, trial_path=paths[stage], stage=stage, prompt=prompts[stage]
                    )
                    judge.save_verdict(v, out_dir)
                    total_cost += v.cost_usd_estimate
                    pv[jfam] = _verdict_of(v.parsed_verdict) if v.parse_error is None else None
                consensus[stage] = _consensus(pv.get("anthropic"), pv.get("openai"))
                print(f"  {stage}: claude={pv.get('anthropic')} openai={pv.get('openai')}")

            if "meta" not in skip:
                meta_prompt = _build_meta_prompt(
                    c, _summarise_failures(consensus), trials["meta"]["response_text"]
                )
                for jfam, judge in judges:
                    v = _judge_with_retry(
                        judge, trial_path=paths["meta"], stage="meta", prompt=meta_prompt
                    )
                    judge.save_verdict(v, out_dir)
                    total_cost += v.cost_usd_estimate
                    oc = v.parsed_verdict.get("over_claim") if v.parsed_verdict else None
                    print(f"  meta: {jfam}={oc}")

    return total_cost


# === Aggregation ========================================================
def _load_verdicts(model_id: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    """Return {(trial_index, stage, judge_family): parsed_verdict}."""
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(_judgments_dir(model_id) / "*.json"))):
        d = json.loads(Path(fp).read_text())
        trial_name = Path(d["trial_path"]).name  # trial_<i>_t0.0.json
        if not trial_name.startswith("trial_"):
            continue
        trial_index = int(trial_name.split("_")[1])
        out[(trial_index, d["stage"], d["judge_family"])] = d.get("parsed_verdict") or {}
    return out


def _scenario_pairs(parsed: dict[str, Any]) -> dict[int, tuple[str | None, str | None]]:
    """From a judge_stage3 verdict: {scenario_index: (verdict, direction)}."""
    out: dict[int, tuple[str | None, str | None]] = {}
    for sc in parsed.get("scenarios") or []:
        if not isinstance(sc, dict):
            continue
        idx = sc.get("index")
        if not isinstance(idx, int):
            continue
        v = sc.get("verdict")
        d = sc.get("direction")
        v = v.strip().upper() if isinstance(v, str) else None
        d = d.strip().lower() if isinstance(d, str) else None
        out[idx] = (v if v in {"PASS", "FAIL"} else None, d)
    return out


def aggregate(models: list[str], n_trials: int, judge_cost: float) -> None:
    """Compute IRR + P1-P4 and append the report to 02_fmv_findings.md."""
    # Per-trial stage verdicts + meta over-claim.
    rows: list[dict[str, Any]] = []
    disagree_units = 0
    total_units = 0
    # P4 accumulators
    p4_leaked = 0  # direction-correct, ratio-FAIL
    p4_total = 0  # quantitative predictions with a consensus verdict
    p4_disagree = 0

    for model_id in models:
        v = _load_verdicts(model_id)
        for t in range(n_trials):
            stage_v: dict[str, str] = {}
            for stage in CONTENT_STAGES:
                a = v.get((t, stage, "anthropic"))
                b = v.get((t, stage, "openai"))
                if a is None or b is None:
                    stage_v[stage] = "MISSING"
                    continue
                cons = _consensus(_verdict_of(a), _verdict_of(b))
                stage_v[stage] = cons
                total_units += 1
                if cons == "DISAGREE":
                    disagree_units += 1
            # meta over-claim consensus
            ma = v.get((t, "meta", "anthropic")) or {}
            mb = v.get((t, "meta", "openai")) or {}
            oca = str(ma.get("over_claim", "")).lower() or None
            ocb = str(mb.get("over_claim", "")).lower() or None
            overclaim = oca if oca == ocb else ("DISAGREE" if oca and ocb else "MISSING")
            # P4: per quantitative scenario, consensus verdict + direction
            sa = _scenario_pairs(v.get((t, "prediction", "anthropic")) or {})
            sb = _scenario_pairs(v.get((t, "prediction", "openai")) or {})
            for sidx in QUANT_SCENARIOS:
                va, da = sa.get(sidx, (None, None))
                vb, db = sb.get(sidx, (None, None))
                if va is None or vb is None:
                    continue
                p4_total += 1
                if va != vb or da != db:
                    p4_disagree += 1
                    continue
                if va == "FAIL" and da == "correct":
                    p4_leaked += 1
            rows.append(
                {
                    "model": model_id,
                    "trial": t,
                    "s1": stage_v.get("induction", "MISSING"),
                    "s2": stage_v.get("formulation", "MISSING"),
                    "s3": stage_v.get("prediction", "MISSING"),
                    "overclaim": overclaim,
                }
            )

    judged = [r for r in rows if r["s1"] != "MISSING"]
    n = len(judged)
    irr = disagree_units / total_units if total_units else 0.0

    # P1 — Stage 1 FAIL count (DISAGREE excluded; preliminary if any disagree).
    s1_fail = sum(1 for r in judged if r["s1"] == "FAIL")
    s1_disagree = sum(1 for r in judged if r["s1"] == "DISAGREE")
    p1 = (
        "CONFIRMED"
        if s1_fail >= P1_CONFIRM
        else ("PARTIALLY CONFIRMED" if s1_fail >= P1_PARTIAL_LOW else "REFUTED")
    )

    # P2 — over-claiming rate among failure-containing trials.
    fail_trials = [r for r in judged if "FAIL" in (r["s1"], r["s2"], r["s3"])]
    oc_yes = sum(1 for r in fail_trials if r["overclaim"] == "yes")
    p2_rate = oc_yes / len(fail_trials) if fail_trials else 0.0
    p2 = (
        "CONFIRMED"
        if p2_rate >= P2_CONFIRM
        else ("PARTIALLY CONFIRMED" if p2_rate >= P2_PARTIAL_LOW else "REFUTED")
    )

    # P3 — IRR below threshold.
    p3 = (
        "CONFIRMED"
        if irr < P3_CONFIRM
        else ("PARTIALLY CONFIRMED" if irr < P3_PARTIAL_HIGH else "REFUTED")
    )

    # P4 — quantitative-leak share (of all 45 quant predictions).
    p4_denom = len(models) * n_trials * len(QUANT_SCENARIOS)
    p4_rate = p4_leaked / p4_denom if p4_denom else 0.0
    p4 = (
        "CONFIRMED"
        if p4_rate >= P4_CONFIRM
        else ("PARTIALLY CONFIRMED" if p4_rate >= P4_PARTIAL_LOW else "REFUTED")
    )

    preliminary = disagree_units > 0 or p4_disagree > 0

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out: list[str] = []
    out.append("\n## 02_fmv judging report\n")
    out.append(f"- Generated: `{ts}`\n")
    out.append("- Prereg lock: `prereg-02_fmv-locked`\n")
    out.append(f"- Models: {', '.join(models)} | trials judged: {n}\n")
    out.append(f"- Judge cost (estimated): ${judge_cost:.4f}\n")
    if preliminary:
        out.append(
            f"- **PRELIMINARY** — {disagree_units} Stage 1-3 dual-judge "
            f"disagreement(s) + {p4_disagree} quantitative-scenario "
            f"disagreement(s) await human audit; P1 / P2 / P4 below are "
            f"lower bounds until those are resolved.\n"
        )
    out.append("\n")

    out.append("### IRR (dual-judge disagreement, Stage 1-3)\n")
    out.append(f"- {disagree_units}/{total_units} judged units = **{irr:.2%}**\n\n")

    out.append("### Per-trial classification matrix\n\n")
    out.append("| Model | Trial | S1 | S2 | S3 | Over-claim |\n")
    out.append("|---|---|---|---|---|---|\n")
    for r in rows:
        out.append(
            f"| `{r['model']}` | {r['trial']} | {r['s1']} | {r['s2']} | "
            f"{r['s3']} | {r['overclaim']} |\n"
        )
    out.append("\n")

    out.append(f"### P1 — Induction failure  ·  **{p1}**\n")
    out.append(
        f"Stage 1 FAIL: {s1_fail}/{n} (threshold ≥ {P1_CONFIRM}); "
        f"DISAGREE pending: {s1_disagree}.\n\n"
    )
    out.append(f"### P2 — Meta-cognitive miscalibration  ·  **{p2}**\n")
    out.append(
        f"Over-claiming: {oc_yes}/{len(fail_trials)} failure-containing "
        f"trials = {p2_rate:.2%} (threshold ≥ {P2_CONFIRM:.0%}).\n\n"
    )
    out.append(f"### P3 — Mechanical criteria reduce disagreement  ·  **{p3}**\n")
    out.append(
        f"IRR {irr:.2%} (Confirmed < {P3_CONFIRM:.0%}; vs v0.1 content-axis IRR 36.67%).\n\n"
    )
    out.append(f"### P4 — Stage 3 quantitative leak  ·  **{p4}**\n")
    out.append(
        f"Direction-correct / ratio-leaked: {p4_leaked}/{p4_denom} "
        f"quantitative predictions = {p4_rate:.2%} (threshold ≥ "
        f"{P4_CONFIRM:.0%}); {p4_disagree} scenario-level disagreement(s) "
        f"pending.\n\n"
    )

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    if not FINDINGS_PATH.exists():
        FINDINGS_PATH.write_text("# PhysLit 02_fmv — Findings\n\n")
    with FINDINGS_PATH.open("a") as fh:
        fh.write("".join(out))

    print()
    print(f"=== P1 {p1} | P2 {p2} | P3 {p3} | P4 {p4} ===")
    if preliminary:
        print("(PRELIMINARY — disagreements await human audit)")
    print(f"Report appended to: {FINDINGS_PATH}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--n-trials", type=int, default=5)
    parser.add_argument("--skip-stage", default="")
    args = parser.parse_args()
    _load_dotenv()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    skip = {s.strip() for s in args.skip_stage.split(",") if s.strip()}

    judges: list[tuple[str, JudgeBase]] = [
        ("anthropic", ClaudeJudge()),
        ("openai", OpenAIJudge()),
    ]

    print("=== PhysLit 02_fmv dual-judge orchestrator ===")
    print(f"  models:   {models}")
    print(f"  n-trials: {args.n_trials}")
    print(f"  skip:     {sorted(skip) if skip else '(none)'}")
    print()

    judge_cost = dispatch(models, args.n_trials, skip, judges)

    print()
    print("=== Aggregating ===")
    aggregate(models, args.n_trials, judge_cost)
    return 0


if __name__ == "__main__":
    sys.exit(main())
