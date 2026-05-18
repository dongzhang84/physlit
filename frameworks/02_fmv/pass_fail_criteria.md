# Pass / Fail Criteria

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-17
> **Framework ID:** 02_fmv
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

## Stage 2 — Formulation

A trial PASSES when **all** of the following hold; otherwise FAIL.

- [ ] Each rule from Stage 1 is restated in operational form — a
  proportionality, a ranking rule, an explicit conditional, or a
  procedure a third party could apply.
- [ ] The two proportional relations are made quantitative and
  combinable: pace rises in proportion to the push (the doubling of
  observation 4), and pace falls in inverse proportion to heaviness
  (the doubling-halves of observation 5). A third party must be able
  to obtain a pace from a given push and a given heaviness. (Whether
  this is stated as one combined rule or two rules does not matter.)
- [ ] Scope is stated for each rule — which bodies, which kind of
  motion (pushed motion, falling), which conditions.
- [ ] No banned token appears anywhere in the response
  (`ideal_induction.md` §3).
- [ ] No disqualifying pattern P1–P7 (`ideal_induction.md` §5) is
  present in the operational rules.
- [ ] Observations the operational rules do not fully cover are named
  explicitly, not silently dropped.

## Stage 3 — Prediction

The model produces one prediction per scenario in
`prediction_tests.md`. A trial PASSES **for that scenario** when
**all** of the following hold; otherwise FAIL.

- [ ] The prediction matches the **F=mv (PASS)** column of the
  scenario.
- [ ] The justification cites the model's own Stage 2 operational
  rules, or paraphrases them faithfully.
- [ ] No banned token appears anywhere in the response
  (`ideal_induction.md` §3).
- [ ] No disqualifying pattern P1–P7 (`ideal_induction.md` §5) is
  present in the prediction or its justification.

### Quantitative scenarios — the ratio is binding

Scenarios 1, 2, and 4 are quantitative. For these, a prediction that
names the right direction but gives a ratio matching the
**standard-physics** column is a **FAIL**, not a partial pass: the
mismatched ratio is direct evidence the model is computing with
acceleration underneath, whatever its words say.

- **Scenario 1:** PASS requires "about twice D". "About four times D"
  (or any super-linear growth) → FAIL.
- **Scenario 2:** PASS requires "about twice T". "About 1.4 times T"
  (√2 · T), or any sub-linear growth, → FAIL.
- **Scenario 4:** PASS requires a time ratio of about 2 : 1. A ratio
  of about √2 : 1 (≈ 1.4 : 1), or "they finish close together", →
  FAIL, even though the winner (block B) is named correctly.

For the non-quantitative scenarios (3, 5) a qualitative prediction
matching the F=mv column is sufficient; no ratio is required.

## Cross-stage consistency

Independent of per-stage pass/fail. A trial PASSES the cross-stage
check when **all** of the following hold; otherwise FAIL.

- [ ] The Stage 2 operational rules are derivable from the Stage 1
  rules — no rule appears at Stage 2 that has no Stage 1 origin.
- [ ] Every Stage 3 prediction is derivable from the Stage 2 rules as
  stated, applied directly. A Stage 3 prediction that contradicts the
  trial's own Stage 2 rules — even if it matches the F=mv column —
  counts as a cross-stage failure.
- [ ] The framework is the same at every stage. A trial that induces
  the F=mv world at Stage 1 and then predicts with standard physics
  at Stage 3 fails cross-stage even if individual stages pass.

## Meta-cognitive

See `meta_questions.md`. Scored separately; not aggregated into the
stage matrix.

## Notes for judges

- **Banned-token use is the dominant signal.** If a banned token
  appears anywhere in the response, the relevant stage fails — the
  test is lexical, applied to the whole response, with no exceptions
  (`ideal_induction.md` §3). Record the exact token.
- **The positive criteria are checked by meaning.** "Pace is the push
  divided by the heaviness" and "a body's speed is its push shared
  out over how heavy it is" satisfy the Stage 2 quantitative
  criterion equally. This charity applies to the checkbox criteria —
  it does **not** apply to the banned-token test.
- **Inter-rater disagreements** on a trial are escalated for human
  review; disagreement rate is published per framework.
- **Hedging is not a pass.** "It depends which physics you assume" is
  a failure of commitment unless the model goes on to commit, inside
  this world's rules, to a definite prediction.
