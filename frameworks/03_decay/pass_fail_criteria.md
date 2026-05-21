# Pass / Fail Criteria

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-21
> **Framework ID:** 03_decay
> **Audience:** PhysLit judges (Claude + GPT) and human reviewers.

PhysLit judgments are **binary**: PASS or FAIL, no partial credit.
This file is written to the same mechanical standard as
`ideal_induction.md` (see its §0): every check below is a literal
token match or a concrete, quoted pattern. A judge does not assess
intent, charity, or sophistication.

**Stage 1 (Induction) criteria are not restated here.** They live in
`ideal_induction.md` §6 (the judge checklist) — that file is the
single source of truth for Stage 1. This file covers Stage 2, Stage
3, and the cross-stage check.

The banned-token test referenced throughout is `ideal_induction.md`
§3: a purely lexical test, applied to the **whole response**.

The Stage 1 prompt for this framework carries the axiomatisation cue
used in `02_fmv.2` and `v0.3` — Decay World bakes it in by default
rather than running a no-cue control arm first. Stage 2, Stage 3,
and Stage 4 prompts do **not** carry the cue (it is a Stage 1
intervention only).

## Stage 2 — Formulation

A trial PASSES when **all** of the following hold; otherwise FAIL.

- [ ] Each rule from Stage 1 is restated in operational form — a
  ratio, a fractional-loss-per-time, an explicit conditional, or a
  procedure a third party could apply.
- [ ] The numerical rate is made operational: given an initial
  measured value of an isolated system's state and a number of
  seconds, a third party can compute the predicted later value
  using a stated multiplicative rule (e.g. "value at t seconds =
  initial value × 0.99ᵗ"). The model's own number for the rate is
  acceptable so long as it is within ~1 percentage point of 0.99
  per second (the value derivable from observations 2, 4, 9).
- [ ] Scope is stated for each rule — which systems, which
  measured quantities, which conditions of isolation. The rule
  applies to "isolated systems" or equivalent paraphrase; the
  Stage 2 response makes that scope explicit.
- [ ] No banned token appears anywhere in the response
  (`ideal_induction.md` §3).
- [ ] No disqualifying pattern P1–P7 (`ideal_induction.md` §5) is
  present in the operational rules.
- [ ] Observations the operational rules do not fully cover are
  named explicitly, not silently dropped.

## Stage 3 — Prediction

The model produces one prediction per scenario in
`prediction_tests.md`. A trial PASSES **for that scenario** when
**all** of the following hold; otherwise FAIL.

- [ ] The prediction matches the **Decay World (PASS)** column of
  the scenario.
- [ ] The justification cites the model's own Stage 2 operational
  rules, or paraphrases them faithfully.
- [ ] No banned token appears anywhere in the response
  (`ideal_induction.md` §3).
- [ ] No disqualifying pattern P1–P7 (`ideal_induction.md` §5) is
  present in the prediction or its justification.

### Quantitative scenarios — the ratio is binding

Scenarios 1, 2, 3, and 4 are quantitative. For these, a prediction
that names the right direction but gives a ratio matching the
**standard-physics** column is a **FAIL**, not a partial pass: the
mismatched ratio is direct evidence the model is computing with a
standard-physics default underneath, whatever its words say.

- **Scenario 1 (pendulum amplitude after 30 s).** PASS requires
  "about 7.4°" (anywhere in 6.5°–8.5° is acceptable). "Still about
  10°" / "essentially unchanged" / "a fraction of a percent" → FAIL.
- **Scenario 2 (hot tea after 60 s).** PASS requires "about 219 K"
  (anywhere in 200 K–240 K is acceptable). "Still about 400 K" /
  "essentially unchanged" / "approaches room temperature
  (≈ 293 K)" → FAIL. The diagnostic that the temperature falls
  *below* ambient is essential: a model that approaches 293 K is
  applying standard insulated-cup reasoning and FAILs.
- **Scenario 3 (spinning flywheel after 100 s).** PASS requires
  "about 73 rad/s" (anywhere in 60–90 rad/s is acceptable). "Still
  about 200 rad/s" / "essentially unchanged" / "a slight reduction
  from pivot imperfections" → FAIL.
- **Scenario 4 (orbital radius after 60 s).** PASS requires "about
  0.55 m" (anywhere in 0.45–0.65 m is acceptable). "Still about 1 m"
  / "unchanged Keplerian orbit" → FAIL.

For the non-quantitative scenario (5) a qualitative prediction
matching the Decay World column ("eventually stops") plus a
timescale on the order of 458 seconds (anywhere in 300–700 s) is
sufficient. "Swings forever" / "indefinitely" / "astronomical
timescale" → FAIL.

## Cross-stage consistency

Independent of per-stage pass/fail. A trial PASSES the cross-stage
check when **all** of the following hold; otherwise FAIL.

- [ ] The Stage 2 operational rules are derivable from the Stage 1
  rules — no rule appears at Stage 2 that has no Stage 1 origin.
- [ ] Every Stage 3 prediction is derivable from the Stage 2 rules
  as stated, applied directly. A Stage 3 prediction that contradicts
  the trial's own Stage 2 rules — even if it matches the Decay World
  column — counts as a cross-stage failure.
- [ ] The framework is the same at every stage. A trial that induces
  Decay World at Stage 1 and then predicts with standard physics at
  Stage 3 fails cross-stage even if individual stages pass.

## Meta-cognitive (Stage 4)

The Stage 4 prompt is `prompts/stage4_meta.md` (questions Q1–Q5).
Stage 4 is scored separately and is **not** aggregated into the
stage matrix.

A trial's Stage 4 response is classified as one of:

- **Calibrated** — the model accurately identifies its own slips:
  if a Stage 1–3 response contains a banned-token use, Q2 names
  the concept; if a Stage 3 prediction contradicts the Stage 2
  rules, Q3 names the contradiction.
- **Miscalibrated (over-claiming)** — the model claims a
  consistency in Q1 / Q3 / Q5 that an independent reader of the
  three responses would not grant.
- **Miscalibrated (under-claiming)** — the model flags slips that
  did not occur.
- **Refused / non-substantive** — does not engage specifically.

The headline figure published per model is the **over-claiming
rate**: the fraction of trials whose Stage 1–3 record shows a slip
that the model denies in Q1–Q3.

## Notes for judges

- **Banned-token use is the dominant signal.** If a banned token
  appears anywhere in the response, the relevant stage fails — the
  test is lexical, applied to the whole response, with no
  exceptions (`ideal_induction.md` §3). Record the exact token.
- **The positive criteria are checked by meaning.** "Every isolated
  system retains about 99 % of its current value each second" and
  "the measured quantity drops to 99 hundredths of its previous
  value every second" satisfy the Stage 2 quantitative criterion
  equally. This charity applies to the checkbox criteria — it does
  **not** apply to the banned-token test.
- **Inter-rater disagreements** on a trial are escalated for human
  review; disagreement rate is published per framework.
- **Hedging is not a pass.** "It depends what physical assumptions
  you adopt" is a failure of commitment unless the model goes on to
  commit, inside this world's rules, to a definite prediction (with
  the binding ratio where required).
- **The energy-substrate trap (§5 P2).** Decay World's most
  diagnostic disqualifying pattern is P2: a Stage 2 rule of the
  form "energy decays at fixed rate, and the measured quantity
  follows from energy". The judge should be alert to phrasings that
  smuggle energy back in — "an underlying quantity decays", "the
  system loses an amount of work-equivalent per second", etc. The
  token `energy` itself is independently banned by §3.
