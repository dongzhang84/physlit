"""Build ``analysis/fmv/02_fmv_2_audit_worksheet.md`` — the 02_fmv.2
human-audit worksheet for the treatment-arm dual-judge disagreements.

Mirrors the layout of the prior worksheets
(``scripts/build_02_fmv_audit_worksheet.py``,
``scripts/build_02_fmv_1_structural_worksheet.py``): each case carries
a clickable link to the trial's ``.md`` companion (and its ``.json``
source of truth), prior-stage context where relevant, links to the
frozen criteria, and an empty audit-decision block.

The 02_fmv.2 treatment arm produced:

- **Content axis** — 10 stage-level dual-judge splits (IRR 22.22 %).
- **Structural axis** — 6 trial-level dual-judge splits (IRR 40.00 %,
  above the 25 % threshold — a human audit is mandatory per
  ``predictions/02_fmv_2_prereg.md`` §1.3).

Content cases marked **decisive** flip the trial's content verdict;
**non-decisive** cases sit on a trial that is content-FAIL regardless
(resolve them for the record, but they do not change P2).

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
OUTPUT = REPO / "analysis" / "fmv" / "02_fmv_2_audit_worksheet.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
PRIOR_STAGE = {"formulation": "induction", "prediction": "formulation"}
STAGE_TITLE = {
    "induction": "Stage 1 — induction",
    "formulation": "Stage 2 — formulation",
    "prediction": "Stage 3 — prediction",
}
STAGE_LABEL = {"induction": "Stage 1", "formulation": "Stage 2", "prediction": "Stage 3"}


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


def _trial_links(model: str, trial: int, under_judgment: str | tuple[str, ...]) -> list[str]:
    """Clickable links (relative to ``analysis/``) to the trial's ``.md``
    companions and ``.json`` sources. ``under_judgment`` is the stage (or
    tuple of stages) whose response is the rule set under judgment; the
    remaining four stages are listed as "same trial, other stages"."""
    base = f"../results/{model}/{TREATMENT_ID}"
    under = (under_judgment,) if isinstance(under_judgment, str) else under_judgment
    primary_links = " · ".join(
        f"{STAGE_LABEL.get(s, s)} "
        f"[`.md`]({base}/{s}/trial_{trial}_t0.0.md) "
        f"[`.json`]({base}/{s}/trial_{trial}_t0.0.json)"
        for s in under
    )
    others = " · ".join(
        f"[{STAGE_LABEL.get(s, s)}]({base}/{s}/trial_{trial}_t0.0.md)"
        for s in (*CONTENT_STAGES, "meta")
        if s not in under
    )
    return [
        f"**Trial files** (under judgment): {primary_links}",
        f"**Same trial, other stages:** {others}",
        "",
    ]


HEADER_LINES = [
    "# 02_fmv.2 Audit Worksheet — treatment-arm dual-judge disagreements",
    "",
    "_Generated by `scripts/build_02_fmv_2_worksheet.py` from the "
    "`prereg-02_fmv.2-locked` treatment-arm verdicts._",
    "",
    "## How to use this worksheet",
    "",
    "The 02_fmv.2 treatment arm split the dual judges on "
    "**10 content** stage-units (IRR 22.22 %) and "
    "**6 structural** trials (IRR 40.00 %, above the 25 % audit "
    "threshold — a human audit is mandatory per "
    "[`predictions/02_fmv_2_prereg.md`](../predictions/02_fmv_2_prereg.md) §1.3).",
    "",
    "For each case below:",
    "",
    "1. Open the trial files (links given per case). The `.md` companions "
    "render the prompt + response + both judges in one view; the `.json` "
    "files are the source of truth.",
    "2. Compare both judges' verdicts and cited evidence inline.",
    "3. Refer to the frozen criteria as needed:",
    "   - Content axis (`prereg-02_fmv-locked`): "
    "[`ideal_induction.md`](../frameworks/02_fmv/ideal_induction.md) (Stage 1; "
    "§3 banned tokens, §5 patterns) · "
    "[`pass_fail_criteria.md`](../frameworks/02_fmv/pass_fail_criteria.md) "
    "(Stages 2-3) · "
    "[`prediction_tests.md`](../frameworks/02_fmv/prediction_tests.md) "
    "(Stage 3 answer key)",
    "   - Structural axis (`prereg-02_fmv.1-locked`): "
    "[`structural_criteria.md`](../frameworks/02_fmv/structural_criteria.md) "
    "(N9-N12)",
    "   - Treatment Stage 1 prompt (the manipulated variable): "
    "[`stage1_induction_axiomatised.md`](../frameworks/02_fmv/prompts/stage1_induction_axiomatised.md)",
    "4. Fill the **Audit decision** block.",
    "5. Add **Audit notes** quoting the text that decided it.",
    "",
    "Content cases marked **decisive** flip the trial's content verdict; "
    "**non-decisive** cases sit on a trial that is content-FAIL regardless "
    "(resolve them for the record, but they do not change P2).",
    "",
    "Once decided, fill the `HUMAN_CONTENT` / `HUMAN_STRUCTURAL` tables in "
    "[`scripts/apply_02_fmv_2.py`](../scripts/apply_02_fmv_2.py) and re-run "
    "it for the canonical P1 / P2 verdicts.",
    "",
    "**Agent 1 + Agent 2 verdicts (non-canonical preview):** "
    "[`02_fmv_2_agents_review.md`](./02_fmv_2_agents_review.md). Look at "
    "them only after forming an independent verdict — the canonical "
    "resolution is your audit.",
    "",
    "---",
    "",
]


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

    lines: list[str] = list(HEADER_LINES)
    lines.append(f"# Part A — Content axis ({len(content_cases)} cases)")
    lines.append("")

    for n, (model, trial, stage) in enumerate(content_cases, start=1):
        cj = content[model]
        a = cj.get((trial, stage, "anthropic")) or {}
        b = cj.get((trial, stage, "openai")) or {}
        decisive = "decisive" if _decisive(model, trial, stage) else "non-decisive"
        resp = _response(model, trial, stage).strip()
        lines.append(f"## C{n}: `{model}` trial {trial} — {STAGE_TITLE[stage]} _({decisive})_")
        lines.append("")
        lines.append(f"_Split: Claude judge -> `{_verdict(a)}`, OpenAI judge -> `{_verdict(b)}`_")
        lines.append("")
        lines += _trial_links(model, trial, stage)

        # Prior-stage context for Stage 2 / Stage 3 cases.
        prior = PRIOR_STAGE.get(stage)
        if prior:
            ctx = _response(model, trial, prior).strip()
            lines += [
                f"### {STAGE_TITLE[prior]} response (context, {len(ctx):,} chars)",
                "",
                "```",
                ctx,
                "```",
                "",
            ]
        lines += [
            f"### {STAGE_TITLE[stage]} response (under judgment, {len(resp):,} chars)",
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
        lines.append(f"## S{n}: `{model}` trial {trial} — structural axis (N9-N12)")
        lines.append("")
        lines.append(
            f"_Split: Claude structural judge -> `{_verdict(a)}`, "
            f"OpenAI structural judge -> `{_verdict(b)}`_"
        )
        lines.append("")
        lines += _trial_links(model, trial, ("induction", "formulation"))
        lines += [
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
