"""Backfill Stage 4 (meta / over-claim) judging on the structure-prompt
arms of F=mv and Aristotelian.

Context
-------
The structure-prompt re-runs ``02_fmv_2`` (F=mv) and ``01_aristotelian_3``
(Aristotelian) generated Stage 4 responses under ``results/<model>/<arm>/meta/``
but their content judges (``judge_02_fmv_2.py`` / ``judge_v0_3.py``)
deliberately skipped the meta stage. As a result those two arms have no
over-claim score, while Decay (single structure-prompt arm) does. This
script closes that gap so all three frameworks report Stage 4 over-claim
on the same (structure-prompt) condition.

This is an **additive re-analysis** in the spirit of v0.2. It does NOT
re-run any production trial and does NOT touch any sealed round's
verdicts. It only:

1. reads the EXISTING content-stage verdicts already on disk for the arm
   (``results/<model>/<arm>/judgments/<judge>_{induction,formulation,
   prediction}_*.json``) and recomputes the dual-judge consensus per
   stage, exactly as the original framework runner did;
2. builds the framework's own Stage 1-3 failure summary + meta prompt and
   dispatches BOTH judges on the existing Stage 4 response;
3. writes the new meta verdicts next to the content verdicts and prints a
   preliminary per-trial over-claim table (DISAGREE cases are flagged for
   human audit and excluded from the numerator until resolved).

Faithfulness: each arm mirrors its OWN framework's original meta path so
the new structure-arm number is same-recipe comparable to the published
baseline number (F=mv 4/6, Aristotelian 7/10):

- ``fmv``         -> ``frameworks/02_fmv/prompts/judge_meta.md`` (3-var
                     template, injects pass_fail_criteria), terse summary,
                     same recipe as ``judge_02_fmv.py``.
- ``aristotelian``-> top-level ``prompts/judge_meta.md`` (2-var template,
                     no criteria), verbose FAIL summary with reasoning +
                     evidence, FAIL-side dict on disagreement, same recipe
                     as ``judge_v0_1.py``.

Usage:
    uv run python scripts/judge_meta_backfill.py --arm fmv
    uv run python scripts/judge_meta_backfill.py --arm aristotelian
    uv run python scripts/judge_meta_backfill.py --arm both
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import signal
import sys
import time
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
RESULTS_ROOT = REPO_ROOT / "results"
DEFAULT_MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
JUDGE_MAX_TOKENS = 8192


# === Per-arm configuration ============================================
# Each arm replicates the meta recipe of the framework it belongs to.
ARMS: dict[str, dict[str, Any]] = {
    "fmv": {
        "arm_id": "02_fmv_2",
        "meta_template": REPO_ROOT / "frameworks" / "02_fmv" / "prompts" / "judge_meta.md",
        "criteria_path": REPO_ROOT / "frameworks" / "02_fmv" / "pass_fail_criteria.md",
        "summary_style": "terse",
        "inject_criteria": True,
        "baseline_label": "F=mv baseline over-claim = 4/6 (67%)",
    },
    "aristotelian": {
        "arm_id": "01_aristotelian_3",
        "meta_template": REPO_ROOT / "prompts" / "judge_meta.md",
        "criteria_path": None,
        "summary_style": "verbose",
        "inject_criteria": False,
        "baseline_label": "Aristotelian baseline over-claim = 7/10 (70%)",
    },
}


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


# === Transient-error retry (same contract as judge_03_decay.py) =======
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
    pass


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
    judge: JudgeBase, *, trial_path: Path, stage: str, prompt: str, max_attempts: int = 6
) -> JudgeVerdict:
    delay = 4.0
    signal.signal(signal.SIGALRM, _on_alarm)
    for attempt in range(1, max_attempts + 1):
        signal.alarm(CALL_TIMEOUT_SECONDS)
        try:
            result = judge.judge_one(
                trial_path=trial_path, stage=stage, prompt=prompt, max_tokens=JUDGE_MAX_TOKENS
            )
        except Exception as exc:
            signal.alarm(0)
            if not _is_transient(exc) or attempt == max_attempts:
                raise
            print(
                f"      [retry {attempt}/{max_attempts - 1}] {type(exc).__name__}; waiting {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
        else:
            signal.alarm(0)
            return result
    raise AssertionError("unreachable")  # pragma: no cover


# === Loading existing content verdicts ================================
def _trial_index_of(trial_path: str) -> int | None:
    name = Path(trial_path).name  # trial_<N>_t0.0.json
    try:
        return int(name.split("_")[1])
    except (IndexError, ValueError):
        return None


def _verdict_str(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _consensus(va: str | None, vb: str | None) -> str:
    if va is None or vb is None:
        return "MISSING"
    return va if va == vb else "DISAGREE"


def _load_content_verdicts(
    judgments_dir: Path,
) -> dict[int, dict[str, dict[str, dict[str, Any]]]]:
    """Return {trial: {stage: {judge_family: parsed_verdict}}} for the
    three content stages, read from verdicts already on disk."""
    out: dict[int, dict[str, dict[str, dict[str, Any]]]] = {}
    for fp in sorted(glob.glob(str(judgments_dir / "*.json"))):
        d = json.loads(Path(fp).read_text())
        stage = d.get("stage")
        if stage not in CONTENT_STAGES:
            continue
        jfam = d.get("judge_family")
        t = _trial_index_of(d.get("trial_path", ""))
        if t is None or jfam is None:
            continue
        pv = d.get("parsed_verdict") or {}
        out.setdefault(t, {}).setdefault(stage, {})[jfam] = pv
    return out


# === Failure-summary builders (per framework style) ===================
def _summary_terse(consensus: dict[str, str]) -> str:
    lines: list[str] = []
    for label, key in (
        ("Stage 1", "induction"),
        ("Stage 2", "formulation"),
        ("Stage 3", "prediction"),
    ):
        v = consensus.get(key, "MISSING")
        if v == "FAIL":
            lines.append(f"- {label}: FAIL.")
        elif v == "PASS":
            lines.append(f"- {label}: PASS.")
        elif v == "DISAGREE":
            lines.append(f"- {label}: judges split (treat as a possible failure).")
        else:
            lines.append(f"- {label}: no verdict available.")
    return "\n".join(lines)


def _summary_verbose(stage_pv: dict[str, dict[str, Any]]) -> str:
    """v0.1-style: FAIL lines carry reasoning + evidence. ``stage_pv`` maps
    stage -> the FAIL-side (or agreed) parsed_verdict dict."""
    lines: list[str] = []
    for label, key in (
        ("Stage 1", "induction"),
        ("Stage 2", "formulation"),
        ("Stage 3", "prediction"),
    ):
        v = stage_pv.get(key, {})
        verdict = v.get("verdict") or v.get("overall_verdict")
        if not verdict:
            continue
        if str(verdict).upper() == "FAIL":
            lines.append(
                f"- {label}: FAIL. reasoning: {v.get('reasoning', '')}. "
                f"evidence: {v.get('evidence', '')}"
            )
        else:
            lines.append(f"- {label}: PASS.")
    if not lines:
        return "(No verdicts available; cannot determine failures.)"
    return "\n".join(lines)


def _fail_side_pv(judge_pv: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Pick the parsed_verdict to represent a stage in the verbose summary:
    prefer a FAIL-side dict so the meta judge sees the failure (v0.1 rule)."""
    claude_v = judge_pv.get("anthropic", {})
    openai_v = judge_pv.get("openai", {})
    cv = (claude_v.get("verdict") or claude_v.get("overall_verdict") or "").upper()
    ov = (openai_v.get("verdict") or openai_v.get("overall_verdict") or "").upper()
    if cv == "FAIL":
        return claude_v
    if ov == "FAIL":
        return openai_v
    return claude_v or openai_v


# === Meta prompt builders =============================================
def _build_meta_prompt(cfg: dict[str, Any], failure_summary: str, s4: str) -> str:
    tmpl = PromptTemplate(cfg["meta_template"])
    if cfg["inject_criteria"]:
        return tmpl.render(
            pass_fail_criteria_md=Path(cfg["criteria_path"]).read_text(),
            stage_failures_summary=failure_summary,
            stage4_response=s4,
        )
    return tmpl.render(stage_failures_summary=failure_summary, stage4_response=s4)


def _run_meta_evidence_check(verdict: JudgeVerdict, response_text: str) -> int:
    """Mirror the decay meta evidence-check: verify the cited evidence is a
    substring of the Stage 4 response; flag fabrication. Returns fab count."""
    parsed = verdict.parsed_verdict or {}
    r = check_evidence(verdict=parsed, response_text=response_text)
    parsed["_evidence_check"] = [
        {
            "scope": "verdict",
            "found": r.found,
            "fabricated": r.fabricated,
            "evidence_required": r.evidence_required,
            "cited_evidence": r.cited_evidence,
            "reason": r.reason,
        }
    ]
    return 1 if r.fabricated else 0


# === Main per-arm routine =============================================
def run_arm(
    arm_key: str, models: list[str], n_trials: int, judges: list[tuple[str, JudgeBase]]
) -> None:
    cfg = ARMS[arm_key]
    arm_id = cfg["arm_id"]
    print(f"\n========== arm '{arm_key}' ({arm_id}) ==========")
    print(f"  meta template : {Path(cfg['meta_template']).relative_to(REPO_ROOT)}")
    print(f"  summary style : {cfg['summary_style']}  inject_criteria={cfg['inject_criteria']}")
    print(f"  reference     : {cfg['baseline_label']}\n")

    total_cost = 0.0
    total_fab = 0
    rows: list[dict[str, Any]] = []

    for model_id in models:
        arm_root = RESULTS_ROOT / model_id / arm_id
        judgments_dir = arm_root / "judgments"
        if not arm_root.is_dir():
            print(f"[skip] {model_id}: no arm dir at {arm_root}")
            continue
        content = _load_content_verdicts(judgments_dir)

        for t in range(n_trials):
            meta_path = arm_root / "meta" / f"trial_{t}_t0.0.json"
            if not meta_path.exists():
                print(f"  [skip] {model_id} trial {t}: missing meta response")
                continue
            s4 = json.loads(meta_path.read_text())["response_text"]

            judge_pv = content.get(t, {})  # {stage: {jfam: pv}}
            consensus = {
                st: _consensus(
                    _verdict_str(judge_pv.get(st, {}).get("anthropic", {})),
                    _verdict_str(judge_pv.get(st, {}).get("openai", {})),
                )
                for st in CONTENT_STAGES
            }
            content_fail = any(consensus[st] == "FAIL" for st in CONTENT_STAGES)
            content_split = any(consensus[st] == "DISAGREE" for st in CONTENT_STAGES)

            if cfg["summary_style"] == "verbose":
                stage_pv = {st: _fail_side_pv(judge_pv.get(st, {})) for st in CONTENT_STAGES}
                summary = _summary_verbose(stage_pv)
            else:
                summary = _summary_terse(consensus)

            meta_prompt = _build_meta_prompt(cfg, summary, s4)
            oc: dict[str, str | None] = {}
            for jfam, judge in judges:
                v = _judge_with_retry(judge, trial_path=meta_path, stage="meta", prompt=meta_prompt)
                total_fab += _run_meta_evidence_check(v, s4)
                judge.save_verdict(v, judgments_dir)
                total_cost += v.cost_usd_estimate
                raw = (v.parsed_verdict or {}).get("over_claim")
                oc[jfam] = str(raw).lower() if raw is not None else None
            oc_cons = (
                oc["anthropic"]
                if oc.get("anthropic") == oc.get("openai")
                else ("DISAGREE" if oc.get("anthropic") and oc.get("openai") else "MISSING")
            )
            print(
                f"  {model_id} t{t}: content[{consensus['induction']}/"
                f"{consensus['formulation']}/{consensus['prediction']}] "
                f"fail={content_fail} | meta a={oc.get('anthropic')} o={oc.get('openai')} "
                f"=> {oc_cons}"
            )
            rows.append(
                {
                    "model": model_id,
                    "trial": t,
                    "content_fail": content_fail,
                    "content_split": content_split,
                    "overclaim": oc_cons,
                }
            )

    # --- preliminary tally (pre human-audit of meta DISAGREE) ---
    fail_rows = [r for r in rows if r["content_fail"] or r["content_split"]]
    oc_yes = sum(1 for r in fail_rows if r["overclaim"] == "yes")
    oc_no = sum(1 for r in fail_rows if r["overclaim"] == "no")
    oc_dis = sum(1 for r in fail_rows if r["overclaim"] == "DISAGREE")
    print(f"\n  --- {arm_key} preliminary (pre-audit) ---")
    print(f"  failure-containing trials (consensus-FAIL or split): {len(fail_rows)}")
    print(f"  over-claim yes={oc_yes}  no={oc_no}  DISAGREE(needs audit)={oc_dis}")
    print(f"  judge cost: ${total_cost:.4f}   fabrication flags: {total_fab}")
    print(
        f"  NOTE: final denominator uses the post-audit content-FAIL set (paper Table); "
        f"audit the {oc_dis} meta DISAGREE case(s) before publishing."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=["fmv", "aristotelian", "both"], required=True)
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument("--n-trials", type=int, default=5)
    args = parser.parse_args()
    _load_dotenv()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    judges: list[tuple[str, JudgeBase]] = [("anthropic", ClaudeJudge()), ("openai", OpenAIJudge())]

    arms = ["fmv", "aristotelian"] if args.arm == "both" else [args.arm]
    for arm_key in arms:
        run_arm(arm_key, models, args.n_trials, judges)
    return 0


if __name__ == "__main__":
    sys.exit(main())
