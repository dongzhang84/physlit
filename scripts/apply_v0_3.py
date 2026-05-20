"""v0.3 — compute P1 / P2 and the treatment-vs-control comparison.

Reads the v0.3 treatment-arm dual-judge verdicts produced by
``judge_v0_3.py``, resolves any disagreement with the human-audit
override tables below (canonical, per ``prereg-v0.3-locked`` §1.4),
and computes:

- the treatment-arm content-axis and structural-axis pass counts;
- **P1** — three-tier verdict on the structural pass rate against the
  Aristotelian control's 8/15 (strongly confirmed ≥13, directionally
  confirmed 9-12, refuted ≤8);
- **P2** — whether the treatment content-axis pass rate degrades
  materially below the control's 5/15 (confirmed ≥4, refuted ≤3);
- the per-model treatment-vs-control comparison;
- a **cross-framework comparison** against `02_fmv.2` (the same
  axiomatisation instruction on F=mv).

Rewrites the "## v0.3 post-audit final results" block of
``analysis/v0_3_findings.md`` (idempotent). No API calls.

Before any human audit the override tables are empty; a DISAGREE with
no override is reported as PENDING and verdicts are marked preliminary.

Usage: uv run python scripts/apply_v0_3.py
"""

from __future__ import annotations

import glob
import json
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
TREATMENT_ID = "01_aristotelian_3"
FINDINGS = REPO / "analysis" / "v0_3_findings.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")

# Aristotelian control arm — v0.1 audit-resolved content + v0.2
# audit-resolved structural verdicts. Source:
# analysis/v0_1_findings.md + analysis/v0_2_findings.md.
CONTROL: dict[tuple[str, int], dict[str, str]] = {
    ("claude-opus-4-7", 0): {"content": "FAIL", "structural": "PASS"},
    ("claude-opus-4-7", 1): {"content": "PASS", "structural": "PASS"},
    ("claude-opus-4-7", 2): {"content": "FAIL", "structural": "PASS"},
    ("claude-opus-4-7", 3): {"content": "FAIL", "structural": "PASS"},
    ("claude-opus-4-7", 4): {"content": "FAIL", "structural": "PASS"},
    ("gpt-5.5-2026-04-23", 0): {"content": "PASS", "structural": "FAIL"},
    ("gpt-5.5-2026-04-23", 1): {"content": "FAIL", "structural": "FAIL"},
    ("gpt-5.5-2026-04-23", 2): {"content": "PASS", "structural": "FAIL"},
    ("gpt-5.5-2026-04-23", 3): {"content": "FAIL", "structural": "FAIL"},
    ("gpt-5.5-2026-04-23", 4): {"content": "PASS", "structural": "FAIL"},
    ("gemini-3.1-pro-preview", 0): {"content": "FAIL", "structural": "FAIL"},
    ("gemini-3.1-pro-preview", 1): {"content": "FAIL", "structural": "PASS"},
    ("gemini-3.1-pro-preview", 2): {"content": "PASS", "structural": "PASS"},
    ("gemini-3.1-pro-preview", 3): {"content": "FAIL", "structural": "FAIL"},
    ("gemini-3.1-pro-preview", 4): {"content": "FAIL", "structural": "PASS"},
}
CONTROL_CONTENT_PASS = sum(1 for v in CONTROL.values() if v["content"] == "PASS")  # 5
CONTROL_STRUCTURAL_PASS = sum(1 for v in CONTROL.values() if v["structural"] == "PASS")  # 8

# 02_fmv pair (control + 02_fmv.2 treatment), for the cross-framework
# row in the comparison table. Hardcoded from the post-audit final
# results of analysis/02_fmv_findings.md, 02_fmv_1_findings.md,
# 02_fmv_2_findings.md.
FMV_CONTROL_CONTENT_PASS = 9
FMV_CONTROL_STRUCTURAL_PASS = 5
FMV_CONTROL_COMPOSITE_PASS = 1
FMV_TREATMENT_CONTENT_PASS = 9
FMV_TREATMENT_STRUCTURAL_PASS = 11
FMV_TREATMENT_COMPOSITE_PASS = 6

# Human-audit overrides for v0.3 dual-judge disagreements (canonical,
# per prereg §1.4). Source: analysis/v0_3_audit_human_review.md.
HUMAN_CONTENT: dict[tuple[str, int, str], str] = {}
HUMAN_STRUCTURAL: dict[tuple[str, int], str] = {
    # S1 — gpt t1: Claude verdict-field self-contradiction
    # ("Correcting my verdict: this should be PASS") + OpenAI PASS.
    # 02_fmv.1 Case 6 precedent: follow the reasoning.
    ("gpt-5.5-2026-04-23", 1): "PASS",
    # S2 — gemini t3: OpenAI N10 FAIL is the Stage 1+2 double-count
    # bug (counted 4+4=8, called Stage 2 mirror "duplicate"). Under
    # the established Stage-1-only principle (the v0.2-criteria
    # defect that 02_fmv.1 fixed): 4 rules, N12 exempt, N10 PASS.
    ("gemini-3.1-pro-preview", 3): "PASS",
    # S3 — gemini t4: Claude verdict-field self-contradiction
    # ("Verdict should be PASS") on 3 rules (N12 exempt). Same
    # defect class as 02_fmv.1 Case 6 and v0.3 S1. OpenAI also PASS.
    ("gemini-3.1-pro-preview", 4): "PASS",
}


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


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


def _resolve(a: str | None, b: str | None, override: str | None) -> str:
    if a is None or b is None:
        return "MISSING"
    if a == b:
        return a
    return override if override in {"PASS", "FAIL"} else "PENDING"


def main() -> int:
    rows: list[dict[str, Any]] = []
    pending = 0
    for model in MODELS:
        cj = _load(model, "judgments")
        sj = _load(model, "structural")
        for t in range(5):
            stage_v: dict[str, str] = {}
            for stage in CONTENT_STAGES:
                a = cj.get((t, stage, "anthropic"))
                b = cj.get((t, stage, "openai"))
                stage_v[stage] = _resolve(
                    _verdict(a) if a is not None else None,
                    _verdict(b) if b is not None else None,
                    HUMAN_CONTENT.get((model, t, stage)),
                )
            if "PENDING" in stage_v.values() or "MISSING" in stage_v.values():
                content = "PENDING" if "PENDING" in stage_v.values() else "MISSING"
            elif all(v == "PASS" for v in stage_v.values()):
                content = "PASS"
            else:
                content = "FAIL"

            sa = sj.get((t, "structural", "anthropic"))
            sb = sj.get((t, "structural", "openai"))
            structural = _resolve(
                _verdict(sa) if sa is not None else None,
                _verdict(sb) if sb is not None else None,
                HUMAN_STRUCTURAL.get((model, t)),
            )
            if content in {"PENDING", "MISSING"} or structural in {"PENDING", "MISSING"}:
                pending += 1
            rows.append(
                {
                    "model": model,
                    "trial": t,
                    "s1": stage_v["induction"],
                    "s2": stage_v["formulation"],
                    "s3": stage_v["prediction"],
                    "content": content,
                    "structural": structural,
                }
            )

    t_content = sum(1 for r in rows if r["content"] == "PASS")
    t_structural = sum(1 for r in rows if r["structural"] == "PASS")
    for r in rows:
        r["composite"] = "PASS" if r["content"] == "PASS" and r["structural"] == "PASS" else "FAIL"
    t_composite = sum(1 for r in rows if r["composite"] == "PASS")
    c_composite = sum(
        1 for v in CONTROL.values() if v["content"] == "PASS" and v["structural"] == "PASS"
    )

    # P1 — three-tier on the structural pass rate, anchored on absolute
    # lift (control 8 → +5 = strongly).
    if t_structural >= 13:
        p1 = "STRONGLY CONFIRMED"
    elif t_structural >= 9:
        p1 = "DIRECTIONALLY CONFIRMED"
    else:
        p1 = "REFUTED"

    p2 = "CONFIRMED" if t_content >= 4 else "REFUTED"

    per_model: list[tuple[str, int, int, int, int, int, int]] = []
    for model in MODELS:
        mr = [r for r in rows if r["model"] == model]
        tc = sum(1 for r in mr if r["content"] == "PASS")
        tsg = sum(1 for r in mr if r["structural"] == "PASS")
        tcm = sum(1 for r in mr if r["composite"] == "PASS")
        cc = sum(1 for tt in range(5) if CONTROL[(model, tt)]["content"] == "PASS")
        cs = sum(1 for tt in range(5) if CONTROL[(model, tt)]["structural"] == "PASS")
        ccm = sum(
            1
            for tt in range(5)
            if CONTROL[(model, tt)]["content"] == "PASS"
            and CONTROL[(model, tt)]["structural"] == "PASS"
        )
        per_model.append((model, cc, tc, cs, tsg, ccm, tcm))

    # Judge / agent vs human (only meaningful once the audit is done).
    def _agent_records(model: str, subdir: str) -> list[dict[str, Any]]:
        return [
            json.loads(Path(p).read_text())
            for p in sorted(glob.glob(str(RESULTS / model / TREATMENT_ID / subdir / "*.json")))
        ]

    a1_agree = a1_total = 0
    cj_agree = oj_agree = c_total_units = 0
    for (model, t, stage), human_v in HUMAN_CONTENT.items():
        cj = _load(model, "judgments")
        a = _verdict(cj.get((t, stage, "anthropic")) or {})
        b = _verdict(cj.get((t, stage, "openai")) or {})
        c_total_units += 1
        if a == human_v:
            cj_agree += 1
        if b == human_v:
            oj_agree += 1
        for rec in _agent_records(model, "content_resolved"):
            if rec.get("trial_index") == t and rec.get("stage") == stage:
                if _verdict(rec.get("parsed_verdict") or {}) == human_v:
                    a1_agree += 1
                a1_total += 1
                break

    a2_agree = a2_total = 0
    cs_agree = os_agree = s_total_units = 0
    for (model, t), human_v in HUMAN_STRUCTURAL.items():
        sj = _load(model, "structural")
        a = _verdict(sj.get((t, "structural", "anthropic")) or {})
        b = _verdict(sj.get((t, "structural", "openai")) or {})
        s_total_units += 1
        if a == human_v:
            cs_agree += 1
        if b == human_v:
            os_agree += 1
        for rec in _agent_records(model, "structural_resolved"):
            if rec.get("trial_index") == t:
                if _verdict(rec.get("parsed_verdict") or {}) == human_v:
                    a2_agree += 1
                a2_total += 1
                break

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    o: list[str] = []
    o.append("\n## v0.3 post-audit final results\n")
    o.append(f"- Generated: `{ts}`\n")
    o.append("- Prereg lock: `prereg-v0.3-locked`\n")
    if pending:
        o.append(
            f"- **PRELIMINARY** — {pending} treatment trial(s) have an "
            f"unresolved dual-judge disagreement; fill the `HUMAN_CONTENT` / "
            f"`HUMAN_STRUCTURAL` tables in `apply_v0_3.py` after the audit "
            f"and re-run.\n"
        )
    o.append("\n### Treatment-arm per-trial matrix\n\n")
    o.append("| Model | Trial | S1 | S2 | S3 | Content-only | Structural | Composite |\n")
    o.append("|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        o.append(
            f"| `{r['model']}` | {r['trial']} | {r['s1']} | {r['s2']} | "
            f"{r['s3']} | {r['content']} | {r['structural']} | {r['composite']} |\n"
        )
    o.append("\n")

    o.append("### Treatment vs. control (Aristotelian)\n\n")
    o.append(
        "| Arm | Content-axis PASS | Structural-axis PASS | Composite PASS |\n|---|---|---|---|\n"
    )
    o.append(
        f"| Control (v0.1 / v0.2) | {CONTROL_CONTENT_PASS}/15 | "
        f"{CONTROL_STRUCTURAL_PASS}/15 | {c_composite}/15 |\n"
    )
    o.append(f"| Treatment (v0.3) | {t_content}/15 | {t_structural}/15 | {t_composite}/15 |\n\n")
    o.append("Per model (control → treatment):\n\n")
    o.append("| Model | Content | Structural | Composite |\n|---|---|---|---|\n")
    for model, cc, tc, cs, tsg, ccm, tcm in per_model:
        o.append(f"| `{model}` | {cc}/5 → {tc}/5 | {cs}/5 → {tsg}/5 | {ccm}/5 → {tcm}/5 |\n")
    o.append("\n")

    o.append("### Cross-framework comparison (same axiomatisation instruction)\n\n")
    o.append(
        "| Framework | Content (ctrl → treat) | Structural (ctrl → treat) | "
        "Composite (ctrl → treat) |\n|---|---|---|---|\n"
    )
    o.append(
        f"| Aristotelian (v0.1 → v0.3) | {CONTROL_CONTENT_PASS}/15 → {t_content}/15 | "
        f"{CONTROL_STRUCTURAL_PASS}/15 → {t_structural}/15 | "
        f"{c_composite}/15 → {t_composite}/15 |\n"
    )
    o.append(
        f"| F=mv (02_fmv → 02_fmv.2) | {FMV_CONTROL_CONTENT_PASS}/15 → "
        f"{FMV_TREATMENT_CONTENT_PASS}/15 | "
        f"{FMV_CONTROL_STRUCTURAL_PASS}/15 → {FMV_TREATMENT_STRUCTURAL_PASS}/15 | "
        f"{FMV_CONTROL_COMPOSITE_PASS}/15 → {FMV_TREATMENT_COMPOSITE_PASS}/15 |\n\n"
    )

    o.append(f"### P1 — Axiomatisation raises the structural pass rate  ·  **{p1}**\n")
    o.append(
        f"Treatment structural-axis PASS **{t_structural}/15** vs control "
        f"**{CONTROL_STRUCTURAL_PASS}/15**. Bands (prereg §2): strongly "
        f"confirmed ≥13 (+5 absolute), directionally confirmed 9-12, "
        f"refuted ≤8. Per-model and per-criterion breakdown is the primary "
        f"reading in the directional band.\n\n"
    )
    o.append(f"### P2 — Content competence does not degrade  ·  **{p2}**\n")
    o.append(
        f"Treatment content-axis PASS **{t_content}/15** vs control "
        f"**{CONTROL_CONTENT_PASS}/15**. Confirmed ≥4 (within one trial of "
        f"control — no material degradation); refuted ≤3.\n"
    )
    if p2 == "REFUTED":
        o.append(
            "- Content degraded: the P1 structural comparison is reported as "
            "potentially confounded by content loss.\n"
        )
    o.append("\n")

    if c_total_units:
        o.append("### LLM judge vs the human audit (per axis)\n\n")
        o.append("| Axis | Cases | Claude judge | OpenAI judge |\n|---|---|---|---|\n")
        o.append(
            f"| Content | {c_total_units} | {cj_agree}/{c_total_units} "
            f"({cj_agree / c_total_units:.0%}) | {oj_agree}/{c_total_units} "
            f"({oj_agree / c_total_units:.0%}) |\n"
        )
        if s_total_units:
            o.append(
                f"| Structural | {s_total_units} | {cs_agree}/{s_total_units} "
                f"({cs_agree / s_total_units:.0%}) | {os_agree}/{s_total_units} "
                f"({os_agree / s_total_units:.0%}) |\n"
            )
        o.append("\n")

    if a1_total or a2_total:
        o.append("### Agent 1 / Agent 2 vs the human audit\n\n")
        if a1_total:
            o.append(
                f"- Agent 1 (content resolver): **{a1_agree}/{a1_total}** "
                f"({a1_agree / a1_total:.0%}).\n"
            )
        if a2_total:
            o.append(
                f"- Agent 2 (structural resolver): **{a2_agree}/{a2_total}** "
                f"({a2_agree / a2_total:.0%}).\n"
            )
        o.append("\n")

    marker = "\n## v0.3 post-audit final results\n"
    FINDINGS.parent.mkdir(parents=True, exist_ok=True)
    existing = FINDINGS.read_text() if FINDINGS.exists() else "# PhysLit v0.3 — Findings\n"
    head = existing.split(marker)[0].rstrip()
    FINDINGS.write_text(head + "\n" + "".join(o))

    print(f"P1 {p1} (structural {t_structural}/15 vs control {CONTROL_STRUCTURAL_PASS}/15)")
    print(f"P2 {p2} (content {t_content}/15 vs control {CONTROL_CONTENT_PASS}/15)")
    print(f"Composite: {t_composite}/15 vs control {c_composite}/15")
    if pending:
        print(f"PRELIMINARY — {pending} trial(s) await human audit")
    print(f"Block written to {FINDINGS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
