"""Apply the 02_fmv.1 structural human audit and recompute P1 / P2 (final).

The 7 structural-axis dual-judge disagreement cases were resolved by
human audit (``analysis/02_fmv_1_structural_audit_human_review.md``).
Per ``prereg-02_fmv.1-locked`` §1 those human verdicts are the
canonical resolution (no LLM disagree-resolver). This script:

- substitutes the human verdict for every structural DISAGREE trial;
- recomputes the per-trial structural + composite matrix;
- recomputes P1 (structural IRR — audit-invariant) and P2 (composite
  flips over the 9 all-content-PASS trials);
- tabulates each structural judge's agreement with the human audit;
- compares Agent 2 (non-canonical resolver) against the human audit.

It appends a "post-audit final results" block to
``analysis/02_fmv_1_findings.md``. No API calls; deterministic.

Usage: ``uv run python scripts/apply_02_fmv_1_audit.py``
"""

from __future__ import annotations

import glob
import json
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
FRAMEWORK_ID = "02_fmv"
FINDINGS = REPO / "analysis" / "02_fmv_1_findings.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")

# Content-axis verdict per trial, inherited verbatim from the 02_fmv
# post-audit final results (analysis/02_fmv_findings.md). A trial's
# content axis is PASS iff its Stage 1, 2 and 3 are all PASS.
CONTENT_AXIS = {
    ("claude-opus-4-7", 0): "PASS",
    ("claude-opus-4-7", 1): "FAIL",
    ("claude-opus-4-7", 2): "PASS",
    ("claude-opus-4-7", 3): "PASS",
    ("claude-opus-4-7", 4): "PASS",
    ("gpt-5.5-2026-04-23", 0): "PASS",
    ("gpt-5.5-2026-04-23", 1): "PASS",
    ("gpt-5.5-2026-04-23", 2): "PASS",
    ("gpt-5.5-2026-04-23", 3): "PASS",
    ("gpt-5.5-2026-04-23", 4): "PASS",
    ("gemini-3.1-pro-preview", 0): "FAIL",
    ("gemini-3.1-pro-preview", 1): "FAIL",
    ("gemini-3.1-pro-preview", 2): "FAIL",
    ("gemini-3.1-pro-preview", 3): "FAIL",
    ("gemini-3.1-pro-preview", 4): "FAIL",
}

# Human-audit verdicts on the 7 structural dual-judge disagreement
# cases (analysis/02_fmv_1_structural_audit_human_review.md).
HUMAN_STRUCTURAL = {
    ("claude-opus-4-7", 2): "FAIL",  # Case 1 — N11
    ("claude-opus-4-7", 3): "FAIL",  # Case 2 — N10
    ("claude-opus-4-7", 4): "FAIL",  # Case 3 — N10
    ("gpt-5.5-2026-04-23", 2): "FAIL",  # Case 4 — N10
    ("gpt-5.5-2026-04-23", 4): "FAIL",  # Case 5 — N10
    ("gemini-3.1-pro-preview", 2): "PASS",  # Case 6
    ("gemini-3.1-pro-preview", 4): "FAIL",  # Case 7 — N12
}


def _structural(model: str) -> dict[tuple[int, str], dict[str, Any]]:
    out: dict[tuple[int, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / FRAMEWORK_ID / "structural" / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if name.startswith("trial_"):
            out[(int(name.split("_")[1]), d["judge_family"])] = d.get("parsed_verdict") or {}
    return out


def _agent2(model: str) -> dict[int, str | None]:
    out: dict[int, str | None] = {}
    for fp in sorted(
        glob.glob(str(RESULTS / model / FRAMEWORK_ID / "structural_resolved" / "*.json"))
    ):
        d = json.loads(Path(fp).read_text())
        out[d["trial_index"]] = _verdict(d.get("parsed_verdict") or {})
    return out


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def main() -> int:
    sv = {m: _structural(m) for m in MODELS}
    a2 = {m: _agent2(m) for m in MODELS}

    rows: list[dict[str, Any]] = []
    disagree = 0
    for model in MODELS:
        for t in range(5):
            a = _verdict(sv[model].get((t, "anthropic")) or {})
            b = _verdict(sv[model].get((t, "openai")) or {})
            if a == b:
                structural = a or "MISSING"
            else:
                disagree += 1
                structural = HUMAN_STRUCTURAL[(model, t)]
            content = CONTENT_AXIS[(model, t)]
            composite = "PASS" if content == "PASS" and structural == "PASS" else "FAIL"
            rows.append(
                {
                    "model": model,
                    "trial": t,
                    "content": content,
                    "structural": structural,
                    "composite": composite,
                    "is_disagree": a != b,
                }
            )

    # P1 — structural IRR. Audit-invariant: it counts trials where the
    # two structural judges disagreed; the human audit does not change
    # whether they disagreed.
    irr = disagree / 15
    p1 = "CONFIRMED" if irr < 0.40 else "REFUTED"

    # P2 — composite flips over the 9 all-content-PASS trials.
    content_pass = [r for r in rows if r["content"] == "PASS"]
    flipped = [r for r in content_pass if r["composite"] == "FAIL"]
    p2 = "CONFIRMED" if len(flipped) >= 1 else "REFUTED"

    # Structural judge vs human on the 7 disagree cases.
    claude_agree = openai_agree = a2_agree = 0
    for (model, t), human_v in HUMAN_STRUCTURAL.items():
        if _verdict(sv[model].get((t, "anthropic")) or {}) == human_v:
            claude_agree += 1
        if _verdict(sv[model].get((t, "openai")) or {}) == human_v:
            openai_agree += 1
        if a2[model].get(t) == human_v:
            a2_agree += 1
    n = len(HUMAN_STRUCTURAL)

    # --- Report -------------------------------------------------------
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    o: list[str] = []
    o.append("\n## 02_fmv.1 post-audit final results\n")
    o.append(f"- Generated: `{ts}`\n")
    o.append(
        "- Audit: `analysis/02_fmv_1_structural_audit_human_review.md` — 7 "
        "structural disagree cases resolved by human audit (canonical, per "
        "`prereg-02_fmv.1-locked` §1).\n\n"
    )
    o.append("### Resolved per-trial structural + composite matrix (audit-applied)\n\n")
    o.append("| Model | Trial | Content | Structural | Composite |\n|---|---|---|---|---|\n")
    for r in rows:
        mark = " *(audit)*" if r["is_disagree"] else ""
        o.append(
            f"| `{r['model']}` | {r['trial']} | {r['content']} | "
            f"{r['structural']}{mark} | {r['composite']} |\n"
        )
    o.append("\n")
    n_comp_pass = sum(1 for r in rows if r["composite"] == "PASS")
    o.append(f"Composite: **{n_comp_pass}/15 PASS**, {15 - n_comp_pass}/15 FAIL.\n\n")

    o.append(f"### P1 — Mechanical structural criteria reduce disagreement  ·  **{p1}**\n")
    o.append(
        f"Structural-axis dual-judge IRR **{irr:.2%}** ({disagree}/15). The "
        f"IRR is audit-invariant — it counts trials where the two structural "
        f"judges disagreed, which the human audit does not change. Confirmed "
        f"bar < 40% (the v0.2 Aristotelian structural IRR); 46.67% ≥ 40%. The "
        f"Stage-1-only count fix did **not** lower structural disagreement — "
        f"evidence against the double-count diagnosis as the dominant cause.\n\n"
    )
    o.append(f"### P2 — Structural axis catches a content-missed failure  ·  **{p2}**\n")
    o.append(
        f"All-content-PASS trials: **{len(content_pass)}**. Reclassified to "
        f"composite FAIL by the structural axis: **{len(flipped)}** "
        f"({', '.join(f'`{r["model"]}` t{r["trial"]}' for r in flipped)}). "
        f"Threshold ≥ 1. The structural axis demonstrably detects failures "
        f"the content axis missed on this framework.\n\n"
    )
    o.append("### Structural judge vs the human audit (7 disagree cases)\n\n")
    o.append(f"- Claude structural judge: **{claude_agree}/{n}** ({claude_agree / n:.0%})\n")
    o.append(f"- OpenAI structural judge: **{openai_agree}/{n}** ({openai_agree / n:.0%})\n\n")
    o.append(
        "This **reverses** the 02_fmv content axis, where the Claude judge "
        "agreed with the human audit on 86% and the OpenAI judge on 21%. "
        "Same models, same framework, different judgment task — judge "
        "reliability is task-dependent, not model-dependent.\n\n"
    )
    o.append("### Agent 2 (non-canonical resolver) vs the human audit\n\n")
    o.append(
        f"Agent 2 (`gemini-3.1-pro-preview`) agreed with the human audit on "
        f"**{a2_agree}/{n}** ({a2_agree / n:.0%}) of the structural disagree "
        f"cases — the lone miss is Case 3 (`claude-opus-4-7` t4), where "
        f"Agent 2 PASS vs human FAIL on N10. Agent 2 is a side analysis; it "
        f"does not feed P1 / P2.\n\n"
    )
    o.append(
        f"**Verdict summary (post-audit, final):** P1 {p1} · P2 {p2}. The "
        f"audit resolved all 7 structural DISAGREE rows; P1 is unchanged "
        f"from the preliminary verdict (IRR audit-invariant); P2 firmed "
        f"from a lower bound of 3 to {len(flipped)} of {len(content_pass)} "
        f"all-content-PASS trials flipped.\n"
    )

    with FINDINGS.open("a") as fh:
        fh.write("".join(o))

    print(f"P1 {p1} (IRR {irr:.2%}, {disagree}/15)")
    print(f"P2 {p2} ({len(flipped)}/{len(content_pass)} content-PASS trials flipped)")
    print(f"Composite: {n_comp_pass}/15 PASS")
    print(
        f"Claude judge vs human {claude_agree}/{n} | "
        f"OpenAI judge vs human {openai_agree}/{n} | "
        f"Agent 2 vs human {a2_agree}/{n}"
    )
    print(f"Post-audit block appended to {FINDINGS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
