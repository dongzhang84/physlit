"""v0.2 structural-axis dual-judge runner.

For each of the 60 v0.1 production trials (3 models x5 trials x4
stages; here we use 3 models x5 trials = 15 trial-sets), loads the
trial's Stage 1 (induction) and Stage 2 (formulation) responses,
concatenates them, and dispatches the result to both structural
judges (Claude Opus + GPT-5.5) using the
`prompts/judge_structural.md` template.

Each judge emits a single PASS/FAIL verdict per trial (per the
prereg's D3 decision: one structural verdict per trial, not per
criterion). Verdicts are saved to
``results/<model>/01_aristotelian/structural/<judge>_structural_<id>.json``.

Per the v0.2 prereg:
- Fresh client per call, strict identity equality check
- Total expected calls: 15 trials x2 judges = 30 calls

Usage:
    uv run python scripts/run_structural_judging.py [--dry-run]
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

from physlit.judges import ClaudeJudge, JudgeBase, OpenAIJudge  # noqa: E402
from physlit.prompts import PromptTemplate  # noqa: E402

FRAMEWORK_ID = "01_aristotelian"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPT_PATH = REPO_ROOT / "prompts" / "judge_structural.md"
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


def _load_trial_text(model_id: str, trial_index: int, stage: str) -> tuple[Path, str]:
    """Find a trial JSON and return its (path, response_text)."""
    stage_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / stage
    # Trial filenames look like `trial_<N>_t<temp>.json`; v0.1 used t0.0.
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
) -> str:
    return template.render(
        structural_criteria_md=structural_criteria_md,
        observations_md=observations_md,
        stage1_response=stage1_response,
        stage2_response=stage2_response,
    )


def _judge_one_trial(
    *,
    judges: tuple[JudgeBase, ...],
    prompt: str,
    trial_path: Path,
    out_dir: Path,
) -> list[tuple[str, str, float]]:
    """Dispatch both judges on one trial; return per-judge (family, verdict, cost)."""
    summaries: list[tuple[str, str, float]] = []
    for judge in judges:
        verdict = judge.judge_one(
            trial_path=trial_path,
            stage="structural",
            prompt=prompt,
            max_tokens=2048,
        )
        judge.save_verdict(verdict, out_dir)
        v_str = verdict.parsed_verdict.get("verdict", "PARSE_ERR")
        summaries.append((judge.judge_family, str(v_str), verdict.cost_usd_estimate))
    return summaries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the trial-set that would be judged. No API calls.",
    )
    args = parser.parse_args()

    _load_dotenv()

    template = PromptTemplate(PROMPT_PATH)
    structural_criteria_md = (FRAMEWORK_DIR / "structural_criteria.md").read_text()
    observations_md = (FRAMEWORK_DIR / "observations.md").read_text()

    targets: list[tuple[str, int]] = [
        (model_id, trial_index) for model_id in DEFAULT_MODELS for trial_index in range(N_TRIALS)
    ]

    print(
        f"Structural judging targets: {len(targets)} trials x2 judges = "
        f"{2 * len(targets)} API calls\n",
        file=sys.stderr,
    )

    if args.dry_run:
        for model_id, trial_index in targets:
            print(f"  {model_id}  trial {trial_index}")
        return 0

    judges: tuple[JudgeBase, ...] = (ClaudeJudge(), OpenAIJudge())
    total_cost = 0.0

    for i, (model_id, trial_index) in enumerate(targets, 1):
        trial_path, stage1_response = _load_trial_text(model_id, trial_index, "induction")
        _, stage2_response = _load_trial_text(model_id, trial_index, "formulation")

        prompt = _build_prompt(
            template,
            structural_criteria_md=structural_criteria_md,
            observations_md=observations_md,
            stage1_response=stage1_response,
            stage2_response=stage2_response,
        )

        out_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / "structural"
        summaries = _judge_one_trial(
            judges=judges,
            prompt=prompt,
            trial_path=trial_path,
            out_dir=out_dir,
        )

        for family, verdict_str, cost in summaries:
            total_cost += cost
            print(
                f"  [{i:>2}/{len(targets)}] {model_id} trial {trial_index} "
                f"({family:>9}): {verdict_str:>4}  (${cost:.4f})",
                file=sys.stderr,
            )
        time.sleep(0.5)  # gentle pacing

    print(f"\nTotal structural-judging spend: ${total_cost:.4f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
