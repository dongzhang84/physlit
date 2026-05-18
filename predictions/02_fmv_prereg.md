# Pre-Registered Predictions for PhysLit — F=mv World (`02_fmv`)

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `<PENDING>`
- Locked at git tag: `prereg-02_fmv-locked`
- Lock timestamp (UTC): `<PENDING>`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `<PENDING>`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST NOT
> be modified.** Any revision requires a new version (`02_fmv.1`,
> `02_fmv.2`, …) with its own tag and an explicit "deviation from
> prereg" notice published alongside any results.
>
> The artifact files referenced below are frozen at the locked commit.
> Retrieve any of them post-lock with:
> `git show prereg-02_fmv-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## 0. Relationship to prior PhysLit work

This is PhysLit's **second framework experiment** and the **first
from-scratch experiment since v0.1**. It is not part of the v0.1 /
v0.2 / v0.2.1 line and does not modify any of those locked envelopes.

It is framework-scoped: the pre-registration, the lock tag, and the
results all carry the framework identifier `02_fmv` rather than a
`v0.X` number. The v0.1 Aristotelian experiment is closed; v0.2 added
a structural-axis analysis layer to it; both are frozen. This
experiment reuses **none** of their data.

**One methodological change is carried in deliberately.** v0.1's
judging criteria left their hardest call to interpretation
(`ideal_induction.md` §3 banned "density (as a defined quantity)"
while §5 failed the bare word "denser"); a human auditor and an LLM
resolver resolved that gap in opposite directions. This experiment's
criteria are written to be **mechanical** — see
`frameworks/02_fmv/ideal_induction.md` §0. Whether that change reduces
dual-judge disagreement is itself pre-registered below (P3).

## 1. Scope

PhysLit `02_fmv` tests whether three frontier models can **induce,
formulate, apply, and reflect on** the rules of a counterfactual world
— the F=mv World (`frameworks/02_fmv/spec.yaml`) — without sliding
back to the F=ma physics that saturates their training data.

**Protocol.**

- **Tested models (3):**
  - Anthropic Claude Opus 4.7 — `claude-opus-4-7`
  - OpenAI GPT-5.5 — `gpt-5.5-2026-04-23`
  - Google Gemini 3.1 Pro — `gemini-3.1-pro-preview`

  Exact version strings are re-verified by
  `scripts/discover_model_versions.py` immediately before the lock; if
  any vendor has published a more specific identifier by lock time,
  the pin is updated and the change noted here before locking.
- **N = 5 trials per model.** Each trial is a fresh API client with a
  new session UUID. Multi-turn or context reuse across stages is
  forbidden (`CLAUDE.md`, "N=5 trials, fresh sessions").
- **4 stages per trial:** Stage 1 induction → Stage 2 formulation →
  Stage 3 prediction → Stage 4 meta. Each stage is an independent
  fresh session; the runner replays the model's own prior-stage
  responses as input where a stage requires them.
- **Sampling:** every call requests `temperature = 0`, matching the
  v0.1 runner. OpenAI and Google honour the parameter; Anthropic Opus
  4.7 rejects it and runs at its own default — the requested value is
  still recorded. Result files carry the requested value
  (`trial_N_t0.0.json`). No temperature=0.7 secondary pass.
- **Observations are hand-authored.** `02_fmv` is a Tier 1
  (simulator) framework, but its first production run uses the
  hand-written observation set `frameworks/02_fmv/observations.md`.
  The deterministic simulator is deferred; it is not on the critical
  path for this experiment and not part of this prereg envelope.

**Content axis only.** Trials are judged on the content axis
(necessary conditions N1–N6, the §3 banned-token test, and the §5
disqualifying patterns, all in `frameworks/02_fmv/ideal_induction.md`;
Stage 2 / Stage 3 criteria in `frameworks/02_fmv/pass_fail_criteria.md`).
The structural axis (the v0.2 N9–N12 layer) is **not** used. The first
F=mv round is a content-axis experiment.

**Dual-judge evaluation, human-audit resolution.** Each Stage 1–3
response is scored independently by two LLM judges:

- Anthropic Claude Opus 4.7 — `claude-opus-4-7`
- OpenAI GPT-5.5 — `gpt-5.5-2026-04-23`

Where the two judges agree, that is the verdict. Where they disagree,
the case is resolved by **human audit** — as in v0.1, and unlike v0.2.
No LLM disagree-resolver agent (no "Agent 1" / "Agent 2") is used in
this experiment. The per-framework dual-judge disagreement rate (IRR)
is published as a methodology-quality indicator; a disagreement rate
above 25 % triggers a full human audit before public release
(`CLAUDE.md`, "Inter-rater reliability").

**Out of scope, by explicit decision:**

- The structural axis (N9–N12) and any structural judging.
- LLM disagree-resolver agents; disagreements are resolved by human
  audit only.
- The deterministic simulator; this round uses the hand-written
  observation set.
- Temperature variation.
- Any reuse, re-judging, or modification of v0.1 / v0.2 data.

**Budget.** Estimated ≤ $60 USD total (tested models + judges; 3
models × 5 trials × 4 stages + dual-judge on Stages 1–3 and Stage 4
meta judging). `scripts/estimate_cost.py` runs before the production
batch; per `CLAUDE.md`, a runner estimate above $5 requires explicit
confirmation. Every result file records its actual cost.

**Pre-lock dry run.** A single-model, N=1 dry run (Claude only)
precedes the lock, with output written to `results/_dryrun/<timestamp>/`
and never to `results/<model>/02_fmv/`. Dry-run findings may revise
the artifacts below; the lock happens only after those revisions
settle.

## 2. Predictions

Four predictions are committed by this lock: **P1** (induction
failure), **P2** (meta-cognitive miscalibration), **P3** (mechanical
criteria reduce dual-judge disagreement), **P4** (quantitative leak in
Stage 3).

### P1 — Induction failure under training-data conflict

**Prediction.** Of the 15 Stage 1 induction trials (3 models × N=5), a
**majority — at least 8 of 15 — FAIL**: the model imports F=ma
machinery rather than inducing the F=mv rules. A Stage 1 FAIL is any
of: a banned token (`ideal_induction.md` §3), a disqualifying pattern
P1–P7 (§5), an unmet necessary condition N1–N6, or a coverage /
consistency failure — per the §6 judge checklist.

**Rationale.** The F=mv World contradicts the F=ma physics that
saturates every tested model's training data. Observations 2 and 3
(motion starts and stops *with* the push — no build-up, no coasting)
are direct contradictions of inertia, the single most over-learned
fact in the relevant training distribution. v0.1 found 8 of 15 Stage 1
trials FAIL on Aristotelian Mechanics post-audit; F=mv presents a
sharper, more numerically explicit contradiction.

**Scoring.**

- **Confirmed:** ≥ 8 of 15 Stage 1 trials FAIL.
- **Partially confirmed:** 5–7 of 15 FAIL.
- **Refuted:** ≤ 4 of 15 FAIL — the models induce the F=mv rules
  cleanly despite the training-data conflict.

Per-model Stage 1 FAIL counts are published alongside the headline.

### P2 — Meta-cognitive miscalibration

**Prediction.** Among the trials that contain at least one Stage 1–3
audit-FAIL, the model's Stage 4 reflection **over-claims** — denies or
fails to identify a slip that the trial's own stage record shows — in
**at least 50 %** of them.

**Rationale.** v0.1's P3 found a 70 % over-claiming rate on
Aristotelian: models could name abstract categories of their error
but missed the specific banned concept their own rules contained. The
F=mv banned-token set is concrete and lexical, which could make slips
easier to self-identify; 50 % is therefore set below the v0.1 figure.

**Scoring.**

- **Confirmed:** over-claiming rate ≥ 50 %.
- **Partially confirmed:** 30–49 %.
- **Refuted:** < 30 %.

Over-claiming is classified per the rubric in
`frameworks/02_fmv/pass_fail_criteria.md`, "Meta-cognitive (Stage 4)".

### P3 — Mechanical criteria reduce dual-judge disagreement

**Prediction.** The dual-judge content-axis disagreement rate (IRR)
across the Stage 1–3 judgments will be **below v0.1's 36.67 %**, and
specifically **below the 25 % human-audit threshold**.

**Rationale.** v0.1's content-axis disagreement was substantially
driven by an ambiguous criterion: `ideal_induction.md` §3 banned
"density (as a defined quantity)" while §5 failed the bare comparative
"denser", and the two judges resolved that gap differently. The
`02_fmv` §3 banned-token test is purely lexical — a fixed token list,
no "as a defined quantity" qualifier, no intent assessment (see
`ideal_induction.md` §0 and §3). If a mechanical criterion does not
lower the disagreement rate, the criteria-ambiguity diagnosis is
wrong; that is a publishable negative result.

**Scoring.**

- **Confirmed:** IRR < 25 %.
- **Partially confirmed:** 25 % ≤ IRR < 36.67 %.
- **Refuted:** IRR ≥ 36.67 % — the mechanical criteria did not reduce
  judge disagreement relative to v0.1.

IRR is computed over all Stage 1–3 judgments (3 models × 5 trials × 3
stages = 45 judged units, two judges each).

### P4 — Quantitative leak in Stage 3 predictions

**Prediction.** Across the 45 quantitative-scenario predictions (15
trials × Scenarios 1, 2, and 4), **at least 30 %** name the correct
direction but give a ratio that matches the **standard-physics (F=ma)
column** rather than the F=mv column — "direction-correct,
ratio-leaked".

**Rationale.** Scenarios 1, 2, and 4 are built so that the *direction*
is shared by both physics — longer / slower / the lighter block wins —
and only the *ratio* discriminates (2×D vs 4×D; 2T vs √2·T; 2 : 1 vs
√2 : 1; see `prediction_tests.md` and `pass_fail_criteria.md`). A model
can therefore sound in-framework — pick the right direction — while
its arithmetic is still F=ma kinematics underneath. P4 measures how
often the words pass but the computation leaks.

**Scoring.**

- **Confirmed:** ≥ 30 % of the 45 quantitative predictions are
  direction-correct / ratio-leaked.
- **Partially confirmed:** 15–29 %.
- **Refuted:** < 15 %.

Each quantitative prediction is classified into exactly one of:
F=mv-correct (direction and ratio both F=mv), direction-correct /
ratio-leaked (the P4 bucket), or direction-wrong-or-other. Per-scenario
counts and a breakdown restricted to Stage-1-passing trials are
published alongside the headline.

## 3. Scoring procedure

1. Production trials are run: 3 models × 5 trials × 4 stages, fresh
   client + new session UUID per stage, using the four prompts frozen
   at the locked commit (`frameworks/02_fmv/prompts/stage{1,2,3,4}_*.md`).
   Every prompt sent and every response received is committed to
   `results/<model>/02_fmv/<stage>/trial_N_t0.0.json`, including any
   API-side failure record. Selective publishing is forbidden.
2. Each Stage 1–3 response is scored by both content judges
   independently, using the judge prompts frozen at the locked commit
   and the criteria files `frameworks/02_fmv/ideal_induction.md` and
   `frameworks/02_fmv/pass_fail_criteria.md`.
3. Per-stage classification = the two judges' agreed verdict.
   Disagreements are recorded, the IRR is computed, and — if IRR
   exceeds 25 % — every disagree case is resolved by human audit
   before any public release. The audit verdicts are committed.
4. Stage 4 responses are classified per the Meta-cognitive rubric in
   `pass_fail_criteria.md`.
5. P1 is computed from the Stage 1 FAIL count; P2 from the Stage 4
   over-claiming rate; P3 from the Stage 1–3 dual-judge IRR; P4 from
   the classification of the 45 quantitative-scenario predictions
   (Scenarios 1, 2, 4).
6. The findings document (`analysis/02_fmv_findings.md`) records: the
   per-trial stage matrix; the dual-judge IRR; any human-audit
   verdicts; the P1 / P2 / P3 / P4 verdicts; and any deviation from
   this prereg, with timestamps and rationale.

## 4. Frozen artifacts (referenced by the `prereg-02_fmv-locked` tag)

At the locked commit, the contents of the following files are part of
the `02_fmv` prereg envelope and must not change without a new prereg
version:

- `frameworks/02_fmv/spec.yaml`
- `frameworks/02_fmv/observations.md` — the model-facing observation
  set (the `## Observations` section is what the runner injects)
- `frameworks/02_fmv/ideal_induction.md` — Stage 1 judge criteria
  (N1–N6, the §3 banned-token test, the §5 disqualifying patterns)
- `frameworks/02_fmv/pass_fail_criteria.md` — Stage 2 / Stage 3 /
  cross-stage criteria and the Stage 4 meta rubric
- `frameworks/02_fmv/prediction_tests.md` — the five Stage 3 scenarios
- `frameworks/02_fmv/prompts/stage1_induction.md`
- `frameworks/02_fmv/prompts/stage2_formulation.md`
- `frameworks/02_fmv/prompts/stage3_prediction.md`
- `frameworks/02_fmv/prompts/stage4_meta.md`
- the four `02_fmv`-specific content-judge prompts (the shared global
  `prompts/judge_*.md` are **not** reused — the F=mv banned-token set
  differs from v0.1's): `frameworks/02_fmv/prompts/judge_stage1.md`,
  `judge_stage2.md`, `judge_stage3.md`, `judge_meta.md` — authored
  before the lock

The `.zh.md` translation aids (`observations.zh.md`,
`prediction_tests.zh.md`) are **not** part of the envelope; on any
discrepancy the English files govern.

The v0.1 and v0.2 prereg envelopes are **not** modified by this
experiment.

## 5. Publication policy

PhysLit commits to publishing the **complete `02_fmv` output set** —
all 60 trial responses (3 models × 5 trials × 4 stages), all Stage 1–3
dual-judge verdicts, all human-audit verdicts if an audit is
triggered, and all Stage 4 classifications — under the same commit
that publishes `analysis/02_fmv_findings.md`. Selective publication is
forbidden by `CLAUDE.md`.

The author commits to publishing the P1 / P2 / P3 / P4 verdicts
**regardless of direction**. A refutation of P1 (the models induce the
F=mv rules cleanly) is as publishable as confirmation. A refutation of
P3 (mechanical criteria do not reduce judge disagreement) is
explicitly publishable — it would be direct evidence against the
criteria-ambiguity diagnosis that motivated this experiment's design.
