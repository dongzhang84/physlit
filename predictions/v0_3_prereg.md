# Pre-Registered Predictions for PhysLit — v0.3 (Aristotelian Axiomatisation Control)

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `41c11fe8d1f92c2352b14585036dd24774db2f06`
- Locked at git tag: `prereg-v0.3-locked`
- Lock timestamp (UTC): `2026-05-20T16:28:12Z`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `7a0c6c143f4ca5c14fa75f5f628179a7d1b07e049f8ad4afa5f9bbee0f0f02f7`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST
> NOT be modified.** Any revision requires a new version
> (`v0.3.1`, …) with its own tag and an explicit "deviation from
> prereg" notice published alongside any results.
>
> The artifact files referenced below are frozen at the locked commit.
> Retrieve them post-lock with `git show prereg-v0.3-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## 0. Relationship to prior PhysLit work

`v0.3` is a **single-variable control experiment** on the Aristotelian
framework. It is the **direct parallel of `02_fmv.2`** on the F=mv
framework, with one purpose: test whether the axiomatisation effect
established on F=mv (`02_fmv.2`: structural pass rate 5/15 → 11/15,
P1 STRONGLY CONFIRMED) **generalises across frameworks** when the same
natural-language instruction is applied to a different counterfactual.

The control arm reuses the existing v0.1 production trials, frozen at
`prereg-v0.1-locked`, with the content verdicts from v0.1
(audit-resolved, `analysis/v0_1_findings.md`) and the structural
verdicts from v0.2 (audit-resolved, `analysis/v0_2_findings.md`). No
control trial is re-run; no prior verdict is modified.

The treatment arm is a **new** four-stage run of 3 models × N=5 = 60
trials, identical to v0.1 in every respect except the Stage 1
induction prompt (§1).

**The treatment instruction is byte-for-byte identical to the
`02_fmv.2` instruction.** This is the load-bearing methodological
commitment of this round: cross-framework generalisation can only be
claimed if the intervention is the *same intervention*. The "don't
introduce forces not present in the observations" refinement raised by
`02_fmv.2`'s Finding 4 (Claude t2 P3 fabrication under parsimony
pressure) is **deliberately not adopted here**; that refinement is
deferred to a separate future round.

The predictions of this round are numbered P1–P2; they are **distinct
from** v0.1's P1–P4 and v0.2's V1–V2. v0.3 runs new tested-model
trials (the treatment arm) and does **not** modify any v0.1, v0.2,
`02_fmv`, `02_fmv.1`, or `02_fmv.2` trial, prompt, or verdict.

The eventual report will include a **cross-framework comparison** —
Aristotelian default-vs-instructed against F=mv default-vs-instructed
— as the central deliverable of the F=mv + Aristotelian
axiomatisation arc.

## 1. Scope

### 1.1 Design — a single-variable control experiment

The only manipulated variable is the **Stage 1 induction prompt**. The
treatment arm's Stage 1 prompt is the v0.1 global Stage 1 prompt
(`prompts/stage1_induction.md`) with one added instruction, inserted
into the task paragraph. The control arm is the v0.1 trials, which
used the Stage 1 prompt without that instruction.

### 1.2 The added instruction — byte-for-byte identical to `02_fmv.2`

Inserted between the "Your task" sentence and the "Return your rules"
sentence of the Stage 1 prompt, verbatim:

> Aim for the **smallest** set of rules that still explains every
> observation. Do not state as a separate rule anything that already
> follows from rules you have given; if one rule is a special case or
> a consequence of another, say so instead of listing it on its own.
> Prefer a few general rules over a long list of specific ones.

This wording is the same as `02_fmv.2`'s frozen treatment instruction
(`frameworks/02_fmv/prompts/stage1_induction_axiomatised.md`), to the
character. The cross-framework comparison is meaningful only if the
intervention is identical; therefore the instruction is **not**
amended here, even though `02_fmv.2`'s Finding 4 surfaced a refinement
worth eventually incorporating.

The frozen treatment prompt for this round is
`frameworks/01_aristotelian/prompts/stage1_induction_axiomatised.md`
(§4). It is the v0.1 global Stage 1 prompt with the paragraph above
inserted at the marked location, and nothing else.

### 1.3 What is held identical to v0.1

Every element below is unchanged from `prereg-v0.1-locked`; the
treatment arm differs from the control arm in the Stage 1 prompt and
nothing else:

- The Aristotelian observation set
  (`frameworks/01_aristotelian/observations.md`).
- The three tested models and their pinned versions —
  `claude-opus-4-7`, `gpt-5.5-2026-04-23`, `gemini-3.1-pro-preview`.
- N = 5 trials per model; the four-stage protocol (induction →
  formulation → prediction → meta); a fresh API client and new
  session UUID per stage; no context reuse across stages.
- `temperature = 0` requested on every call.
- The Stage 2, Stage 3, and Stage 4 prompts (the v0.1 global
  templates) — used verbatim. In particular Stage 2 still asks the
  model to restate its rules mirroring the Stage 1 numbering; this is
  unchanged so that the treatment is confined to Stage 1.
- The v0.1 banned-concept list (`ideal_induction.md` §3) and the v0.1
  pass/fail criteria.

### 1.4 Judging

- **Content axis** — each treatment Stage 1/2/3 response is scored by
  the two content judges (`claude-opus-4-7`, `gpt-5.5-2026-04-23`)
  using the v0.1 judge prompts (`prompts/judge_stage1.md`,
  `judge_stage2.md`, `judge_stage3.md`) and the v0.1 criteria
  (`frameworks/01_aristotelian/ideal_induction.md`,
  `pass_fail_criteria.md`, `prediction_tests.md`), frozen at
  `prereg-v0.1-locked`. A trial's content axis is PASS iff its Stage
  1, 2, and 3 are all PASS.
- **Structural axis** — each treatment trial's **Stage 1** rule set
  (Stage 2 as context only, never counted) is scored by the two
  structural judges using the v0.2 structural criteria
  (`frameworks/01_aristotelian/structural_criteria.md`) and the v0.2
  structural judge prompt (`prompts/judge_structural.md`), frozen at
  `prereg-v0.2-locked`.
- **Dual-judge, human-audit resolution.** Where the two judges agree,
  that is the verdict; where they disagree, the case is resolved by
  **human audit**. Each axis's IRR is published; an IRR above 25 %
  triggers a full human audit before release. No LLM disagree-resolver
  feeds a canonical verdict.

### 1.5 Out of scope, by explicit decision

- Re-running the control arm — the v0.1 trials are frozen and reused
  as-is.
- Re-judging or modifying any v0.1, v0.2, `02_fmv`, `02_fmv.1`, or
  `02_fmv.2` verdict.
- Changing the structural criteria, the content criteria, the judge
  prompts, or any Stage 2/3/4 prompt.
- Amending the treatment instruction (e.g. "don't introduce forces not
  in the observations") — the cross-framework comparison requires
  byte-for-byte identical wording to `02_fmv.2`. A refined-instruction
  round is a separate future prereg.
- LLM disagree-resolver agents for the canonical resolution;
  disagreements are resolved by human audit only.
- Stage 4 (meta) judging — the treatment arm runs Stage 4 so that it
  is a complete mirror of v0.1, and the Stage 4 responses are
  committed, but no prediction of this round depends on the meta axis,
  so meta-judging is not performed.

### 1.6 Budget

Estimated ≤ $30 USD: 60 treatment production calls + 120 judge calls
(content dual-judge on Stage 1-3 = 90; structural dual-judge = 30). No
control-arm calls (reused); no resolver calls (non-canonical Agent 1 /
Agent 2 side analyses are allowed but additive and out of the prereg
envelope).

## 2. Predictions

The control-arm baselines, fixed by prior locked rounds:

- **Control structural-axis PASS = 8 / 15** — v0.2 post-audit
  (`analysis/v0_2_findings.md` → audit-resolved structural column).
- **Control content-axis PASS = 5 / 15** — v0.1 post-audit
  content-only verdict, S1 ∧ S2 ∧ S3 (`analysis/v0_1_findings.md`).
- **Control composite PASS = 2 / 15** — Claude t1 and Gemini t2.

### P1 — The axiomatisation instruction raises the structural pass rate

**Prediction.** The treatment arm's structural-axis pass rate is
**greater than** the control arm's 8/15.

**Rationale.** v0.2 found that, unprompted, the three models produce
structurally-mixed Aristotelian rule sets (structural PASS 8/15; GPT
0/5). `02_fmv.2` showed that, on F=mv, a natural-language
axiomatisation instruction raises structural PASS from 5/15 to 11/15
(+6 trials; STRONGLY CONFIRMED in that prereg's tier scheme). If the
axiomatisation effect generalises across frameworks, the same
instruction on Aristotelian should also lift the structural pass rate
above its 8/15 baseline.

**Scoring.** The verdict is three-tier, fixed here so that the
magnitude of any effect is interpreted by a pre-committed rule, not
post-hoc. The control baseline is 8/15 (substantially higher than
F=mv's 5/15 control), so the `02_fmv.2` "doubling" threshold does not
apply; the bands are anchored on **absolute lift** matched to the
`02_fmv.2` net structural improvement (+6 trials would saturate; +5
trials matches the `02_fmv.2` STRONGLY tier directly).

- **Strongly confirmed:** treatment structural-axis PASS ≥ 13/15 — an
  absolute lift of ≥ 5 trials, matching or exceeding the
  `02_fmv.2` structural lift.
- **Directionally confirmed:** treatment structural-axis PASS is
  9–12/15 — the sign is correct (the instruction helped) but the lift
  is smaller than on F=mv. In this band the **per-model and
  per-criterion (N9–N12) breakdown is the primary reading**: the
  verdict is reported together with whether the gain is broad
  (present in all three models) or concentrated (one model), and
  which criteria moved.
- **Refuted:** treatment structural-axis PASS ≤ 8/15 — the
  instruction did not raise the structural pass rate above the
  control baseline, which would be evidence the axiomatisation effect
  observed on F=mv does not generalise to the Aristotelian framework.

PhysLit reports N = 5 per model descriptively and does not claim
statistical significance; the thresholds above are descriptive
magnitude bands, not the output of an inferential test. If P2 is
Refuted (content degraded under the treatment), any non-Refuted P1
tier is additionally reported as potentially confounded by content
loss.

### P2 — Content competence does not degrade under the treatment

**Prediction.** The treatment arm's content-axis pass rate is **not
materially lower** than the control arm's 5/15.

**Rationale.** This is the same confound-control as in `02_fmv.2`. If
instructing the model to minimise its rule set causes it to drop a
rule and lose observation coverage, a structural-axis gain in P1 would
be confounded — the model would have "axiomatised" by sacrificing
content. P2 verifies that the structural effect, if any, is not bought
with content loss. A material drop invalidates the clean causal
reading of P1. (On `02_fmv.2`, content held exactly at the control's
9/15 under the same instruction.)

**Scoring.**

- **Confirmed:** treatment content-axis PASS ≥ 4/15 — within one trial
  of the control's 5/15. A one-trial gap between two independent
  N = 15 samples is within sampling noise; no material degradation.
- **Refuted:** treatment content-axis PASS ≤ 3/15 — content degraded;
  P1's structural comparison is then reported as potentially
  confounded by content loss, and interpreted accordingly.

## 3. Scoring procedure

1. The treatment arm is run: 3 models × N = 5 × 4 stages = 60 trials,
   each stage on a fresh API client with a new session UUID,
   `temperature = 0`, using the treatment Stage 1 prompt
   (`stage1_induction_axiomatised.md`) and the unchanged v0.1
   Stage 2/3/4 prompts, all frozen at the locked commit.
2. Content judging: both content judges score each treatment
   Stage 1/2/3 response with the v0.1 judge prompts. Per-trial
   content axis = Stage 1 ∧ Stage 2 ∧ Stage 3. The content IRR is
   computed; an IRR above 25 % triggers a human audit.
3. Structural judging: both structural judges score each treatment
   trial's Stage 1 rule set (Stage 2 as context) with the v0.2
   structural criteria and judge prompt. The structural IRR is
   computed; an IRR above 25 % triggers a human audit.
4. P1 is computed from the treatment structural-axis PASS count
   against the control's 8/15; P2 from the treatment content-axis
   PASS count against the control's 5/15.
5. The treatment-vs-control comparison is reported in full: per-model
   structural and content PASS counts, the per-criterion N9–N12
   movement, and the trial-level matrices for both arms.
6. The **cross-framework comparison** — Aristotelian
   default-vs-instructed alongside F=mv default-vs-instructed — is
   computed as the central deliverable of this round and reported in
   `analysis/v0_3_report.md`.
7. Results are recorded in `analysis/v0_3_findings.md`: the per-trial
   treatment matrix, both IRRs, any human-audit verdicts, the
   P1 / P2 verdicts, and any deviation from this prereg with
   timestamps and rationale.

## 4. Frozen artifacts (referenced by the `prereg-v0.3-locked` tag)

At the locked commit, the contents of the following files are part of
the v0.3 prereg envelope:

- `frameworks/01_aristotelian/prompts/stage1_induction_axiomatised.md`
  — the treatment Stage 1 prompt: the v0.1 global Stage 1 prompt with
  the §1.2 axiomatisation instruction added at the marked location.
  **The only new artifact.** Wording byte-for-byte identical to
  `frameworks/02_fmv/prompts/stage1_induction_axiomatised.md`.
- `frameworks/01_aristotelian/observations.md` — the Aristotelian
  observation set, unchanged.

Read-only inputs, already frozen at their own tags and not modified by
this round:

- The control-arm trials and content verdicts — `prereg-v0.1-locked`.
- The control-arm structural verdicts, the v0.1 content judge prompts,
  and the v0.2 structural criteria + judge prompt — `prereg-v0.1-locked`
  and `prereg-v0.2-locked`.
- The v0.1 Stage 2/3/4 global prompts (`prompts/stage2_formulation.md`,
  `stage3_prediction.md`, `stage4_meta.md`) — `prereg-v0.1-locked`.

## 5. Publication policy

PhysLit commits to publishing the **complete v0.3 output set** — all
60 treatment trials, all judge verdicts, all human-audit verdicts if
an audit is triggered, the full treatment-vs-control comparison, and
the cross-framework comparison against `02_fmv.2` — under the same
commit that publishes `analysis/v0_3_findings.md`. Selective
publication is forbidden by `CLAUDE.md`.

The author commits to publishing the P1 / P2 verdicts **regardless of
direction**. A refutation of P1 (the axiomatisation instruction does
not raise the structural pass rate on Aristotelian) is explicitly
publishable — it would be evidence the axiomatisation effect observed
on F=mv does **not** generalise to a different framework, which is a
stronger and more informative result for the paper than P1 confirmed.
A refutation of P2 (content degrades under the treatment) is equally
publishable — it would itself be a finding, especially in light of
`02_fmv.2`'s clean content-flat result.
