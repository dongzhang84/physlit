# PhysLit v0.2 — Plan

> **Status: PLANNING. Not a prereg. Not locked.**
> This document is the design under discussion. The v0.2 prereg
> (`predictions/v0_2_prereg.md`) will be drafted *from* this plan
> only after the design here is approved.
>
> **Date:** 2026-05-12
> **Author note:** v0.1 verdicts at the `prereg-v0.1-locked` tag are
> not affected by anything in this document.

---

## 1. Scope

v0.2 is an **additive analysis layer** on top of the existing v0.1
Aristotelian dataset. No new production trials are run; no new framework
is introduced.

What's reused (no new API calls):

- 60 v0.1 production trial responses (Stages 1-4)
- 360 v0.1 content-judge verdicts (Stages 1-3 × 2 judges)
- 22 v0.1 human-audit verdicts on dual-judge DISAGREE cases

What's added (new API calls):

- 1 **content disagree resolver** (Agent 1) — auto-resolves the v0.1
  content disagree cases, validated against the 22 known human-audit
  verdicts
- 2 **structural judges** — independent Claude + GPT scoring of the rule
  set against N9-N12, per trial, Stage 1 + Stage 2 combined input
- 1 **structural disagree resolver** (Agent 2) — same role as Agent 1
  but on the structural axis
- 1 **composite aggregator** — produces a per-trial v0.2 verdict from
  the two-axis output, with `FAIL = content_FAIL OR structural_FAIL`

5-framework v0.2 expansion (the older plan) is **deferred** —
post-v0.2, gated on the success of this architecture validation.

---

## 2. Architecture

Two parallel axes, each using the v0.1-style **dual-judge plus
disagree-resolver** pattern. Stage 4 (meta over-claim) is intentionally
out of scope for this plan; its v0.1 verdicts stay as-is.

```
                          ┌────────────────────────────────────────────┐
                          │ Content axis (N1-N8, Stages 1-3)           │
                          │                                            │
trial response ─────────► │ Claude content judge + GPT content judge   │
(Stages 1-3, existing)    │      ├─ agree → PASS / FAIL (content)      │
                          │      └─ disagree → Agent 1 → PASS / FAIL   │
                          └────────────────────────────────────────────┘
                                            │
trial response ─────────► ┌────────────────────────────────────────────┐
(Stage 1 + Stage 2,       │ Structural axis (N9-N12 combined verdict)  │
 concatenated, new)       │                                            │
                          │ Claude structural judge + GPT structural   │
                          │ judge                                      │
                          │      ├─ agree → PASS / FAIL (structural)   │
                          │      └─ disagree → Agent 2 → PASS / FAIL   │
                          └────────────────────────────────────────────┘
                                            │
                                            ▼
                            FINAL v0.2 VERDICT (per trial):
                            PASS iff both axes PASS;
                            FAIL if either axis FAILs.
```

---

## 3. Design decisions (user-confirmed; carried into prereg as-is)

| # | Decision | Note |
| --- | --- | --- |
| D1 | **Structural judges = Claude Opus 4.7 + GPT-5.5** — the same two vendors used as content judges in v0.1, given a different prompt | Reuses dual-judge IRR convention; structural axis matches v0.1 content-axis pattern |
| D2 | **Agent 1 = Agent 2 = the same OpenAI cheap-tier model** (`gpt-5-mini`) | Single model serves both resolver roles; only the prompt differs. Claude side is already loaded with judge duty |
| D3 | **Structural verdict = one total PASS/FAIL per trial** | N9 through N12 are not scored separately; the judge produces a single overall verdict with evidence pointing at whichever criterion(ia) failed |
| D4 | **Structural judge input = Stage 1 + Stage 2 concatenated, one judging call per trial** | Stage 3 (prediction) is not part of the structural-axis input — the rule set lives in Stages 1+2 |

Anything not in this table is either an existing v0.1 convention
(carried over) or an open question (see §6).

---

## 4. Cost estimate

| Component | New API calls | Estimated USD |
| --- | --- | --- |
| Production trials | 0 (reuse v0.1) | $0 |
| Content judging | 0 (reuse v0.1) | $0 |
| **Agent 1 — content disagree resolver** | ~17-22 (one per content DISAGREE) | ~$0.20 |
| **Structural judging — dual** | 60 × 2 = 120 | ~$6-8 |
| **Agent 2 — structural disagree resolver** | ~15-20 (one per structural DISAGREE; IRR unknown until run) | ~$0.20 |
| **Composite aggregator** | 0 (deterministic Python) | $0 |
| **v0.2 total NEW spend** | ~160 | **~$7-9** |

Within the v0.2 ≤ $250 budget cap by a wide margin. Calibration
spend in this plan is bundled into the same run (no separate
pre-flight needed at this scale).

---

## 5. Validation strategy

The single most informative output of v0.2 is **how often Agent 1 agrees
with the existing 22 v0.1 human-audit verdicts on the same cases**. That
is the direct measure of whether the agent-as-resolver design works.

Published in `analysis/v0_2_findings.md`:

- **Agent 1 vs human audit:** per-stage agreement rate; cases where they
  diverge listed verbatim
- **Structural axis IRR:** how often Claude- and GPT-as-structural-judge
  agree (new datapoint, parallel to v0.1's 36.67 % content IRR)
- **Composite verdict shift:** which v0.1 trials' final PASS/FAIL change
  when the structural axis is added, and why
- **Silent-PASS audit:** trials that were content-PASS in v0.1 but
  structural-FAIL in v0.2 (the GPT trial 3 case is the canonical
  example; this validates whether the new architecture catches it)

---

## 6. Open questions (need answers before prereg lock)

**Q1 — Agent 1 scope: 17 or 22 disagree cases?**
v0.1's 22 DISAGREE cases split as: 5 Stage 1 + 7 Stage 2 + 5 Stage 3 +
5 Stage 4 (over-claim). The content axis covers Stages 1-3 only, so
Agent 1 strictly applies to 17. The Stage 4 cases were resolved by
human audit in v0.1; **proposed default: leave the 5 Stage-4 audits
as-is, Agent 1 handles only the 17**.

**Q2 — Stage 4 status in v0.2 final verdicts.**
v0.1 had Stage 4 over-claim as a separate axis feeding into P3, not
into the per-trial PASS/FAIL. **Proposed default: v0.2 verdicts
inherit Stage 4 over-claim findings from v0.1 verbatim, no new work.**

**Q3 — Source of N9-N12 criteria text for the structural judge.**
`frameworks/01_aristotelian/ideal_induction.md` §8 (already on main)
documents N9-N12. **Proposed default: lift §8 into a new
`frameworks/01_aristotelian/structural_criteria.md` to give judges a
focused, judge-only file (mirroring how `pass_fail_criteria.md`
already exists for content judging). The §8 documentation in
`ideal_induction.md` stays as the human-readable narrative.**

**Q4 — Does v0.2 produce a new prereg-locked tag?**
Two paths: (a) lock `prereg-v0.2-locked` with the new criteria,
prompts, decisions D1-D4 + answers to Q1-Q3, before any API call.
(b) Stay in development mode, no new lock, treat v0.2 as
analysis-layer-only that doesn't need its own prereg.
**Proposed default: (a), full prereg lock.** v0.2 introduces new
judging criteria; that's a methodology change and deserves the same
prereg discipline as v0.1.

---

## 7. Files to be created (list only — no code yet)

After Q1-Q4 are answered, the v0.2 build produces these new artifacts.
Existing v0.1 files are not modified.

**Frozen criteria (will be in the prereg envelope):**

- `predictions/v0_2_prereg.md` — locked, SHA-256 sealed, tagged
- `frameworks/01_aristotelian/structural_criteria.md` — N9-N12 spec
  derived from §8 of `ideal_induction.md`, judge-facing
- `prompts/agent1_content_resolver.md` — system prompt for Agent 1
- `prompts/agent2_structural_resolver.md` — system prompt for Agent 2
- `prompts/judge_structural.md` — system prompt for both structural
  judges (Claude + GPT)

**Runner scripts (Python):**

- `scripts/run_agent1.py` — load v0.1 disagree cases, dispatch Agent 1,
  save resolver verdicts
- `scripts/run_structural_judging.py` — 60 trials × 2 judges; save
  per-trial structural-judge verdicts
- `scripts/run_agent2.py` — load structural-judge disagreements,
  dispatch Agent 2, save resolver verdicts
- `scripts/v0_2_aggregate.py` — combine content + structural verdicts
  into the composite v0.2 verdict; emit `analysis/v0_2_findings.md`

**Python module:**

- `src/physlit/v0_2/` — minimal new code (judges/resolvers wrappers,
  aggregator); deliberately separate from `src/physlit/judges/` so the
  v0.1 path is untouched

**Output (gitignored or committed per current convention):**

- `results/<model-id>/01_aristotelian/structural/judge_*.json`
- `results/<model-id>/01_aristotelian/structural/agent2_*.json`
- `results/<model-id>/01_aristotelian/content_resolved/agent1_*.json`
- `analysis/v0_2_findings.md` — the new verdicts file

---

## 8. Methodological notes

- **v0.1 is frozen.** Nothing in v0.2 modifies the v0.1 prereg, the
  v0.1 trial responses, the v0.1 content-judge verdicts, or the 22
  v0.1 human-audit verdicts. v0.2 reads them; v0.2 does not write them.
- **v0.2 is post-hoc with respect to v0.1 data.** The same Aristotelian
  trials are being re-analyzed under a stricter aggregation. This is a
  legitimate methodological move (new criteria, same data) but must be
  reported as such — not as "v0.1 was wrong."
- **Agent 1 is a verdict producer.** It outputs PASS/FAIL, not flags.
  This was the v0.1 audit pathway with a human in that role; v0.2
  replaces the human with an LLM and accepts the methodological cost.
  Mitigation: Agent 1's output is compared against the 22 v0.1 human
  audits as a built-in calibration. Agreement rate is published.
- **No flagging architecture.** The earlier "Agent 2 emits flags for
  human review" design is dropped. v0.2's dual-structural-judge +
  Agent 2 design replaces it entirely.

---

## 9. What this plan does *not* include

- 5-framework expansion (Phlogiston, F=mv, reverse-gravity, color-force):
  deferred to v0.3+, gated on v0.2 outcome.
- Stage 4 (meta over-claim) re-processing: out of scope. v0.1 Stage 4
  verdicts inherited verbatim.
- Temperature variation: deferred to whenever Anthropic re-supports
  the `temperature` parameter for Opus-class models.
- Cross-trial / cross-stage consistency checks (P5 in the original
  prereg): deferred to v0.3+.
- Replacement of any v0.1 verdict: v0.1 stays as published.

---

## 10. Next step after this plan is approved

1. Answer Q1-Q4 in §6 (4 small decisions)
2. Draft `predictions/v0_2_prereg.md` from this plan + answers
3. Draft the 4 prompt files + 1 criteria file
4. Review the prereg + prompts before lock
5. Lock `prereg-v0.2-locked` tag
6. Implement runner scripts
7. Run (~$7-9, ~30-60 minutes wall time)
8. Aggregate + write `analysis/v0_2_findings.md`
