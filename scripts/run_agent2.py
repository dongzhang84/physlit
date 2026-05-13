"""v0.2 Agent 2 runner — structural-axis disagree resolver.

Run AFTER `scripts/run_structural_judging.py`. Loads every
structural-judge verdict, finds the (model, trial) pairs where the
two structural judges produced different PASS/FAIL verdicts, and
dispatches Gemini 3.1 Pro (the Agent 2 prompt) to resolve each.

The number of disagree cases here is not known in advance — it
depends on how often Claude and GPT structural judges differ on the
60 trial-sets. v0.1 content-axis IRR was 36.67 %; structural-axis IRR
is unknown until the structural-judging run completes.

Per the v0.2 prereg envelope:
- Fresh Gemini client per call
- Strict identity equality check
- Save raw_response + parsed JSON + token counts + USD estimate

Usage:
    uv run python scripts/run_agent2.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from physlit.prompts import PromptTemplate  # noqa: E402
from physlit.v0_2 import GeminiAgent, load_structural_verdicts  # noqa: E402
from physlit.v0_2.gemini_agent import DEFAULT_AGENT_MAX_TOKENS  # noqa: E402

FRAMEWORK_ID = "01_aristotelian"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPT_PATH = REPO_ROOT / "prompts" / "agent2_structural_resolver.md"
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


def _load_stage_response(model_id: str, trial_index: int, stage: str) -> tuple[Path, str]:
    stage_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / stage
    matches = sorted(stage_dir.glob(f"trial_{trial_index}_t*.json"))
    if not matches:
        raise SystemExit(f"No trial JSON found for {model_id} trial {trial_index} stage {stage}")
    trial_path = matches[0]
    data = json.loads(trial_path.read_text())
    return trial_path, str(data["response_text"])


def _build_prompt(
    template: PromptTemplate,
    *,
    structural_criteria_md: str,
    observations_md: str,
    stage1_response: str,
    stage2_response: str,
    case_metadata: dict[str, object],
    judge_a_parsed: dict[str, object],
    judge_b_parsed: dict[str, object],
) -> str:
    return template.render(
        structural_criteria_md=structural_criteria_md,
        observations_md=observations_md,
        framework_id=str(case_metadata["framework_id"]),
        tested_model=str(case_metadata["tested_model"]),
        trial_index=str(case_metadata["trial_index"]),
        stage1_response=stage1_response,
        stage2_response=stage2_response,
        judge_a_verdict=str(judge_a_parsed.get("verdict", "?")),
        judge_a_failed_criteria=json.dumps(judge_a_parsed.get("failed_criteria", [])),
        judge_a_rule_count=str(judge_a_parsed.get("rule_count", "?")),
        judge_a_reasoning=str(judge_a_parsed.get("reasoning", "")),
        judge_b_verdict=str(judge_b_parsed.get("verdict", "?")),
        judge_b_failed_criteria=json.dumps(judge_b_parsed.get("failed_criteria", [])),
        judge_b_rule_count=str(judge_b_parsed.get("rule_count", "?")),
        judge_b_reasoning=str(judge_b_parsed.get("reasoning", "")),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the structural disagree cases. No API calls.",
    )
    args = parser.parse_args()

    _load_dotenv()

    template = PromptTemplate(PROMPT_PATH)
    structural_criteria_md = (FRAMEWORK_DIR / "structural_criteria.md").read_text()
    observations_md = (FRAMEWORK_DIR / "observations.md").read_text()

    bundles = load_structural_verdicts(
        results_root=RESULTS_ROOT,
        model_ids=DEFAULT_MODELS,
        n_trials=N_TRIALS,
    )

    disagree_keys = [
        (model_id, trial_index)
        for (model_id, trial_index), bundle in sorted(bundles.items())
        if bundle.joint_verdict == "DISAGREE"
    ]

    print(
        f"Found {len(disagree_keys)} structural-axis disagree cases "
        f"(structural-axis IRR not pre-known; report at run time).\n",
        file=sys.stderr,
    )

    if args.dry_run:
        for model_id, trial_index in disagree_keys:
            bundle = bundles[(model_id, trial_index)]
            assert bundle.judge_a_parsed is not None
            assert bundle.judge_b_parsed is not None
            print(
                f"  {model_id} trial {trial_index}: "
                f"Claude={bundle.judge_a_parsed.get('verdict')} "
                f"GPT={bundle.judge_b_parsed.get('verdict')}"
            )
        return 0

    agent = GeminiAgent()
    total_cost = 0.0
    for i, (model_id, trial_index) in enumerate(disagree_keys, 1):
        bundle = bundles[(model_id, trial_index)]
        assert bundle.judge_a_parsed is not None
        assert bundle.judge_b_parsed is not None

        trial_path, stage1_response = _load_stage_response(model_id, trial_index, "induction")
        _, stage2_response = _load_stage_response(model_id, trial_index, "formulation")

        prompt = _build_prompt(
            template,
            structural_criteria_md=structural_criteria_md,
            observations_md=observations_md,
            stage1_response=stage1_response,
            stage2_response=stage2_response,
            case_metadata={
                "framework_id": FRAMEWORK_ID,
                "tested_model": model_id,
                "trial_index": trial_index,
            },
            judge_a_parsed=bundle.judge_a_parsed,
            judge_b_parsed=bundle.judge_b_parsed,
        )

        verdict = agent.judge_one(
            trial_path=trial_path,
            stage="agent2_structural",
            prompt=prompt,
            max_tokens=DEFAULT_AGENT_MAX_TOKENS,
        )

        out_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / "structural_resolved"
        saved = agent.save_verdict(verdict, out_dir)

        verdict_summary = verdict.parsed_verdict.get("verdict", "PARSE_ERR")
        total_cost += verdict.cost_usd_estimate
        print(
            f"  [{i:>2}/{len(disagree_keys)}] {model_id} trial {trial_index}: "
            f"Agent 2 → {verdict_summary}  "
            f"(${verdict.cost_usd_estimate:.4f})  → {saved.relative_to(REPO_ROOT)}",
            file=sys.stderr,
        )
        time.sleep(0.5)

    print(f"\nTotal Agent 2 spend: ${total_cost:.4f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
