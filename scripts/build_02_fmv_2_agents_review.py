"""Build ``analysis/02_fmv_2_agents_review.md`` — case-by-case review
of how Agent 1 (content) and Agent 2 (structural) resolved each
treatment-arm dual-judge disagreement.

Mirrors ``analysis/02_fmv_1_agent2_review.md`` (structural only) but
covers both axes. Companion to the audit worksheet
``analysis/02_fmv_2_audit_worksheet.md``: same case labels (``C1``…
``C10`` for content, ``S1``…``S6`` for structural). The agents are
``gemini-3.1-pro-preview``, non-canonical resolvers; their verdicts do
NOT feed P1 / P2 — the human audit (the worksheet) is canonical. This
review documents what each agent did so the eventual agent-vs-human
agreement can be tabulated.

Usage: ``uv run python scripts/build_02_fmv_2_agents_review.py``
"""

from __future__ import annotations

import glob
import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
TREATMENT_ID = "02_fmv_2"
OUTPUT = REPO / "analysis" / "02_fmv_2_agents_review.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
STAGE_TITLE = {
    "induction": "Stage 1 (induction)",
    "formulation": "Stage 2 (formulation)",
    "prediction": "Stage 3 (prediction)",
}


def _load_judgments(model: str, subdir: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / TREATMENT_ID / subdir / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if name.startswith("trial_"):
            out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
                d.get("parsed_verdict") or {}
            )
    return out


def _load_agent_content(model: str) -> dict[tuple[int, str], dict[str, Any]]:
    """{(trial, stage): full Agent 1 record}."""
    out: dict[tuple[int, str], dict[str, Any]] = {}
    for fp in sorted(
        glob.glob(str(RESULTS / model / TREATMENT_ID / "content_resolved" / "*.json"))
    ):
        d = json.loads(Path(fp).read_text())
        d["_file"] = Path(fp).name
        out[(d["trial_index"], d["stage"])] = d
    return out


def _load_agent_structural(model: str) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for fp in sorted(
        glob.glob(str(RESULTS / model / TREATMENT_ID / "structural_resolved" / "*.json"))
    ):
        d = json.loads(Path(fp).read_text())
        d["_file"] = Path(fp).name
        out[d["trial_index"]] = d
    return out


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _content_judge_line(label: str, parsed: dict[str, Any]) -> list[str]:
    clause = parsed.get("first_fail_clause") or parsed.get("failed_criterion") or "(n/a)"
    return [
        f"**{label} — `{_verdict(parsed)}`** (failed clause: {clause})",
        "",
        f"> {(parsed.get('reasoning') or '').strip()}",
        "",
    ]


def _structural_judge_line(label: str, parsed: dict[str, Any]) -> list[str]:
    fc = ", ".join(parsed.get("failed_criteria") or []) or "(none)"
    return [
        f"**{label} — `{_verdict(parsed)}`** (Stage 1 rule count "
        f"`{parsed.get('stage1_rule_count', '?')}`, failed: {fc})",
        "",
        f"> {(parsed.get('reasoning') or '').strip()}",
        "",
    ]


def main() -> None:
    # Collect disagreements + Agent records.
    content_cases: list[tuple[str, int, str]] = []
    structural_cases: list[tuple[str, int]] = []
    cj_all: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}
    sj_all: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}
    a1_all: dict[str, dict[tuple[int, str], dict[str, Any]]] = {}
    a2_all: dict[str, dict[int, dict[str, Any]]] = {}
    for model in MODELS:
        cj_all[model] = _load_judgments(model, "judgments")
        sj_all[model] = _load_judgments(model, "structural")
        a1_all[model] = _load_agent_content(model)
        a2_all[model] = _load_agent_structural(model)
        for t in range(5):
            for stage in CONTENT_STAGES:
                va = _verdict(cj_all[model].get((t, stage, "anthropic")) or {})
                vb = _verdict(cj_all[model].get((t, stage, "openai")) or {})
                if va and vb and va != vb:
                    content_cases.append((model, t, stage))
            sa = _verdict(sj_all[model].get((t, "structural", "anthropic")) or {})
            sb = _verdict(sj_all[model].get((t, "structural", "openai")) or {})
            if sa and sb and sa != sb:
                structural_cases.append((model, t))

    # Tallies.
    a1_v = []
    a1_sided = {"judge_a": 0, "judge_b": 0, "neither": 0}
    for model, t, stage in content_cases:
        rec = a1_all[model].get((t, stage), {})
        pv = rec.get("parsed_verdict") or {}
        a1_v.append(_verdict(pv))
        sw = pv.get("agreed_with")
        if sw in a1_sided:
            a1_sided[sw] += 1
    a1_pass = sum(1 for v in a1_v if v == "PASS")
    a1_fail = sum(1 for v in a1_v if v == "FAIL")

    a2_v = []
    a2_sided = {"judge_a": 0, "judge_b": 0, "neither": 0}
    for model, t in structural_cases:
        rec = a2_all[model].get(t, {})
        pv = rec.get("parsed_verdict") or {}
        a2_v.append(_verdict(pv))
        sw = pv.get("agreed_with")
        if sw in a2_sided:
            a2_sided[sw] += 1
    a2_pass = sum(1 for v in a2_v if v == "PASS")
    a2_fail = sum(1 for v in a2_v if v == "FAIL")

    lines: list[str] = []
    lines.append("# 02_fmv.2 Agents review — Agent 1 (content) + Agent 2 (structural)")
    lines.append("")
    lines.append(
        "> Generated by `scripts/build_02_fmv_2_agents_review.py`. Case-by-case "
        "review of how the two NON-CANONICAL LLM resolvers handled each "
        "treatment-arm dual-judge disagreement. Same case labels as "
        "[`02_fmv_2_audit_worksheet.md`](./02_fmv_2_audit_worksheet.md)."
    )
    lines.append(">")
    lines.append(
        "> - **Agent 1** — `gemini-3.1-pro-preview` on the content-axis "
        "(Stage 1/2/3) splits. Returns PASS/FAIL."
    )
    lines.append(
        "> - **Agent 2** — `gemini-3.1-pro-preview` on the structural-axis "
        "(N9-N12) splits. Returns PASS/FAIL."
    )
    lines.append(">")
    lines.append(
        "> Both are side analyses — they do NOT feed P1 / P2. The canonical "
        "resolution is the human audit "
        "([`02_fmv_2_audit_worksheet.md`](./02_fmv_2_audit_worksheet.md)). "
        "This file documents what each agent did so the eventual "
        "agent-vs-human agreement rate can be tabulated."
    )
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(
        f"**Content axis** — {len(content_cases)} dual-judge disagreements "
        f"(IRR 22.22 %). Agent 1: **PASS {a1_pass}, FAIL {a1_fail}.** "
        f"Sided with: Claude judge {a1_sided['judge_a']}/{len(content_cases)}, "
        f"OpenAI judge {a1_sided['judge_b']}/{len(content_cases)}, "
        f"neither {a1_sided['neither']}/{len(content_cases)}."
    )
    lines.append("")
    lines.append(
        f"**Structural axis** — {len(structural_cases)} dual-judge "
        f"disagreements (IRR 40.00 %, mandatory audit). Agent 2: "
        f"**PASS {a2_pass}, FAIL {a2_fail}.** Sided with: Claude judge "
        f"{a2_sided['judge_a']}/{len(structural_cases)}, OpenAI judge "
        f"{a2_sided['judge_b']}/{len(structural_cases)}, neither "
        f"{a2_sided['neither']}/{len(structural_cases)}."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"# Part A — Content axis ({len(content_cases)} cases)")
    lines.append("")

    for k, (model, t, stage) in enumerate(content_cases, start=1):
        a = cj_all[model].get((t, stage, "anthropic")) or {}
        b = cj_all[model].get((t, stage, "openai")) or {}
        rec = a1_all[model].get((t, stage), {})
        pv = rec.get("parsed_verdict") or {}
        clause = pv.get("first_fail_clause") or pv.get("failed_criterion") or "(n/a)"

        lines.append(f"## Case C{k} — `{model}` trial {t} · {STAGE_TITLE[stage]}")
        lines.append("")
        lines += _content_judge_line("Claude judge", a)
        lines += _content_judge_line("OpenAI judge", b)
        lines.append(
            f"### Agent 1 resolution — **`{_verdict(pv)}`** "
            f"(agreed_with: `{pv.get('agreed_with', '?')}`)"
        )
        lines.append("")
        lines.append(f"- failed clause / criterion: {clause}")
        lines.append(f"- reasoning: {(pv.get('reasoning') or '').strip()}")
        lines.append("")
        lines.append(
            f"_(verdict JSON: `results/{model}/02_fmv_2/content_resolved/{rec.get('_file', '?')}`)_"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(f"# Part B — Structural axis ({len(structural_cases)} cases)")
    lines.append("")

    for k, (model, t) in enumerate(structural_cases, start=1):
        a = sj_all[model].get((t, "structural", "anthropic")) or {}
        b = sj_all[model].get((t, "structural", "openai")) or {}
        rec = a2_all[model].get(t, {})
        pv = rec.get("parsed_verdict") or {}
        fc = ", ".join(pv.get("failed_criteria") or []) or "(none)"

        lines.append(f"## Case S{k} — `{model}` trial {t} · structural axis")
        lines.append("")
        lines += _structural_judge_line("Claude structural judge", a)
        lines += _structural_judge_line("OpenAI structural judge", b)
        lines.append(
            f"### Agent 2 resolution — **`{_verdict(pv)}`** "
            f"(agreed_with: `{pv.get('agreed_with', '?')}`)"
        )
        lines.append("")
        lines.append(f"- Agent 2's own Stage 1 rule count: `{pv.get('stage1_rule_count', '?')}`")
        lines.append(f"- failed_criteria: `{fc}`")
        lines.append(f"- reasoning: {(pv.get('reasoning') or '').strip()}")
        lines.append("")
        lines.append(
            f"_(verdict JSON: `results/{model}/02_fmv_2/structural_resolved/"
            f"{rec.get('_file', '?')}`)_"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    text = "\n".join(line.rstrip() for line in lines)
    OUTPUT.write_text(text.rstrip() + "\n")
    print(
        f"Wrote {OUTPUT.relative_to(REPO)} — "
        f"{len(content_cases)} content + {len(structural_cases)} structural cases."
    )


if __name__ == "__main__":
    main()
