"""Render every v0.3 treatment-arm trial JSON into a companion .md.

Parallel to scripts/render_02_fmv_2_to_md.py: targets the ``v0_3``
framework subtree under ``results/<model>/v0_3/`` and skips all
non-stage subdirs.

Usage: ``uv run python scripts/render_v0_3_to_md.py``
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
FRAMEWORK_ID = "v0_3"
STAGE_DIRS = {"induction", "formulation", "prediction", "meta"}

STAGE_TITLES = {
    "induction": "Stage 1 — Induction",
    "formulation": "Stage 2 — Formulation",
    "prediction": "Stage 3 — Prediction",
    "meta": "Stage 4 — Meta",
}


def _max_backtick_run(s: str) -> int:
    longest = current = 0
    for ch in s:
        if ch == "`":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _code_block(s: str) -> str:
    fence = "`" * max(3, _max_backtick_run(s) + 1)
    return f"{fence}\n{s}\n{fence}"


def _load_judge_verdicts(model_dir: Path) -> dict[Path, dict[str, dict[str, Any]]]:
    out: dict[Path, dict[str, dict[str, Any]]] = defaultdict(dict)
    judgments_dir = model_dir / FRAMEWORK_ID / "judgments"
    if not judgments_dir.exists():
        return out
    for vp in judgments_dir.glob("*.json"):
        d = json.loads(vp.read_text())
        out[Path(d["trial_path"])][d.get("judge_family") or "unknown"] = d
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
        rows.append(("Vendor identity fields", "`" + json.dumps(identity, sort_keys=True) + "`"))
    out = ["| Field | Value |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in rows]
    return "\n".join(out)


def _render_judge_block(judge_family: str, verdict_record: dict[str, Any]) -> str:
    parsed = verdict_record.get("parsed_verdict") or {}
    judge_model = verdict_record.get("judge_model", "?")
    parse_error = verdict_record.get("parse_error")
    label = {"anthropic": "Claude-as-judge", "openai": "OpenAI-as-judge"}.get(
        judge_family, f"{judge_family}-as-judge"
    )
    lines: list[str] = [f"### {label} (`{judge_model}`)", ""]
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
                f"- **Scenario {sc.get('index', '?')}** — verdict: "
                f"`{sc.get('verdict', '?')}` (direction: `{sc.get('direction', '?')}`)"
            )
            for key in ("failed_criterion", "evidence", "reasoning"):
                if sc.get(key):
                    lines.append(f"  - {key}: {sc[key]}")
    elif "over_claim" in parsed:
        lines.append(f"- over_claim: `{parsed.get('over_claim', '?')}`")
        for key in ("evidence", "reasoning"):
            if parsed.get(key):
                lines.append(f"- {key}: {parsed[key]}")
    else:
        lines.append(f"- verdict: `{parsed.get('verdict', '?')}`")
        for key in ("first_fail_step", "first_fail_clause", "failed_criterion"):
            if parsed.get(key) is not None:
                lines.append(f"- {key}: `{parsed[key]}`")
        for key in ("evidence", "reasoning"):
            if parsed.get(key):
                lines.append(f"- {key}: {parsed[key]}")

    cost = verdict_record.get("cost_usd_estimate")
    if cost is not None:
        lines.append(f"- judge call cost (USD): `${float(cost):.4f}`")
    return "\n".join(lines)


def render_one(trial_path: Path, judge_verdicts: dict[Path, dict[str, dict[str, Any]]]) -> Path:
    trial: dict[str, Any] = json.loads(trial_path.read_text())
    model = str(trial.get("model_full_version", "?"))
    stage = str(trial.get("stage", "?"))
    stage_title = STAGE_TITLES.get(stage, f"Stage `{stage}`")

    parts: list[str] = [
        f"# `{model}` — Trial {trial.get('trial_index', '?')} — {stage_title}",
        "",
        f"_Companion view of [`{trial_path.name}`](./{trial_path.name})._",
        "_Auto-generated by `scripts/render_v0_3_to_md.py` — do not edit by hand;_",
        "_re-run the script to regenerate. The JSON file is the source of truth._",
        "",
        "## Metadata",
        "",
        _render_metadata_table(trial),
        "",
        "## Prompt",
        "",
        "_Verbatim, in a code block (sent to the API exactly as-is)._",
        "",
        _code_block(str(trial.get("prompt_text", ""))),
        "",
        "## Response",
        "",
        "_Rendered as markdown for readability; the byte-exact text is in the JSON._",
        "",
        "---",
        "",
        str(trial.get("response_text", "")).rstrip(),
        "",
        "---",
        "",
    ]

    judges_for_trial = judge_verdicts.get(trial_path, {})
    if judges_for_trial:
        parts += ["## Judge verdicts", ""]
        for jf in ("anthropic", "openai", *sorted(set(judges_for_trial) - {"anthropic", "openai"})):
            if jf in judges_for_trial:
                parts += [_render_judge_block(jf, judges_for_trial[jf]), ""]

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
            continue
        framework_dir = model_dir / FRAMEWORK_ID
        if not framework_dir.is_dir():
            continue
        judge_verdicts = _load_judge_verdicts(model_dir)
        for stage_dir in sorted(framework_dir.iterdir()):
            if not stage_dir.is_dir() or stage_dir.name not in STAGE_DIRS:
                continue
            for trial_path in sorted(stage_dir.glob("trial_*.json")):
                rendered.append(render_one(trial_path, judge_verdicts))
    print(f"Rendered {len(rendered)} markdown files.")
    by_dir: dict[Path, int] = defaultdict(int)
    for p in rendered:
        by_dir[p.parent] += 1
    for d, n in sorted(by_dir.items()):
        print(f"  {d.relative_to(REPO)}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
