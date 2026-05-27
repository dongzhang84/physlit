"""Build ``analysis/03_decay_audit_worksheet.md`` — the 03_decay human
audit worksheet for the dual-judge disagreements + fabrication-flagged
cases produced by the production judging run.

03_decay has three parts of disagreements that need human resolution:

- **Part A — Stage-level content verdict** (Stage 1 / Stage 2 /
  Stage 3 overall PASS/FAIL): 18 cases. All non-decisive for P1
  because every trial has at least one Stage 3 scenario that FAILs,
  forcing composite content = FAIL on every trial; resolving them is
  still required per the prereg, but the canonical P1 verdict
  (0/15 composite content PASS) is robust to their resolution.

- **Part B — Stage 3 per-scenario** (over the 4 quantitative
  scenarios x 15 trials = 60 units): 32 cases needing resolution
  (verdict disagreements + direction disagreements + fabrication
  flags). Collectively decisive for P3 — the ratio-leaked vs
  direction-wrong count depends on all 32 resolutions.

- **Part C — Meta over-claim** (Stage 4 yes/no/vacuous): 4
  disagreement cases. All decisive for P4 (current 6 yes vs 5 no;
  margin = 1, vs 4 pending).

Mirrors ``scripts/build_v0_3_worksheet.py`` and
``scripts/build_02_fmv_audit_worksheet.py``: clickable trial links,
prior-stage context for Stage 2/3 cases, scenario answer-key
extraction for Part B, empty audit-decision blocks.

The Agent 1 + Agent 2 non-canonical preview lives in
``analysis/03_decay_agents_review.md`` (a separate file) so the
auditor can form an independent verdict first.

Usage: ``uv run python scripts/build_03_decay_worksheet.py``
"""

from __future__ import annotations

import glob
import json
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
FRAMEWORK_ID = "03_decay"
FRAMEWORK_DIR = REPO / "frameworks" / FRAMEWORK_ID
OUTPUT = REPO / "analysis" / "03_decay_audit_worksheet.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
PRIOR_STAGE = {"formulation": "induction", "prediction": "formulation"}
STAGE_TITLE = {
    "induction": "Stage 1 — induction",
    "formulation": "Stage 2 — formulation",
    "prediction": "Stage 3 — prediction",
    "meta": "Stage 4 — meta",
}
STAGE_LABEL = {
    "induction": "Stage 1",
    "formulation": "Stage 2",
    "prediction": "Stage 3",
    "meta": "Stage 4",
}
QUANT_SCENARIOS = (1, 2, 3, 4)


# --- Loaders ----------------------------------------------------------
def _load_verdicts(model: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / FRAMEWORK_ID / "judgments" / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if not name.startswith("trial_"):
            continue
        out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
            d.get("parsed_verdict") or {}
        )
    return out


def _response(model: str, trial: int, stage: str) -> str:
    p = RESULTS / model / FRAMEWORK_ID / stage / f"trial_{trial}_t0.0.json"
    if not p.exists():
        return f"[trial JSON missing at {p}]"
    return json.loads(p.read_text())["response_text"]


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _scenario_block(parsed: dict[str, Any], idx: int) -> dict[str, Any]:
    for sc in parsed.get("scenarios") or []:
        if isinstance(sc, dict) and sc.get("index") == idx:
            return sc
    return {}


def _scenario_fab(parsed: dict[str, Any], idx: int) -> bool:
    for ev in parsed.get("_evidence_check") or []:
        if ev.get("scope") == f"scenario_{idx}" and ev.get("fabricated"):
            return True
    return False


def _meta_overclaim(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("over_claim")
    if not isinstance(raw, str):
        return None
    low = raw.strip().lower()
    return low if low in {"yes", "no", "vacuous"} else None


# --- Scenario prompt + PASS range extraction --------------------------
SCENARIO_PASS_RANGES = {
    1: "6.5 deg - 8.5 deg (target ~ 7.4 deg)",
    2: "200 K - 240 K (target ~ 219 K). Approaching room temperature ~ 293 K is FAIL.",
    3: "60 - 90 rad/s (target ~ 73 rad/s)",
    4: "0.45 m - 0.65 m (target ~ 0.55 m)",
    5: "Eventually stops (not 'forever') AND timescale 300 - 700 s (target ~ 458 s)",
}


def _extract_scenario_prompt(idx: int) -> str:
    """Pull the scenario prompt from the framework's prediction_tests.md
    (the same text the runner sends to the tested model)."""
    text = (FRAMEWORK_DIR / "prediction_tests.md").read_text()
    pattern = re.compile(
        rf"^## Scenario {idx} —.*?\*\*Prompt to the model\.\*\*(.+?)(?:\n\n\||\n\n-{{3,}})",
        re.DOTALL | re.MULTILINE,
    )
    m = pattern.search(text)
    return m.group(1).strip() if m else f"(prompt for scenario {idx} not found)"


# --- Format helpers ---------------------------------------------------
def _evidence_short(s: Any, maxlen: int = 300) -> str:
    if not isinstance(s, str):
        return "(none)"
    s = s.strip().replace("\n", " ")
    return s if len(s) <= maxlen else s[: maxlen - 3] + "..."


def _trial_links(model: str, trial: int, under_judgment: str | tuple[str, ...]) -> list[str]:
    base = f"../results/{model}/{FRAMEWORK_ID}"
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
        f"**Same trial, other stages (.md companions):** {others}",
        "",
    ]


def _content_judge_lines(label: str, parsed: dict[str, Any]) -> list[str]:
    v = _verdict(parsed) or "(missing)"
    clause = parsed.get("first_fail_clause") or parsed.get("failed_criterion") or "(n/a)"
    fab_status = "(no evidence_check)"
    for ev in parsed.get("_evidence_check") or []:
        if ev.get("scope") == "verdict":
            fab_status = "**FABRICATED**" if ev.get("fabricated") else "OK"
            break
    out = [f"**{label} — verdict: `{v}`** (evidence_check: {fab_status})", ""]
    step = parsed.get("first_fail_step")
    if step is not None:
        out.append(f"- first_fail_step: `{step}`")
    out.append(f"- failed clause / criterion: {clause}")
    out.append(f"- evidence: > {_evidence_short(parsed.get('evidence'))}")
    out.append(f"- reasoning: {_evidence_short(parsed.get('reasoning'), 800)}")
    out.append("")
    return out


def _scenario_judge_lines(label: str, sc: dict[str, Any], fab: bool) -> list[str]:
    v = sc.get("verdict") or "(missing)"
    d = sc.get("direction") or "(missing)"
    fab_tag = "**FABRICATED**" if fab else "OK"
    out = [
        f"**{label} — verdict: `{v}` direction: `{d}`** (evidence_check: {fab_tag})",
        "",
        f"- failed_criterion: {sc.get('failed_criterion') or '(n/a)'}",
        f"- evidence: > {_evidence_short(sc.get('evidence'))}",
        f"- reasoning: {_evidence_short(sc.get('reasoning'), 800)}",
        "",
    ]
    return out


def _meta_judge_lines(label: str, parsed: dict[str, Any]) -> list[str]:
    oc = _meta_overclaim(parsed) or "(missing)"
    return [
        f"**{label} — over_claim: `{oc}`**",
        "",
        f"- evidence: > {_evidence_short(parsed.get('evidence'))}",
        f"- reasoning: {_evidence_short(parsed.get('reasoning'), 800)}",
        "",
    ]


# --- Audit-decision templates -----------------------------------------
CONTENT_AUDIT = """\
**Audit decision** _(fill in)_:

- Resolved verdict for this stage: [ ] PASS  [ ] FAIL
- Agreed with: [ ] Claude judge  [ ] OpenAI judge  [ ] neither

**Audit notes** _(verbatim quote that decided it)_:

>
"""

SCENARIO_AUDIT = """\
**Audit decision** _(fill in)_:

- Resolved verdict: [ ] PASS  [ ] FAIL
- Resolved direction: [ ] correct  [ ] wrong  [ ] n/a
- Resulting bucket: [ ] decay-correct  [ ] direction-correct, ratio-leaked  [ ] direction-wrong
- Agreed with: [ ] Claude judge  [ ] OpenAI judge  [ ] neither

**Audit notes** _(model's headline number / qualitative answer for this scenario; verbatim)_:

>
"""

META_AUDIT = """\
**Audit decision** _(fill in)_:

- Resolved over_claim: [ ] yes  [ ] no  [ ] vacuous
- Agreed with: [ ] Claude judge  [ ] OpenAI judge  [ ] neither

**Audit notes** _(verbatim quote from Stage 4 that decided it)_:

>
"""


HEADER_LINES = [
    "# 03_decay Audit Worksheet — dual-judge disagreements + fabrication-flagged cases",
    "",
    "_Generated by `scripts/build_03_decay_worksheet.py` from the "
    "`prereg-03_decay-locked` production-arm verdicts._",
    "",
    "## How to use this worksheet",
    "",
    "The 03_decay production run produced an IRR of **40.00 % (18 of 45 "
    "Stage 1-3 judged units)**, which triggers the `CLAUDE.md` "
    "mandatory-audit threshold (> 25 %). The audit also covers the "
    "Stage 3 per-scenario disagreements and the meta over-claim "
    "disagreements that affect P3 / P4.",
    "",
    "Three parts:",
    "",
    "- **Part A — content stage-verdict cases** (18). All **non-decisive "
    "for P1**: every trial has at least one Stage 3 scenario that FAILs, "
    "so composite content = FAIL on every trial; P1 stays 0/15 "
    "regardless of these resolutions. Resolve for the record.",
    "- **Part B — Stage 3 per-scenario cases** (32). Collectively "
    "**decisive for P3**: the ratio-leaked vs direction-wrong margin "
    "depends on all 32 resolutions. Current pre-audit margin (post-Agent 2 "
    "non-canonical preview) is 22 ratio-leaked vs 1 direction-wrong, "
    "with all 32 reclassified by Agent 2 — your audit is canonical.",
    "- **Part C — meta over-claim cases** (4). All **decisive for P4**: "
    "current 6 yes vs 5 no, so 4 pending can flip the verdict.",
    "",
    "For each case below:",
    "",
    "1. Open the trial JSON files (links per case).",
    "2. Compare both judges' verdicts and cited evidence. Note the "
    "`evidence_check` status — `FABRICATED` means the judge's cited "
    "evidence is not a substring of the response (the OpenAI judge "
    "exhibited this on a number of Stage 1 / Stage 3 §3 citations; see "
    "`analysis/03_decay_dryrun_findings.md` §6 Gap 4).",
    "3. Refer to the frozen criteria as needed: "
    "[`ideal_induction.md`](../frameworks/03_decay/ideal_induction.md) "
    "(Stage 1; §3 banned tokens, §5 patterns, §6 6-step checklist) · "
    "[`pass_fail_criteria.md`](../frameworks/03_decay/pass_fail_criteria.md) "
    "(Stages 2-3) · "
    "[`prediction_tests.md`](../frameworks/03_decay/prediction_tests.md) "
    "(Stage 3 answer key with PASS ranges per scenario).",
    "4. Fill the **Audit decision** block.",
    "5. Add **Audit notes** with a verbatim quote.",
    "",
    "**Agent 1 + Agent 2 non-canonical preview:** "
    "[`03_decay_agents_review.md`](./03_decay_agents_review.md). "
    "Case numbering is **1:1 aligned**: Part A `C{n}` ↔ Agent 1 `A1-{n}` "
    "(18 cases), Part B `B{n}` ↔ Agent 2 `A2-{n}` (32 cases). Each case "
    "block below labels its agent counterpart so you can cross-check "
    "after forming an independent verdict. Part C (meta over-claim) has "
    "no agent counterpart. "
    "Look at the agent preview only after forming an independent "
    "verdict — the "
    "canonical resolution is your audit.",
    "",
    "Once decided, fill the corresponding tables in "
    "`scripts/apply_03_decay.py` (TBD) and re-run for the canonical "
    "P1 / P2 / P3 / P4 verdicts.",
    "",
    "---",
    "",
]


def main() -> None:
    verdicts: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}
    for m in MODELS:
        verdicts[m] = _load_verdicts(m)

    # --- Part A: stage-level content cases
    # Sort key (model_index, stage_name, trial) matches the ordering of
    # ``sorted(glob('agent1_<stage>_t<N>_*.json'))`` in
    # ``build_03_decay_agents_review.py`` so worksheet C-numbers align 1:1
    # with the Agent 1 A1-numbers across the 18 cases.
    content_cases: list[tuple[str, int, str]] = []
    for m in MODELS:
        v = verdicts[m]
        for t in range(5):
            for stage in CONTENT_STAGES:
                va = _verdict(v.get((t, stage, "anthropic")) or {})
                vb = _verdict(v.get((t, stage, "openai")) or {})
                if va and vb and va != vb:
                    content_cases.append((m, t, stage))
    content_cases.sort(key=lambda c: (MODELS.index(c[0]), c[2], c[1]))

    # --- Part B: per-scenario Stage 3 cases
    scenario_cases: list[tuple[str, int, int, str]] = []  # (model, trial, scenario, reason)
    for m in MODELS:
        v = verdicts[m]
        for t in range(5):
            a = v.get((t, "prediction", "anthropic")) or {}
            b = v.get((t, "prediction", "openai")) or {}
            for sidx in QUANT_SCENARIOS:
                sca = _scenario_block(a, sidx)
                scb = _scenario_block(b, sidx)
                va = _verdict(sca)
                vb = _verdict(scb)
                da = sca.get("direction")
                db = scb.get("direction")
                fab_a = _scenario_fab(a, sidx)
                fab_b = _scenario_fab(b, sidx)
                reasons = []
                if va is None or vb is None:
                    reasons.append("missing verdict")
                elif va != vb:
                    reasons.append("verdict disagree")
                elif va == "FAIL" and da != db:
                    reasons.append("direction disagree")
                if fab_a or fab_b:
                    reasons.append(f"fab(claude={fab_a},openai={fab_b})")
                if reasons:
                    scenario_cases.append((m, t, sidx, "; ".join(reasons)))

    # --- Part C: meta over-claim cases
    meta_cases: list[tuple[str, int]] = []
    for m in MODELS:
        v = verdicts[m]
        for t in range(5):
            a = v.get((t, "meta", "anthropic")) or {}
            b = v.get((t, "meta", "openai")) or {}
            oa = _meta_overclaim(a)
            ob = _meta_overclaim(b)
            if oa and ob and oa != ob:
                meta_cases.append((m, t))

    # --- Build worksheet
    lines: list[str] = list(HEADER_LINES)

    # Part A
    lines.append(f"# Part A — Content stage-verdict cases ({len(content_cases)})")
    lines.append("")
    lines.append("_All non-decisive for P1; resolve for the record._")
    lines.append("")
    for n, (model, trial, stage) in enumerate(content_cases, start=1):
        v = verdicts[model]
        a = v.get((trial, stage, "anthropic")) or {}
        b = v.get((trial, stage, "openai")) or {}
        resp = _response(model, trial, stage).strip()
        lines.append(f"## C{n}: `{model}` trial {trial} — {STAGE_TITLE[stage]} _(non-decisive)_")
        lines.append("")
        lines.append(f"_Split: Claude judge -> `{_verdict(a)}`, OpenAI judge -> `{_verdict(b)}`_")
        lines.append("")
        lines.append(
            f"_Agent 1 preview: **A1-{n}** in [`03_decay_agents_review.md`](./03_decay_agents_review.md)._"
        )
        lines.append("")
        lines += _trial_links(model, trial, stage)
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

    # Part B
    lines.append(f"# Part B — Stage 3 per-scenario cases ({len(scenario_cases)})")
    lines.append("")
    lines.append(
        "_Collectively decisive for P3. Each case shows the scenario prompt "
        "+ PASS range + the model's full Stage 3 response so the audit can "
        "locate the scenario-specific prediction._"
    )
    lines.append("")
    for n, (model, trial, sidx, reason) in enumerate(scenario_cases, start=1):
        v = verdicts[model]
        a = v.get((trial, "prediction", "anthropic")) or {}
        b = v.get((trial, "prediction", "openai")) or {}
        sca = _scenario_block(a, sidx)
        scb = _scenario_block(b, sidx)
        resp = _response(model, trial, "prediction").strip()
        s2 = _response(model, trial, "formulation").strip()
        prompt = _extract_scenario_prompt(sidx)
        pass_range = SCENARIO_PASS_RANGES.get(sidx, "(unknown)")
        lines.append(f"## B{n}: `{model}` trial {trial} — Scenario {sidx} _({reason})_")
        lines.append("")
        lines.append(
            f"_Agent 2 preview: **A2-{n}** in [`03_decay_agents_review.md`](./03_decay_agents_review.md)._"
        )
        lines.append("")
        lines.append(
            f"_Split: Claude -> `{sca.get('verdict')}` / direction `{sca.get('direction')}`, "
            f"OpenAI -> `{scb.get('verdict')}` / direction `{scb.get('direction')}`_"
        )
        lines.append("")
        lines.append(f"**Scenario {sidx} PASS range:** {pass_range}")
        lines.append("")
        lines += _trial_links(model, trial, "prediction")
        lines += [
            f"### Scenario {sidx} — prompt sent to model",
            "",
            "```",
            prompt,
            "```",
            "",
            f"### Stage 2 — formulation response (context, {len(s2):,} chars)",
            "",
            "```",
            s2,
            "```",
            "",
            f"### Stage 3 — full prediction response ({len(resp):,} chars)",
            "",
            "```",
            resp,
            "```",
            "",
            "---",
            "",
        ]
        lines += _scenario_judge_lines("Claude judge", sca, _scenario_fab(a, sidx))
        lines += _scenario_judge_lines("OpenAI judge", scb, _scenario_fab(b, sidx))
        lines += ["---", "", SCENARIO_AUDIT, "---", ""]

    # Part C
    lines.append(f"# Part C — Meta over-claim cases ({len(meta_cases)})")
    lines.append("")
    lines.append("_All decisive for P4 (current 6 yes vs 5 no; 4 pending can flip)._")
    lines.append("")
    for n, (model, trial) in enumerate(meta_cases, start=1):
        v = verdicts[model]
        a = v.get((trial, "meta", "anthropic")) or {}
        b = v.get((trial, "meta", "openai")) or {}
        s4 = _response(model, trial, "meta").strip()
        s1 = _response(model, trial, "induction").strip()
        s2 = _response(model, trial, "formulation").strip()
        s3 = _response(model, trial, "prediction").strip()
        oa = _meta_overclaim(a) or "?"
        ob = _meta_overclaim(b) or "?"
        lines.append(f"## M{n}: `{model}` trial {trial} — Stage 4 over-claim")
        lines.append("")
        lines.append(f"_Split: Claude meta -> `{oa}`, OpenAI meta -> `{ob}`_")
        lines.append("")
        lines += _trial_links(model, trial, "meta")
        lines += [
            f"### Stage 1 — induction (context, {len(s1):,} chars)",
            "",
            "```",
            s1,
            "```",
            "",
            f"### Stage 2 — formulation (context, {len(s2):,} chars)",
            "",
            "```",
            s2,
            "```",
            "",
            f"### Stage 3 — prediction (context, {len(s3):,} chars)",
            "",
            "```",
            s3,
            "```",
            "",
            f"### Stage 4 — meta response (under judgment, {len(s4):,} chars)",
            "",
            "```",
            s4,
            "```",
            "",
            "---",
            "",
        ]
        lines += _meta_judge_lines("Claude meta judge", a)
        lines += _meta_judge_lines("OpenAI meta judge", b)
        lines += ["---", "", META_AUDIT, "---", ""]

    text = "\n".join(line.rstrip() for line in lines)
    OUTPUT.write_text(text.rstrip() + "\n")
    print(
        f"Wrote {OUTPUT.relative_to(REPO)} — "
        f"{len(content_cases)} content + {len(scenario_cases)} scenario + {len(meta_cases)} meta cases."
    )


if __name__ == "__main__":
    main()
