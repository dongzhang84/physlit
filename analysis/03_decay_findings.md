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

---

## Why P1 is non-decisive to the Part A audit (per-trial composite breakdown)

A trial earns a composite content PASS only if **S1=PASS AND S2=PASS AND every Stage 3 scenario PASSes**. Stage 1 / Stage 2 verdicts are from the dual-judge collapse (PASS if both judges agree, FAIL if both agree, DISAGREE otherwise → Part A). Stage 3 per-scenario columns show the source as `(c)` consensus, `(a)` Agent 2 non-canonical resolver, `(?)` neither judge produced a verdict for that scenario.

| model | trial | S1 | S2 | s1 | s2 | s3 | s4 | s5 | composite |
|---|---|---|---|---|---|---|---|---|---|
| claude | 0 | DISAGREE | DISAGREE | FAIL (a) | FAIL (a) | FAIL (a) | FAIL (c) | ? | **FAIL** |
| claude | 1 | DISAGREE | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | ? | **FAIL** |
| claude | 2 | DISAGREE | DISAGREE | PASS (c) | PASS (c) | PASS (c) | FAIL (c) | PASS (c) | **FAIL** |
| claude | 3 | FAIL | DISAGREE | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | ? | **FAIL** |
| claude | 4 | DISAGREE | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | ? | **FAIL** |
| gpt | 0 | DISAGREE | DISAGREE | PASS (c) | PASS (c) | PASS (c) | FAIL (c) | ? | **FAIL** |
| gpt | 1 | FAIL | DISAGREE | FAIL (c) | PASS (c) | PASS (c) | FAIL (c) | FAIL (c) | **FAIL** |
| gpt | 2 | DISAGREE | DISAGREE | PASS (a) | PASS (c) | PASS (a) | FAIL (c) | PASS (c) | **FAIL** |
| gpt | 3 | FAIL | FAIL | FAIL (a) | PASS (c) | PASS (c) | FAIL (c) | ? | **FAIL** |
| gpt | 4 | FAIL | FAIL | FAIL (a) | FAIL (c) | FAIL (c) | FAIL (c) | FAIL (c) | **FAIL** |
| gemini | 0 | DISAGREE | DISAGREE | PASS (a) | PASS (c) | PASS (c) | FAIL (a) | PASS (c) | **FAIL** |
| gemini | 1 | DISAGREE | DISAGREE | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | ? | **FAIL** |
| gemini | 2 | DISAGREE | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | FAIL (c) | **FAIL** |
| gemini | 3 | FAIL | FAIL | FAIL (a) | PASS (a) | PASS (a) | FAIL (a) | FAIL (c) | **FAIL** |
| gemini | 4 | FAIL | FAIL | PASS (a) | PASS (a) | PASS (a) | PASS (a) | ? | **FAIL** |

**Composite content PASS: 0/15** under Agent 2's non-canonical preview, with the Part A 18 DISAGREE cases left unresolved.

Two failure paths kill every trial, independently:

1. **Stage 1 / Stage 2 already-consensus FAIL** — 8 trials (claude t1/t3/t4, gpt t1/t3/t4, gemini t2/t3/t4) lose S1 or S2 outright. Even if every Stage 3 scenario PASSes, composite = FAIL.
2. **Scenario 4 (falling-body asymptote, target ~ 0.55 m) is FAIL in 14 of 15 trials**, almost all by judge consensus. The single exception is gemini t4, whose S1 and S2 are both consensus FAIL.

Together: **no DISAGREE-resolution path through Part A can flip any trial to composite PASS**. This is what the worksheet header means by "All non-decisive for P1." The Part A audit is for-the-record only; the canonical-affecting work is Part B (P3) and Part C (P4).
