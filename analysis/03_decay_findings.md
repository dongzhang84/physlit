# PhysLit 03_decay — Findings

This file accumulates 03_decay evaluation findings,
including R1(b) Gemini post-trial-set re-ping disclosures.

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/gemini-3.1-pro-preview`
- Re-ping timestamp (UTC): `2026-05-22T18:01:22Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## 03_decay judging report
- Generated: `2026-05-22T19:36:12Z`
- Prereg lock: `prereg-03_decay-locked`
- Models: claude-opus-4-7, gpt-5.5-2026-04-23, gemini-3.1-pro-preview | trials judged: 13
- Judge cost (estimated): $16.4739
- Fabrication flags (evidence_check): 21 total (14 judged units affected on Stage 1-3 + meta)
- **PRELIMINARY** — 11 Stage 1-3 dual-judge disagreement(s), 14 fabrication-flagged unit(s), 25 P3 scenario disagreement(s), 7 P3 fabrication-flagged scenario(s) await human audit; verdicts below are lower bounds until resolved.

### IRR (dual-judge disagreement, Stage 1-3)
- 11/45 judged units = **24.44%**

### Per-trial classification matrix

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | DISAGREE | DISAGREE | FAIL | DISAGREE |
| `claude-opus-4-7` | 1 | DISAGREE | FAIL | FAIL | no |
| `claude-opus-4-7` | 2 | DISAGREE | MISSING | FAIL | yes |
| `claude-opus-4-7` | 3 | FAIL | MISSING | FAIL | DISAGREE |
| `claude-opus-4-7` | 4 | DISAGREE | FAIL | FAIL | no |
| `gpt-5.5-2026-04-23` | 0 | DISAGREE | MISSING | FAIL | DISAGREE |
| `gpt-5.5-2026-04-23` | 1 | FAIL | MISSING | FAIL | no |
| `gpt-5.5-2026-04-23` | 2 | DISAGREE | DISAGREE | FAIL | yes |
| `gpt-5.5-2026-04-23` | 3 | FAIL | FAIL | FAIL | no |
| `gpt-5.5-2026-04-23` | 4 | FAIL | FAIL | FAIL | DISAGREE |
| `gemini-3.1-pro-preview` | 0 | MISSING | MISSING | FAIL | no |
| `gemini-3.1-pro-preview` | 1 | DISAGREE | MISSING | FAIL | yes |
| `gemini-3.1-pro-preview` | 2 | DISAGREE | FAIL | FAIL | yes |
| `gemini-3.1-pro-preview` | 3 | MISSING | FAIL | FAIL | yes |
| `gemini-3.1-pro-preview` | 4 | FAIL | FAIL | DISAGREE | yes |

### P1 — Decay harder than both priors  ·  **CONFIRMED**
Composite content PASS: **0/13**. Confirmed iff ≤ 4; Refuted iff ≥ 5. Baselines: F=mv 9/15, Aristotelian 5/15.

### P2 — Hidden-substrate framing is the modal §5 pattern  ·  **VACUOUS (no §5-pattern FAILs cited by both judges)**
(No §5-pattern FAILs with both judges agreeing on the label.)

### P3 — Ratio-leaked > direction-wrong (60 quant predictions)  ·  **CONFIRMED**
- decay-correct: **13**
- direction-correct, ratio-leaked: **15**
- direction-wrong: **0**
- pending (judge disagreement or fabrication): **32**
Confirmed iff leaked > wrong.

### P4 — Over-claim > correct-self-identify  ·  **CONFIRMED**
Among 13 failure-containing trials: over-claim **yes=5**, no**=4**. Confirmed iff yes > no.


## 03_decay judging report
- Generated: `2026-05-22T19:39:51Z`
- Prereg lock: `prereg-03_decay-locked`
- Models: claude-opus-4-7, gpt-5.5-2026-04-23, gemini-3.1-pro-preview | trials judged: 15
- Judge cost (estimated): $0.0000
- Fabrication flags (evidence_check): 0 total (14 judged units affected on Stage 1-3 + meta)
- **PRELIMINARY** — 18 Stage 1-3 dual-judge disagreement(s), 14 fabrication-flagged unit(s), 25 P3 scenario disagreement(s), 7 P3 fabrication-flagged scenario(s) await human audit; verdicts below are lower bounds until resolved.

### IRR (dual-judge disagreement, Stage 1-3)
- 18/45 judged units = **40.00%**

### Per-trial classification matrix

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | DISAGREE | DISAGREE | FAIL | DISAGREE |
| `claude-opus-4-7` | 1 | DISAGREE | FAIL | FAIL | no |
| `claude-opus-4-7` | 2 | DISAGREE | DISAGREE | FAIL | yes |
| `claude-opus-4-7` | 3 | FAIL | DISAGREE | FAIL | DISAGREE |
| `claude-opus-4-7` | 4 | DISAGREE | FAIL | FAIL | no |
| `gpt-5.5-2026-04-23` | 0 | DISAGREE | DISAGREE | FAIL | DISAGREE |
| `gpt-5.5-2026-04-23` | 1 | FAIL | DISAGREE | FAIL | no |
| `gpt-5.5-2026-04-23` | 2 | DISAGREE | DISAGREE | FAIL | yes |
| `gpt-5.5-2026-04-23` | 3 | FAIL | FAIL | FAIL | no |
| `gpt-5.5-2026-04-23` | 4 | FAIL | FAIL | FAIL | DISAGREE |
| `gemini-3.1-pro-preview` | 0 | DISAGREE | DISAGREE | FAIL | no |
| `gemini-3.1-pro-preview` | 1 | DISAGREE | DISAGREE | FAIL | yes |
| `gemini-3.1-pro-preview` | 2 | DISAGREE | FAIL | FAIL | yes |
| `gemini-3.1-pro-preview` | 3 | FAIL | FAIL | FAIL | yes |
| `gemini-3.1-pro-preview` | 4 | FAIL | FAIL | DISAGREE | yes |

### P1 — Decay harder than both priors  ·  **CONFIRMED**
Composite content PASS: **0/15**. Confirmed iff ≤ 4; Refuted iff ≥ 5. Baselines: F=mv 9/15, Aristotelian 5/15.

### P2 — Hidden-substrate framing is the modal §5 pattern  ·  **VACUOUS (no §5-pattern FAILs cited by both judges)**
(No §5-pattern FAILs with both judges agreeing on the label.)

### P3 — Ratio-leaked > direction-wrong (60 quant predictions)  ·  **CONFIRMED**
- decay-correct: **13**
- direction-correct, ratio-leaked: **15**
- direction-wrong: **0**
- pending (judge disagreement or fabrication): **32**
Confirmed iff leaked > wrong.

### P4 — Over-claim > correct-self-identify  ·  **CONFIRMED**
Among 15 failure-containing trials: over-claim **yes=6**, no**=5**. Confirmed iff yes > no.
