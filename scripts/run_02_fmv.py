"""02_fmv production runner — F=mv World x {Claude, GPT-5.5, Gemini 3.1 Pro}.

Usage:
    uv run python scripts/run_02_fmv.py [options]

Options:
    --models <csv>          Subset of models to run (default: all three).
                            Allowed values: claude, openai, gemini.
    --n-trials <int>        Number of trials per (model, stage). Default: 5.
    --output-mode {production,calibration,dryrun}
                            ``production``  → results/<model-version>/...
                            ``calibration`` → results/_calibration/<utc-ts>/...
                            ``dryrun``      → results/_dryrun/<utc-ts>/...
                            Default: production.

The script implements the protocol drafted in
``predictions/02_fmv_prereg.md``:

- Each trial creates a fresh API client and a new session UUID
  (``CLAUDE.md`` hard rule).
- Stages run sequentially; each stage in its own session, no context
  reuse across stages.
- Prompts are the **framework-specific** templates under
  ``frameworks/02_fmv/prompts/`` — the F=mv banned-token set differs
  from the v0.1 global ``prompts/``, so the global templates are not
  reused.
- Every Stage 3 prompt is built by parsing the
  ``frameworks/02_fmv/prediction_tests.md`` answer file (single
  source of truth) — no hardcoded scenario constant.
- After the full trial set, R1(b) post-trial-set re-ping for Gemini.

This runner does not modify ``run_v0_1.py`` or any library code; the
v0.1 and 02_fmv experiments are independent.

The R1(a) per-call halt-on-drift is enforced by the base
``run_trial`` (``RuntimeError`` on identity mismatch). If the run
halts, partial trial output up to that point is preserved on disk.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from physlit.judges import scan_for_banned
from physlit.prompts import PromptTemplate
from physlit.runners import ClaudeRunner, GeminiRunner, OpenAIRunner, TestedModelRunner
from physlit.runners.gemini import GEMINI_MODEL_ID
from physlit.scenarios import load_scenarios, render_scenarios_block

if TYPE_CHECKING:
    from physlit.runners.base import TrialRecord

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "02_fmv"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPTS_DIR = FRAMEWORK_DIR / "prompts"
RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"
FINDINGS_PATH = ANALYSIS_DIR / "02_fmv_findings.md"

MODEL_REGISTRY: dict[str, type[TestedModelRunner]] = {
    "claude": ClaudeRunner,
    "openai": OpenAIRunner,
    "gemini": GeminiRunner,
}


@dataclass(frozen=True)
class StageOutput:
    """One stage's output bundle for use as input to the next stage."""

    stage: str
    response_text: str


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


def _extract_observations_list(observations_md: str) -> str:
    """Extract just the numbered observation list, hiding meta sections.

    The Author note and Authoring-constraints sections describe intent
    — that would leak. The model only sees the ``## Observations``
    section.
    """
    pattern = re.compile(
        r"^## Observations\s*\n(.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(observations_md)
    if match is None:
        raise ValueError("observations.md has no '## Observations' section")
    return match.group(1).strip()


# Per-stage max_tokens budgets — must cover both visible output and any
# internal "thinking" tokens reasoning models charge against the same
# budget. Values mirror the v0.1 runner.
STAGE_MAX_TOKENS = {
    "induction": 8192,
    "formulation": 8192,
    "prediction": 12288,  # 5 scenarios → larger output expected
    "meta": 8192,
}


def run_one_trial_set(
    runner: TestedModelRunner,
    trial_index: int,
    output_root: Path,
    *,
    observations_list: str,
    scenarios_block: str,
) -> list[TrialRecord]:
    """Run all four stages for one (runner, trial_index). Returns the four
    TrialRecords. Stages are sequential; each uses a fresh session via
    ``runner.run_trial``.

    Raises ``RuntimeError`` on R1(a) identity-drift halt; partial
    records saved before the halt remain on disk under ``output_root``.
    """
    records: list[TrialRecord] = []

    # Stage 1 — induction
    s1_tmpl = PromptTemplate(PROMPTS_DIR / "stage1_induction.md")
    s1_prompt = s1_tmpl.render(observations=observations_list)
    s1 = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="induction",
        prompt_text=s1_prompt,
        prompt_version=s1_tmpl.version,
        trial_index=trial_index,
        temperature=0.0,
        max_tokens=STAGE_MAX_TOKENS["induction"],
    )
    runner.save_trial(s1, output_root)
    records.append(s1)

    # Stage 2 — formulation
    s2_tmpl = PromptTemplate(PROMPTS_DIR / "stage2_formulation.md")
    s2_prompt = s2_tmpl.render(induced_rules=s1.response_text)
    s2 = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="formulation",
        prompt_text=s2_prompt,
        prompt_version=s2_tmpl.version,
        trial_index=trial_index,
        temperature=0.0,
        max_tokens=STAGE_MAX_TOKENS["formulation"],
    )
    runner.save_trial(s2, output_root)
    records.append(s2)

    # Stage 3 — prediction
    s3_tmpl = PromptTemplate(PROMPTS_DIR / "stage3_prediction.md")
    s3_prompt = s3_tmpl.render(
        operational_rules=s2.response_text,
        scenarios=scenarios_block,
    )
    s3 = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="prediction",
        prompt_text=s3_prompt,
        prompt_version=s3_tmpl.version,
        trial_index=trial_index,
        temperature=0.0,
        max_tokens=STAGE_MAX_TOKENS["prediction"],
    )
    runner.save_trial(s3, output_root)
    records.append(s3)

    # Stage 4 — meta
    s4_tmpl = PromptTemplate(PROMPTS_DIR / "stage4_meta.md")
    s4_prompt = s4_tmpl.render(
        stage1_response=s1.response_text,
        stage2_response=s2.response_text,
        stage3_response=s3.response_text,
    )
    s4 = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="meta",
        prompt_text=s4_prompt,
        prompt_version=s4_tmpl.version,
        trial_index=trial_index,
        temperature=0.0,
        max_tokens=STAGE_MAX_TOKENS["meta"],
    )
    runner.save_trial(s4, output_root)
    records.append(s4)

    return records


def _output_root_for_run(output_mode: str, runner: TestedModelRunner, run_timestamp: str) -> Path:
    """Per-mode output directory.

    Production:  ``results/<model-version>/``
    Calibration: ``results/_calibration/<utc-ts>/<model-id>/``
    Dry run:     ``results/_dryrun/<utc-ts>/<model-id>/``

    The per-model subdir is required for non-production modes because
    ``save_trial`` writes to ``<root>/<framework>/<stage>/trial_<i>_t<temp>.json``
    and multiple models share a trial filename.
    """
    if output_mode == "production":
        return RESULTS_ROOT / runner.model_id
    if output_mode == "dryrun":
        return RESULTS_ROOT / "_dryrun" / run_timestamp / runner.model_id
    return RESULTS_ROOT / "_calibration" / run_timestamp / runner.model_id


def _summarise_banned_signal(records: list[TrialRecord]) -> dict[str, int]:
    """Count banned-concept hits per stage for a quick eyeball signal.

    This is **not** the judge — see ``physlit/judges/banned_check.py``.
    Note ``scan_for_banned`` uses the v0.1 banned list; for 02_fmv it
    is only an approximate smoke-test signal, not the verdict.
    """
    out: dict[str, int] = {}
    for r in records:
        out[r.stage] = len(scan_for_banned(r.response_text))
    return out


def _r1b_post_run_disclosure(
    runner: GeminiRunner, output_root: Path, *, write_findings: bool
) -> dict[str, str]:
    """R1(b) post-trial-set re-ping for Gemini. Returns the captured
    identity dict. When ``write_findings`` is true (production runs), a
    disclosure block is appended to ``analysis/02_fmv_findings.md``
    (created if absent)."""
    captured = runner.r1b_post_run_ping()
    expected = GEMINI_MODEL_ID
    actual = captured.get("response_model_version", "<missing>")
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    drift = "no" if actual == expected else "yes"

    if not write_findings:
        return captured

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    if not FINDINGS_PATH.exists():
        FINDINGS_PATH.write_text(
            "# PhysLit 02_fmv — Findings\n\n"
            "This file accumulates 02_fmv evaluation findings, including\n"
            "R1(b) Gemini post-trial-set re-ping disclosures.\n"
        )

    block = (
        f"\n## R1(b) post-trial-set re-ping (Gemini)\n\n"
        f"- Trial-set output root: `{output_root}`\n"
        f"- Re-ping timestamp (UTC): `{timestamp}`\n"
        f"- Lock-time identifier:    `{expected}`\n"
        f"- Post-run identifier:     `{actual}`\n"
        f"- Identity-field drift:    **{drift}**\n"
    )
    if drift == "yes":
        block += (
            f"- All captured identity fields:\n"
            f"```json\n{json.dumps(captured, indent=2)}\n```\n"
            f"- Methodology: this is a deviation from the intended\n"
            f"  tested-model identity. The operator must classify the\n"
            f"  deviation magnitude and decide whether the 02_fmv\n"
            f"  results stand, are amended with a deviation notice, or\n"
            f"  are re-run.\n"
        )
    with FINDINGS_PATH.open("a") as fh:
        fh.write(block)
    return captured


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--models",
        default="claude,openai,gemini",
        help="Comma-separated subset of {claude,openai,gemini}",
    )
    parser.add_argument("--n-trials", type=int, default=5)
    parser.add_argument(
        "--output-mode",
        choices=("production", "calibration", "dryrun"),
        default="production",
    )
    args = parser.parse_args()

    requested = [m.strip() for m in args.models.split(",") if m.strip()]
    unknown = [m for m in requested if m not in MODEL_REGISTRY]
    if unknown:
        print(f"Unknown model(s): {unknown}", file=sys.stderr)
        return 2

    _load_dotenv()

    observations_list = _extract_observations_list((FRAMEWORK_DIR / "observations.md").read_text())
    scenarios = load_scenarios(FRAMEWORK_DIR / "prediction_tests.md")
    scenarios_block = render_scenarios_block(scenarios)

    run_timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    print("=== PhysLit 02_fmv runner ===")
    print(f"  models:     {requested}")
    print(f"  n-trials:   {args.n_trials}")
    print(f"  output:     {args.output_mode}")
    print(f"  scenarios:  {len(scenarios)} parsed from prediction_tests.md")
    print(f"  timestamp:  {run_timestamp}")
    print()

    total_cost = 0.0
    total_trials = 0
    per_model_summary: dict[str, dict[str, object]] = {}
    gemini_runner: GeminiRunner | None = None

    for model_key in requested:
        runner_cls = MODEL_REGISTRY[model_key]
        runner = runner_cls()
        if isinstance(runner, GeminiRunner):
            gemini_runner = runner
        output_root = _output_root_for_run(args.output_mode, runner, run_timestamp)
        print(f"--- {model_key} ({runner.model_id}) ---")
        print(f"  output_root: {output_root}")

        all_records: list[TrialRecord] = []
        for trial_index in range(args.n_trials):
            print(f"  trial {trial_index}: ", end="", flush=True)
            try:
                records = run_one_trial_set(
                    runner,
                    trial_index,
                    output_root,
                    observations_list=observations_list,
                    scenarios_block=scenarios_block,
                )
            except RuntimeError as exc:
                print(f"\n[HALT] R1(a) drift or version mismatch: {exc}")
                return 3
            all_records.extend(records)
            trial_cost = sum(r.cost_usd_estimate for r in records)
            total_cost += trial_cost
            total_trials += 1
            banned = _summarise_banned_signal(records)
            print(f"~${trial_cost:.4f} | banned hits per stage: {banned}")

        model_cost = sum(r.cost_usd_estimate for r in all_records)
        model_banned_stage1 = sum(
            len(scan_for_banned(r.response_text)) for r in all_records if r.stage == "induction"
        )
        per_model_summary[model_key] = {
            "model_id": runner.model_id,
            "n_trials": args.n_trials,
            "total_cost_usd": round(model_cost, 4),
            "stage1_banned_concept_hits_total": model_banned_stage1,
            "output_root": str(output_root),
        }

    # R1(b) post-trial-set re-ping for Gemini, if it ran.
    if gemini_runner is not None:
        print()
        print("--- R1(b) post-trial-set Gemini re-ping ---")
        try:
            output_root_for_disclosure = _output_root_for_run(
                args.output_mode, gemini_runner, run_timestamp
            )
            captured = _r1b_post_run_disclosure(
                gemini_runner,
                output_root_for_disclosure,
                write_findings=(args.output_mode == "production"),
            )
            print(f"  captured identity: {captured}")
            if args.output_mode == "production":
                print(f"  disclosure appended to: {FINDINGS_PATH}")
            else:
                print("  (non-production run — disclosure printed, not written to findings)")
        except Exception as exc:
            print(f"  R1(b) re-ping failed: {type(exc).__name__}: {exc}")
            print("  (Failure does not invalidate trial output; record manually.)")

    print()
    print("=== Summary ===")
    print(f"  total trial-sets: {total_trials}")
    print(f"  total cost (estimated, USD): ${total_cost:.4f}")
    for model_key, summary in per_model_summary.items():
        print(f"  {model_key}: {summary}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
