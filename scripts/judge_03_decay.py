"""03_decay dual-judge orchestrator + P1-P4 aggregator.

Written before any 03_decay production trial lands, so the scoring
logic is fixed in advance of seeing data (a methodology-hygiene
requirement: judging must not be tuned to the results).

For every Stage 1-4 trial JSON under ``results/<model>/03_decay/``:

- Stages 1-3: dispatch to two content judges (Claude + GPT-5.5),
  each given the framework-specific judge prompt + the frozen
  criteria (locked at ``prereg-03_decay-locked``).
- Stage 4: build a Stage 1-3 failure summary, dispatch the meta judge.
- After every judge call, ``physlit.judges.evidence_check`` verifies
  the cited evidence is a substring of the tested-model response;
  fabricated verdicts are flagged and routed to human audit (Gap 4).
- Save every verdict to ``results/<model>/03_decay/judgments/``.

Then aggregate, per the locked ``predictions/03_decay_prereg.md``
§2-§3:

- **IRR**  = dual-judge disagreement over the 45 Stage 1-3 judged units
  (methodology-quality metric; not itself a prereg prediction).
- **P1**   = composite content PASS count (S1 ∧ S2 ∧ S3) compared
  against the F=mv 9/15 and Aristotelian 5/15 baselines.
  Confirmed iff PASS ≤ 4; Refuted iff PASS ≥ 5.
- **P2**   = modal §5 disqualifying pattern among Stage 1 FAIL
  first-FAIL clauses. Confirmed iff P2 (hidden-substrate framing)
  strictly the most-cited §5 pattern.
- **P3**   = three-bucket classification of the 60 quantitative
  Stage 3 predictions (Scenarios 1-4 across 15 trials). Confirmed
  iff count(direction-correct, ratio-leaked) > count(direction-wrong).
- **P4**   = over-claim count vs correct-self-identify count among
  failure-containing trials. Confirmed iff count(yes) > count(no).

DISAGREE cases (the two judges split) and judge-fabrication flags
are routed to human audit per the prereg; while unresolved they are
excluded from the P1 / P2 / P3 / P4 numerators, so verdicts are
reported as **preliminary lower bounds** whenever any audit is
pending.

This runner does not modify ``run_v0_1.py``, ``judge_v0_1.py``,
``judge_02_fmv.py``, ``judge_02_fmv_2.py``, ``judge_v0_3.py``, or
any library code; the 03_decay experiment is independent of all
prior PhysLit rounds.

Usage:
    uv run python scripts/judge_03_decay.py [options]

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
import re
import signal
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from physlit.judges import (
    ClaudeJudge,
    JudgeBase,
    JudgeVerdict,
    OpenAIJudge,
    check_evidence,
)
from physlit.prompts import PromptTemplate

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "03_decay"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
JUDGE_PROMPTS_DIR = FRAMEWORK_DIR / "prompts"
RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"
FINDINGS_PATH = ANALYSIS_DIR / "03_decay_findings.md"

DEFAULT_MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
JUDGE_MAX_TOKENS = 8192  # reasoning judges burn thinking tokens; keep headroom

# Quantitative Stage 3 scenarios with ratio binding (prereg P3). Scenario 5
# is qualitative + timescale and is judged separately for its PASS / FAIL
# but does not enter the three-bucket count for P3.
QUANT_SCENARIOS = (1, 2, 3, 4)

# §5 disqualifying patterns from frameworks/03_decay/ideal_induction.md
# (P1..P7). Used to tally the modal §5 pattern for P2.
S5_PATTERNS = ("P1", "P2", "P3", "P4", "P5", "P6", "P7")


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


# --- Transient-error retry (same contract as judge_02_fmv.py) ---------
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

CALL_TIMEOUT_SECONDS = 300


class _CallTimeout(Exception):
    """Raised when one judge call exceeds CALL_TIMEOUT_SECONDS."""


def _on_alarm(signum: int, frame: object) -> None:
    raise _CallTimeout(f"judge call exceeded {CALL_TIMEOUT_SECONDS}s")


def _is_transient(exc: Exception) -> bool:
    if isinstance(exc, _CallTimeout):
        return True
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
    signal.signal(signal.SIGALRM, _on_alarm)
    for attempt in range(1, max_attempts + 1):
        signal.alarm(CALL_TIMEOUT_SECONDS)
        try:
            result = judge.judge_one(
                trial_path=trial_path,
                stage=stage,
                prompt=prompt,
                max_tokens=JUDGE_MAX_TOKENS,
            )
        except Exception as exc:
            signal.alarm(0)
            if not _is_transient(exc) or attempt == max_attempts:
                raise
            print(
                f"      [retry {attempt}/{max_attempts - 1}] "
                f"{type(exc).__name__}; waiting {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
        else:
            signal.alarm(0)
            return result
    raise AssertionError("unreachable")  # pragma: no cover


# --- Criteria files (read once; injected whole into judge prompts) ----
def _criteria() -> dict[str, str]:
    return {
        "ideal_induction_md": (FRAMEWORK_DIR / "ideal_induction.md").read_text(),
        "pass_fail_criteria_md": (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text(),
        "prediction_tests_md": (FRAMEWORK_DIR / "prediction_tests.md").read_text(),
    }


def _build_stage1_prompt(c: dict[str, str], s1: str) -> str:
    return PromptTemplate(JUDGE_PROMPTS_DIR / "judge_stage1.md").render(
        ideal_induction_md=c["ideal_induction_md"],
        stage1_response=s1,
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


def _run_evidence_checks(verdict: JudgeVerdict, response_text: str) -> list[dict[str, Any]]:
    """Run evidence-check on every verdict-with-evidence emitted by the
    judge. Returns a list of per-evidence-claim results (the Stage 3
    judge emits one evidence claim per scenario; other stages emit at
    most one). Each entry has ``{found, fabricated, evidence_required,
    cited_evidence, reason, scope}``.

    The result list is also persisted into ``verdict.parsed_verdict``
    under the key ``_evidence_check`` so downstream aggregation can
    see it.
    """
    parsed: dict[str, Any] = verdict.parsed_verdict or {}
    results: list[dict[str, Any]] = []

    if "scenarios" in parsed:
        # Stage 3 — one evidence claim per scenario.
        for sc in parsed.get("scenarios") or []:
            if not isinstance(sc, dict):
                continue
            r = check_evidence(verdict=sc, response_text=response_text)
            results.append(
                {
                    "scope": f"scenario_{sc.get('index')}",
                    "found": r.found,
                    "fabricated": r.fabricated,
                    "evidence_required": r.evidence_required,
                    "cited_evidence": r.cited_evidence,
                    "reason": r.reason,
                }
            )
    else:
        r = check_evidence(verdict=parsed, response_text=response_text)
        results.append(
            {
                "scope": "verdict",
                "found": r.found,
                "fabricated": r.fabricated,
                "evidence_required": r.evidence_required,
                "cited_evidence": r.cited_evidence,
                "reason": r.reason,
            }
        )

    # Persist into the verdict dict so save_verdict serialises it too.
    parsed["_evidence_check"] = results
    # JudgeVerdict is frozen; mutating parsed_verdict in place is the
    # supported escape hatch (it is the same dict object referenced by
    # the dataclass field).
    return results


# === Dispatch =========================================================
def _judgments_dir(model_id: str) -> Path:
    return RESULTS_ROOT / model_id / FRAMEWORK_ID / "judgments"


def dispatch(
    models: list[str],
    n_trials: int,
    skip: set[str],
    judges: list[tuple[str, JudgeBase]],
) -> tuple[float, int]:
    """Run both judges over every trial on disk. Returns
    ``(total_judge_cost, total_fabrication_flags)``."""
    c = _criteria()
    total_cost = 0.0
    total_fab = 0

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

            stage_response = {s: trials[s]["response_text"] for s in (*CONTENT_STAGES, "meta")}
            prompts = {
                "induction": _build_stage1_prompt(c, stage_response["induction"]),
                "formulation": _build_stage2_prompt(
                    c, stage_response["induction"], stage_response["formulation"]
                ),
                "prediction": _build_stage3_prompt(
                    c, stage_response["formulation"], stage_response["prediction"]
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
                    ev_results = _run_evidence_checks(v, stage_response[stage])
                    fab_here = sum(1 for r in ev_results if r["fabricated"])
                    total_fab += fab_here
                    judge.save_verdict(v, out_dir)
                    total_cost += v.cost_usd_estimate
                    pv[jfam] = _verdict_of(v.parsed_verdict) if v.parse_error is None else None
                    fab_tag = f" [FAB={fab_here}]" if fab_here else ""
                    print(f"  {stage} {jfam}={pv[jfam]}{fab_tag}", end="  ", flush=True)
                consensus[stage] = _consensus(pv.get("anthropic"), pv.get("openai"))
                print(f"|cons={consensus[stage]}")

            if "meta" not in skip:
                meta_prompt = _build_meta_prompt(
                    c, _summarise_failures(consensus), stage_response["meta"]
                )
                for jfam, judge in judges:
                    v = _judge_with_retry(
                        judge, trial_path=paths["meta"], stage="meta", prompt=meta_prompt
                    )
                    ev_results = _run_evidence_checks(v, stage_response["meta"])
                    fab_here = sum(1 for r in ev_results if r["fabricated"])
                    total_fab += fab_here
                    judge.save_verdict(v, out_dir)
                    total_cost += v.cost_usd_estimate
                    oc = v.parsed_verdict.get("over_claim") if v.parsed_verdict else None
                    fab_tag = f" [FAB={fab_here}]" if fab_here else ""
                    print(f"  meta {jfam}={oc}{fab_tag}")

    return total_cost, total_fab


# === Aggregation ======================================================
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


def _scenario_triples(
    parsed: dict[str, Any],
) -> dict[int, tuple[str | None, str | None, bool]]:
    """From a judge_stage3 verdict: {scenario_index: (verdict, direction,
    any_fabricated)}."""
    out: dict[int, tuple[str | None, str | None, bool]] = {}
    fab_by_idx: dict[int, bool] = {}
    for ev in parsed.get("_evidence_check") or []:
        scope = ev.get("scope", "")
        m = re.match(r"scenario_(\d+)$", scope)
        if m and ev.get("fabricated"):
            fab_by_idx[int(m.group(1))] = True
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
        out[idx] = (
            v if v in {"PASS", "FAIL"} else None,
            d,
            fab_by_idx.get(idx, False),
        )
    return out


def _extract_s5_pattern(parsed: dict[str, Any]) -> str | None:
    """From a judge_stage1 FAIL verdict, return the §5 pattern label
    ('P1'..'P7') if the first-FAIL clause is a §5 pattern. Returns None
    for §3 banned-token FAILs, N-condition FAILs, or PASS verdicts."""
    if _verdict_of(parsed) != "FAIL":
        return None
    clause = parsed.get("first_fail_clause")
    if not isinstance(clause, str):
        return None
    # Match a bare P1..P7 token (the judge prompt schema). Patterns
    # prefixed with extra context ("§5 P2", "P2 (hidden-substrate)")
    # still match via regex.
    m = re.search(r"\bP[1-7]\b", clause)
    return m.group(0) if m else None


def _verdict_has_fabrication(parsed: dict[str, Any]) -> bool:
    return any(ev.get("fabricated") for ev in parsed.get("_evidence_check") or [])


def aggregate(models: list[str], n_trials: int, judge_cost: float, fab_count: int) -> None:
    """Compute IRR + P1-P4 and append the report to 03_decay_findings.md."""
    rows: list[dict[str, Any]] = []
    disagree_units = 0
    total_units = 0
    fab_units = 0
    # P2 accumulators
    s5_counts: Counter[str] = Counter()
    # P3 accumulators
    p3_buckets: Counter[str] = Counter()
    p3_disagree = 0
    p3_fab = 0

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
                # Fabrication flag (either judge) counts the unit for
                # mandatory human audit, just like a DISAGREE.
                fab_a = _verdict_has_fabrication(a)
                fab_b = _verdict_has_fabrication(b)
                if fab_a or fab_b:
                    fab_units += 1

            # meta over-claim consensus
            ma = v.get((t, "meta", "anthropic")) or {}
            mb = v.get((t, "meta", "openai")) or {}
            oca = str(ma.get("over_claim", "")).lower() or None
            ocb = str(mb.get("over_claim", "")).lower() or None
            if oca and oca == ocb:
                overclaim = oca
            elif oca and ocb:
                overclaim = "DISAGREE"
            else:
                overclaim = "MISSING"

            # P2: §5-pattern modal (only when both judges agree on the
            # §5 label; otherwise this trial doesn't contribute to the
            # distribution).
            pa_s5 = _extract_s5_pattern(a or {})
            pb_s5 = _extract_s5_pattern(b or {})
            if pa_s5 is not None and pa_s5 == pb_s5:
                s5_counts[pa_s5] += 1

            # P3: per-quant-scenario three-bucket classification.
            sa = _scenario_triples(v.get((t, "prediction", "anthropic")) or {})
            sb = _scenario_triples(v.get((t, "prediction", "openai")) or {})
            for sidx in QUANT_SCENARIOS:
                va, da, fa = sa.get(sidx, (None, None, False))
                vb, db, fb = sb.get(sidx, (None, None, False))
                if va is None or vb is None:
                    continue
                if fa or fb:
                    p3_fab += 1
                    continue
                if va != vb:
                    p3_disagree += 1
                    continue
                if va == "PASS":
                    p3_buckets["decay-correct"] += 1
                else:  # both FAIL
                    if da != db or da is None:
                        p3_disagree += 1
                        continue
                    if da == "correct":
                        p3_buckets["direction-correct, ratio-leaked"] += 1
                    elif da == "wrong":
                        p3_buckets["direction-wrong"] += 1
                    else:
                        # 'n/a' shouldn't appear for Scenarios 1-4 per
                        # the judge prompt; treat as disagree-pending.
                        p3_disagree += 1

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

    # P1 — composite content PASS (S1 AND S2 AND S3 all PASS).
    composite_pass = sum(
        1 for r in judged if r["s1"] == "PASS" and r["s2"] == "PASS" and r["s3"] == "PASS"
    )
    # Confirmed iff strictly less than 5 (below the Aristotelian 5/15 floor).
    if composite_pass <= 4:
        p1 = "CONFIRMED"
    elif composite_pass == 5:
        p1 = "REFUTED (tied-floor with Aristotelian 5/15)"
    else:
        p1 = "REFUTED"

    # P2 — modal §5 pattern.
    if not s5_counts:
        p2 = "VACUOUS (no §5-pattern FAILs cited by both judges)"
        p2_top = None
        p2_top_n = 0
    else:
        p2_top, p2_top_n = s5_counts.most_common(1)[0]
        # Is it strictly higher than every other pattern?
        others = [c for p, c in s5_counts.items() if p != p2_top]
        if p2_top == "P2" and (not others or p2_top_n > max(others)):
            p2 = "CONFIRMED"
        elif p2_top != "P2":
            p2 = f"REFUTED (modal pattern is {p2_top})"
        else:
            p2 = "REFUTED (P2 is tied with another pattern, not strictly modal)"

    # P3 — ratio-leaked vs direction-wrong.
    leaked = p3_buckets.get("direction-correct, ratio-leaked", 0)
    wrong = p3_buckets.get("direction-wrong", 0)
    correct = p3_buckets.get("decay-correct", 0)
    if leaked == 0 and wrong == 0:
        p3 = "VACUOUS (all quantitative predictions decay-correct)"
    elif leaked > wrong:
        p3 = "CONFIRMED"
    else:
        p3 = "REFUTED"

    # P4 — over-claim vs no-overclaim among failure-containing trials.
    fail_trials = [r for r in judged if "FAIL" in (r["s1"], r["s2"], r["s3"])]
    oc_yes = sum(1 for r in fail_trials if r["overclaim"] == "yes")
    oc_no = sum(1 for r in fail_trials if r["overclaim"] == "no")
    if not fail_trials:
        p4 = "VACUOUS (no failure-containing trials)"
    elif oc_yes > oc_no:
        p4 = "CONFIRMED"
    else:
        p4 = "REFUTED"

    preliminary = disagree_units > 0 or fab_units > 0 or p3_disagree > 0 or p3_fab > 0

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out: list[str] = []
    out.append("\n## 03_decay judging report\n")
    out.append(f"- Generated: `{ts}`\n")
    out.append("- Prereg lock: `prereg-03_decay-locked`\n")
    out.append(f"- Models: {', '.join(models)} | trials judged: {n}\n")
    out.append(f"- Judge cost (estimated): ${judge_cost:.4f}\n")
    out.append(
        f"- Fabrication flags (evidence_check): {fab_count} total "
        f"({fab_units} judged units affected on Stage 1-3 + meta)\n"
    )
    if preliminary:
        out.append(
            f"- **PRELIMINARY** — {disagree_units} Stage 1-3 dual-judge "
            f"disagreement(s), {fab_units} fabrication-flagged unit(s), "
            f"{p3_disagree} P3 scenario disagreement(s), {p3_fab} P3 "
            f"fabrication-flagged scenario(s) await human audit; "
            f"verdicts below are lower bounds until resolved.\n"
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

    out.append(f"### P1 — Decay harder than both priors  ·  **{p1}**\n")
    out.append(
        f"Composite content PASS: **{composite_pass}/{n}**. Confirmed "
        f"iff ≤ 4; Refuted iff ≥ 5. Baselines: F=mv 9/15, "
        f"Aristotelian 5/15.\n\n"
    )

    out.append(f"### P2 — Hidden-substrate framing is the modal §5 pattern  ·  **{p2}**\n")
    if s5_counts:
        out.append("§5-pattern citation counts (both judges agreeing on the label):\n")
        for pat in S5_PATTERNS:
            out.append(f"- {pat}: {s5_counts.get(pat, 0)}\n")
    else:
        out.append("(No §5-pattern FAILs with both judges agreeing on the label.)\n")
    out.append("\n")

    out.append(f"### P3 — Ratio-leaked > direction-wrong (60 quant predictions)  ·  **{p3}**\n")
    out.append(
        f"- decay-correct: **{correct}**\n"
        f"- direction-correct, ratio-leaked: **{leaked}**\n"
        f"- direction-wrong: **{wrong}**\n"
        f"- pending (judge disagreement or fabrication): "
        f"**{p3_disagree + p3_fab}**\n"
        f"Confirmed iff leaked > wrong.\n\n"
    )

    out.append(f"### P4 — Over-claim > correct-self-identify  ·  **{p4}**\n")
    out.append(
        f"Among {len(fail_trials)} failure-containing trials: "
        f"over-claim **yes={oc_yes}**, no**={oc_no}**. "
        f"Confirmed iff yes > no.\n\n"
    )

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    if not FINDINGS_PATH.exists():
        FINDINGS_PATH.write_text(
            "# PhysLit 03_decay — Findings\n\n"
            "This file accumulates 03_decay evaluation findings,\n"
            "including R1(b) Gemini post-trial-set re-ping disclosures\n"
            "and the dual-judge + evidence_check report.\n"
        )
    with FINDINGS_PATH.open("a") as fh:
        fh.write("".join(out))

    print()
    print(f"=== P1 {p1} | P2 {p2} | P3 {p3} | P4 {p4} ===")
    if preliminary:
        print("(PRELIMINARY — disagreements / fabrication flags await human audit)")
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

    print("=== PhysLit 03_decay dual-judge orchestrator ===")
    print(f"  models:   {models}")
    print(f"  n-trials: {args.n_trials}")
    print(f"  skip:     {sorted(skip) if skip else '(none)'}")
    print()

    judge_cost, fab_count = dispatch(models, args.n_trials, skip, judges)

    print()
    print("=== Aggregating ===")
    aggregate(models, args.n_trials, judge_cost, fab_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
