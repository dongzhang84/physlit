"""Render every production trial JSON into a companion .md file.

For each ``results/<model-id>/01_aristotelian/<stage>/trial_<N>_t<T>.json``,
emit a sibling ``trial_<N>_t<T>.md`` containing the verbatim prompt,
the verbatim response, the trial metadata, and (when present) both
judges' verdicts pulled from ``results/<model-id>/judgments/``.

Why: trial JSONs are the source of truth (referenced by the
prereg-locked tag) but JSON is awful to skim. The .md siblings make
it possible to scroll through a trial in any markdown viewer without
copying out of jq.

The .md files are derivative — never edit them by hand. Re-run the
script to regenerate from the JSON. The JSON files are untouched.

Usage: ``uv run python scripts/render_trials_to_md.py``
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
FRAMEWORK_ID = "01_aristotelian"

STAGE_TITLES = {
    "induction": "Stage 1 — Induction",
    "formulation": "Stage 2 — Formulation",
    "prediction": "Stage 3 — Prediction",
    "meta": "Stage 4 — Meta",
}


def _max_backtick_run(s: str) -> int:
    longest = 0
    current = 0
    for ch in s:
        if ch == "`":
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0
    return longest


def _fence(s: str) -> str:
    """Return a backtick fence one longer than any backtick run in ``s``,
    minimum 3. This makes the resulting code block safe to nest content
    that itself contains triple-backticks (which the prompts do)."""
    return "`" * max(3, _max_backtick_run(s) + 1)


def _code_block(s: str) -> str:
    fence = _fence(s)
    return f"{fence}\n{s}\n{fence}"


def _load_judge_verdicts(model_dir: Path) -> dict[Path, dict[str, dict[str, Any]]]:
    """Return ``{trial_path: {judge_family: parsed_verdict}}`` for one model.

    Each trial may have 0, 1, or 2 judge verdicts on disk.
    """
    out: dict[Path, dict[str, dict[str, Any]]] = defaultdict(dict)
    judgments_dir = model_dir / "judgments"
    if not judgments_dir.exists():
        return out
    for vp in judgments_dir.glob("*.json"):
        d = json.loads(vp.read_text())
        trial_path = Path(d["trial_path"])
        judge_family = d.get("judge_family") or "unknown"
        out[trial_path][judge_family] = d
    return out


def _render_metadata_table(trial: dict[str, Any]) -> str:
    rows: list[tuple[str, str]] = [
        ("Framework", f"`{trial.get('framework_id', '?')}`"),
        ("Stage", f"`{trial.get('stage', '?')}`"),
        ("Trial index", str(trial.get("trial_index", "?"))),
        ("Model", f"`{trial.get('model_full_version', '?')}`"),
        ("Prompt version", f"`{trial.get('prompt_version', '?')}`"),
        ("Temperature (requested)", f"`{trial.get('temperature', '?')}`"),
        ("Session ID", f"`{trial.get('api_session_id', '?')}`"),
        ("Timestamp (UTC)", f"`{trial.get('response_timestamp_utc', '?')}`"),
        ("Input tokens", str(trial.get("input_tokens", "?"))),
        ("Output tokens", str(trial.get("output_tokens", "?"))),
        ("Estimated cost (USD)", f"${float(trial.get('cost_usd_estimate', 0.0)):.4f}"),
    ]
    identity = trial.get("vendor_identity_fields") or {}
    if identity:
        rows.append(
            (
                "Vendor identity fields",
                "`" + json.dumps(identity, sort_keys=True) + "`",
            )
        )
    out = ["| Field | Value |", "|---|---|"]
    for k, v in rows:
        out.append(f"| {k} | {v} |")
    return "\n".join(out)


def _render_judge_block(judge_family: str, verdict_record: dict[str, Any]) -> str:
    parsed = verdict_record.get("parsed_verdict") or {}
    judge_model = verdict_record.get("judge_model", "?")
    parse_error = verdict_record.get("parse_error")
    judge_label = {
        "anthropic": "Claude-as-judge",
        "openai": "OpenAI-as-judge",
    }.get(judge_family, f"{judge_family}-as-judge")

    lines: list[str] = [f"### {judge_label} (`{judge_model}`)", ""]

    if parse_error:
        lines.append(f"- parse_error: `{parse_error}`")

    if not parsed and not parse_error:
        lines.append("- (no parsed verdict on disk)")
        return "\n".join(lines)

    if "scenarios" in parsed:
        lines.append(f"- overall_verdict: `{parsed.get('overall_verdict', '?')}`")
        lines.append("")
        for sc in parsed.get("scenarios") or []:
            lines.append(
                f"- **Scenario {sc.get('index', '?')}** — verdict: `{sc.get('verdict', '?')}`"
            )
            failed = sc.get("failed_criterion")
            if failed:
                lines.append(f"  - failed_criterion: {failed}")
            ev = sc.get("evidence")
            if ev:
                lines.append(f"  - evidence: {ev}")
            rs = sc.get("reasoning")
            if rs:
                lines.append(f"  - reasoning: {rs}")
    elif "over_claim" in parsed:
        lines.append(f"- over_claim: `{parsed.get('over_claim', '?')}`")
        ev = parsed.get("evidence")
        if ev:
            lines.append(f"- evidence: {ev}")
        rs = parsed.get("reasoning")
        if rs:
            lines.append(f"- reasoning: {rs}")
    else:
        lines.append(f"- verdict: `{parsed.get('verdict', '?')}`")
        for key in ("first_fail_step", "first_fail_clause", "failed_criterion"):
            if key in parsed and parsed[key] is not None:
                lines.append(f"- {key}: `{parsed[key]}`")
        ev = parsed.get("evidence")
        if ev:
            lines.append(f"- evidence: {ev}")
        rs = parsed.get("reasoning")
        if rs:
            lines.append(f"- reasoning: {rs}")

    cost = verdict_record.get("cost_usd_estimate")
    if cost is not None:
        lines.append(f"- judge call cost (USD): `${float(cost):.4f}`")
    return "\n".join(lines)


def render_one(
    trial_path: Path,
    judge_verdicts: dict[Path, dict[str, dict[str, Any]]],
) -> Path:
    trial: dict[str, Any] = json.loads(trial_path.read_text())
    model = str(trial.get("model_full_version", "?"))
    stage = str(trial.get("stage", "?"))
    stage_title = STAGE_TITLES.get(stage, f"Stage `{stage}`")
    trial_index = trial.get("trial_index", "?")

    title = f"# `{model}` — Trial {trial_index} — {stage_title}"

    response_text = str(trial.get("response_text", "")).rstrip()
    parts: list[str] = [
        title,
        "",
        f"_Companion view of [`{trial_path.name}`](./{trial_path.name})._",
        "_Auto-generated by `scripts/render_trials_to_md.py` — do not edit by hand;_",
        "_re-run the script to regenerate. The JSON file is the source of truth._",
        "",
        "## Metadata",
        "",
        _render_metadata_table(trial),
        "",
        "## Prompt",
        "",
        "_Verbatim, in a code block (the prompt was sent to the API exactly as-is)._",
        "",
        _code_block(str(trial.get("prompt_text", ""))),
        "",
        "## Response",
        "",
        "_Rendered as markdown for readability — model output is already markdown-formatted, so headings, bullets, and code blocks below are how the model meant them to appear. The byte-exact text is in the JSON._",
        "",
        "---",
        "",
        response_text,
        "",
        "---",
        "",
    ]

    judges_for_trial = judge_verdicts.get(trial_path, {})
    if judges_for_trial:
        parts.append("## Judge verdicts")
        parts.append("")
        # Display in a stable order: anthropic first, then openai, then any
        # other (future) judge families.
        for judge_family in (
            "anthropic",
            "openai",
            *sorted(set(judges_for_trial) - {"anthropic", "openai"}),
        ):
            if judge_family in judges_for_trial:
                parts.append(_render_judge_block(judge_family, judges_for_trial[judge_family]))
                parts.append("")

    out_path = trial_path.with_suffix(".md")
    out_path.write_text("\n".join(parts).rstrip() + "\n")
    return out_path


def main() -> int:
    if not RESULTS.exists():
        print(f"results/ not found at {RESULTS}", file=sys.stderr)
        return 1

    rendered: list[Path] = []
    for model_dir in sorted(RESULTS.iterdir()):
        if not model_dir.is_dir() or model_dir.name.startswith("_"):
            continue  # skip _calibration/_dryrun pseudo-models for the production renderer
        framework_dir = model_dir / FRAMEWORK_ID
        if not framework_dir.is_dir():
            continue
        judge_verdicts = _load_judge_verdicts(model_dir)
        for trial_path in sorted(framework_dir.rglob("trial_*.json")):
            md_path = render_one(trial_path, judge_verdicts)
            rendered.append(md_path)

    print(f"Rendered {len(rendered)} markdown files.")
    by_dir: dict[Path, int] = defaultdict(int)
    for p in rendered:
        by_dir[p.parent] += 1
    for d, n in sorted(by_dir.items()):
        print(f"  {d.relative_to(REPO)}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
