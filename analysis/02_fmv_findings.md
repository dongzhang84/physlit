# PhysLit 02_fmv — Findings

This file accumulates 02_fmv evaluation findings, including
R1(b) Gemini post-trial-set re-ping disclosures.

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/gemini-3.1-pro-preview`
- Re-ping timestamp (UTC): `2026-05-18T18:29:04Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## 02_fmv judging report
- Generated: `2026-05-18T18:41:29Z`
- Prereg lock: `prereg-02_fmv-locked`
- Models: claude-opus-4-7, gpt-5.5-2026-04-23, gemini-3.1-pro-preview | trials judged: 15
- Judge cost (estimated): $11.8964
- **PRELIMINARY** — 12 Stage 1-3 dual-judge disagreement(s) + 0 quantitative-scenario disagreement(s) await human audit; P1 / P2 / P4 below are lower bounds until those are resolved.

### IRR (dual-judge disagreement, Stage 1-3)
- 12/45 judged units = **26.67%**

### Per-trial classification matrix

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | DISAGREE | PASS | DISAGREE |
| `claude-opus-4-7` | 1 | PASS | DISAGREE | PASS | no |
| `claude-opus-4-7` | 2 | PASS | PASS | PASS | vacuous |
| `claude-opus-4-7` | 3 | DISAGREE | DISAGREE | PASS | yes |
| `claude-opus-4-7` | 4 | DISAGREE | DISAGREE | DISAGREE | yes |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | vacuous |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | vacuous |
| `gpt-5.5-2026-04-23` | 2 | PASS | DISAGREE | PASS | no |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | vacuous |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | vacuous |
| `gemini-3.1-pro-preview` | 0 | DISAGREE | DISAGREE | PASS | DISAGREE |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PASS | yes |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | FAIL | yes |
| `gemini-3.1-pro-preview` | 3 | DISAGREE | PASS | PASS | no |
| `gemini-3.1-pro-preview` | 4 | FAIL | DISAGREE | PASS | yes |

### P1 — Induction failure  ·  **REFUTED**
Stage 1 FAIL: 3/15 (threshold ≥ 8); DISAGREE pending: 4.

### P2 — Meta-cognitive miscalibration  ·  **CONFIRMED**
Over-claiming: 3/3 failure-containing trials = 100.00% (threshold ≥ 50%).

### P3 — Mechanical criteria reduce disagreement  ·  **PARTIALLY CONFIRMED**
IRR 26.67% (Confirmed < 25%; vs v0.1 content-axis IRR 36.67%).

### P4 — Stage 3 quantitative leak  ·  **REFUTED**
Direction-correct / ratio-leaked: 0/45 quantitative predictions = 0.00% (threshold ≥ 30%); 0 scenario-level disagreement(s) pending.

## 02_fmv post-audit final results
- Generated: `2026-05-18T22:39:43Z`
- Audit: `analysis/02_fmv_audit_human_review.md` — 14 disagree cases resolved by human audit (canonical, per prereg).

### Resolved per-trial matrix (audit-applied)

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | PASS | no |
| `claude-opus-4-7` | 1 | PASS | FAIL | PASS | no |
| `claude-opus-4-7` | 2 | PASS | PASS | PASS | vacuous |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | yes |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | yes |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | vacuous |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | vacuous |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | no |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | vacuous |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | vacuous |
| `gemini-3.1-pro-preview` | 0 | PASS | FAIL | PASS | yes |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PASS | yes |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | FAIL | yes |
| `gemini-3.1-pro-preview` | 3 | FAIL | PASS | PASS | no |
| `gemini-3.1-pro-preview` | 4 | FAIL | PASS | PASS | yes |

### P1 — Induction failure  ·  **REFUTED**
Stage 1 FAIL: **4/15** (threshold ≥ 8). All 4 are Gemini; Claude 0/5, GPT 0/5, Gemini 4/5.

### P2 — Meta-cognitive miscalibration  ·  **CONFIRMED**
Over-claiming: **4/6** failure-containing trials = 66.7% (threshold ≥ 50%).

### P3 — Mechanical criteria reduce disagreement  ·  **PARTIALLY CONFIRMED**
Stage 1-3 dual-judge IRR **26.67%** (12/45); unchanged by the audit. Confirmed bar < 25%; vs v0.1 content-axis IRR 36.67%.

### P4 — Stage 3 quantitative leak  ·  **REFUTED**
0/45 direction-correct / ratio-leaked. The single Stage 3 disagree (Claude trial 4) resolved PASS — all five scenarios answered with the F=mv ratios.

### Agent 1 vs the human audit (V1-style calibration)

Agent 1 (`gemini-3.1-pro-preview`, non-canonical resolver) agreed with the human audit on **12/12 content cases (100%)** — cross-vendor 8/8, same-vendor (Gemini) 4/4.

For contrast, v0.2 Aristotelian Agent 1 agreed with the human audit on 29.4%. The mechanical 02_fmv criteria lift LLM-resolver agreement to 100% — direct support for the criteria-ambiguity diagnosis.

### LLM judge vs the human audit (on the 14 disagree cases)

- Claude judge: **11/14** (79%)
- OpenAI judge: **3/14** (21%)

This reverses v0.1 Aristotelian (OpenAI was the more reliable judge there). See `analysis/02_fmv_audit_human_review.md` — "Judge reliability does not transfer across frameworks" and the OpenAI verdict-field self-contradiction defect (5/14 cases).

**Verdict summary (post-audit, final):** P1 REFUTED · P2 CONFIRMED · P3 PARTIALLY CONFIRMED · P4 REFUTED. All four match the preliminary dual-judge verdicts; the audit firmed the underlying counts and resolved every DISAGREE row.
