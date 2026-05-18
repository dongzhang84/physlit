# PhysLit 02_fmv.1 — Structural-Axis Findings


## 02_fmv.1 structural-axis report
- Generated: `2026-05-18T23:21:17Z`
- Prereg lock: `prereg-02_fmv.1-locked`
- Structural judge cost (estimated): $3.6191
- **PRELIMINARY** — 7 structural dual-judge disagreement(s) await human audit. P1's IRR is audit-invariant; P2 is a lower bound while a disagreement on a content-PASS trial is unresolved (5 such).

### Structural-axis IRR
- 7/15 trials = **46.67%**

### Per-trial structural + composite verdicts

| Model | Trial | Content | Structural | Composite |
|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | PASS |
| `claude-opus-4-7` | 1 | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 2 | PASS | DISAGREE | DISAGREE |
| `claude-opus-4-7` | 3 | PASS | DISAGREE | DISAGREE |
| `claude-opus-4-7` | 4 | PASS | DISAGREE | DISAGREE |
| `gpt-5.5-2026-04-23` | 0 | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 1 | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 2 | PASS | DISAGREE | DISAGREE |
| `gpt-5.5-2026-04-23` | 3 | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | DISAGREE | DISAGREE |
| `gemini-3.1-pro-preview` | 0 | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | DISAGREE | FAIL |
| `gemini-3.1-pro-preview` | 3 | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | DISAGREE | FAIL |

### P1 — Mechanical structural criteria reduce disagreement  ·  **REFUTED**
Structural IRR 46.67% (Confirmed < 40%; v0.2 Aristotelian structural IRR was 40%).

### P2 — Structural axis catches a content-missed failure  ·  **CONFIRMED**
All-content-PASS trials: 9. Flipped to composite FAIL via the structural axis: **3** (gpt-5.5-2026-04-23 t0, gpt-5.5-2026-04-23 t1, gpt-5.5-2026-04-23 t3). Threshold ≥ 1.
- 5 content-PASS trial(s) have a structural DISAGREE pending audit: claude-opus-4-7 t2, claude-opus-4-7 t3, claude-opus-4-7 t4, gpt-5.5-2026-04-23 t2, gpt-5.5-2026-04-23 t4.
