"""Apply the 03_decay human audit and recompute P1-P4 (post-audit, final).

The 54 dual-judge disagreement cases (18 content stage-verdict + 32
Stage 3 per-scenario + 4 meta over-claim) were resolved by human audit
(``analysis/decay/03_decay_audit_human_review.md``). Per
``prereg-03_decay-locked`` §1.4 those human verdicts are the canonical
resolution. This script loads the dual-judge verdicts, substitutes the
human verdict for every DISAGREE row, recomputes P1 / P2 / P3 / P4, and
additionally:

- aggregates the post-audit Stage 1 first-FAIL clause distribution
  (the §6 mechanical halt-at-first-FAIL procedure: §3 banned tokens →
  §4 N1-N6 → §5 P1-P7 → §6.3 coverage) for the P2 verdict;
- tabulates each LLM judge's and the non-canonical Agent 1 / Agent 2
  resolvers' agreement with the human audit.

It rewrites the "## 03_decay post-audit final results" block of
``analysis/decay/03_decay_findings.md`` (idempotent). No API calls.

Usage: ``uv run python scripts/apply_03_decay.py``
"""

from __future__ import annotations

import glob
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "results"
FRAMEWORK_ID = "03_decay"
FINDINGS = REPO / "analysis" / "decay" / "03_decay_findings.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")

# --- Human-audit overrides (canonical, per prereg §1.4) --------------
# Source: analysis/decay/03_decay_audit_human_review.md.

# Part A — 18 stage-level content cases. C{n} ↔ A1-{n}.
HUMAN_CONTENT: dict[tuple[str, int, str], str] = {
    # C1 — claude t0 S2 (formulation): OpenAI misclassified "pulled" as force.
    ("claude-opus-4-7", 0, "formulation"): "PASS",
    # C2 — claude t2 S2: OpenAI misclassified "preserved" as conservation.
    ("claude-opus-4-7", 2, "formulation"): "PASS",
    # C3 — claude t3 S2: same "preserved" misclassification.
    ("claude-opus-4-7", 3, "formulation"): "PASS",
    # C4 — claude t0 S1: OpenAI hallucinated "resistance" (not in response).
    ("claude-opus-4-7", 0, "induction"): "PASS",
    # C5 — claude t1 S1: OpenAI hallucinated "deceleration".
    ("claude-opus-4-7", 1, "induction"): "PASS",
    # C6 — claude t2 S1: OpenAI hallucinated "resistance".
    ("claude-opus-4-7", 2, "induction"): "PASS",
    # C7 — claude t4 S1: OpenAI misclassified "fired" as form of force.
    ("claude-opus-4-7", 4, "induction"): "PASS",
    # C8 — gpt t0 S2: P2 — orbital radius treated as a "derived observed
    # outcome" and sideways speed used as the underlying decaying quantity.
    ("gpt-5.5-2026-04-23", 0, "formulation"): "FAIL",
    # C9 — gpt t1 S2: N4 — different τ values per system, no universal
    # constant declared.
    ("gpt-5.5-2026-04-23", 1, "formulation"): "FAIL",
    # C10 — gpt t2 S2: unified e^{-t/100}, orbital handled causally without
    # treating radius as a downstream quantity.
    ("gpt-5.5-2026-04-23", 2, "formulation"): "PASS",
    # C11 — gpt t0 S1: OpenAI misclassified "influences" as force.
    ("gpt-5.5-2026-04-23", 0, "induction"): "PASS",
    # C12 — gpt t2 S1: OpenAI cited "radiation" (not in §3 banned list).
    ("gpt-5.5-2026-04-23", 2, "induction"): "PASS",
    # C13 — gemini t0 S2: P2 — scope does not include radius; speed is
    # used as the underlying decaying quantity.
    ("gemini-3.1-pro-preview", 0, "formulation"): "FAIL",
    # C14 — gemini t1 S2: P2 — same pattern, sideways speed → radius.
    ("gemini-3.1-pro-preview", 1, "formulation"): "FAIL",
    # C15 — gemini t0 S1: response truncated but Rule 2 body complete; the
    # six N1-N6 necessary conditions are all stated.
    ("gemini-3.1-pro-preview", 0, "induction"): "PASS",
    # C16 — gemini t1 S1: P2 — scope does not include radius; sideways
    # speed is the underlying decaying quantity (the canonical §5 hit).
    ("gemini-3.1-pro-preview", 1, "induction"): "FAIL",
    # C17 — gemini t2 S1: truncation; obs 8 coverage incomplete.
    ("gemini-3.1-pro-preview", 2, "induction"): "FAIL",
    # C18 — gemini t4 S3 (prediction): all 5 scenarios within PASS ranges;
    # Scenario 4 (orbital radius) correctly applies the decay rule.
    ("gemini-3.1-pro-preview", 4, "prediction"): "PASS",
}

# Part B — 32 Stage 3 per-scenario cases. B{n} ↔ A2-{n}.
# Value is (verdict, direction). Direction is "correct", "wrong", or "n/a"
# (decline-to-commit). Per prereg P3, decline-to-commit goes to ratio-leaked.
HUMAN_SCENARIO: dict[tuple[str, int, int], tuple[str, str]] = {
    # B1-B3 — claude t0 scenarios 1/2/3: §3 "forced" appears in
    # Scenario 4 and pollutes the entire response → FAIL on all three.
    ("claude-opus-4-7", 0, 1): ("FAIL", "correct"),
    ("claude-opus-4-7", 0, 2): ("FAIL", "correct"),
    ("claude-opus-4-7", 0, 3): ("FAIL", "correct"),
    # B4-B6 — claude t1 scenarios 1/2/3: all decay-correct.
    ("claude-opus-4-7", 1, 1): ("PASS", "correct"),
    ("claude-opus-4-7", 1, 2): ("PASS", "correct"),
    ("claude-opus-4-7", 1, 3): ("PASS", "correct"),
    # B7-B9 — claude t3 scenarios 1/2/3: all decay-correct.
    ("claude-opus-4-7", 3, 1): ("PASS", "correct"),
    ("claude-opus-4-7", 3, 2): ("PASS", "correct"),
    ("claude-opus-4-7", 3, 3): ("PASS", "correct"),
    # B10-B12 — claude t4 scenarios 1/2/3: all decay-correct.
    ("claude-opus-4-7", 4, 1): ("PASS", "correct"),
    ("claude-opus-4-7", 4, 2): ("PASS", "correct"),
    ("claude-opus-4-7", 4, 3): ("PASS", "correct"),
    # B13-B14 — gpt t2 scenarios 1/3: decay-correct.
    ("gpt-5.5-2026-04-23", 2, 1): ("PASS", "correct"),
    ("gpt-5.5-2026-04-23", 2, 3): ("PASS", "correct"),
    # B15 — gpt t3 s1: decline-to-commit (scope issue) → ratio-leaked.
    ("gpt-5.5-2026-04-23", 3, 1): ("FAIL", "correct"),
    # B16 — gpt t4 s1: decline-to-commit (no r_pendulum value).
    ("gpt-5.5-2026-04-23", 4, 1): ("FAIL", "correct"),
    # B17 — gemini t0 s1: decay-correct.
    ("gemini-3.1-pro-preview", 0, 1): ("PASS", "correct"),
    # B18 — gemini t0 s4: orbital outside scope → decline-to-commit.
    ("gemini-3.1-pro-preview", 0, 4): ("FAIL", "correct"),
    # B19-B21 — gemini t1 scenarios 1/2/3: decay-correct.
    ("gemini-3.1-pro-preview", 1, 1): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 1, 2): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 1, 3): ("PASS", "correct"),
    # B22-B24 — gemini t2 scenarios 1/2/3: decay-correct.
    ("gemini-3.1-pro-preview", 2, 1): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 2, 2): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 2, 3): ("PASS", "correct"),
    # B25 — gemini t3 s1: decline-to-commit (scope issue), bucket = ratio-leaked.
    ("gemini-3.1-pro-preview", 3, 1): ("FAIL", "n/a"),
    # B26-B27 — gemini t3 scenarios 2/3: decay-correct.
    ("gemini-3.1-pro-preview", 3, 2): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 3, 3): ("PASS", "correct"),
    # B28 — gemini t3 s4: orbital outside scope → decline-to-commit.
    ("gemini-3.1-pro-preview", 3, 4): ("FAIL", "correct"),
    # B29-B32 — gemini t4 scenarios 1/2/3/4: all decay-correct.
    ("gemini-3.1-pro-preview", 4, 1): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 4, 2): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 4, 3): ("PASS", "correct"),
    ("gemini-3.1-pro-preview", 4, 4): ("PASS", "correct"),
}

# Part C — 4 Stage 4 over-claim cases. M{n}.
HUMAN_META: dict[tuple[str, int], str] = {
    # M1 — claude t0: Stage 3 FAIL but Q5 says "minor".
    ("claude-opus-4-7", 0): "yes",
    # M2 — claude t3: Stage 1+3 FAIL but Q5 says "minor".
    ("claude-opus-4-7", 3): "yes",
    # M3 — gpt t0: Stage 2 P2 FAIL + Stage 3 FAIL; did not identify P2.
    ("gpt-5.5-2026-04-23", 0): "yes",
    # M4 — gpt t4: Stage 1+2+3 all FAIL (N4); did not identify N4.
    ("gpt-5.5-2026-04-23", 4): "yes",
}

# Post-audit Stage 1 first-FAIL clause (per §6 halt-at-first-FAIL).
# Audit-overridden Stage 1 FAILs: clause comes from the audit reason.
# Consensus Stage 1 FAILs: Claude judge clause is canonical (per the
# audit, the OpenAI judge fabricated/misclassified §3 banned tokens in
# nearly every Stage 1 disagreement — its §3 citations are not
# evidence on the consensus FAILs either).
STAGE1_FIRST_FAIL: dict[tuple[str, int], str] = {
    # Six consensus FAIL trials (both judges FAIL pre-audit) — Claude judge clause:
    ("claude-opus-4-7", 3): "N4",
    ("gpt-5.5-2026-04-23", 1): "N4",
    ("gpt-5.5-2026-04-23", 3): "N4",
    ("gpt-5.5-2026-04-23", 4): "N4",
    ("gemini-3.1-pro-preview", 3): "N6",
    ("gemini-3.1-pro-preview", 4): "coverage",
    # Two audit-resolved Stage 1 FAILs:
    ("gemini-3.1-pro-preview", 1): "§5 P2",  # C16
    ("gemini-3.1-pro-preview", 2): "coverage",  # C17 (truncation, obs 8 incomplete)
}


# --- Loaders ----------------------------------------------------------
def _judgments(model: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / FRAMEWORK_ID / "judgments" / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if name.startswith("trial_"):
            out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
                d.get("parsed_verdict") or {}
            )
    return out


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


def _agent1() -> dict[tuple[str, int, str], str]:
    out: dict[tuple[str, int, str], str] = {}
    for model in MODELS:
        d = RESULTS / model / FRAMEWORK_ID / "content_resolved"
        for fp in sorted(glob.glob(str(d / "*.json"))):
            r = json.loads(Path(fp).read_text())
            v = _verdict(r.get("parsed_verdict") or {})
            if v:
                out[(model, r["trial_index"], r["stage"])] = v
    return out


def _agent2() -> dict[tuple[str, int, int], tuple[str, str]]:
    out: dict[tuple[str, int, int], tuple[str, str]] = {}
    for model in MODELS:
        d = RESULTS / model / FRAMEWORK_ID / "scenario_resolved"
        for fp in sorted(glob.glob(str(d / "*.json"))):
            r = json.loads(Path(fp).read_text())
            pv = r.get("parsed_verdict") or {}
            v = _verdict(pv)
            direction = pv.get("direction") or "-"
            if v:
                out[(model, r["trial_index"], r["scenario_index"])] = (v, direction)
    return out


def _bucket(verdict: str, direction: str) -> str:
    if verdict == "PASS":
        return "decay-correct"
    if direction == "wrong":
        return "direction-wrong"
    return "ratio-leaked"


def main() -> int:
    j = {m: _judgments(m) for m in MODELS}

    rows: list[dict[str, Any]] = []
    s13_disagree = s13_total = 0
    scenario_pre_audit: Counter[str] = Counter()
    scenario_audit: Counter[str] = Counter()

    for model in MODELS:
        for t in range(5):
            row: dict[str, Any] = {"model": model, "trial": t, "scenarios": {}}
            # Stages 1-3 overall content verdict.
            for stage in CONTENT_STAGES:
                a = _verdict(j[model].get((t, stage, "anthropic")) or {})
                b = _verdict(j[model].get((t, stage, "openai")) or {})
                s13_total += 1
                if a is not None and b is not None and a == b:
                    row[stage] = a
                elif a is None or b is None:
                    row[stage] = "MISSING"
                else:
                    s13_disagree += 1
                    row[stage] = HUMAN_CONTENT[(model, t, stage)]
            # Stage 3 per-scenario buckets across scenarios 1..4.
            pa = j[model].get((t, "prediction", "anthropic")) or {}
            pb = j[model].get((t, "prediction", "openai")) or {}
            for sidx in (1, 2, 3, 4):
                sa = _scenario_block(pa, sidx)
                sb = _scenario_block(pb, sidx)
                va = _verdict(sa)
                vb = _verdict(sb)
                da = sa.get("direction")
                db = sb.get("direction")
                key = (model, t, sidx)
                if key in HUMAN_SCENARIO:
                    v, d = HUMAN_SCENARIO[key]
                    bucket = _bucket(v, d)
                    row["scenarios"][sidx] = (v, d, "audit")
                    scenario_audit[bucket] += 1
                elif va is None or vb is None:
                    row["scenarios"][sidx] = (None, None, "missing")
                elif va == vb and (va == "PASS" or da == db):
                    if va == "PASS":
                        bucket = "decay-correct"
                    else:
                        bucket = "direction-wrong" if da == "wrong" else "ratio-leaked"
                    row["scenarios"][sidx] = (va, da, "consensus")
                    scenario_pre_audit[bucket] += 1
                else:
                    # should be covered by HUMAN_SCENARIO; mark for safety
                    row["scenarios"][sidx] = (None, None, "unresolved")
            # Stage 4 over-claim.
            ma = str((j[model].get((t, "meta", "anthropic")) or {}).get("over_claim") or "").lower()
            mb = str((j[model].get((t, "meta", "openai")) or {}).get("over_claim") or "").lower()
            if ma == mb and ma in {"yes", "no", "vacuous"}:
                row["overclaim"] = ma
            else:
                row["overclaim"] = HUMAN_META.get((model, t), "pending")
            rows.append(row)

    # Composite content axis (S1 PASS AND S2 PASS AND all 4 scenarios PASS).
    for r in rows:
        scenarios_all_pass = all(r["scenarios"].get(s, (None,))[0] == "PASS" for s in (1, 2, 3, 4))
        r["composite"] = (
            "PASS"
            if r["induction"] == "PASS" and r["formulation"] == "PASS" and scenarios_all_pass
            else "FAIL"
        )

    # --- P1 ----------------------------------------------------------
    composite_pass = sum(1 for r in rows if r["composite"] == "PASS")
    p1 = "CONFIRMED" if composite_pass < 5 else "REFUTED"

    # --- P2 — §5-pattern first-FAIL distribution ---------------------
    p5_counter: Counter[str] = Counter()
    for (model, t), clause in STAGE1_FIRST_FAIL.items():
        if rows[MODELS.index(model) * 5 + t]["induction"] != "FAIL":
            continue
        if clause.startswith("§5"):
            # "§5 P2" → "P2"; "§5 P1" → "P1" etc.
            p5_counter[clause.split(" ", 1)[1]] += 1
    p2_count = p5_counter.get("P2", 0)
    other_p5_max = max(
        (c for k, c in p5_counter.items() if k != "P2"),
        default=0,
    )
    total_p5_fails = sum(p5_counter.values())
    if total_p5_fails == 0:
        p2 = "VACUOUS"
    elif p2_count > other_p5_max:
        p2 = "CONFIRMED"
    else:
        p2 = "REFUTED"

    # --- P3 — quantitative bucket comparison -------------------------
    total_buckets = scenario_pre_audit + scenario_audit
    decay_correct = total_buckets["decay-correct"]
    ratio_leaked = total_buckets["ratio-leaked"]
    direction_wrong = total_buckets["direction-wrong"]
    if decay_correct == 60:
        p3 = "VACUOUS"
    elif ratio_leaked > direction_wrong:
        p3 = "CONFIRMED"
    else:
        p3 = "REFUTED"

    # --- P4 — meta over-claim distribution among failure trials -----
    failure_trials = [
        r for r in rows if "FAIL" in (r["induction"], r["formulation"], r["prediction"])
    ]
    oc_yes = sum(1 for r in failure_trials if r["overclaim"] == "yes")
    oc_no = sum(1 for r in failure_trials if r["overclaim"] == "no")
    if len(failure_trials) == 0:
        p4 = "VACUOUS"
    elif oc_yes > oc_no:
        p4 = "CONFIRMED"
    else:
        p4 = "REFUTED"

    # --- Agent / judge agreement -------------------------------------
    a1 = _agent1()
    a1_agree = a1_total = 0
    for (model, t, stage), human_v in HUMAN_CONTENT.items():
        av = a1.get((model, t, stage))
        if av is None:
            continue
        a1_total += 1
        if av == human_v:
            a1_agree += 1

    a2 = _agent2()
    a2_agree = a2_total = 0
    for (model, t, sidx), (human_v, human_d) in HUMAN_SCENARIO.items():
        av2 = a2.get((model, t, sidx))
        if av2 is None:
            continue
        a2_total += 1
        if av2[0] == human_v and (human_v == "PASS" or av2[1] == human_d):
            a2_agree += 1

    cj_agree = oj_agree = 0
    content_units = 0
    for (model, t, stage), human_v in HUMAN_CONTENT.items():
        content_units += 1
        if _verdict(j[model].get((t, stage, "anthropic")) or {}) == human_v:
            cj_agree += 1
        if _verdict(j[model].get((t, stage, "openai")) or {}) == human_v:
            oj_agree += 1

    cjs_agree = ojs_agree = 0
    scenario_units = 0
    for (model, t, sidx), (human_v, human_d) in HUMAN_SCENARIO.items():
        pa = j[model].get((t, "prediction", "anthropic")) or {}
        pb = j[model].get((t, "prediction", "openai")) or {}
        sa = _scenario_block(pa, sidx)
        sb = _scenario_block(pb, sidx)
        va = _verdict(sa)
        vb = _verdict(sb)
        da = sa.get("direction")
        db = sb.get("direction")
        scenario_units += 1
        if va == human_v and (human_v == "PASS" or da == human_d):
            cjs_agree += 1
        if vb == human_v and (human_v == "PASS" or db == human_d):
            ojs_agree += 1

    cjm_agree = ojm_agree = 0
    meta_units = 0
    for (model, t), human_v in HUMAN_META.items():
        ma = str((j[model].get((t, "meta", "anthropic")) or {}).get("over_claim") or "").lower()
        mb = str((j[model].get((t, "meta", "openai")) or {}).get("over_claim") or "").lower()
        meta_units += 1
        if ma == human_v:
            cjm_agree += 1
        if mb == human_v:
            ojm_agree += 1

    # --- Report -------------------------------------------------------
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    o: list[str] = []
    o.append("\n## 03_decay post-audit final results\n")
    o.append(f"- Generated: `{ts}`\n")
    o.append(
        "- Audit: `analysis/decay/03_decay_audit_human_review.md` — "
        "54 cases resolved by human audit (18 content + 32 per-scenario + "
        "4 meta), canonical per prereg §1.4.\n\n"
    )

    o.append("### Resolved per-trial matrix (audit-applied)\n\n")
    o.append("| Model | Trial | S1 | S2 | S3 | s1 | s2 | s3 | s4 | Over-claim | Composite |\n")
    o.append("|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        sc_cells = []
        for sidx in (1, 2, 3, 4):
            v, _d, src = r["scenarios"].get(sidx, (None, None, "missing"))
            tag = {"consensus": "c", "audit": "a", "missing": "?", "unresolved": "u"}[src]
            sc_cells.append(f"{v or '-'} ({tag})")
        o.append(
            f"| `{r['model']}` | {r['trial']} | {r['induction']} | "
            f"{r['formulation']} | {r['prediction']} | "
            f"{sc_cells[0]} | {sc_cells[1]} | {sc_cells[2]} | {sc_cells[3]} | "
            f"{r['overclaim']} | {r['composite']} |\n"
        )
    o.append("\nSource tags: `(c)` = pre-audit judge consensus; `(a)` = audit-resolved.\n\n")

    o.append(f"### P1 — Decay harder than both priors  ·  **{p1}**\n")
    o.append(
        f"Composite content PASS: **{composite_pass}/15**. Confirmed iff "
        f"< 5; refuted iff ≥ 5. Baselines: F=mv 9/15 (`02_fmv` post-audit), "
        f"Aristotelian 5/15 (v0.1 post-audit). The Decay World composite "
        f"pass count is the lowest of the three frameworks.\n\n"
    )

    o.append(f"### P2 — Hidden-substrate framing is the modal §5 pattern  ·  **{p2}**\n")
    o.append(
        f"Stage 1 post-audit first-FAIL clauses ({len([r for r in rows if r['induction'] == 'FAIL'])} FAILs across 15 trials):\n\n"
    )
    fail_clause_counter: Counter[str] = Counter()
    for r in rows:
        if r["induction"] == "FAIL":
            fail_clause_counter[STAGE1_FIRST_FAIL[(r["model"], r["trial"])]] += 1
    o.append("| First-FAIL clause | Count |\n|---|---|\n")
    for clause, n in fail_clause_counter.most_common():
        o.append(f"| {clause} | {n} |\n")
    o.append(
        f"\nOf the {sum(fail_clause_counter.values())} Stage 1 FAILs, "
        f"§5-pattern hits = **{total_p5_fails}** "
        f"(P2 = {p2_count}, all others = {other_p5_max}). "
        f"Per the prereg P2 is confirmed iff P2's count is strictly greater "
        f"than each of P1, P3, P4, P5, P6, P7's counts.\n\n"
    )

    o.append(f"### P3 — Ratio-leaked > direction-wrong (60 quant predictions)  ·  **{p3}**\n")
    o.append("| Bucket | Pre-audit consensus | Audit-resolved | **Total** |\n|---|---|---|---|\n")
    for bucket in ("decay-correct", "ratio-leaked", "direction-wrong"):
        o.append(
            f"| {bucket} | {scenario_pre_audit[bucket]} | "
            f"{scenario_audit[bucket]} | **{total_buckets[bucket]}** |\n"
        )
    o.append(
        f"\n_Total 60 = {sum(total_buckets.values())}._ "
        f"Confirmed iff ratio-leaked > direction-wrong: "
        f"**{ratio_leaked} > {direction_wrong}**.\n\n"
    )

    o.append(f"### P4 — Over-claim > correct-self-identify  ·  **{p4}**\n")
    o.append(
        f"Across {len(failure_trials)} failure-containing trials: "
        f"over-claim **yes = {oc_yes}**, **no = {oc_no}**. "
        f"Confirmed iff yes > no.\n\n"
    )

    o.append("### Agent 1 / Agent 2 vs the human audit\n\n")
    o.append(
        f"- Agent 1 (content resolver, `gemini-3.1-pro-preview`): "
        f"**{a1_agree}/{a1_total}** "
        f"({a1_agree / a1_total:.0%}) — non-canonical.\n"
    )
    o.append(
        f"- Agent 2 (per-scenario resolver, `gemini-3.1-pro-preview`): "
        f"**{a2_agree}/{a2_total}** "
        f"({a2_agree / a2_total:.0%}) — non-canonical.\n\n"
    )

    o.append("### LLM judge vs the human audit (per part)\n\n")
    o.append("| Part | Cases | Claude judge | OpenAI judge |\n|---|---|---|---|\n")
    o.append(
        f"| A (content) | {content_units} | {cj_agree}/{content_units} "
        f"({cj_agree / content_units:.0%}) | {oj_agree}/{content_units} "
        f"({oj_agree / content_units:.0%}) |\n"
    )
    o.append(
        f"| B (per-scenario) | {scenario_units} | {cjs_agree}/{scenario_units} "
        f"({cjs_agree / scenario_units:.0%}) | {ojs_agree}/{scenario_units} "
        f"({ojs_agree / scenario_units:.0%}) |\n"
    )
    o.append(
        f"| C (meta) | {meta_units} | {cjm_agree}/{meta_units} "
        f"({cjm_agree / meta_units:.0%}) | {ojm_agree}/{meta_units} "
        f"({ojm_agree / meta_units:.0%}) |\n\n"
    )

    o.append(
        f"**Verdict summary (post-audit, final):** "
        f"P1 **{p1}** · P2 **{p2}** · P3 **{p3}** · P4 **{p4}**.\n"
    )

    marker = "\n## 03_decay post-audit final results\n"
    FINDINGS.parent.mkdir(parents=True, exist_ok=True)
    existing = FINDINGS.read_text() if FINDINGS.exists() else "# PhysLit 03_decay — Findings\n"
    head = existing.split(marker)[0].rstrip()
    FINDINGS.write_text(head + "\n" + "".join(o))

    print(
        f"P1 {p1} (composite {composite_pass}/15) | "
        f"P2 {p2} (P2={p2_count}, other §5 max={other_p5_max}) | "
        f"P3 {p3} (leaked {ratio_leaked} vs wrong {direction_wrong}) | "
        f"P4 {p4} ({oc_yes} yes vs {oc_no} no)"
    )
    print(f"Agent 1 vs human: {a1_agree}/{a1_total} content cases")
    print(f"Agent 2 vs human: {a2_agree}/{a2_total} scenario cases")
    print(f"Post-audit block written to {FINDINGS.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
