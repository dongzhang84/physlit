"""Build ``analysis/aristotelian/v0_1_audit_worksheet.md`` from production trials + judge verdicts.

For every (model, trial, stage) where the two judges disagreed, emit
one numbered case with:

- trial JSON path
- the tested-model response (truncated if long, with byte-count
  preserved for traceability)
- Claude-as-judge verdict + reasoning + evidence (verbatim)
- OpenAI-as-judge verdict + reasoning + evidence (verbatim)
- an empty "Audit decision" checkbox block for the operator

For Stage 4 (meta over-claim) cases, also include the operator-visible
consensus Stage 1-3 verdicts that were the inputs to the meta judges.

Cases are grouped by stage so the operator can audit one stage's worth
of judge calibration in a single pass.

Usage: ``uv run python scripts/build_audit_worksheet.py``
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
ANALYSIS = REPO / "analysis"
OUTPUT = ANALYSIS / "aristotelian" / "v0_1_audit_worksheet.md"
FRAMEWORK_ID = "01_aristotelian"

MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
STAGE_ORDER = ("induction", "formulation", "prediction", "meta")
STAGE_TITLES = {
    "induction": "Stage 1 — Induction",
    "formulation": "Stage 2 — Formulation",
    "prediction": "Stage 3 — Prediction",
    "meta": "Stage 4 — Meta over-claim",
}

RESPONSE_TRUNCATE_CHARS = 3000


@dataclass(frozen=True)
class DisagreeCase:
    model: str
    trial_index: int
    stage: str
    claude_parsed: dict[str, Any]
    openai_parsed: dict[str, Any]
    claude_verdict: str  # normalised label for header
    openai_verdict: str


def _load_trial_response(model: str, trial_index: int, stage: str) -> tuple[str, int]:
    p = RESULTS / model / FRAMEWORK_ID / stage / f"trial_{trial_index}_t0.0.json"
    if not p.exists():
        return f"[trial JSON missing at {p}]", 0
    text = json.loads(p.read_text())["response_text"]
    return text, len(text)


def _load_judge_verdicts(model: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    judgments_dir = RESULTS / model / "judgments"
    if not judgments_dir.exists():
        return out
    for vp in judgments_dir.glob("*.json"):
        d = json.loads(vp.read_text())
        trial_path = Path(d["trial_path"])
        fname = trial_path.name
        if not fname.startswith("trial_"):
            continue
        trial_index = int(fname.split("_")[1])
        stage = trial_path.parent.name
        key = (trial_index, stage, d["judge_family"])
        out[key] = d.get("parsed_verdict", {}) or {}
    return out


def _verdict_label(parsed: dict[str, Any], stage: str) -> str:
    """Return a short label for the case header.

    Stage 1/2: "PASS" / "FAIL".
    Stage 3:   "PASS" / "FAIL" (overall).
    Stage 4:   "yes" / "no" / "vacuous".
    """
    if not parsed:
        return "(missing)"
    if stage == "meta":
        return str(parsed.get("over_claim", "?")).lower()
    raw = parsed.get("verdict") or parsed.get("overall_verdict") or "?"
    return str(raw).upper()


def _truncate(s: str, max_chars: int = RESPONSE_TRUNCATE_CHARS) -> str:
    if len(s) <= max_chars:
        return s
    return (
        s[:max_chars]
        + f"\n\n[... truncated, {len(s) - max_chars:,} more chars; full text in trial JSON]"
    )


def _render_judge_block(label: str, parsed: dict[str, Any], stage: str) -> list[str]:
    out: list[str] = []
    if not parsed:
        out.append(f"**{label}:** (no parsed verdict — judge call may have failed to return JSON)")
        return out

    if stage == "prediction":
        overall = parsed.get("overall_verdict", "?")
        out.append(f"**{label} — overall_verdict: `{overall}`**")
        out.append("")
        scenarios = parsed.get("scenarios") or []
        for sc in scenarios:
            idx = sc.get("index", "?")
            v = sc.get("verdict", "?")
            failed = sc.get("failed_criterion") or "(n/a)"
            ev = sc.get("evidence") or "(n/a)"
            rs = sc.get("reasoning", "")
            out.append(f"- **Scenario {idx}:** `{v}`")
            out.append(f"  - failed_criterion: {failed}")
            out.append(f"  - evidence: {ev}")
            out.append(f"  - reasoning: {rs}")
        return out

    if stage == "meta":
        oc = parsed.get("over_claim", "?")
        ev = parsed.get("evidence") or "(n/a)"
        rs = parsed.get("reasoning", "")
        out.append(f"**{label} — over_claim: `{oc}`**")
        out.append("")
        out.append(f"- evidence: {ev}")
        out.append(f"- reasoning: {rs}")
        return out

    # Stage 1 / 2
    v = parsed.get("verdict", "?")
    out.append(f"**{label} — verdict: `{v}`**")
    out.append("")
    if stage == "induction":
        step = parsed.get("first_fail_step")
        if step is not None:
            out.append(f"- first_fail_step: {step}")
        clause = parsed.get("first_fail_clause") or "(n/a)"
        out.append(f"- first_fail_clause: {clause}")
    else:
        clause = parsed.get("failed_criterion") or "(n/a)"
        out.append(f"- failed_criterion: {clause}")
    out.append(f"- evidence: {parsed.get('evidence') or '(n/a)'}")
    out.append(f"- reasoning: {parsed.get('reasoning', '')}")
    return out


def _stage1_3_consensus(
    model: str,
    trial_index: int,
    verdicts: dict[tuple[int, str, str], dict[str, Any]],
) -> list[str]:
    """Render the Stage 1-3 consensus summary that the meta judges saw."""
    out: list[str] = []
    for stage in ("induction", "formulation", "prediction"):
        cv_p = verdicts.get((trial_index, stage, "anthropic"), {})
        ov_p = verdicts.get((trial_index, stage, "openai"), {})
        cv = _verdict_label(cv_p, stage)
        ov = _verdict_label(ov_p, stage)
        joint = cv if cv == ov else f"DISAGREE (claude={cv} / openai={ov})"
        out.append(f"- **{STAGE_TITLES[stage]}:** {joint}")
    return out


def _decision_block(stage: str) -> list[str]:
    out = ["", "**Audit decision** _(fill in)_:", ""]
    if stage == "meta":
        out.extend(
            [
                "- [ ] over_claim = yes (model failed to flag a real Stage 1-3 failure)",
                "- [ ] over_claim = no (model correctly identified its slips)",
                "- [ ] over_claim = vacuous (no Stage 1-3 failure to over-claim about)",
                "- [ ] other: ___",
            ]
        )
    else:
        out.extend(
            [
                "- [ ] PASS (Claude judge was right)",
                "- [ ] FAIL (OpenAI judge was right)",
                "- [ ] PASS, but for different reason than Claude judge gave",
                "- [ ] FAIL, but for different reason than OpenAI judge gave",
                "- [ ] other: ___",
            ]
        )
    out.extend(
        [
            "",
            "**Audit notes** _(verbatim quotes from response or criteria as evidence)_:",
            "",
            "> ",
            "",
        ]
    )
    return out


def main() -> int:
    cases_by_stage: dict[str, list[DisagreeCase]] = defaultdict(list)
    all_verdicts_by_model: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}

    for model in MODELS:
        verdicts = _load_judge_verdicts(model)
        all_verdicts_by_model[model] = verdicts
        for trial_index in range(5):
            for stage in STAGE_ORDER:
                cv_p = verdicts.get((trial_index, stage, "anthropic"), {})
                ov_p = verdicts.get((trial_index, stage, "openai"), {})
                if not cv_p or not ov_p:
                    continue
                cv = _verdict_label(cv_p, stage)
                ov = _verdict_label(ov_p, stage)
                if cv == "?" or ov == "?":
                    continue
                if cv == ov:
                    continue
                cases_by_stage[stage].append(
                    DisagreeCase(
                        model=model,
                        trial_index=trial_index,
                        stage=stage,
                        claude_parsed=cv_p,
                        openai_parsed=ov_p,
                        claude_verdict=cv,
                        openai_verdict=ov,
                    )
                )

    # --- Render ---
    lines: list[str] = []
    total_cases = sum(len(cs) for cs in cases_by_stage.values())
    lines.append(f"# v0.1 Audit Worksheet — {total_cases} DISAGREE cases\n")
    lines.append(
        "_Generated by `scripts/build_audit_worksheet.py` from the\n"
        "`prereg-v0.1-locked` production trials + judge verdicts._\n"
    )
    lines.append(
        "## How to use this worksheet\n\n"
        "Per the prereg locked at `prereg-v0.1-locked`, the v0.1 dual-judge\n"
        "inter-rater disagreement rate of 36.67 % exceeds the 25 % threshold\n"
        "that triggers human audit before public release. This file is the\n"
        "audit input.\n\n"
        "For each case below:\n\n"
        "1. Read the tested-model response excerpt.\n"
        "2. Compare both judges' verdicts and their cited evidence.\n"
        "3. Refer to the frozen criteria as needed:\n"
        "   - [`frameworks/01_aristotelian/ideal_induction.md`]"
        "(../frameworks/01_aristotelian/ideal_induction.md) (Stage 1)\n"
        "   - [`frameworks/01_aristotelian/pass_fail_criteria.md`]"
        "(../frameworks/01_aristotelian/pass_fail_criteria.md) (Stages 1-3)\n"
        "4. Tick one box in the **Audit decision** block, or write in OTHER.\n"
        "5. Add **Audit notes** quoting the specific evidence that decided it.\n\n"
        "When all 22 cases are decided, the verdicts replay through the\n"
        "aggregator's P1 / P3 logic with audit-derived classifications\n"
        "substituting for `DISAGREE` rows. The publication-ready findings\n"
        "block goes back into `analysis/aristotelian/v0_1_findings.md` along with this\n"
        "audit's deviation rationale, signed by author + external\n"
        "physics-trained reader.\n"
    )
    lines.append("---\n")

    case_counter = 0
    for stage in STAGE_ORDER:
        cases = cases_by_stage[stage]
        if not cases:
            continue
        lines.append(f"\n## {STAGE_TITLES[stage]} — {len(cases)} cases\n")

        for case in cases:
            case_counter += 1
            lines.append(
                f"\n### Case {case_counter}: `{case.model}` trial {case.trial_index}"
                f" — {STAGE_TITLES[stage]}\n"
            )
            lines.append(
                f"_Verdict split: Claude judge → `{case.claude_verdict}`, "
                f"OpenAI judge → `{case.openai_verdict}`_\n"
            )
            md_path = (
                f"results/{case.model}/{FRAMEWORK_ID}/{case.stage}/trial_{case.trial_index}_t0.0.md"
            )
            json_path = md_path[:-3] + ".json"
            formulation_md_path = (
                f"results/{case.model}/{FRAMEWORK_ID}/formulation/trial_{case.trial_index}_t0.0.md"
            )
            lines.append(
                f"**Trial:** [`{md_path}`](../{md_path}) "
                f"(human-readable; source-of-truth JSON: "
                f"[`{Path(json_path).name}`](../{json_path}))\n"
            )
            lines.append(
                f"**Same trial's Stage 2 (formulation) — cross-stage context:** "
                f"[`{Path(formulation_md_path).name}`](../{formulation_md_path})\n"
            )

            response, total_len = _load_trial_response(case.model, case.trial_index, case.stage)
            lines.append(f"\n**Tested-model response** ({total_len:,} chars total):\n")
            lines.append("```")
            lines.append(_truncate(response))
            lines.append("```")

            if stage == "meta":
                lines.append("\n**Stage 1-3 consensus inputs the meta-judges saw:**\n")
                lines.extend(
                    _stage1_3_consensus(
                        case.model, case.trial_index, all_verdicts_by_model[case.model]
                    )
                )

            lines.append("\n---\n")
            lines.extend(_render_judge_block("Claude judge", case.claude_parsed, case.stage))
            lines.append("")
            lines.extend(_render_judge_block("OpenAI judge", case.openai_parsed, case.stage))
            lines.extend(_decision_block(case.stage))
            lines.append("---\n")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines))
    print(f"Wrote {OUTPUT} — {case_counter} cases across {len(cases_by_stage)} stages.")
    parts = ", ".join(f"{STAGE_TITLES[s]}={len(cases_by_stage[s])}" for s in STAGE_ORDER)
    print(f"  cases per stage: {parts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
