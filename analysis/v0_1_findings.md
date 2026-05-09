# PhysLit v0.1 — Findings

This file accumulates v0.1 evaluation findings, including
R1(b) Gemini post-trial-set re-ping disclosures.

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/_calibration/20260509T172235Z`
- Re-ping timestamp (UTC): `2026-05-09T17:27:05Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/_calibration/20260509T173127Z/gemini-3.1-pro-preview`
- Re-ping timestamp (UTC): `2026-05-09T17:41:36Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/gemini-3.1-pro-preview`
- Re-ping timestamp (UTC): `2026-05-09T18:39:08Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## v0.1 final report
- Generated: `2026-05-09T18:49:09Z`
- Models: claude-opus-4-7, gpt-5.5-2026-04-23, gemini-3.1-pro-preview
- N trials per model: 5
- Judge cost (estimated): $8.2274

### IRR (judge disagreement rate)
- Stage 1: 5/15 = 33.33%
- Stage 2: 7/15 = 46.67%
- Stage 3: 5/15 = 33.33%
- Meta:    5/15 = 33.33%
- Overall: 36.67%

### P1 — Induction failure under training-data conflict
**Verdict: PARTIALLY CONFIRMED**

Per-model both-judge-FAIL counts on Stage 1: {'claude-opus-4-7': 1, 'gemini-3.1-pro-preview': 2}. Per-model both-judge-PASS counts: {'claude-opus-4-7': 2, 'gpt-5.5-2026-04-23': 3, 'gemini-3.1-pro-preview': 2}. Per-model judge-DISAGREE counts: {'claude-opus-4-7': 2, 'gpt-5.5-2026-04-23': 2, 'gemini-3.1-pro-preview': 1}.

### P3 — Meta-cognitive miscalibration
**Verdict: CONFIRMED**

Failure-containing trials: 5. Over-claim trials (both judges agree 'yes'): 2. Rate: 40.00%.

### Per-trial classification matrix

| Model | Trial | S1 | S2 | S3 | Over-claim | Any failure |
|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | FAIL | PASS | no | yes |
| `claude-opus-4-7` | 1 | PASS | PASS | PASS | vacuous | no |
| `claude-opus-4-7` | 2 | DISAGREE | DISAGREE | PASS | yes | no |
| `claude-opus-4-7` | 3 | DISAGREE | DISAGREE | DISAGREE | DISAGREE | no |
| `claude-opus-4-7` | 4 | FAIL | DISAGREE | PASS | DISAGREE | yes |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | vacuous | no |
| `gpt-5.5-2026-04-23` | 1 | DISAGREE | PASS | DISAGREE | DISAGREE | no |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | DISAGREE | no | no |
| `gpt-5.5-2026-04-23` | 3 | DISAGREE | DISAGREE | DISAGREE | DISAGREE | no |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | vacuous | no |
| `gemini-3.1-pro-preview` | 0 | PASS | DISAGREE | PASS | DISAGREE | no |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PASS | no | yes |
| `gemini-3.1-pro-preview` | 2 | PASS | PASS | PASS | vacuous | no |
| `gemini-3.1-pro-preview` | 3 | FAIL | DISAGREE | DISAGREE | yes | yes |
| `gemini-3.1-pro-preview` | 4 | DISAGREE | DISAGREE | FAIL | yes | yes |
