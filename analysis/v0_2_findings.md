# PhysLit v0.2 — Findings

This file accumulates v0.2 evaluation findings: structural-axis
judging, Agent 1 / Agent 2 resolver outputs, and the composite
verdict over v0.1 trials.

## v0.2.1 final report
- Generated: `2026-05-13T19:49:09Z`
- Prereg lock: `prereg-v0.2.1-locked`
- Resolver agent (Agent 1 + Agent 2): `gemini-2.5-pro`

### V1 — Agent 1 calibration against human audit
**Verdict: REFUTED**

Agent 1 agreed with the v0.1 human audit on **5 of 17 content disagree cases (29.4 %)**. Threshold for CONFIRMED was ≥ 12 of 17 per the prereg.

#### Cases where Agent 1 differed from human audit

| Model | Trial | Stage | Agent 1 | Human audit |
|---|---|---|---|---|
| `claude-opus-4-7` | 2 | formulation | PASS | FAIL |
| `claude-opus-4-7` | 4 | formulation | PASS | FAIL |
| `claude-opus-4-7` | 3 | induction | PASS | FAIL |
| `claude-opus-4-7` | 3 | prediction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | formulation | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 1 | induction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | induction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | prediction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 2 | prediction | FAIL | PASS |
| `gemini-3.1-pro-preview` | 3 | formulation | PASS | FAIL |
| `gemini-3.1-pro-preview` | 0 | formulation | PASS | FAIL |
| `gemini-3.1-pro-preview` | 4 | formulation | PASS | FAIL |

### V2 — Structural axis adds detection over content-only
**Verdict: CONFIRMED**

Of the 5 v0.1 all-content-PASS trials (Claude trial 1, GPT trials 0/2/4, Gemini trial 2), **4 flipped to composite FAIL** via the structural axis. Threshold for CONFIRMED was ≥ 2 per the prereg.

#### Flipped trials

- `gpt-5.5-2026-04-23` trial 0
- `gpt-5.5-2026-04-23` trial 2
- `gpt-5.5-2026-04-23` trial 4
- `gemini-3.1-pro-preview` trial 2

### Structural-axis IRR
Structural judges disagreed on **6 of 15 trials (40.00 %)**. Compare to v0.1 content-axis IRR of 36.67 %.

### Composite per-trial verdicts (content AND structural)

| Model | Trial | S1 | S2 | S3 | Structural | Composite |
|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | FAIL | PASS | PASS | FAIL |
| `claude-opus-4-7` | 1 | PASS | PASS | PASS | PASS | PASS |
| `claude-opus-4-7` | 2 | FAIL | PASS | PASS | PASS | FAIL |
| `claude-opus-4-7` | 3 | PASS | FAIL | PASS | FAIL | FAIL |
| `claude-opus-4-7` | 4 | FAIL | PASS | PASS | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | FAIL | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 0 | PASS | PASS | PASS | PASS | PASS |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PASS | PASS | FAIL |
| `gemini-3.1-pro-preview` | 2 | PASS | PASS | PASS | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 3 | FAIL | PASS | PASS | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | PASS | FAIL | PASS | FAIL |
