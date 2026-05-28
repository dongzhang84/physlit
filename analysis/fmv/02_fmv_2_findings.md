# PhysLit 02_fmv.2 — Findings

This file accumulates 02_fmv.2 (axiomatisation control)
evaluation findings, including R1(b) Gemini post-trial-set
re-ping disclosures.

## R1(b) post-trial-set re-ping (Gemini)

- Trial-set output root: `/Users/dong/Projects/physlit/results/gemini-3.1-pro-preview`
- Re-ping timestamp (UTC): `2026-05-19T19:00:28Z`
- Lock-time identifier:    `gemini-3.1-pro-preview`
- Post-run identifier:     `gemini-3.1-pro-preview`
- Identity-field drift:    **no**

## 02_fmv.2 judging report (preliminary)
- Generated: `2026-05-19T19:11:07Z`
- Prereg lock: `prereg-02_fmv.2-locked`
- Judge cost (estimated): $12.5452
- Content axis judged with the `02_fmv` criteria + judge prompts; structural axis with the `02_fmv.1` criteria + judge prompt.
- **PRELIMINARY** — 10 content + 6 structural dual-judge disagreement(s) await human audit. Canonical P1 / P2 and the treatment-vs-control comparison: `apply_02_fmv_2.py`.

### Treatment-arm IRR
- Content (Stage 1-3): 10/45 units = **22.22%**
- Structural: 6/15 trials = **40.00%**

### Per-trial treatment-arm verdicts

| Model | Trial | S1 | S2 | S3 | Content-only | Structural |
|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 1 | PASS | DISAGREE | PASS | DISAGREE | PASS |
| `claude-opus-4-7` | 2 | PASS | DISAGREE | PASS | DISAGREE | PASS |
| `claude-opus-4-7` | 3 | DISAGREE | PASS | PASS | DISAGREE | PASS |
| `claude-opus-4-7` | 4 | DISAGREE | PASS | PASS | DISAGREE | PASS |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | DISAGREE |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | DISAGREE |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | PASS | DISAGREE |
| `gpt-5.5-2026-04-23` | 4 | DISAGREE | PASS | PASS | DISAGREE | DISAGREE |
| `gemini-3.1-pro-preview` | 0 | DISAGREE | FAIL | PASS | FAIL | DISAGREE |
| `gemini-3.1-pro-preview` | 1 | FAIL | DISAGREE | FAIL | FAIL | PASS |
| `gemini-3.1-pro-preview` | 2 | FAIL | DISAGREE | PASS | FAIL | DISAGREE |
| `gemini-3.1-pro-preview` | 3 | DISAGREE | PASS | PASS | DISAGREE | PASS |
| `gemini-3.1-pro-preview` | 4 | FAIL | DISAGREE | PASS | FAIL | FAIL |

## 02_fmv.2 post-audit final results
- Generated: `2026-05-20T09:07:03Z`
- Prereg lock: `prereg-02_fmv.2-locked`

### Treatment-arm per-trial matrix

| Model | Trial | S1 | S2 | S3 | Content-only | Structural | Composite |
|---|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 1 | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 2 | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 0 | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 3 | PASS | PASS | PASS | PASS | PASS | PASS |
| `gemini-3.1-pro-preview` | 4 | FAIL | PASS | PASS | FAIL | FAIL | FAIL |

### Treatment vs. control

| Arm | Content-axis PASS | Structural-axis PASS | Composite PASS |
|---|---|---|---|
| Control (`02_fmv` / `02_fmv.1`) | 9/15 | 5/15 | 1/15 |
| Treatment (`02_fmv.2`) | 9/15 | 11/15 | 6/15 |

Per model (control → treatment):

| Model | Content (ctrl → treat) | Structural (ctrl → treat) | Composite (ctrl → treat) |
|---|---|---|---|
| `claude-opus-4-7` | 4/5 → 3/5 | 2/5 → 5/5 | 1/5 → 3/5 |
| `gpt-5.5-2026-04-23` | 5/5 → 5/5 | 0/5 → 2/5 | 0/5 → 2/5 |
| `gemini-3.1-pro-preview` | 0/5 → 1/5 | 3/5 → 4/5 | 0/5 → 1/5 |

### P1 — Axiomatisation instruction raises the structural pass rate  ·  **STRONGLY CONFIRMED**
Treatment structural-axis PASS **11/15** vs control **5/15**. Bands (prereg §2): strongly confirmed ≥10, directionally confirmed 6-9, refuted ≤5. Per-model and per-criterion breakdown is the primary reading in the directional band.

### P2 — Content competence does not degrade under the treatment  ·  **CONFIRMED**
Treatment content-axis PASS **9/15** vs control **9/15**. Confirmed ≥8 (within one trial of the control — no material degradation); refuted ≤7.

### LLM judge vs the human audit (per axis)

| Axis | Cases | Claude judge | OpenAI judge |
|---|---|---|---|
| Content | 10 | 5/10 (50%) | 5/10 (50%) |
| Structural | 6 | 3/6 (50%) | 3/6 (50%) |

### Agent 1 / Agent 2 vs the human audit

- Agent 1 (content resolver, `gemini-3.1-pro-preview`): **5/10** (50%) on the content disagreements.
- Agent 2 (structural resolver, `gemini-3.1-pro-preview`): **5/6** (83%) on the structural disagreements.
