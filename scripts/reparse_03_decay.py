"""Re-parse 03_decay judge verdicts that previously failed JSON parsing.

The 03_decay production judging run surfaced a Claude-judge failure
mode in which the model "thinks out loud" — emitting a JSON draft,
then self-correcting prose, then a revised draft, repeatedly — and
the original ``parse_verdict_json`` regex collapsed under the
multi-object output. The parser has been updated to return the
**last** valid JSON dict; this script re-parses every previously
parse-errored verdict on disk using the new parser, re-runs
``evidence_check`` against the trial response, and writes the
updated verdict back. No new API calls are made.

After re-parsing, the script re-aggregates the full P1-P4 verdicts
by invoking ``aggregate`` from ``judge_03_decay``. The original
judging report stays in ``analysis/decay/03_decay_findings.md`` (a
historical record of the parse-error state); the new report is
appended below it.

Usage:
    uv run python scripts/reparse_03_decay.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from physlit.judges import check_evidence
from physlit.judges.judge_base import parse_verdict_json

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "03_decay"
RESULTS_ROOT = REPO_ROOT / "results"

MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")


def _run_evidence_check_on_parsed(parsed: dict, response_text: str) -> list[dict]:
    """Mirror the evidence-check logic from judge_03_decay.py."""
    results: list[dict] = []
    if "scenarios" in parsed:
        for sc in parsed.get("scenarios") or []:
            if not isinstance(sc, dict):
                continue
            r = check_evidence(verdict=sc, response_text=response_text)
            results.append(
                {
                    "scope": f"scenario_{sc.get('index')}",
                    "found": r.found,
                    "fabricated": r.fabricated,
                    "evidence_required": r.evidence_required,
                    "cited_evidence": r.cited_evidence,
                    "reason": r.reason,
                }
            )
    else:
        r = check_evidence(verdict=parsed, response_text=response_text)
        results.append(
            {
                "scope": "verdict",
                "found": r.found,
                "fabricated": r.fabricated,
                "evidence_required": r.evidence_required,
                "cited_evidence": r.cited_evidence,
                "reason": r.reason,
            }
        )
    return results


def _trial_response_text(model: str, stage: str, trial_index: int) -> str:
    """Locate the corresponding tested-model trial JSON and return its
    response_text."""
    trial_path = RESULTS_ROOT / model / FRAMEWORK_ID / stage / f"trial_{trial_index}_t0.0.json"
    if not trial_path.exists():
        raise FileNotFoundError(f"missing tested-model trial: {trial_path}")
    return json.loads(trial_path.read_text())["response_text"]


def reparse_one(verdict_path: Path) -> dict | None:
    """Re-parse one saved verdict file. Returns the updated verdict dict
    if it changed, else None.
    """
    d = json.loads(verdict_path.read_text())
    if not d.get("parse_error"):
        return None  # already parsed cleanly

    parsed, err = parse_verdict_json(d["raw_response"])
    if parsed is None:
        print(f"  STILL BROKEN: {verdict_path.name}: {err}")
        return None

    # Locate the tested-model response so we can run evidence_check.
    # trial_path looks like
    # ".../results/<model>/03_decay/<stage>/trial_<i>_t0.0.json"
    trial_path_str = d["trial_path"]
    trial_path = Path(trial_path_str)
    stage = trial_path.parent.name
    trial_index = int(trial_path.stem.split("_")[1])
    model = trial_path.parents[2].name
    response_text = _trial_response_text(model, stage, trial_index)

    # Run evidence_check (mutates parsed in place by adding _evidence_check)
    ev_results = _run_evidence_check_on_parsed(parsed, response_text)
    parsed["_evidence_check"] = ev_results

    # Rebuild the verdict record. Preserve identity fields; clear
    # parse_error; replace parsed_verdict.
    d["parsed_verdict"] = parsed
    d["parse_error"] = None
    verdict_path.write_text(json.dumps(d, indent=2, sort_keys=True))
    return d


def main() -> int:
    n_fixed = 0
    n_still_broken = 0
    n_already_ok = 0
    fab_added = 0

    for model in MODELS:
        jdir = RESULTS_ROOT / model / FRAMEWORK_ID / "judgments"
        if not jdir.exists():
            continue
        for fp in sorted(jdir.glob("*.json")):
            d = json.loads(fp.read_text())
            if not d.get("parse_error"):
                n_already_ok += 1
                continue
            updated = reparse_one(fp)
            if updated is None:
                n_still_broken += 1
                continue
            n_fixed += 1
            new_fab = sum(
                1
                for ev in updated["parsed_verdict"].get("_evidence_check", [])
                if ev.get("fabricated")
            )
            fab_added += new_fab
            verdict_label = updated["parsed_verdict"].get("verdict") or updated[
                "parsed_verdict"
            ].get("overall_verdict")
            print(
                f"  fixed: {fp.relative_to(REPO_ROOT)}  ->  {verdict_label}"
                + (f" [FAB={new_fab}]" if new_fab else "")
            )

    print()
    print("=== Reparse summary ===")
    print(f"  fixed:        {n_fixed}")
    print(f"  still broken: {n_still_broken}")
    print(f"  already OK:   {n_already_ok}")
    print(f"  new fabrication flags surfaced by reparse: {fab_added}")
    print()
    print("Now re-run aggregation:")
    print(
        "  uv run python -c 'from scripts.judge_03_decay import aggregate; "
        'aggregate(["claude-opus-4-7","gpt-5.5-2026-04-23",'
        '"gemini-3.1-pro-preview"], 5, 0.0, 0)\''
    )
    print("...or simpler: run the aggregation block below directly.")

    # Re-run aggregation inline to keep this a single command.
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    # judge_03_decay isn't a package; import as module
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "judge_03_decay", REPO_ROOT / "scripts" / "judge_03_decay.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    print()
    print("=== Re-aggregating with reparsed verdicts ===")
    # Fab count and judge cost are informational; pass 0 since this
    # script doesn't re-do the judging.
    mod.aggregate(list(MODELS), 5, 0.0, 0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
