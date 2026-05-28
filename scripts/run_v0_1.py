"""v0.1 production runner — Aristotelian x {Claude, GPT-5.5, Gemini 3.1 Pro}.

Usage:
    uv run python scripts/run_v0_1.py [options]

Options:
    --models <csv>          Subset of models to run (default: all three).
                            Allowed values: claude, openai, gemini.
    --n-trials <int>        Number of trials per (model, stage). Default: 5.
    --output-mode {production,calibration}
                            ``production``  → results/<model-version>/...
                            ``calibration`` → results/_calibration/<utc-ts>/...
                            Default: production.

The script implements the protocol locked in
``predictions/v0_1_prereg.md``:

- Each trial creates a fresh API client and a new session UUID
  (``CLAUDE.md`` hard rule).
- Stages run sequentially; each stage in its own session, no
  context reuse across stages.
- Default sampling for all three vendors.
- Every Stage 3 prompt is built by parsing the locked
  ``frameworks/01_aristotelian/prediction_tests.md`` (single source
  of truth) — there is no hardcoded scenario constant.
- After the full trial set, R1(b) post-trial-set re-ping for Gemini
  with a disclosure entry written to
  ``analysis/aristotelian/v0_1_findings.md`` (auto-created if absent).

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
FRAMEWORK_ID = "01_aristotelian"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPTS_DIR = REPO_ROOT / "prompts"
RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"

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

    The Author note in observations.md describes which observations are
    boundary tests — that would leak intent. The model only sees the
    ``## Observations`` section.
    """
    pattern = re.compile(
        r"^## Observations\s*\n(.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(observations_md)
    if match is None:
        raise ValueError("observations.md has no '## Observations' section")
    return match.group(1).strip()


# Per-stage max_tokens budgets. These need to comfortably cover both
# the visible response and any internal "thinking" tokens that
# reasoning models (Gemini 3 Pro, OpenAI GPT-5.x) produce — the
# google-genai SDK in particular charges thinking tokens against the
# same max_output_tokens budget as visible output (confirmed via
# scripts/discover_model_versions.py findings on 2026-05-09: Gemini
# 3.1 Pro Preview consumed ~1965 thinking tokens for the Aristotelian
# induction prompt, leaving only 79 visible tokens out of 2048 → the
# visible response was truncated mid-sentence with finish_reason =
# MAX_TOKENS).
#
# We pick budgets that are roughly 4-6x the prior (2048-2560) so
# reasoning has room. Non-reasoning models stop early and pay only
# for their actual output; cost impact is negligible for them.
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
    TrialRecords. Stages are sequential; each stage uses a fresh session
    via ``runner.run_trial``.

    Raises ``RuntimeError`` on R1(a) identity-drift halt; partial records
    saved before the halt remain on disk under ``output_root``.
    """
    records: list[TrialRecord] = []

    # Stage 1
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

    # Stage 2
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

    # Stage 3
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

    # Stage 4
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

    Production: ``results/<model-version>/`` (then framework/stage are
    appended by save_trial).
    Calibration: ``results/_calibration/<utc-ts>/<model-id>/`` (the
    model-id subdir is required because save_trial writes to
    ``<output_root>/<framework>/<stage>/trial_<i>_t<temp>.json`` and
    multiple models share the same trial filename — without the
    per-model subdir later models overwrite earlier ones).
    """
    if output_mode == "production":
        return RESULTS_ROOT / runner.model_id
    return RESULTS_ROOT / "_calibration" / run_timestamp / runner.model_id


def _summarise_banned_signal(records: list[TrialRecord]) -> dict[str, int]:
    """Count banned-concept hits per stage for a quick PASS/FAIL signal.

    Returns ``{stage: hit_count}``. This is **not** the v0.1 judge — see
    ``physlit/judges/banned_check.py`` docstring.
    """
    out: dict[str, int] = {}
    for r in records:
        out[r.stage] = len(scan_for_banned(r.response_text))
    return out


def _r1b_post_run_disclosure(runner: GeminiRunner, output_root: Path) -> dict[str, str]:
    """R1(b) post-trial-set re-ping for Gemini. Writes a disclosure
    block into ``analysis/aristotelian/v0_1_findings.md`` (creating the file if
    needed) and returns the captured identity dict for inclusion in the
    run summary."""
    captured = runner.r1b_post_run_ping()
    expected = GEMINI_MODEL_ID
    actual = captured.get("response_model_version", "<missing>")
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    drift = "no" if actual == expected else "yes"

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    findings_path = ANALYSIS_DIR / "aristotelian" / "v0_1_findings.md"
    if not findings_path.exists():
        findings_path.write_text(
            "# PhysLit v0.1 — Findings\n\n"
            "This file accumulates v0.1 evaluation findings, including\n"
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
            f"- Methodology: this constitutes a deviation from the\n"
            f"  prereg-locked tested-model identity. The v0.1 results\n"
            f"  written under `{output_root}` were generated against a\n"
            f"  Gemini model that may have changed underlying weights\n"
            f"  during or before the trial set. Operator must classify\n"
            f"  the deviation magnitude (none / minor / major) and\n"
            f"  decide whether v0.1 results stand as-is, are amended\n"
            f"  with a deviation notice, or are re-run under a v0.1.1\n"
            f"  prereg.\n"
        )
    with findings_path.open("a") as fh:
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
        choices=("production", "calibration"),
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
    print("=== PhysLit v0.1 runner ===")
    print(f"  models:     {requested}")
    print(f"  n-trials:   {args.n_trials}")
    print(f"  output:     {args.output_mode}")
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

        # Per-model totals
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
            captured = _r1b_post_run_disclosure(gemini_runner, output_root_for_disclosure)
            print(f"  captured identity: {captured}")
            print(f"  disclosure appended to: {ANALYSIS_DIR / 'v0_1_findings.md'}")
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
