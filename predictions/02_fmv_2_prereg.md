# Pre-Registered Predictions for PhysLit — F=mv World, Axiomatisation Control Experiment (`02_fmv.2`)

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `<PENDING>`
- Locked at git tag: `prereg-02_fmv.2-locked`
- Lock timestamp (UTC): `<PENDING>`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `<PENDING>`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST
> NOT be modified.** Any revision requires a new version
> (`02_fmv.3`, …) with its own tag and an explicit "deviation from
> prereg" notice published alongside any results.
>
> The artifact files referenced below are frozen at the locked commit.
> Retrieve them post-lock with `git show prereg-02_fmv.2-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## 0. Relationship to prior PhysLit work

`02_fmv.2` is a **control experiment** on the F=mv framework. It tests
one thing: whether explicitly instructing the tested model to
**axiomatise** its rule set raises the structural-axis (N9–N12) pass
rate.

It exists because `02_fmv.1` exposed a scoping gap. The `02_fmv.1`
structural axis judged each Stage 1 rule set on parsimony (N9),
independence (N10), traceability (N11), and hierarchy (N12) — but the
`02_fmv` Stage 1 induction prompt never asked the model to produce a
parsimonious, non-redundant, hierarchical rule set. It asked only for
"a self-consistent set of rules that explains every observation … as a
numbered list … be specific". The `02_fmv.1` structural result is
therefore a **default-behaviour** measurement — what models do when
not asked to axiomatise — not a capability claim. (N11 traceability is
the exception: "explains every observation" and "do not import
information from outside the list" were in the prompt, so an N11
failure is a failure against an explicit instruction.)

`02_fmv.2` isolates the effect of the instruction. It is a
**single-variable control experiment**:

- **Control arm** — the 60 `02_fmv` production trials, frozen at
  `prereg-02_fmv-locked`, with the structural verdicts established in
  `02_fmv.1` (post-audit) and the content verdicts established in
  `02_fmv` (post-audit). No new control trials are run.
- **Treatment arm** — a **new** run of the full F=mv four-stage
  protocol, identical to `02_fmv` in every respect except that the
  **Stage 1 induction prompt carries an added axiomatisation
  instruction** (§1).

The predictions of this round are numbered P1–P2; they are **distinct
from** the `02_fmv` content round's P1–P4 and the `02_fmv.1`
structural round's P1–P2. `02_fmv.2` runs new tested-model trials (the
treatment arm) and does **not** modify any `02_fmv` or `02_fmv.1`
trial, prompt, or verdict.

## 1. Scope

### 1.1 Design — a single-variable control experiment

The only manipulated variable is the **Stage 1 induction prompt**. The
treatment arm's Stage 1 prompt is the `02_fmv` Stage 1 prompt
(`frameworks/02_fmv/prompts/stage1_induction.md`) with one added
instruction, inserted into the task paragraph. The control arm is the
`02_fmv` trials, which used the Stage 1 prompt without that
instruction.

**The added instruction (the treatment).** Inserted between the
"Your task" sentence and the "Return your rules" sentence of the
Stage 1 prompt, verbatim:

> Aim for the **smallest** set of rules that still explains every
> observation. Do not state as a separate rule anything that already
> follows from rules you have given; if one rule is a special case or
> a consequence of another, say so instead of listing it on its own.
> Prefer a few general rules over a long list of specific ones.

This instruction is deliberately **natural-language induction
guidance**, not the N9–N12 judge rubric. It names no criterion, no
rule-count threshold, and no scoring scheme; it does not tell the
model it will be graded on structure. It is the cue a physics teacher
would give. The experiment therefore tests whether models respond to
a **normal prompt cue**, not whether they can satisfy the rubric when
handed it. The frozen treatment prompt is
`frameworks/02_fmv/prompts/stage1_induction_axiomatised.md` (§4).

### 1.2 What is held identical to `02_fmv`

Every element below is unchanged from `prereg-02_fmv-locked`; the
treatment arm differs from the control arm in the Stage 1 prompt and
nothing else:

- The 12 observations (`frameworks/02_fmv/observations.md`).
- The three tested models and their pinned versions —
  `claude-opus-4-7`, `gpt-5.5-2026-04-23`, `gemini-3.1-pro-preview`.
- N = 5 trials per model; the four-stage protocol (induction →
  formulation → prediction → meta); a fresh API client and new
  session UUID per stage; no context reuse across stages.
- `temperature = 0` requested on every call.
- The Stage 2, Stage 3, and Stage 4 prompts — used verbatim. In
  particular Stage 2 still asks the model to restate its rules
  "mirroring the numbering you used at Stage 1"; this is unchanged so
  that the treatment is confined to Stage 1.
- The §3 banned-token list.

### 1.3 Judging

- **Content axis** — each treatment Stage 1/2/3 response is scored by
  the two content judges (`claude-opus-4-7`, `gpt-5.5-2026-04-23`)
  using the `02_fmv` judge prompts frozen at `prereg-02_fmv-locked`. A
  trial's content axis is PASS iff its Stage 1, 2, and 3 are all PASS.
- **Structural axis** — each treatment trial's **Stage 1** rule set
  (Stage 2 as context only, never counted) is scored by the two
  structural judges using the structural criteria
  (`frameworks/02_fmv/structural_criteria.md`) and the structural
  judge prompt (`frameworks/02_fmv/prompts/judge_structural.md`),
  both frozen at `prereg-02_fmv.1-locked`.
- **Dual-judge, human-audit resolution.** Where the two judges agree,
  that is the verdict; where they disagree, the case is resolved by
  **human audit**. The dual-judge disagreement rate (IRR) is published
  for both axes; an IRR above 25 % triggers a full human audit before
  release. No LLM disagree-resolver feeds a canonical verdict.

### 1.4 Out of scope, by explicit decision

- Re-running the control arm — the `02_fmv` trials are frozen and
  reused as-is.
- Re-judging or modifying any `02_fmv` or `02_fmv.1` verdict.
- Changing the structural criteria, the content criteria, the judge
  prompts, or any Stage 2/3/4 prompt.
- An axiomatisation treatment on the Aristotelian framework — a
  possible later round, not this one.
- LLM disagree-resolver agents for the canonical resolution;
  disagreements are resolved by human audit only.
- Stage 4 (meta) judging — the treatment arm runs Stage 4 so that it
  is a complete mirror of `02_fmv`, and the Stage 4 responses are
  committed, but no prediction of this round depends on the meta axis,
  so meta-judging is not performed.

### 1.5 Budget

Estimated ≤ $30 USD: 60 treatment production calls + 120 judge calls
(content dual-judge on Stage 1–3 = 90; structural dual-judge = 30). No
control-arm calls (reused); no resolver calls.

## 2. Predictions

The control-arm baselines, fixed by prior locked rounds:

- **Control structural-axis PASS = 5 / 15** — `02_fmv.1` post-audit
  (`analysis/02_fmv_1_findings.md`).
- **Control content-axis PASS = 9 / 15** — `02_fmv` post-audit
  content-only verdict (`analysis/02_fmv_findings.md`).

### P1 — The axiomatisation instruction raises the structural pass rate

**Prediction.** The treatment arm's structural-axis pass rate is
**greater than** the control arm's 5 / 15.

**Rationale.** `02_fmv.1` found that, unprompted, frontier models
produce bloated, redundant rule sets (structural PASS only 5/15;
GPT 0/5). The `02_fmv.2` Discussion (`02_fmv_1_report.md` §2.7)
argued this is a self-organisation gap — the models *know* the
correct rules but do not, by default, compress them into a
parsimonious system. If that reading is right, a natural-language
instruction to do so should lift the structural pass rate: the
treatment supplies the cue the default prompt withheld. The added
instruction maps onto N9 (parsimony), N10 (independence), and N12
(hierarchy); N11 (traceability) was already cued by the original
prompt and is not a target of the treatment.

**Scoring.**

- **Confirmed:** treatment structural-axis PASS > 5/15 (i.e. ≥ 6/15).
- **Refuted:** treatment structural-axis PASS ≤ 5/15 — the
  instruction does not help, which would be evidence the structural
  shortfall is a capability limit rather than a default-behaviour one.

The per-model breakdown and the per-criterion (N9–N12) movement are
reported alongside the verdict, so that a marginal one-trial shift is
visible and not over-read.

### P2 — Content competence does not degrade under the treatment

**Prediction.** The treatment arm's content-axis pass rate is **not
materially lower** than the control arm's 9 / 15.

**Rationale.** This is a confound control. If instructing the model to
minimise its rule set causes it to drop a rule and lose observation
coverage, a structural-axis gain in P1 would be confounded — the model
would have "axiomatised" by sacrificing content, not by organising it
better. P2 verifies that the treatment's structural effect, if any, is
not bought with content loss. A material drop invalidates the clean
causal reading of P1.

**Scoring.**

- **Confirmed:** treatment content-axis PASS ≥ 8/15 — within one trial
  of the control's 9/15. A one-trial gap between two independent
  N = 15 samples is within sampling noise; no material degradation.
- **Refuted:** treatment content-axis PASS ≤ 7/15 — content degraded;
  P1's structural comparison is then reported as potentially
  confounded by content loss, and interpreted accordingly.

## 3. Scoring procedure

1. The treatment arm is run: 3 models × N = 5 × 4 stages = 60 trials,
   each stage on a fresh API client with a new session UUID,
   `temperature = 0`, using the treatment Stage 1 prompt
   (`stage1_induction_axiomatised.md`) and the unchanged Stage 2/3/4
   prompts, all frozen at the locked commit.
2. Content judging: both content judges score each treatment
   Stage 1/2/3 response with the `02_fmv` judge prompts. Per-trial
   content axis = Stage 1 ∧ Stage 2 ∧ Stage 3. The content IRR is
   computed; an IRR above 25 % triggers a human audit.
3. Structural judging: both structural judges score each treatment
   trial's Stage 1 rule set (Stage 2 as context) with the `02_fmv.1`
   structural criteria and judge prompt. The structural IRR is
   computed; an IRR above 25 % triggers a human audit.
4. P1 is computed from the treatment structural-axis PASS count
   against the control's 5/15; P2 from the treatment content-axis
   PASS count against the control's 9/15.
5. The treatment-vs-control comparison is reported in full: per-model
   structural and content PASS counts, the per-criterion N9–N12
   movement, and the trial-level matrices for both arms.
6. Results are recorded in `analysis/02_fmv_2_findings.md`: the
   per-trial treatment matrix, both IRRs, any human-audit verdicts,
   the P1 / P2 verdicts, and any deviation from this prereg with
   timestamps and rationale.

## 4. Frozen artifacts (referenced by the `prereg-02_fmv.2-locked` tag)

At the locked commit, the contents of the following files are part of
the `02_fmv.2` prereg envelope:

- `frameworks/02_fmv/prompts/stage1_induction_axiomatised.md` — the
  treatment Stage 1 prompt: the `02_fmv` Stage 1 prompt with the §1.1
  axiomatisation instruction added. **The only new artifact.**
- `frameworks/02_fmv/observations.md` — the 12 observations, unchanged.
- `frameworks/02_fmv/prompts/stage2_formulation.md`,
  `stage3_prediction.md`, `stage4_meta.md` — unchanged from `02_fmv`.

Read-only inputs, already frozen at their own tags and not modified by
this round:

- The control-arm trials and content verdicts —
  `prereg-02_fmv-locked`.
- The control-arm structural verdicts, the structural criteria, and
  the structural judge prompt — `prereg-02_fmv.1-locked`.
- The `02_fmv` content judge prompts — `prereg-02_fmv-locked`.

## 5. Publication policy

PhysLit commits to publishing the **complete `02_fmv.2` output set** —
all 60 treatment trials, all judge verdicts, all human-audit verdicts
if an audit is triggered, and the full treatment-vs-control comparison
— under the same commit that publishes `analysis/02_fmv_2_findings.md`.
Selective publication is forbidden by `CLAUDE.md`.

The author commits to publishing the P1 / P2 verdicts **regardless of
direction**. A refutation of P1 (the axiomatisation instruction does
not raise the structural pass rate) is explicitly publishable — it
would be evidence that the structural shortfall is a capability limit,
not a default-behaviour one, which is a stronger and more surprising
result than P1 confirmed. A refutation of P2 (content degrades under
the treatment) is equally publishable — it would itself be a finding:
that frontier models, asked to axiomatise, trade coverage for brevity.
