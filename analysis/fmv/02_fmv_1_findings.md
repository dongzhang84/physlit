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

## 02_fmv.1 post-audit final results
- Generated: `2026-05-19T07:41:38Z`
- Audit: `analysis/02_fmv_1_structural_audit_human_review.md` — 7 structural disagree cases resolved by human audit (canonical, per `prereg-02_fmv.1-locked` §1).

### Resolved per-trial matrix (audit-applied)

> `S1`/`S2`/`S3` — the 02_fmv post-audit content verdicts per stage (induction / formulation / prediction), inherited verbatim from `analysis/02_fmv_findings.md`. `Content-only` = S1 ∧ S2 ∧ S3 — the per-trial verdict if there were no structural axis. `Structural` uses the human-audit verdict for the 7 dual-judge disagree trials and the dual-judge agreed verdict for the other 8 (`†` = the structural verdict was not human-audited). `Composite` = Content-only ∧ Structural.

| Model | Trial | S1 | S2 | S3 | Content-only | Structural | Composite |
|---|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | PASS | PASS | PASS † | PASS |
| `claude-opus-4-7` | 1 | PASS | FAIL | PASS | FAIL | PASS † | FAIL |
| `claude-opus-4-7` | 2 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 0 | PASS | FAIL | PASS | FAIL | PASS † | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PASS | FAIL | FAIL † | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 3 | FAIL | PASS | PASS | FAIL | PASS † | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | PASS | PASS | FAIL | FAIL | FAIL |

**Content-only: 9/15 PASS.** Structural axis: 5/15 PASS. With both axes, **composite PASS drops to 1/15** (`claude-opus-4-7` t0). The structural axis flips 8 content-PASS trials to FAIL — every GPT trial (5/5) and three Claude trials (t2, t3, t4); GPT passed all three content stages in every trial yet failed the structural axis in every trial.

### P1 — Mechanical structural criteria reduce disagreement  ·  **REFUTED**
Structural-axis dual-judge IRR **46.67%** (7/15). The IRR is audit-invariant — it counts trials where the two structural judges disagreed, which the human audit does not change. Confirmed bar < 40% (the v0.2 Aristotelian structural IRR); 46.67% ≥ 40%. The Stage-1-only count fix did **not** lower structural disagreement — evidence against the double-count diagnosis as the dominant cause.

### P2 — Structural axis catches a content-missed failure  ·  **CONFIRMED**
All-content-PASS trials: **9**. Reclassified to composite FAIL by the structural axis: **8** (`claude-opus-4-7` t2, `claude-opus-4-7` t3, `claude-opus-4-7` t4, `gpt-5.5-2026-04-23` t0, `gpt-5.5-2026-04-23` t1, `gpt-5.5-2026-04-23` t2, `gpt-5.5-2026-04-23` t3, `gpt-5.5-2026-04-23` t4). Threshold ≥ 1. The structural axis demonstrably detects failures the content axis missed on this framework.

### Structural judge vs the human audit (7 disagree cases)

- Claude structural judge: **1/7** (14%)
- OpenAI structural judge: **6/7** (86%)

This **reverses** the 02_fmv content axis, where the Claude judge agreed with the human audit on 86% and the OpenAI judge on 21%. Same models, same framework, different judgment task — judge reliability is task-dependent, not model-dependent.

### Agent 2 (non-canonical resolver) vs the human audit

Agent 2 (`gemini-3.1-pro-preview`) agreed with the human audit on **6/7** (86%) of the structural disagree cases — the lone miss is Case 3 (`claude-opus-4-7` t4), where Agent 2 PASS vs human FAIL on N10. Agent 2 is a side analysis; it does not feed P1 / P2.

**Verdict summary (post-audit, final):** P1 REFUTED · P2 CONFIRMED. The audit resolved all 7 structural DISAGREE rows; P1 is unchanged from the preliminary verdict (IRR audit-invariant); P2 firmed from a lower bound of 3 to 8 of 9 all-content-PASS trials flipped.
