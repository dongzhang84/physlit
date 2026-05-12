"""CLI: run the structural-audit (Agent 2) prototype over v0.1 trial JSONs.

Walks ``results/<model-id>/<framework_id>/<stage>/trial_*.json`` and emits
one structural-audit report per trial in ``analysis/structural_audit/<stage>/``.

Default behaviour: regex layer only (zero API cost). Pass ``--use-llm`` to
enable the N11 LLM smuggling-detection layer (≈ $0.001 per trial via
Anthropic Haiku; ANTHROPIC_API_KEY required).

Usage::

    # Free dry-run on Stage-1 (induction) trials, all models:
    uv run python scripts/run_structural_audit.py

    # Stage-2 (formulation) with LLM layer:
    uv run python scripts/run_structural_audit.py --stage formulation --use-llm

    # Single model, single stage:
    uv run python scripts/run_structural_audit.py \\
        --model claude-opus-4-7 --stage induction
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from physlit.audit import audit_trial_response  # noqa: E402
from physlit.audit.llm_smuggle import SmuggleDetectorLLM  # noqa: E402
from physlit.audit.models import StructuralAuditReport  # noqa: E402

DEFAULT_RESULTS_ROOT = REPO_ROOT / "results"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "analysis" / "structural_audit"
DEFAULT_FRAMEWORK = "01_aristotelian"
DEFAULT_OBSERVATIONS_PATH = REPO_ROOT / "frameworks" / DEFAULT_FRAMEWORK / "observations.md"

ALL_MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
STAGES_WITH_RULES = ("induction", "formulation")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "--model",
        action="append",
        default=None,
        help=f"Model ID to audit. Repeatable. Default: all of {ALL_MODELS}.",
    )
    p.add_argument(
        "--stage",
        choices=STAGES_WITH_RULES,
        default="induction",
        help="Trial stage to audit (only induction and formulation produce rule sets).",
    )
    p.add_argument(
        "--framework",
        default=DEFAULT_FRAMEWORK,
        help="Framework directory under results/<model>/.",
    )
    p.add_argument(
        "--results-root",
        type=Path,
        default=DEFAULT_RESULTS_ROOT,
        help="Root of the results tree.",
    )
    p.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Where to write structural-audit reports.",
    )
    p.add_argument(
        "--use-llm",
        action="store_true",
        help="Enable N11 LLM smuggling-detection layer (~$0.001 per trial).",
    )
    p.add_argument(
        "--observations",
        type=Path,
        default=DEFAULT_OBSERVATIONS_PATH,
        help="Path to the framework's observations.md (used by the LLM layer).",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    models = tuple(args.model) if args.model else ALL_MODELS

    observations_text = ""
    llm_detector: SmuggleDetectorLLM | None = None
    if args.use_llm:
        if not args.observations.is_file():
            print(f"ERROR: observations file not found: {args.observations}", file=sys.stderr)
            return 2
        observations_text = args.observations.read_text()
        llm_detector = SmuggleDetectorLLM()
        print(f"LLM layer ENABLED (model={llm_detector.model})", file=sys.stderr)
    else:
        print("LLM layer disabled (regex-only run, $0 cost).", file=sys.stderr)

    out_dir = args.output_root / args.stage
    out_dir.mkdir(parents=True, exist_ok=True)

    summary: list[dict[str, object]] = []
    for model_id in models:
        stage_dir = args.results_root / model_id / args.framework / args.stage
        if not stage_dir.is_dir():
            print(f"  skip: {stage_dir} (not found)", file=sys.stderr)
            continue
        trial_files = sorted(stage_dir.glob("trial_*_t*.json"))
        for trial_path in trial_files:
            trial_json = json.loads(trial_path.read_text())
            trial_json["trial_path"] = str(trial_path)
            llm_flags = None
            if llm_detector is not None:
                llm_flags = llm_detector.detect_as_flags(
                    trial_json["response_text"], observations_text
                )
            report = audit_trial_response(trial_json, llm_smuggle_flags=llm_flags)
            out_subdir = out_dir / model_id
            out_file = StructuralAuditReport.save(report, out_subdir)
            summary.append(
                {
                    "model": model_id,
                    "trial": report.trial_index,
                    "stage": report.stage,
                    "rule_count": report.rule_count,
                    "tier1": report.tier1_count,
                    "tier2": report.tier2_count,
                    "tier3": report.tier3_count,
                    "report": str(out_file.relative_to(REPO_ROOT)),
                }
            )

    _print_summary(summary, args.stage)
    summary_path = out_dir / "_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True))
    print(f"\nSummary written to {summary_path.relative_to(REPO_ROOT)}", file=sys.stderr)
    return 0


def _print_summary(summary: list[dict[str, object]], stage: str) -> None:
    print(f"\n=== Structural audit summary (stage={stage}) ===\n")
    if not summary:
        print("(no trials audited)")
        return
    by_model: dict[str, list[dict[str, object]]] = {}
    for row in summary:
        by_model.setdefault(str(row["model"]), []).append(row)
    for model_id, rows in by_model.items():
        print(f"\n## {model_id}")
        print(f"{'trial':>5}  {'rules':>5}  {'T1':>3}  {'T2':>3}  {'T3':>3}")
        for row in sorted(rows, key=lambda r: int(str(r["trial"]))):
            print(
                f"{row['trial']:>5}  {row['rule_count']:>5}  "
                f"{row['tier1']:>3}  {row['tier2']:>3}  {row['tier3']:>3}"
            )


if __name__ == "__main__":
    raise SystemExit(main())
