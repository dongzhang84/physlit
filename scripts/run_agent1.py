"""v0.2 Agent 1 runner — content-axis disagree resolver.

Identifies every v0.1 content disagree case (Stage 1 / 2 / 3 where the
two LLM judges produced different verdicts), dispatches Gemini 3.1 Pro
with the `prompts/agent1_content_resolver.md` template, and saves
each resolver verdict to
``results/<model>/01_aristotelian/content_resolved/``.

Per the v0.2 prereg envelope:
- Fresh Gemini client per call (no cross-call state)
- Strict identity equality check on every response
- Save raw_response + parsed JSON + token counts + USD estimate
- One verdict per (model, trial, stage) disagree case (target: 17 calls)

The script is reproducible: re-running with the same v0.1 trial data
will dispatch fresh calls and emit fresh verdicts — Gemini sampling
is non-deterministic, so verdict text will differ across runs, but
the structural shape (PASS/FAIL per case) should be stable.

Usage:
    uv run python scripts/run_agent1.py [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from physlit.prompts import PromptTemplate  # noqa: E402
from physlit.v0_2 import GeminiAgent, find_content_disagree_cases  # noqa: E402
from physlit.v0_2.gemini_agent import DEFAULT_AGENT_MAX_TOKENS  # noqa: E402

FRAMEWORK_ID = "01_aristotelian"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPT_PATH = REPO_ROOT / "prompts" / "agent1_content_resolver.md"
RESULTS_ROOT = REPO_ROOT / "results"
DEFAULT_MODELS = (
    "claude-opus-4-7",
    "gpt-5.5-2026-04-23",
    "gemini-3.1-pro-preview",
)
N_TRIALS = 5


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


def _verdict_label(parsed: dict[str, object]) -> str:
    """Normalise a content-judge verdict label.

    Stage 3 judgments use the ``overall_verdict`` JSON key (one verdict
    over five scenarios); Stages 1-2 use ``verdict``. Mirrors the
    fallback used in ``physlit.judges.aggregate._verdict_str``.
    """
    raw = parsed.get("verdict") or parsed.get("overall_verdict") or "?"
    return str(raw)


def _build_prompt(
    template: PromptTemplate,
    *,
    case_metadata: dict[str, object],
    tested_response: str,
    judge_a_verdict: str,
    judge_a_reasoning: str,
    judge_b_verdict: str,
    judge_b_reasoning: str,
    ideal_induction_md: str,
    pass_fail_criteria_md: str,
) -> str:
    return template.render(
        ideal_induction_md=ideal_induction_md,
        pass_fail_criteria_md=pass_fail_criteria_md,
        framework_id=str(case_metadata["framework_id"]),
        tested_model=str(case_metadata["tested_model"]),
        trial_index=str(case_metadata["trial_index"]),
        stage=str(case_metadata["stage"]),
        tested_response=tested_response,
        judge_a_verdict=judge_a_verdict,
        judge_a_reasoning=judge_a_reasoning,
        judge_b_verdict=judge_b_verdict,
        judge_b_reasoning=judge_b_reasoning,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the disagree cases that would be dispatched. No API calls.",
    )
    args = parser.parse_args()

    _load_dotenv()

    template = PromptTemplate(PROMPT_PATH)
    ideal_induction_md = (FRAMEWORK_DIR / "ideal_induction.md").read_text()
    pass_fail_criteria_md = (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()

    cases = find_content_disagree_cases(
        results_root=RESULTS_ROOT,
        model_ids=DEFAULT_MODELS,
        n_trials=N_TRIALS,
    )

    print(f"Found {len(cases)} content disagree cases:", file=sys.stderr)
    by_stage: dict[str, int] = {}
    for case in cases:
        by_stage[case.stage] = by_stage.get(case.stage, 0) + 1
    for stage, count in sorted(by_stage.items()):
        print(f"  {stage}: {count}", file=sys.stderr)
    print(f"  total: {len(cases)} (v0.2 prereg expected 17)\n", file=sys.stderr)

    if args.dry_run:
        for case in cases:
            print(f"  {case.model_id}  trial {case.trial_index}  {case.stage}")
        return 0

    agent = GeminiAgent()
    total_cost = 0.0
    for i, case in enumerate(cases, 1):
        prompt = _build_prompt(
            template,
            case_metadata={
                "framework_id": FRAMEWORK_ID,
                "tested_model": case.model_id,
                "trial_index": case.trial_index,
                "stage": case.stage,
            },
            tested_response=case.response_text,
            judge_a_verdict=_verdict_label(case.judge_a_parsed),
            judge_a_reasoning=str(case.judge_a_parsed.get("reasoning", "")),
            judge_b_verdict=_verdict_label(case.judge_b_parsed),
            judge_b_reasoning=str(case.judge_b_parsed.get("reasoning", "")),
            ideal_induction_md=ideal_induction_md,
            pass_fail_criteria_md=pass_fail_criteria_md,
        )

        verdict = agent.judge_one(
            trial_path=case.trial_path,
            stage=f"agent1_content_{case.stage}",
            prompt=prompt,
            max_tokens=DEFAULT_AGENT_MAX_TOKENS,
        )

        out_dir = RESULTS_ROOT / case.model_id / FRAMEWORK_ID / "content_resolved"
        saved = agent.save_verdict(verdict, out_dir)

        verdict_summary = verdict.parsed_verdict.get("verdict", "PARSE_ERR")
        total_cost += verdict.cost_usd_estimate
        print(
            f"  [{i:>2}/{len(cases)}] {case.model_id} trial {case.trial_index} "
            f"{case.stage}: Agent 1 → {verdict_summary}  "
            f"(${verdict.cost_usd_estimate:.4f})  → {saved.relative_to(REPO_ROOT)}",
            file=sys.stderr,
        )
        time.sleep(0.5)  # gentle pacing

    print(f"\nTotal Agent 1 spend: ${total_cost:.4f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
