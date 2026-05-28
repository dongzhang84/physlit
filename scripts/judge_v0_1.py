"""v0.1 dual-judge orchestrator (Phase 8).

Loads every Stage 1-3 trial JSON under ``results/<model-id>/`` for the
production run, dispatches each (trial, stage) to two judges (Claude +
GPT), saves their structured verdicts, and writes a final aggregate
report into ``analysis/aristotelian/v0_1_findings.md``.

Per ``predictions/v0_1_prereg.md`` Scoring procedure:

- Per-trial classification = both judges agree on PASS or FAIL.
- Disagreements feed the IRR rate (published, not folded into P1/P3).
- P1 verdict and P3 verdict computed from the classifications using the
  rules locked in the prereg (see physlit.judges.aggregate).

Usage:
    uv run python scripts/judge_v0_1.py [options]

Options:
    --models <csv>           Subset of models to judge. Default: all.
    --n-trials <int>         Trials per model expected on disk. Default: 5.
    --skip-stage <csv>       Stages to skip (induction, formulation,
                             prediction, meta). For partial reruns.

Output:
    results/<model-id>/judgments/  — one JSON per (judge, stage, trial)
    analysis/aristotelian/v0_1_findings.md      — appended report block

Cost:
    ~$15-20 estimated for the full 60-trial x 3-stage x 2-judge sweep
    plus 60-trial x 1-meta x 2-judge over-claim assessment.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

from physlit.judges import ClaudeJudge, JudgeBase, JudgeVerdict, OpenAIJudge
from physlit.judges.aggregate import (
    classify_trials,
    evaluate_p1,
    evaluate_p3,
    load_trial_verdicts,
)
from physlit.prompts import PromptTemplate
from physlit.scenarios import load_scenarios, render_scenarios_block

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "01_aristotelian"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPTS_DIR = REPO_ROOT / "prompts"
RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"

DEFAULT_MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")


def _load_dotenv() -> None:
    env_path = REPO_ROOT / ".env.local"
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        import os

        os.environ.setdefault(key.strip(), value.strip())


def _extract_section(md: str, header: str) -> str:
    """Extract one ``## <header>`` section verbatim from a markdown file."""
    pattern = re.compile(
        rf"^## {re.escape(header)}\s*\n(.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(md)
    if match is None:
        raise ValueError(f"section '## {header}' not found")
    return match.group(0).strip()


def _load_trial(trial_path: Path) -> dict[str, Any]:
    data: Any = json.loads(trial_path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"trial JSON {trial_path} is not a dict")
    return data


def _build_stage1_prompt(stage1_response: str) -> str:
    tmpl = PromptTemplate(PROMPTS_DIR / "judge_stage1.md")
    ideal_md = (FRAMEWORK_DIR / "ideal_induction.md").read_text()
    pf_md = (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()
    pf_stage1 = _extract_section(pf_md, "Stage 1 — Induction")
    return tmpl.render(
        ideal_induction_md=ideal_md,
        pass_fail_stage1=pf_stage1,
        stage1_response=stage1_response,
    )


def _build_stage2_prompt(stage1_response: str, stage2_response: str) -> str:
    tmpl = PromptTemplate(PROMPTS_DIR / "judge_stage2.md")
    pf_md = (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()
    pf_stage2 = _extract_section(pf_md, "Stage 2 — Formulation")
    ideal_md = (FRAMEWORK_DIR / "ideal_induction.md").read_text()
    banned = _extract_section(ideal_md, "3. Banned concepts")
    return tmpl.render(
        pass_fail_stage2=pf_stage2,
        banned_concepts_section=banned,
        stage1_response=stage1_response,
        stage2_response=stage2_response,
    )


def _build_stage3_prompt(stage2_response: str, stage3_response: str) -> str:
    tmpl = PromptTemplate(PROMPTS_DIR / "judge_stage3.md")
    pf_md = (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()
    pf_stage3 = _extract_section(pf_md, "Stage 3 — Prediction")
    scenarios = load_scenarios(FRAMEWORK_DIR / "prediction_tests.md")
    return tmpl.render(
        pass_fail_stage3=pf_stage3,
        scenarios_block=render_scenarios_block(scenarios),
        stage2_response=stage2_response,
        stage3_response=stage3_response,
    )


def _build_meta_prompt(stage_failures_summary: str, stage4_response: str) -> str:
    tmpl = PromptTemplate(PROMPTS_DIR / "judge_meta.md")
    return tmpl.render(
        stage_failures_summary=stage_failures_summary,
        stage4_response=stage4_response,
    )


def _summarise_failures(s1_v: dict[str, Any], s2_v: dict[str, Any], s3_v: dict[str, Any]) -> str:
    """Human-readable summary of which stages failed for one trial,
    used as input to the meta-judge prompt. Inputs are the parsed_verdict
    dicts for the consensus verdict per stage (when both judges agree)."""
    lines: list[str] = []
    for label, v in (("Stage 1", s1_v), ("Stage 2", s2_v), ("Stage 3", s3_v)):
        verdict = v.get("verdict") or v.get("overall_verdict")
        if not verdict:
            continue
        if verdict.upper() == "FAIL":
            reasoning = v.get("reasoning", "")
            evidence = v.get("evidence", "")
            lines.append(f"- {label}: FAIL. reasoning: {reasoning}. evidence: {evidence}")
        else:
            lines.append(f"- {label}: PASS.")
    if not lines:
        return "(No verdicts available; cannot determine failures.)"
    return "\n".join(lines)


def judge_trial(
    *,
    judge: JudgeBase,
    trial_path: Path,
    stage: str,
    prompt: str,
    output_dir: Path,
) -> JudgeVerdict:
    verdict = judge.judge_one(trial_path=trial_path, stage=stage, prompt=prompt, max_tokens=2048)
    judge.save_verdict(verdict, output_dir)
    return verdict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--models",
        default=",".join(DEFAULT_MODELS),
        help="Comma-separated list of model ids whose trials to judge.",
    )
    parser.add_argument("--n-trials", type=int, default=5)
    parser.add_argument(
        "--skip-stage",
        default="",
        help="Comma-separated stages to skip (induction|formulation|prediction|meta).",
    )
    args = parser.parse_args()
    _load_dotenv()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    skip = {s.strip() for s in args.skip_stage.split(",") if s.strip()}

    claude_judge = ClaudeJudge()
    openai_judge = OpenAIJudge()
    judges: list[tuple[str, JudgeBase]] = [
        ("anthropic", claude_judge),
        ("openai", openai_judge),
    ]

    print("=== PhysLit v0.1 dual-judge orchestrator ===")
    print(f"  models:    {models}")
    print(f"  n-trials:  {args.n_trials}")
    print(f"  skip:      {sorted(skip) if skip else '(none)'}")
    print()

    judge_total_cost = 0.0

    # --- Stage 1, 2, 3 judging ---
    for model_id in models:
        model_root = RESULTS_ROOT / model_id / FRAMEWORK_ID
        if not model_root.exists():
            print(f"[skip] {model_id}: no production trials at {model_root}")
            continue
        verdicts_dir = RESULTS_ROOT / model_id / "judgments"
        verdicts_dir.mkdir(parents=True, exist_ok=True)

        for trial_index in range(args.n_trials):
            print(f"--- {model_id} trial {trial_index} ---")
            trial_paths = {
                "induction": model_root / "induction" / f"trial_{trial_index}_t0.0.json",
                "formulation": model_root / "formulation" / f"trial_{trial_index}_t0.0.json",
                "prediction": model_root / "prediction" / f"trial_{trial_index}_t0.0.json",
                "meta": model_root / "meta" / f"trial_{trial_index}_t0.0.json",
            }
            missing = [s for s, p in trial_paths.items() if not p.exists()]
            if missing:
                print(f"  [skip] missing trial files: {missing}")
                continue

            s1 = _load_trial(trial_paths["induction"])
            s2 = _load_trial(trial_paths["formulation"])
            s3 = _load_trial(trial_paths["prediction"])
            s4 = _load_trial(trial_paths["meta"])

            stage_to_prompt = {
                "induction": (
                    trial_paths["induction"],
                    _build_stage1_prompt(s1["response_text"]),
                ),
                "formulation": (
                    trial_paths["formulation"],
                    _build_stage2_prompt(s1["response_text"], s2["response_text"]),
                ),
                "prediction": (
                    trial_paths["prediction"],
                    _build_stage3_prompt(s2["response_text"], s3["response_text"]),
                ),
            }

            stage_consensus_verdict: dict[str, dict[str, Any]] = {}

            for stage in ("induction", "formulation", "prediction"):
                if stage in skip:
                    continue
                trial_path, prompt = stage_to_prompt[stage]
                vs: list[JudgeVerdict] = []
                for _jname, judge in judges:
                    v = judge_trial(
                        judge=judge,
                        trial_path=trial_path,
                        stage=stage,
                        prompt=prompt,
                        output_dir=verdicts_dir,
                    )
                    vs.append(v)
                    judge_total_cost += v.cost_usd_estimate
                # Compose a "consensus" parsed_verdict for use as meta-judge
                # input. If both judges agreed, use either parsed verdict;
                # if they disagreed, prefer the FAIL-side dict so the
                # meta-judge sees a failure summary to evaluate.
                claude_v = vs[0].parsed_verdict if vs[0].parse_error is None else {}
                openai_v = vs[1].parsed_verdict if vs[1].parse_error is None else {}
                cv = (claude_v.get("verdict") or claude_v.get("overall_verdict") or "").upper()
                ov = (openai_v.get("verdict") or openai_v.get("overall_verdict") or "").upper()
                if cv == "FAIL":
                    stage_consensus_verdict[stage] = claude_v
                elif ov == "FAIL":
                    stage_consensus_verdict[stage] = openai_v
                else:
                    stage_consensus_verdict[stage] = claude_v or openai_v
                print(f"  {stage}: claude={cv or '?'} | openai={ov or '?'}")

            # Meta over-claim
            if "meta" not in skip:
                summary = _summarise_failures(
                    stage_consensus_verdict.get("induction", {}),
                    stage_consensus_verdict.get("formulation", {}),
                    stage_consensus_verdict.get("prediction", {}),
                )
                meta_prompt = _build_meta_prompt(summary, s4["response_text"])
                for jname, judge in judges:
                    v = judge_trial(
                        judge=judge,
                        trial_path=trial_paths["meta"],
                        stage="meta",
                        prompt=meta_prompt,
                        output_dir=verdicts_dir,
                    )
                    judge_total_cost += v.cost_usd_estimate
                    label = v.parsed_verdict.get("over_claim") if v.parsed_verdict else "?"
                    print(f"  meta:   {jname}={label}")

    # --- Aggregate ---
    print()
    print("=== Aggregating verdicts ===")
    all_verdicts: dict[tuple[str, int, str, str], dict[str, Any]] = {}
    for model_id in models:
        verdicts_dir = RESULTS_ROOT / model_id / "judgments"
        if not verdicts_dir.exists():
            continue
        loaded = load_trial_verdicts(verdicts_dir)
        all_verdicts.update(loaded)
    classifications, irr = classify_trials(all_verdicts, models, args.n_trials)
    p1 = evaluate_p1(classifications)
    p3 = evaluate_p3(classifications)

    # --- Write report ---
    report_lines: list[str] = []
    report_lines.append("\n## v0.1 final report\n")
    report_lines.append(f"- Generated: `{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}`\n")
    report_lines.append(f"- Models: {', '.join(models)}\n")
    report_lines.append(f"- N trials per model: {args.n_trials}\n")
    report_lines.append(f"- Judge cost (estimated): ${judge_total_cost:.4f}\n\n")

    report_lines.append("### IRR (judge disagreement rate)\n")
    report_lines.append(
        f"- Stage 1: {irr.stage1_disagree}/{irr.stage1_total} = "
        f"{(irr.stage1_disagree / max(1, irr.stage1_total)):.2%}\n"
    )
    report_lines.append(
        f"- Stage 2: {irr.stage2_disagree}/{irr.stage2_total} = "
        f"{(irr.stage2_disagree / max(1, irr.stage2_total)):.2%}\n"
    )
    report_lines.append(
        f"- Stage 3: {irr.stage3_disagree}/{irr.stage3_total} = "
        f"{(irr.stage3_disagree / max(1, irr.stage3_total)):.2%}\n"
    )
    report_lines.append(
        f"- Meta:    {irr.meta_disagree}/{irr.meta_total} = "
        f"{(irr.meta_disagree / max(1, irr.meta_total)):.2%}\n"
    )
    report_lines.append(f"- Overall: {irr.overall_disagree_rate:.2%}\n\n")

    report_lines.append("### P1 — Induction failure under training-data conflict\n")
    report_lines.append(f"**Verdict: {p1.verdict.upper()}**\n\n")
    report_lines.append(f"{p1.notes}\n\n")

    report_lines.append("### P3 — Meta-cognitive miscalibration\n")
    report_lines.append(f"**Verdict: {p3.verdict.upper()}**\n\n")
    report_lines.append(f"{p3.notes}\n\n")

    report_lines.append("### Per-trial classification matrix\n\n")
    report_lines.append("| Model | Trial | S1 | S2 | S3 | Over-claim | Any failure |\n")
    report_lines.append("|---|---|---|---|---|---|---|\n")
    for c in classifications:
        report_lines.append(
            f"| `{c.model_id}` | {c.trial_index} | "
            f"{c.stage1_verdict} | {c.stage2_verdict} | {c.stage3_verdict} | "
            f"{c.overclaim} | {'yes' if c.has_any_stage_failure else 'no'} |\n"
        )

    findings_path = ANALYSIS_DIR / "aristotelian" / "v0_1_findings.md"
    findings_path.parent.mkdir(parents=True, exist_ok=True)
    if not findings_path.exists():
        findings_path.write_text("# PhysLit v0.1 — Findings\n\n")
    with findings_path.open("a") as fh:
        fh.write("".join(report_lines))

    print(f"\n=== Done. P1: {p1.verdict.upper()} | P3: {p3.verdict.upper()} ===")
    print(f"Report appended to: {findings_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
