"""Build ``analysis/02_fmv_2_audit_worksheet.md`` — the 02_fmv.2
human-audit worksheet for the treatment-arm dual-judge disagreements.

The 02_fmv.2 treatment arm produced two dual-judge disagreement sets:

- **Content axis** — 10 stage-level splits (IRR 22.22 %). Resolving
  them fixes each trial's content verdict (Stage 1 AND 2 AND 3).
- **Structural axis** — 6 trial-level splits (IRR 40.00 %, above the
  25 % threshold — a human audit is mandatory per prereg §1.3).

This file is the audit input. It emits one numbered case per
disagreement:

- Content cases (``C1``…) — the disputed stage response in full, both
  content judges' verdict + reasoning, and an audit-decision block. A
  case is marked **decisive** when resolving it changes the trial's
  content verdict (the other two stages are both consensus-PASS) and
  **non-decisive** when the trial is already content-FAIL regardless.
- Structural cases (``S1``…) — the Stage 1 rule set under judgment,
  Stage 2 as context, both structural judges' verdict + rule count +
  failed criteria + reasoning, and an audit-decision block.

Once decided, fill the ``HUMAN_CONTENT`` / ``HUMAN_STRUCTURAL`` tables
in ``scripts/apply_02_fmv_2.py`` and re-run it for the canonical
P1 / P2 verdicts.

Usage: ``uv run python scripts/build_02_fmv_2_worksheet.py``
"""

from __future__ import annotations

import glob
import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
TREATMENT_ID = "02_fmv_2"
OUTPUT = REPO / "analysis" / "02_fmv_2_audit_worksheet.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
STAGE_TITLE = {
    "induction": "Stage 1 — induction",
    "formulation": "Stage 2 — formulation",
    "prediction": "Stage 3 — prediction",
}


def _load(model: str, subdir: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / TREATMENT_ID / subdir / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if name.startswith("trial_"):
            out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
                d.get("parsed_verdict") or {}
            )
    return out


def _response(model: str, trial: int, stage: str) -> str:
    p = RESULTS / model / TREATMENT_ID / stage / f"trial_{trial}_t0.0.json"
    if not p.exists():
        return f"[trial JSON missing at {p}]"
    return json.loads(p.read_text())["response_text"]


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _evidence_block(parsed: dict[str, Any]) -> list[str]:
    ev = parsed.get("evidence")
    if isinstance(ev, str):
        return [f"- evidence: > {ev.strip() or '(none)'}"]
    if isinstance(ev, list) and ev:
        out = ["- evidence:"]
        for e in ev:
            if isinstance(e, dict):
                crit = e.get("criterion", "?")
                quote = (e.get("quote") or "").strip().replace("\n", " ")
                out.append(f"  - **{crit}** — > {quote}")
            else:
                out.append(f"  - > {str(e).strip()}")
        return out
    return ["- evidence: (none)"]


def _content_judge_lines(label: str, parsed: dict[str, Any]) -> list[str]:
    v = _verdict(parsed) or "(missing)"
    clause = parsed.get("first_fail_clause") or parsed.get("failed_criterion") or "(n/a)"
    out = [f"**{label} — verdict: `{v}`**", ""]
    step = parsed.get("first_fail_step")
    if step is not None:
        out.append(f"- first_fail_step: `{step}`")
    out.append(f"- failed clause / criterion: {clause}")
    out += _evidence_block(parsed)
    out.append(f"- reasoning: {(parsed.get('reasoning') or '').strip()}")
    out.append("")
    return out


def _structural_judge_lines(label: str, parsed: dict[str, Any]) -> list[str]:
    v = _verdict(parsed) or "(missing)"
    fc = ", ".join(parsed.get("failed_criteria") or []) or "(none)"
    out = [
        f"**{label} — verdict: `{v}`**",
        "",
        f"- stage1_rule_count: `{parsed.get('stage1_rule_count', '?')}`",
        f"- failed_criteria: `{fc}`",
    ]
    out += _evidence_block(parsed)
    out.append(f"- reasoning: {(parsed.get('reasoning') or '').strip()}")
    out.append("")
    return out


CONTENT_AUDIT = """\
**Audit decision** _(fill in)_:

- Resolved verdict for this stage: [ ] PASS  [ ] FAIL
- Agreed with: [ ] Claude judge  [ ] OpenAI judge  [ ] neither

**Audit notes** _(verbatim quote that decided it)_:

>
"""

STRUCTURAL_AUDIT = """\
**Audit decision** _(fill in)_:

- Your Stage 1 rule count: `____`
- N9 — Parsimony:    [ ] PASS  [ ] FAIL
- N10 — Independence: [ ] PASS  [ ] FAIL
- N11 — Traceability: [ ] PASS  [ ] FAIL
- N12 — Hierarchy:    [ ] PASS  [ ] FAIL
- **Overall structural verdict:** [ ] PASS  [ ] FAIL
- Agreed with: [ ] Claude judge  [ ] OpenAI judge  [ ] neither

**Audit notes** _(verbatim quotes from the Stage 1 response or criteria)_:

>
"""


def main() -> None:
    # Collect content + structural disagreements.
    content_cases: list[tuple[str, int, str]] = []
    structural_cases: list[tuple[str, int]] = []
    content: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}
    structural: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}
    for model in MODELS:
        cj = _load(model, "judgments")
        sj = _load(model, "structural")
        content[model] = cj
        structural[model] = sj
        for t in range(5):
            for stage in CONTENT_STAGES:
                va = _verdict(cj.get((t, stage, "anthropic")) or {})
                vb = _verdict(cj.get((t, stage, "openai")) or {})
                if va and vb and va != vb:
                    content_cases.append((model, t, stage))
            sa = _verdict(sj.get((t, "structural", "anthropic")) or {})
            sb = _verdict(sj.get((t, "structural", "openai")) or {})
            if sa and sb and sa != sb:
                structural_cases.append((model, t))

    # Decisiveness: a content split is decisive iff the trial's other
    # two stages are both consensus-PASS (so this stage flips the
    # trial's content verdict).
    def _decisive(model: str, trial: int, stage: str) -> bool:
        cj = content[model]
        for other in CONTENT_STAGES:
            if other == stage:
                continue
            va = _verdict(cj.get((trial, other, "anthropic")) or {})
            vb = _verdict(cj.get((trial, other, "openai")) or {})
            if not (va == vb == "PASS"):
                return False
        return True

    lines: list[str] = []
    lines.append("# 02_fmv.2 Audit Worksheet — treatment-arm dual-judge disagreements")
    lines.append("")
    lines.append(
        "_Generated by `scripts/build_02_fmv_2_worksheet.py` from the "
        "`prereg-02_fmv.2-locked` treatment-arm verdicts._"
    )
    lines.append("")
    lines.append("## How to use this worksheet")
    lines.append("")
    lines.append(
        f"The 02_fmv.2 treatment arm split the dual judges on "
        f"**{len(content_cases)} content** stage-units (IRR 22.22 %) and "
        f"**{len(structural_cases)} structural** trials (IRR 40.00 %, above "
        f"the 25 % audit threshold). Resolve each case below, then fill the "
        f"`HUMAN_CONTENT` / `HUMAN_STRUCTURAL` tables in "
        f"`scripts/apply_02_fmv_2.py` and re-run it for the canonical "
        f"P1 / P2 verdicts."
    )
    lines.append("")
    lines.append(
        "Content cases marked **decisive** flip the trial's content verdict; "
        "**non-decisive** cases sit on a trial that is content-FAIL "
        "regardless (resolve them for the record, but they do not change "
        "P2)."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"# Part A — Content axis ({len(content_cases)} cases)")
    lines.append("")

    for n, (model, trial, stage) in enumerate(content_cases, start=1):
        cj = content[model]
        a = cj.get((trial, stage, "anthropic")) or {}
        b = cj.get((trial, stage, "openai")) or {}
        decisive = "decisive" if _decisive(model, trial, stage) else "non-decisive"
        resp = _response(model, trial, stage).strip()
        lines += [
            f"## C{n}: `{model}` trial {trial} — {STAGE_TITLE[stage]} _({decisive})_",
            "",
            f"_Split: Claude judge -> `{_verdict(a)}`, OpenAI judge -> `{_verdict(b)}`_",
            "",
            f"### {STAGE_TITLE[stage]} response ({len(resp):,} chars)",
            "",
            "```",
            resp,
            "```",
            "",
            "---",
            "",
        ]
        lines += _content_judge_lines("Claude judge", a)
        lines += _content_judge_lines("OpenAI judge", b)
        lines += ["---", "", CONTENT_AUDIT, "---", ""]

    lines.append(f"# Part B — Structural axis ({len(structural_cases)} cases)")
    lines.append("")

    for n, (model, trial) in enumerate(structural_cases, start=1):
        sj = structural[model]
        a = sj.get((trial, "structural", "anthropic")) or {}
        b = sj.get((trial, "structural", "openai")) or {}
        s1 = _response(model, trial, "induction").strip()
        s2 = _response(model, trial, "formulation").strip()
        lines += [
            f"## S{n}: `{model}` trial {trial} — structural axis (N9-N12)",
            "",
            f"_Split: Claude structural judge -> `{_verdict(a)}`, "
            f"OpenAI structural judge -> `{_verdict(b)}`_",
            "",
            f"### Stage 1 — induction (rule set under judgment, {len(s1):,} chars)",
            "",
            "```",
            s1,
            "```",
            "",
            f"### Stage 2 — formulation (context only, never counted, {len(s2):,} chars)",
            "",
            "```",
            s2,
            "```",
            "",
            "---",
            "",
        ]
        lines += _structural_judge_lines("Claude structural judge", a)
        lines += _structural_judge_lines("OpenAI structural judge", b)
        lines += ["---", "", STRUCTURAL_AUDIT, "---", ""]

    text = "\n".join(line.rstrip() for line in lines)
    OUTPUT.write_text(text.rstrip() + "\n")
    print(
        f"Wrote {OUTPUT.relative_to(REPO)} — "
        f"{len(content_cases)} content + {len(structural_cases)} structural cases."
    )


if __name__ == "__main__":
    main()
