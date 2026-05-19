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
