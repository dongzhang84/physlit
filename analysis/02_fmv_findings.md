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
