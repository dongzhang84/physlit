"""03_decay Stage 1 + Stage 2 judge **dry-run** on the Phase-1.5 trial.

Single-purpose pre-lock script: pointed at the Claude x N=1 dry-run
trial at ``results/_dryrun/20260522T073027Z/...``, runs the two
content judges (Claude + GPT-5.5) on Stage 1 and Stage 2 only, and
prints / saves their verdicts.

Goal: verify before locking the prereg that the locked judge prompts
+ criteria actually catch the issues exposed by the dry-run trial,
namely

- **Gap 2 (Stage 2):** Claude introduced ``g`` / ``v* = g/k`` /
  "absolute hotness Θ(t) with K" — concept imports that evade the
  §3 banned-token list lexically. Does ``judge_stage2.md`` flag them?
- **Gap 3 (Stage 1):** Claude's Rule 2 makes the per-second rate
  slowness-dependent, contradicting N4 (universal across systems).
  Does ``judge_stage1.md`` flag this as N4 FAIL?

This script does **not** count toward the production judgments. Its
output is saved under
``results/_dryrun/<ts>/<model-id>/03_decay/judgments_dryrun/``.
Findings go to ``analysis/03_decay_dryrun_findings.md``.

Usage:
    uv run python scripts/judge_03_decay_dryrun.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from physlit.judges import ClaudeJudge, JudgeBase, JudgeVerdict, OpenAIJudge
from physlit.prompts import PromptTemplate

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "03_decay"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
JUDGE_PROMPTS_DIR = FRAMEWORK_DIR / "prompts"

# Hardcoded dry-run target (single trial, single model).
DRYRUN_ROOT = (
    REPO_ROOT / "results" / "_dryrun" / "20260522T073027Z" / "claude-opus-4-7" / FRAMEWORK_ID
)
TRIAL_PATHS = {
    "induction": DRYRUN_ROOT / "induction" / "trial_0_t0.0.json",
    "formulation": DRYRUN_ROOT / "formulation" / "trial_0_t0.0.json",
}
OUTPUT_DIR = DRYRUN_ROOT / "judgments_dryrun"

JUDGE_MAX_TOKENS = 8192


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


def _criteria() -> dict[str, str]:
    return {
        "ideal_induction_md": (FRAMEWORK_DIR / "ideal_induction.md").read_text(),
        "pass_fail_criteria_md": (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text(),
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


def _print_verdict_summary(stage: str, family: str, v: JudgeVerdict) -> None:
    if v.parse_error:
        print(f"  [{family}/{stage}] PARSE ERROR: {v.parse_error}")
        return
    p: dict[str, Any] = v.parsed_verdict
    if stage == "induction":
        # judge_stage1.md schema: {verdict, first_fail_step, first_fail_clause, evidence, reasoning}
        print(f"  [{family}/{stage}] verdict={p.get('verdict')!r}")
        print(f"     first_fail_step:   {p.get('first_fail_step')}")
        print(f"     first_fail_clause: {p.get('first_fail_clause')!r}")
        ev = p.get("evidence")
        if ev:
            ev_short = ev if len(str(ev)) <= 240 else str(ev)[:237] + "..."
            print(f"     evidence:          {ev_short!r}")
        print(f"     reasoning:         {p.get('reasoning')!r}")
    else:  # formulation
        # judge_stage2.md schema varies — print whatever the judge returned.
        print(f"  [{family}/{stage}] keys={sorted(p.keys())}")
        for k in (
            "verdict",
            "first_fail_step",
            "first_fail_clause",
            "failed_criterion",
            "evidence",
            "reasoning",
        ):
            if k in p:
                val = p[k]
                if isinstance(val, str) and len(val) > 240:
                    val = val[:237] + "..."
                print(f"     {k}: {val!r}")
    print(f"     cost: ${v.cost_usd_estimate:.4f} | in={v.input_tokens} out={v.output_tokens}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stages",
        default="induction,formulation",
        help="Stages to judge (comma-separated subset of {induction,formulation}).",
    )
    args = parser.parse_args()
    stages = [s.strip() for s in args.stages.split(",") if s.strip()]

    _load_dotenv()

    # Ensure both trial files exist.
    for stage, p in TRIAL_PATHS.items():
        if stage not in stages:
            continue
        if not p.exists():
            print(f"[ERR] missing trial file: {p}", file=sys.stderr)
            return 2

    c = _criteria()
    s1_text = json.loads(TRIAL_PATHS["induction"].read_text())["response_text"]
    s2_text = (
        json.loads(TRIAL_PATHS["formulation"].read_text())["response_text"]
        if "formulation" in stages
        else ""
    )

    judges: list[tuple[str, JudgeBase]] = [
        ("anthropic", ClaudeJudge()),
        ("openai", OpenAIJudge()),
    ]

    print("=== 03_decay Stage 1 + Stage 2 judge dry-run ===")
    print(f"  trial root: {DRYRUN_ROOT}")
    print(f"  stages:     {stages}")
    print(f"  output:     {OUTPUT_DIR}")
    print()

    total_cost = 0.0
    for stage in stages:
        prompt = (
            _build_stage1_prompt(c, s1_text)
            if stage == "induction"
            else _build_stage2_prompt(c, s1_text, s2_text)
        )
        print(f"--- {stage} (prompt length: {len(prompt)} chars) ---")
        for family, judge in judges:
            v = judge.judge_one(
                trial_path=TRIAL_PATHS[stage],
                stage=stage,
                prompt=prompt,
                max_tokens=JUDGE_MAX_TOKENS,
            )
            judge.save_verdict(v, OUTPUT_DIR)
            total_cost += v.cost_usd_estimate
            _print_verdict_summary(stage, family, v)
        print()

    print(f"=== total dry-run judge cost: ${total_cost:.4f} ===")
    print(f"verdict JSON saved under: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
