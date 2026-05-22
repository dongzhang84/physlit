# Pre-Registered Predictions for PhysLit — Decay World (`03_decay`)

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `<PENDING>`
- Locked at git tag: `prereg-03_decay-locked`
- Lock timestamp (UTC): `<PENDING>`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `<PENDING>`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST NOT
> be modified.** Any revision requires a new version (`03_decay.1`,
> `03_decay.2`, …) with its own tag and an explicit "deviation from
> prereg" notice published alongside any results.
>
> The artifact files referenced below are frozen at the locked commit.
> Retrieve any of them post-lock with:
> `git show prereg-03_decay-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## 0. Relationship to prior PhysLit work

This is PhysLit's **third framework experiment** and the second
from-scratch new-framework round (after `02_fmv`). It does **not**
modify or reuse any v0.1, v0.2, v0.2.1, v0.3, `02_fmv`, `02_fmv.1`, or
`02_fmv.2` data, prompts, or verdicts. Those rounds are closed and
sealed.

The Decay World was designed to be **harder on the content axis** than
either of the two prior counterfactual worlds tested by PhysLit. The
F=mv World has its post-audit composite content PASS at **9/15** under
the original `02_fmv` round (held at 9/15 under axiomatisation in
`02_fmv.2`). The Aristotelian World has its post-audit composite
content PASS at **5/15** under v0.1 (and **6/15** under v0.3
axiomatised treatment). The Decay World rule binds to the *directly
measured quantity* rather than to a derived "energy", and is universal
across mechanical, thermal, rotational, and orbital domains; both
features force the model to override its strongest standard-physics
priors (conservation of energy; standard dissipative mechanisms). See
`frameworks/03_decay/spec.yaml` rationale field.

**Two methodological choices carried in from the F=mv arc, deliberately.**

1. The Stage 1 axiomatisation cue — byte-for-byte identical to the
   `02_fmv.2` / v0.3 wording — is baked into the **default** Decay
   World Stage 1 prompt. The Decay rule set is parsimonious by
   construction (one universal multiplicative decay), so the
   axiomatisation cue is part of the world's induction-stage scaffold
   rather than a separate treatment arm. The wording is reproduced
   verbatim in §1.2.
2. Stage 1 induction criteria are **mechanical** in the
   `02_fmv` / v0.3 sense — see `frameworks/03_decay/ideal_induction.md`
   §0. The §3 banned-token test is purely lexical; the §5
   disqualifying patterns are concrete claim patterns; the §6 judge
   checklist halts at the first FAIL. No "as a defined quantity"
   qualifier and no intent assessment.

## 1. Scope

PhysLit `03_decay` tests whether three frontier models can **induce,
formulate, apply, and reflect on** the rules of the Decay World
(`frameworks/03_decay/spec.yaml`) — a counterfactual world in which
every isolated system's directly measured state (oscillator amplitude,
absolute temperature, rotation rate, orbital radius) shrinks at a
fixed fractional rate per second, universally across mechanical,
thermal, rotational, and orbital domains — without sliding back to
conservation-of-energy and friction / damping reflexes that saturate
their training data.

### 1.1 Protocol

- **Tested models (3):**
  - Anthropic Claude Opus 4.7 — `claude-opus-4-7`
  - OpenAI GPT-5.5 — `gpt-5.5-2026-04-23`
  - Google Gemini 3.1 Pro — `gemini-3.1-pro-preview`

  Exact version strings are re-verified by
  `scripts/discover_model_versions.py` immediately before the lock; if
  any vendor has published a more specific identifier by lock time,
  the pin is updated and the change is noted here before locking.

- **N = 5 trials per model.** Each trial is a fresh API client with a
  new session UUID. Multi-turn or context reuse across stages is
  forbidden (`CLAUDE.md`, "N=5 trials, fresh sessions").

- **4 stages per trial:** Stage 1 induction → Stage 2 formulation →
  Stage 3 prediction → Stage 4 meta. Each stage is an independent
  fresh session; the runner replays the model's own prior-stage
  responses as input where a stage requires them.

- **Sampling:** every call requests `temperature = 0`, matching the
  v0.1 / `02_fmv` runner. OpenAI and Google honour the parameter;
  Anthropic Opus 4.7 rejects it and runs at its own default — the
  requested value is still recorded. Result files carry the requested
  value (`trial_N_t0.0.json`). No temperature=0.7 secondary pass.

- **Observations are hand-authored.** `03_decay` is registered as a
  Tier 1 simulator framework, but its first production run uses the
  hand-written observation set `frameworks/03_decay/observations.md`.
  The deterministic simulator
  (`physlit.generators.tier1.decay`) is deferred and is **not** part
  of this prereg envelope.

### 1.2 The Stage 1 axiomatisation cue (baked in by default)

The Decay World Stage 1 prompt
(`frameworks/03_decay/prompts/stage1_induction.md`) contains the
following instruction, inserted between the "Your task" sentence and
the "Return your rules" sentence, byte-for-byte identical to the
`02_fmv.2` / v0.3 axiomatisation wording:

> Aim for the **smallest** set of rules that still explains every
> observation. Do not state as a separate rule anything that already
> follows from rules you have given; if one rule is a special case or a
> consequence of another, say so instead of listing it on its own.
> Prefer a few general rules over a long list of specific ones.

This is the **default**, not a treatment arm. The Decay World rule
set is parsimonious by construction (a single universal
multiplicative decay rule). The cue is included so that the
induction-stage instruction matches the structural shape of the
world's correct axiomatisation; no separate unaxiomatised arm is run.

### 1.3 Content axis only

Trials are judged on the content axis (necessary conditions N1–N6,
the §3 banned-token test, and the §5 disqualifying patterns, all in
`frameworks/03_decay/ideal_induction.md`; Stage 2 / Stage 3 criteria
in `frameworks/03_decay/pass_fail_criteria.md`). The structural axis
(the v0.2 N9–N12 layer) is **not** used in this round. The
structural axis was designed against an Aristotelian-shape rule set
and is not directly applicable to a single-rule decay world; an
adapted structural layer for `03_decay` is deferred.

### 1.4 Dual-judge evaluation, human-audit resolution

Each Stage 1–3 response is scored independently by two LLM judges:

- Anthropic Claude Opus 4.7 — `claude-opus-4-7`
- OpenAI GPT-5.5 — `gpt-5.5-2026-04-23`

Where the two judges agree, that is the verdict. Where they
disagree, the case is resolved by **human audit** — as in v0.1, v0.3,
and the `02_fmv` arc. No LLM disagree-resolver agent (no "Agent 1" /
"Agent 2") feeds a canonical verdict; non-canonical Agent-1-style
calibration side analyses are allowed but additive and out of the
prereg envelope. The per-framework dual-judge disagreement rate
(IRR) is published as a methodology-quality indicator; an IRR above
25 % triggers a full human audit before public release
(`CLAUDE.md`, "Inter-rater reliability").

### 1.5 Out of scope, by explicit decision

- The structural axis (N9–N12) and any structural judging.
- LLM disagree-resolver agents for the canonical resolution;
  disagreements are resolved by human audit only.
- The Tier 1 deterministic decay simulator; this round uses the
  hand-written observation set.
- Temperature variation.
- An unaxiomatised Stage 1 control arm. The Decay World's default
  Stage 1 prompt embeds the axiomatisation cue; comparing axiomatised
  vs. unaxiomatised on Decay is a separate future round.
- Any reuse, re-judging, or modification of v0.1, v0.2, v0.2.1, v0.3,
  `02_fmv`, `02_fmv.1`, or `02_fmv.2` data.

### 1.6 Budget

Estimated ≤ $50 USD total (tested models + judges; 3 models × 5
trials × 4 stages + dual-judge on Stages 1–3 and Stage 4 meta
judging). `scripts/estimate_cost.py` runs before the production
batch; per `CLAUDE.md`, a runner estimate above $5 requires explicit
confirmation. Every result file records its actual cost.

### 1.7 Pre-lock dry run

A single-model, N=1 dry run (Claude only) may precede the lock, with
output written to `results/_dryrun/<timestamp>/` and never to
`results/<model>/03_decay/`. Dry-run findings may revise the
artifacts below; the lock happens only after those revisions settle.

## 2. Predictions

Four predictions are committed by this lock. **All four are
directional** — they fix the *sign* of the effect, not a specific
numeric threshold. P1 is anchored on two prior-round baselines; P2,
P3, P4 are anchored on within-round comparisons of failure modes.

The control-arm baselines, fixed by prior locked rounds, are quoted
here for P1 but no numeric threshold is locked against them:

- **F=mv composite content PASS = 9/15** — `02_fmv` post-audit
  (`analysis/02_fmv_findings.md` → resolved per-trial matrix).
- **Aristotelian composite content PASS = 5/15** — v0.1 post-audit
  (`analysis/v0_1_findings.md`).

### P1 — Decay is harder on the content axis than both prior frameworks

**Prediction.** The Decay World **composite content-axis PASS count
(of 15) is strictly less than both** prior counterfactual baselines:
**less than F=mv's 9/15 and less than Aristotelian's 5/15.** A trial's
composite content axis is PASS iff its Stage 1, Stage 2, and Stage 3
are all PASS. No numeric threshold is locked; the prediction is
directional.

**Rationale.** The Decay World was designed to be harder on the
content axis. The rule binds to the directly measured quantity rather
than to a derived "energy", which forces the model to override its
strongest standard-physics prior (conservation of energy); the rule is
universal across multiple domains, which requires cross-domain
induction by parsimony; every standard dissipative mechanism
(friction, drag, viscosity, damping, radiative loss) is explicitly
closed off by the observation setup (vacuum, smooth / polished
contact, no force along motion). A model that reaches for any of
those mechanisms fails the §3 banned-token test by lexical match. If
the Decay World is in fact harder than both priors, its composite
content PASS count must be below both 9/15 and 5/15.

**Scoring.**

- **Confirmed:** treatment composite content-axis PASS is **strictly
  less than 5** (i.e. ≤ 4/15) — below both prior baselines.
- **Refuted:** treatment composite content-axis PASS is **5 or
  more** — *not* below the Aristotelian baseline, hence not below both
  priors. (A PASS count of exactly 5 ties Aristotelian and would be
  reported alongside refutation as a tied-floor case for the
  discussion section.)

PhysLit reports N = 5 per model descriptively and does not claim
statistical significance; the comparison is directional, against
prior locked baselines. Per-model PASS counts (Claude / GPT / Gemini)
are published alongside the headline.

### P2 — Hidden-substrate framing is the modal Stage 1 failure mode

**Prediction.** Among Decay World Stage 1 trials that FAIL on a §5
disqualifying pattern, **the most frequently-cited §5 pattern is P2
(hidden-substrate framing).** The prediction is directional: P2's
count is greater than each of P1, P3, P4, P5, P6, and P7's counts.
No specific count is locked.

**Rationale.** The Decay World's most powerful training-data prior is
that some underlying "energy" or substrate decays, and the directly
measured quantities follow from it by a standard-physics derivation
(amplitude ∝ √energy, etc.). The §5 P2 pattern was deliberately
widened (`ideal_induction.md` §5 P2, in this round's locked envelope)
to catch *any* hidden-substrate framing regardless of name — both the
energy-substrate sub-case (which fails on cross-domain rate mismatch)
and the ad-hoc consistent-exponent sub-case (e.g. "X decays at
0.9801/s, all measured quantities = √X", which FAILs as an
unwarranted relabelling). If the Decay World is in fact a
hidden-substrate trap, that trap should show up as the dominant
disqualifying pattern when the trap is sprung. If some other §5
pattern dominates (P1 contact-mechanism rescue, P5 weight-dependent
rate, etc.), the design hypothesis is mis-targeted.

**Scoring.**

- **Confirmed:** of all §5-pattern citations across the 15 Stage 1
  trials' first-FAIL clause (per the §6 mechanical halt-at-first-FAIL
  procedure), **P2 is cited strictly more times than any other §5
  pattern individually.**
- **Refuted:** some other §5 pattern is cited at least as many times
  as P2 (P2 not the unique modal pattern).
- **Vacuous:** zero Stage 1 trials FAIL on a §5 pattern. In that case
  P2 is reported as vacuous — direct evidence that the hidden-substrate
  trap was not the dominant slip path even when the design assumed it
  would be. Banned-token (§3) FAILs and N1–N6 FAILs are *not* counted
  toward this denominator; this prediction is about the §5
  disqualifying patterns specifically.

Per-pattern citation counts (P1–P7) and the per-model breakdown are
published alongside the headline.

### P3 — Direction-correct, ratio-leaked dominates direction-wrong on quantitative scenarios

**Prediction.** Across the 60 quantitative Stage 3 predictions (15
trials × Scenarios 1, 2, 3, 4), the **"direction-correct,
standard-physics-ratio" failure mode is more frequent than the
"direction-wrong" failure mode.** That is, among the
quantitative-scenario *non-PASS* responses, more name the correct
direction (some decay occurs) but give a standard-physics ratio than
name the wrong direction (e.g. "essentially unchanged", "approaches
ambient", quantity grows). The prediction is directional; no specific
rate is locked.

**Rationale.** Scenarios 1, 2, 3, and 4 are built with ratio binding
in this round's `prediction_tests.md` and `pass_fail_criteria.md`: a
response that names the right direction but gives the standard-physics
ratio is a FAIL. A model that has partially internalised the Decay
World (Stage 2 rules name multiplicative decay) but still
back-derives quantitatively from F=ma / Newton-cooling /
angular-momentum-conservation will land in the
"direction-correct / ratio-leaked" bucket — its words sound
in-framework, but its arithmetic remains standard physics. If the
Decay World's hardest failure mode is the *quantitative* slip
(rather than refusal of the world entirely), the leaked-ratio bucket
should outweigh the direction-wrong bucket. `02_fmv` P4 ran the same
direction-vs-ratio diagnostic on the F=mv quantitative scenarios and
was REFUTED at 0/45; this round's analogue is therefore *not* a
percentage threshold inherited from `02_fmv` P4 but a within-round
ordering against a different failure mode (direction-wrong), making
the prediction sharper on a different, decay-specific cleavage.

**Scoring.** Each Stage 3 quantitative prediction is classified into
exactly one of three buckets:

- **decay-correct** — direction and ratio both within the Decay
  World's PASS range (`pass_fail_criteria.md`).
- **direction-correct, ratio-leaked** — the prediction names the
  correct direction (something decays) but gives a standard-physics
  ratio or any ratio outside the Decay PASS range. **This bucket
  also captures predictions that name the correct direction but
  decline to commit to a specific quantitative value** — a
  no-quantitative-commit response is at least as far from
  `decay-correct` as a wrong ratio, and the prediction-stage prompt
  explicitly forbids hedging to a merely directional answer.
- **direction-wrong** — the prediction does not name a decay
  (responses such as "essentially unchanged", "approaches some
  ambient", or the quantity grows / oscillates without net decline).

- **Confirmed:** count(direction-correct, ratio-leaked) **strictly
  greater than** count(direction-wrong) across the 60 quantitative
  predictions.
- **Refuted:** count(direction-correct, ratio-leaked) **≤**
  count(direction-wrong).
- **Vacuous:** all 60 quantitative predictions land in the
  decay-correct bucket. In that case both non-PASS buckets are
  empty; P3 is reported as vacuous, which would itself be a striking
  result (the models fully internalised cross-domain
  multiplicative decay at the ratio level).

Per-scenario and per-model breakdowns are published alongside the
headline.

### P4 — Meta-cognitive over-claiming outweighs correct self-identification

**Prediction.** Among Decay World trials with at least one Stage 1–3
audit-FAIL, the Stage 4 reflection **over-claims** (denies or fails
to identify a slip that the trial's own stage record shows) **more
often than it correctly identifies** the slip. The prediction is
directional; no specific rate is locked.

**Rationale.** v0.1 P3 (Aristotelian) found a 70 % over-claiming rate
post-audit; `02_fmv` P2 (F=mv) found a 66.7 % over-claiming rate
post-audit, both confirming a majority-over-claim pattern. The Decay
World is more conceptually unfamiliar than either prior framework, so
specific slips (an energy-substrate rescue, a friction-shaped
mechanism, a per-cycle rate confused with per-second) may be harder
to self-identify in Stage 4 than the comparatively concrete slips of
prior rounds. If over-claiming continues to be the modal Stage 4
posture, P4 is confirmed. If models on the Decay World correctly
identify their own slips more often than they deny them, P4 is
refuted, which would be the first within-PhysLit evidence of
meta-cognitive calibration improving on a *harder* framework — a
publishable finding either way.

**Scoring.** Over-claiming is classified per the Stage 4
meta-cognitive rubric in
`frameworks/03_decay/pass_fail_criteria.md` ("Meta-cognitive (Stage
4)") and the judge prompt
`frameworks/03_decay/prompts/judge_meta.md` (yes / no / vacuous).

- **Confirmed:** count(over-claim = yes) **strictly greater than**
  count(over-claim = no) across trials with at least one Stage 1–3
  audit-FAIL.
- **Refuted:** count(over-claim = yes) **≤** count(over-claim = no).
- **Vacuous:** zero trials contain any Stage 1–3 audit-FAIL (every
  trial PASSes all three stages). In that case the denominator is
  empty and P4 cannot be evaluated; it is reported as vacuous
  alongside the P1 result, which would itself be strong evidence
  against this round's design hypothesis.

Per-model over-claim counts (Claude / GPT / Gemini) are published
alongside the headline.

## 3. Scoring procedure

1. Production trials are run: 3 models × 5 trials × 4 stages, fresh
   API client + new session UUID per stage, `temperature = 0`, using
   the four model-facing prompts frozen at the locked commit
   (`frameworks/03_decay/prompts/stage{1,2,3,4}_*.md`). Every prompt
   sent and every response received is committed to
   `results/<model>/03_decay/<stage>/trial_N_t0.0.json`, including any
   API-side failure record. Selective publishing is forbidden.
2. Each Stage 1–3 response is scored by both content judges
   independently, using the four `03_decay`-specific judge prompts
   frozen at the locked commit and the criteria files
   `frameworks/03_decay/ideal_induction.md` and
   `frameworks/03_decay/pass_fail_criteria.md`.
2a. **Mechanical evidence post-check.** For every judge verdict
   whose stated FAIL clause is a §3 banned-token citation, the
   ``physlit.judges.evidence_check`` module (frozen at the locked
   commit) verifies that the cited evidence substring actually
   appears in the trial response (case-insensitive, normalising
   whitespace). Verdicts whose cited §3 evidence cannot be located
   in the response are flagged ``judge_fabrication = true`` and
   routed to human audit on the same footing as a dual-judge
   disagreement, regardless of whether the other judge agrees on
   the verdict-level outcome. This is a defence against the OpenAI
   judge §3 fabrication observed in the dry-run; see
   `analysis/03_decay_dryrun_findings.md` §6 (Gap 4).
3. Per-stage classification = the two judges' agreed verdict.
   Disagreements are recorded, the Stage 1–3 dual-judge IRR is
   computed, and — per `CLAUDE.md` and prior-round practice — every
   disagree case is resolved by human audit before any public
   release; if IRR exceeds 25 % a full audit is mandatory. The audit
   verdicts are committed.
4. Stage 4 responses are classified per the Meta-cognitive rubric in
   `pass_fail_criteria.md` by both judges; Stage 4 disagreements are
   also resolved by human audit.
5. P1 is computed from the composite content-axis PASS count
   (S1 ∧ S2 ∧ S3) against the F=mv 9/15 and Aristotelian 5/15
   baselines.
6. P2 is computed from the §5-pattern citation distribution across
   Stage 1 first-FAIL clauses (per the §6 mechanical halt-at-first-FAIL
   procedure).
7. P3 is computed from the three-way classification of the 60
   quantitative-scenario predictions (Scenarios 1, 2, 3, 4 across the
   15 trials).
8. P4 is computed from the Stage 4 over-claim classifications,
   restricted to trials with at least one Stage 1–3 audit-FAIL.
9. The findings document (`analysis/03_decay_findings.md`) records:
   the per-trial stage matrix; the dual-judge IRR; any human-audit
   verdicts; the §5-pattern citation distribution; the
   quantitative-scenario three-way classification; the Stage 4
   over-claim classification; the P1 / P2 / P3 / P4 verdicts; and any
   deviation from this prereg, with timestamps and rationale.

## 4. Frozen artifacts (referenced by the `prereg-03_decay-locked` tag)

At the locked commit, the contents of the following files are part of
the `03_decay` prereg envelope and must not change without a new
prereg version:

- `frameworks/03_decay/spec.yaml`
- `frameworks/03_decay/observations.md` — the model-facing observation
  set (the `## Observations` section is what the runner injects)
- `frameworks/03_decay/ideal_induction.md` — Stage 1 judge criteria
  (N1–N6, the §3 banned-token test, the §5 disqualifying patterns
  P1–P7, the §6 6-step judge checklist)
- `frameworks/03_decay/pass_fail_criteria.md` — Stage 2 / Stage 3 /
  cross-stage criteria and the Stage 4 meta rubric
- `frameworks/03_decay/prediction_tests.md` — the five Stage 3
  scenarios with ratio binding on Scenarios 1–4 and qualitative +
  timescale binding on Scenario 5
- `frameworks/03_decay/prompts/stage1_induction.md` — the model-facing
  Stage 1 prompt with the §1.2 axiomatisation cue baked in
- `frameworks/03_decay/prompts/stage2_formulation.md`
- `frameworks/03_decay/prompts/stage3_prediction.md`
- `frameworks/03_decay/prompts/stage4_meta.md`
- the four `03_decay`-specific content-judge prompts (the v0.1 global
  `prompts/judge_*.md` and the `02_fmv` judge prompts are **not**
  reused — the Decay World banned-token set and §5 pattern list
  differ from both):
  `frameworks/03_decay/prompts/judge_stage1.md`,
  `frameworks/03_decay/prompts/judge_stage2.md`,
  `frameworks/03_decay/prompts/judge_stage3.md`,
  `frameworks/03_decay/prompts/judge_meta.md`
- `src/physlit/judges/evidence_check.py` — the mechanical post-check
  module invoked at scoring step 2a above. Its source is part of the
  prereg envelope so that the substring-verification logic is fixed
  in advance of the production run.

The `.zh.md` translation aids (e.g. `observations.zh.md`) are **not**
part of the envelope; on any discrepancy the English files govern.

The v0.1, v0.2, v0.2.1, v0.3, `02_fmv`, `02_fmv.1`, and `02_fmv.2`
prereg envelopes are **not** modified by this experiment.

## 5. Publication policy

PhysLit commits to publishing the **complete `03_decay` output set** —
all 60 trial responses (3 models × 5 trials × 4 stages), all Stage 1–3
dual-judge verdicts, all human-audit verdicts, and all Stage 4
classifications — under the same commit that publishes
`analysis/03_decay_findings.md`. Selective publication is forbidden
by `CLAUDE.md`.

The author commits to publishing the P1 / P2 / P3 / P4 verdicts
**regardless of direction**. A refutation of P1 (the Decay World is
not harder on the content axis than both priors) is as publishable as
confirmation — it would be evidence that the design hypothesis behind
this round (a quantity-bound, cross-domain universal decay is harder
than a derived-quantity F=mv) does not hold, which is a publishable
finding. A refutation of P2 (hidden-substrate framing is not the
modal §5 pattern) would directly recalibrate which slip the round was
designed to elicit. A refutation of P3 (direction-correct,
ratio-leaked does not dominate direction-wrong on quantitative
scenarios) would be evidence that the Decay World's failure mode is
*refusal of the world*, not *quantitative back-derivation from
standard physics* — also publishable. A refutation of P4 (Stage 4
correctly self-identifies more often than it over-claims) would be
the first within-PhysLit evidence of meta-cognitive calibration
improving on a harder framework.
