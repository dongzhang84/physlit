# PhysLit v0.3 — Findings

This file accumulates v0.3 (Aristotelian axiomatisation
control) evaluation findings, including R1(b) Gemini
post-trial-set re-ping disclosures.

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/gemini-3.1-pro-preview`
- Re-ping timestamp (UTC): `2026-05-20T17:12:34Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## v0.3 judging report (preliminary)
- Generated: `2026-05-20T17:28:18Z`
- Prereg lock: `prereg-v0.3-locked`
- Judge cost (estimated): $9.7966
- Content axis judged with v0.1 criteria + v0.1 global judge prompts; structural axis with v0.2 criteria + global structural judge prompt.
- **PRELIMINARY** — 8 content + 2 structural dual-judge disagreement(s) await human audit. Canonical P1 / P2 and the treatment-vs-control comparison: `apply_v0_3.py`.

### Treatment-arm IRR
- Content (Stage 1-3): 8/45 units = **17.78%**
- Structural: 2/14 trials = **14.29%**

### Per-trial treatment-arm verdicts

| Model | Trial | S1 | S2 | S3 | Content-only | Structural |
|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | DISAGREE | DISAGREE | DISAGREE | DISAGREE | PASS |
| `claude-opus-4-7` | 1 | PASS | PASS | DISAGREE | DISAGREE | PASS |
| `claude-opus-4-7` | 2 | PASS | DISAGREE | PASS | DISAGREE | PASS |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | DISAGREE |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | FAIL | FAIL | PASS |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | PASS |
| `gemini-3.1-pro-preview` | 0 | FAIL | PASS | FAIL | FAIL | PASS |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | DISAGREE | FAIL | PASS |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | DISAGREE | FAIL | PASS |
| `gemini-3.1-pro-preview` | 3 | PASS | FAIL | PASS | FAIL | DISAGREE |
| `gemini-3.1-pro-preview` | 4 | FAIL | DISAGREE | PASS | FAIL | MISSING |


## v0.3 judging report (preliminary)
- Generated: `2026-05-20T17:30:22Z`
- Prereg lock: `prereg-v0.3-locked`
- Judge cost (estimated): $0.0000
- Content axis judged with v0.1 criteria + v0.1 global judge prompts; structural axis with v0.2 criteria + global structural judge prompt.
- **PRELIMINARY** — 8 content + 3 structural dual-judge disagreement(s) await human audit. Canonical P1 / P2 and the treatment-vs-control comparison: `apply_v0_3.py`.

### Treatment-arm IRR
- Content (Stage 1-3): 8/45 units = **17.78%**
- Structural: 3/15 trials = **20.00%**

### Per-trial treatment-arm verdicts

| Model | Trial | S1 | S2 | S3 | Content-only | Structural |
|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | DISAGREE | DISAGREE | DISAGREE | DISAGREE | PASS |
| `claude-opus-4-7` | 1 | PASS | PASS | DISAGREE | DISAGREE | PASS |
| `claude-opus-4-7` | 2 | PASS | DISAGREE | PASS | DISAGREE | PASS |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | DISAGREE |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | FAIL | FAIL | PASS |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | PASS |
| `gemini-3.1-pro-preview` | 0 | FAIL | PASS | FAIL | FAIL | PASS |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | DISAGREE | FAIL | PASS |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | DISAGREE | FAIL | PASS |
| `gemini-3.1-pro-preview` | 3 | PASS | FAIL | PASS | FAIL | DISAGREE |
| `gemini-3.1-pro-preview` | 4 | FAIL | DISAGREE | PASS | FAIL | DISAGREE |

## v0.3 post-audit final results
- Generated: `2026-05-20T18:06:33Z`
- Prereg lock: `prereg-v0.3-locked`
- **PRELIMINARY** — 8 treatment trial(s) have an unresolved dual-judge disagreement; fill the `HUMAN_CONTENT` / `HUMAN_STRUCTURAL` tables in `apply_v0_3.py` after the audit and re-run.

### Treatment-arm per-trial matrix

| Model | Trial | S1 | S2 | S3 | Content-only | Structural | Composite |
|---|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PENDING | PENDING | PENDING | PENDING | PASS | FAIL |
| `claude-opus-4-7` | 1 | PASS | PASS | PENDING | PENDING | PASS | FAIL |
| `claude-opus-4-7` | 2 | PASS | PENDING | PASS | PENDING | PASS | FAIL |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | PENDING | FAIL |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | FAIL | FAIL | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gemini-3.1-pro-preview` | 0 | FAIL | PASS | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PENDING | PENDING | PASS | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | PENDING | PENDING | PASS | FAIL |
| `gemini-3.1-pro-preview` | 3 | PASS | FAIL | PASS | FAIL | PENDING | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | PENDING | PASS | PENDING | PENDING | FAIL |

### Treatment vs. control (Aristotelian)

| Arm | Content-axis PASS | Structural-axis PASS | Composite PASS |
|---|---|---|---|
| Control (v0.1 / v0.2) | 5/15 | 8/15 | 2/15 |
| Treatment (v0.3) | 6/15 | 12/15 | 5/15 |

Per model (control → treatment):

| Model | Content | Structural | Composite |
|---|---|---|---|
| `claude-opus-4-7` | 1/5 → 2/5 | 5/5 → 5/5 | 1/5 → 2/5 |
| `gpt-5.5-2026-04-23` | 3/5 → 4/5 | 0/5 → 4/5 | 0/5 → 3/5 |
| `gemini-3.1-pro-preview` | 1/5 → 0/5 | 3/5 → 3/5 | 1/5 → 0/5 |

### Cross-framework comparison (same axiomatisation instruction)

| Framework | Content (ctrl → treat) | Structural (ctrl → treat) | Composite (ctrl → treat) |
|---|---|---|---|
| Aristotelian (v0.1 → v0.3) | 5/15 → 6/15 | 8/15 → 12/15 | 2/15 → 5/15 |
| F=mv (02_fmv → 02_fmv.2) | 9/15 → 9/15 | 5/15 → 11/15 | 1/15 → 6/15 |

### P1 — Axiomatisation raises the structural pass rate  ·  **DIRECTIONALLY CONFIRMED**
Treatment structural-axis PASS **12/15** vs control **8/15**. Bands (prereg §2): strongly confirmed ≥13 (+5 absolute), directionally confirmed 9-12, refuted ≤8. Per-model and per-criterion breakdown is the primary reading in the directional band.

### P2 — Content competence does not degrade  ·  **CONFIRMED**
Treatment content-axis PASS **6/15** vs control **5/15**. Confirmed ≥4 (within one trial of control — no material degradation); refuted ≤3.
