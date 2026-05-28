"""v0.3 dual-judge orchestrator — content axis + structural axis.

Judges the **treatment arm** of the v0.3 axiomatisation control
(``predictions/v0_3_prereg.md``). For every treatment trial under
``results/<model>/01_aristotelian_3/``:

- **Content axis** — Stage 1/2/3 responses scored by the two content
  judges (Claude + GPT-5.5) with the v0.1 GLOBAL judge prompts
  (``prompts/judge_stage{1,2,3}.md``) and the v0.1 criteria
  (``frameworks/01_aristotelian/{ideal_induction,pass_fail_criteria,
  prediction_tests}.md``), frozen at ``prereg-v0.1-locked``. Verdicts
  → ``results/<model>/01_aristotelian_3/judgments/``. Stage 4 (meta) is **not**
  judged (prereg §1.5).
- **Structural axis** — the Stage 1 rule set (Stage 2 as context)
  scored by the two structural judges with the v0.2 structural
  criteria (``frameworks/01_aristotelian/structural_criteria.md``) and
  the global structural judge prompt (``prompts/judge_structural.md``),
  frozen at ``prereg-v0.2-locked``. Verdicts → ``results/<model>/01_aristotelian_3/
  structural/``.

Writes a **preliminary** judging section to ``analysis/aristotelian/v0_3_findings.md``;
DISAGREE cases are flagged for human audit. The canonical P1 / P2
verdicts and the treatment-vs-control comparison are computed by
``scripts/apply_v0_3.py`` after any audit.

Prompts/criteria are read from the v0.1/v0.2 frozen locations; only
trial data comes from the ``01_aristotelian_3/`` tree. No existing code is modified.

Usage:
    uv run python scripts/judge_v0_3.py [--models <csv>] [--n-trials N]
                                        [--skip-axis content|structural]
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
from pathlib import Path
from typing import Any

from physlit.judges import ClaudeJudge, JudgeBase, JudgeVerdict, OpenAIJudge
from physlit.prompts import PromptTemplate
from physlit.scenarios import load_scenarios, render_scenarios_block

REPO = Path(__file__).resolve().parent.parent
TREATMENT_ID = "01_aristotelian_3"  # results subtree for the v0.3 treatment arm
SOURCE_FRAMEWORK_DIR = REPO / "frameworks" / "01_aristotelian"  # criteria
GLOBAL_PROMPTS_DIR = REPO / "prompts"  # v0.1 global judge prompts
RESULTS = REPO / "results"
FINDINGS = REPO / "analysis" / "aristotelian" / "v0_3_findings.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
JUDGE_MAX_TOKENS = 8192
CALL_TIMEOUT_SECONDS = 300


def _load_dotenv() -> None:
    env = REPO / ".env.local"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        s = raw.strip()
        if s and not s.startswith("#") and "=" in s:
            k, _, v = s.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


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
    return any(m in text for m in _TRANSIENT_MARKERS)


def _judge_with_retry(
    judge: JudgeBase, *, trial_path: Path, stage: str, prompt: str
) -> JudgeVerdict:
    delay = 4.0
    signal.signal(signal.SIGALRM, _on_alarm)
    for attempt in range(1, 7):
        signal.alarm(CALL_TIMEOUT_SECONDS)
        try:
            result = judge.judge_one(
                trial_path=trial_path, stage=stage, prompt=prompt, max_tokens=JUDGE_MAX_TOKENS
            )
        except Exception as exc:
            signal.alarm(0)
            if not _is_transient(exc) or attempt == 6:
                raise
            print(
                f"      [retry {attempt}/5] {type(exc).__name__}; waiting {delay:.0f}s",
                flush=True,
            )
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
        else:
            signal.alarm(0)
            return result
    raise AssertionError("unreachable")  # pragma: no cover


def _trial_path(model: str, trial: int, stage: str) -> Path:
    return RESULTS / model / TREATMENT_ID / stage / f"trial_{trial}_t0.0.json"


def _response(model: str, trial: int, stage: str) -> str:
    p = _trial_path(model, trial, stage)
    return json.loads(p.read_text())["response_text"] if p.exists() else "(missing)"


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _consensus(va: str | None, vb: str | None) -> str:
    if va is None or vb is None:
        return "MISSING"
    return va if va == vb else "DISAGREE"


def _extract_section(md: str, header: str) -> str:
    """Extract one ``## <header>`` section verbatim. Same helper as judge_v0_1.py."""
    pattern = re.compile(
        rf"^## {re.escape(header)}\s*\n(.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(md)
    if match is None:
        raise ValueError(f"section '## {header}' not found")
    return match.group(0).strip()


def _content_criteria() -> dict[str, str]:
    """Pre-slice the v0.1 criteria into the sections the global judge
    prompts expect (matches judge_v0_1.py's prompt construction)."""
    ideal_md = (SOURCE_FRAMEWORK_DIR / "ideal_induction.md").read_text()
    pf_md = (SOURCE_FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()
    scenarios = load_scenarios(SOURCE_FRAMEWORK_DIR / "prediction_tests.md")
    return {
        "ideal_induction_md": ideal_md,
        "banned_concepts_section": _extract_section(ideal_md, "3. Banned concepts"),
        "pass_fail_stage1": _extract_section(pf_md, "Stage 1 — Induction"),
        "pass_fail_stage2": _extract_section(pf_md, "Stage 2 — Formulation"),
        "pass_fail_stage3": _extract_section(pf_md, "Stage 3 — Prediction"),
        "scenarios_block": render_scenarios_block(scenarios),
    }


def _content_prompt(stage: str, c: dict[str, str], s1: str, s2: str, s3: str) -> str:
    if stage == "induction":
        return PromptTemplate(GLOBAL_PROMPTS_DIR / "judge_stage1.md").render(
            ideal_induction_md=c["ideal_induction_md"],
            pass_fail_stage1=c["pass_fail_stage1"],
            stage1_response=s1,
        )
    if stage == "formulation":
        return PromptTemplate(GLOBAL_PROMPTS_DIR / "judge_stage2.md").render(
            pass_fail_stage2=c["pass_fail_stage2"],
            banned_concepts_section=c["banned_concepts_section"],
            stage1_response=s1,
            stage2_response=s2,
        )
    return PromptTemplate(GLOBAL_PROMPTS_DIR / "judge_stage3.md").render(
        pass_fail_stage3=c["pass_fail_stage3"],
        scenarios_block=c["scenarios_block"],
        stage2_response=s2,
        stage3_response=s3,
    )


def _structural_prompt(s1: str, s2: str) -> str:
    return PromptTemplate(GLOBAL_PROMPTS_DIR / "judge_structural.md").render(
        structural_criteria_md=(SOURCE_FRAMEWORK_DIR / "structural_criteria.md").read_text(),
        observations_md=(SOURCE_FRAMEWORK_DIR / "observations.md").read_text(),
        stage1_response=s1,
        stage2_response=s2,
    )


def dispatch(
    models: list[str], n_trials: int, skip_axis: str, judges: list[tuple[str, JudgeBase]]
) -> float:
    c = _content_criteria()
    total_cost = 0.0
    for model in models:
        model_root = RESULTS / model / TREATMENT_ID
        if not model_root.is_dir():
            print(f"[skip] {model}: no treatment trials at {model_root}")
            continue
        content_dir = model_root / "judgments"
        structural_dir = model_root / "structural"
        content_dir.mkdir(parents=True, exist_ok=True)
        structural_dir.mkdir(parents=True, exist_ok=True)

        for t in range(n_trials):
            paths = {s: _trial_path(model, t, s) for s in CONTENT_STAGES}
            missing = [s for s, p in paths.items() if not p.exists()]
            if missing:
                print(f"  [skip] {model} trial {t}: missing {missing}")
                continue
            s1 = _response(model, t, "induction")
            s2 = _response(model, t, "formulation")
            s3 = _response(model, t, "prediction")
            print(f"--- {model} trial {t} ---")

            if skip_axis != "content":
                for stage in CONTENT_STAGES:
                    prompt = _content_prompt(stage, c, s1, s2, s3)
                    pv: dict[str, str | None] = {}
                    for jfam, judge in judges:
                        v = _judge_with_retry(
                            judge, trial_path=paths[stage], stage=stage, prompt=prompt
                        )
                        judge.save_verdict(v, content_dir)
                        total_cost += v.cost_usd_estimate
                        pv[jfam] = _verdict(v.parsed_verdict) if v.parse_error is None else None
                    print(f"  {stage}: claude={pv.get('anthropic')} openai={pv.get('openai')}")

            if skip_axis != "structural":
                prompt = _structural_prompt(s1, s2)
                sv: dict[str, str | None] = {}
                for jfam, judge in judges:
                    v = _judge_with_retry(
                        judge, trial_path=paths["induction"], stage="structural", prompt=prompt
                    )
                    judge.save_verdict(v, structural_dir)
                    total_cost += v.cost_usd_estimate
                    sv[jfam] = _verdict(v.parsed_verdict) if v.parse_error is None else None
                print(f"  structural: claude={sv.get('anthropic')} openai={sv.get('openai')}")
    return total_cost


def _load_verdicts(model: str, subdir: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / TREATMENT_ID / subdir / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if name.startswith("trial_"):
            out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
                d.get("parsed_verdict") or {}
            )
    return out


def aggregate(models: list[str], n_trials: int, judge_cost: float) -> None:
    rows: list[dict[str, Any]] = []
    c_disagree = c_total = s_disagree = s_total = 0
    for model in models:
        cj = _load_verdicts(model, "judgments")
        sj = _load_verdicts(model, "structural")
        for t in range(n_trials):
            stage_v: dict[str, str] = {}
            for stage in CONTENT_STAGES:
                a = cj.get((t, stage, "anthropic"))
                b = cj.get((t, stage, "openai"))
                cons = _consensus(
                    _verdict(a) if a is not None else None,
                    _verdict(b) if b is not None else None,
                )
                stage_v[stage] = cons
                if cons != "MISSING":
                    c_total += 1
                if cons == "DISAGREE":
                    c_disagree += 1
            content = (
                "PASS"
                if all(stage_v[s] == "PASS" for s in CONTENT_STAGES)
                else (
                    "DISAGREE"
                    if "DISAGREE" in stage_v.values() and "FAIL" not in stage_v.values()
                    else ("FAIL" if "FAIL" in stage_v.values() else "MISSING")
                )
            )
            sa = sj.get((t, "structural", "anthropic"))
            sb = sj.get((t, "structural", "openai"))
            structural = _consensus(
                _verdict(sa) if sa is not None else None,
                _verdict(sb) if sb is not None else None,
            )
            if structural != "MISSING":
                s_total += 1
            if structural == "DISAGREE":
                s_disagree += 1
            rows.append(
                {
                    "model": model,
                    "trial": t,
                    "s1": stage_v["induction"],
                    "s2": stage_v["formulation"],
                    "s3": stage_v["prediction"],
                    "content": content,
                    "structural": structural,
                }
            )

    c_irr = c_disagree / c_total if c_total else 0.0
    s_irr = s_disagree / s_total if s_total else 0.0
    preliminary = c_disagree > 0 or s_disagree > 0

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    o: list[str] = []
    o.append("\n## v0.3 judging report (preliminary)\n")
    o.append(f"- Generated: `{ts}`\n")
    o.append("- Prereg lock: `prereg-v0.3-locked`\n")
    o.append(f"- Judge cost (estimated): ${judge_cost:.4f}\n")
    o.append(
        "- Content axis judged with v0.1 criteria + v0.1 global judge prompts; "
        "structural axis with v0.2 criteria + global structural judge prompt.\n"
    )
    if preliminary:
        o.append(
            f"- **PRELIMINARY** — {c_disagree} content + {s_disagree} structural "
            f"dual-judge disagreement(s) await human audit. Canonical P1 / P2 "
            f"and the treatment-vs-control comparison: `apply_v0_3.py`.\n"
        )
    o.append("\n### Treatment-arm IRR\n")
    o.append(f"- Content (Stage 1-3): {c_disagree}/{c_total} units = **{c_irr:.2%}**\n")
    o.append(f"- Structural: {s_disagree}/{s_total} trials = **{s_irr:.2%}**\n\n")
    o.append("### Per-trial treatment-arm verdicts\n\n")
    o.append("| Model | Trial | S1 | S2 | S3 | Content-only | Structural |\n")
    o.append("|---|---|---|---|---|---|---|\n")
    for r in rows:
        o.append(
            f"| `{r['model']}` | {r['trial']} | {r['s1']} | {r['s2']} | "
            f"{r['s3']} | {r['content']} | {r['structural']} |\n"
        )
    o.append("\n")

    FINDINGS.parent.mkdir(parents=True, exist_ok=True)
    if not FINDINGS.exists():
        FINDINGS.write_text("# PhysLit v0.3 — Findings\n\n")
    with FINDINGS.open("a") as fh:
        fh.write("".join(o))

    print()
    print(f"=== content IRR {c_irr:.2%} | structural IRR {s_irr:.2%} ===")
    if preliminary:
        print(f"(PRELIMINARY — {c_disagree} content + {s_disagree} structural disagreements)")
    print(f"Preliminary report appended to {FINDINGS.relative_to(REPO)}")
    print("Run scripts/apply_v0_3.py for canonical P1 / P2 + treatment-vs-control.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", default=",".join(MODELS))
    parser.add_argument("--n-trials", type=int, default=5)
    parser.add_argument("--skip-axis", default="", choices=("", "content", "structural"))
    args = parser.parse_args()
    _load_dotenv()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    judges: list[tuple[str, JudgeBase]] = [("anthropic", ClaudeJudge()), ("openai", OpenAIJudge())]

    print("=== PhysLit v0.3 dual-judge orchestrator (Aristotelian treatment arm) ===")
    print(f"  models:   {models}")
    print(f"  n-trials: {args.n_trials}")
    print(f"  axes:     {'both' if not args.skip_axis else 'skip ' + args.skip_axis}\n")

    cost = dispatch(models, args.n_trials, args.skip_axis, judges)
    print()
    print("=== Aggregating (preliminary) ===")
    aggregate(models, args.n_trials, cost)
    return 0


if __name__ == "__main__":
    sys.exit(main())
