# Aristotelian Mechanics — Pass / Fail Criteria

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-05
> **Framework ID:** 01_aristotelian
> **Audience:** PhysLit judges (Claude + GPT) and human reviewers.

PhysLit judgments are **binary**: PASS or FAIL, no partial credit, no
weighting. Stage-level pass requires consistent results across at least
**4 of 5 trials**; trial-level disagreement is reported separately as
an instability signal.

## Stage 1 — Induction

A trial PASSES when **all** of the following hold; otherwise FAIL.

- [ ] The response proposes a set of named or numbered laws (or
  equivalent rules) intended to explain the observations.
- [ ] Every observation in `observations.md` is covered by at least
  one proposed law, either explicitly cited or unambiguously implied.
- [ ] No forbidden concept (see `ideal_induction.md` §"Concepts that
  must NOT appear") is named or used. Naming a concept *only to deny
  its applicability* still counts as use.
- [ ] The proposed laws are mutually consistent: no two laws make
  contradictory claims about the same kind of body in the same
  situation.
- [ ] The laws collectively cover the natural-vs-forced motion
  distinction (N1 of the ideal induction — two-regime distinction) in
  some form.

## Stage 2 — Formulation

A trial PASSES when **all** of the following hold; otherwise FAIL.

- [ ] Each law from Stage 1 is restated in operational form: a
  proportionality, a ranking rule, an explicit conditional, or a
  procedure that a third party could apply.
- [ ] Scope is stated for each law (which bodies, which media, which
  kind of motion).
- [ ] The response either identifies a conserved quantity *consistent
  with Stage 1* or explicitly states that nothing is conserved. It
  does not import a conservation law (energy, momentum) absent from
  Stage 1.
- [ ] No new forbidden concept is introduced relative to Stage 1.
- [ ] Boundary cases are listed; observations not covered are named,
  not silently dropped.

## Stage 3 — Prediction

The model produces one prediction per scenario in `prediction_tests.md`.
A trial PASSES *for that scenario* when **all** of the following hold;
otherwise FAIL.

- [ ] The prediction matches the *Aristotelian (PASS)* column of the
  scenario.
- [ ] The justification cites the model's own Stage 2 operational laws
  (or paraphrases them faithfully).
- [ ] No standard-physics concept appears in the justification, even
  in passing or as a contrast.
- [ ] The numeric or ordinal claim, where applicable (Scenarios 1 and
  3), is qualitatively in the right direction; exact factor matching
  is not required, but the prediction must clearly favour the heavier
  body in the expected ratio sense.

### Scenario-specific notes

**Scenario 3 (two stones in water, weight ratio 2:1).** Qualitative
ranking is **sufficient** for PASS: a prediction of the form "A reaches
the bottom first, B second" is PASS even without a numerical ratio. A
strict-Aristotelian numerical ratio (e.g. ~2:1) is also PASS but **not
required**. Concrete example from the Phase 1.5 dry run (2026-05-08):
Claude Opus 4.7 gave "A first, B second; my rules give only a ranking,
not a numerical relation, so I cannot give a ratio" — PASS.

**Scenario 4 (sealed evacuated chamber, feather released).** Two
PASS modes are accepted, both of which count as valid framework-fidelity
signals:

- *PASS mode A — Reject the scenario.* The model argues that vacuum is
  impossible within this framework (Aristotle, *Physics* IV.8: motion in a
  vacuum would be of indeterminate or infinite speed, hence absurd, hence
  vacuum cannot exist).
- *PASS mode B — Refuse to predict on scope grounds.* The model
  acknowledges that its Stage 2 rules underdetermine the outcome (e.g.
  the medium-resistance rule has no medium to act through) and explicitly
  declines to commit, rather than fall back on standard physics.

A response that combines elements of both modes also PASSes. A response
that gives the standard-physics answer (the feather falls at *g*; equal
fall in vacuum) FAILs.

## Cross-stage consistency

Independent of per-stage pass/fail. A framework PASSES the cross-stage
check when **all** of the following hold; otherwise FAIL.

- [ ] The laws stated at Stage 2 are derivable from the rules
  proposed at Stage 1 (no smuggled additions).
- [ ] Every Stage 3 prediction is derivable from the Stage 2 laws as
  stated, applied directly. A Stage 3 prediction that contradicts the
  Stage 2 laws — even if it matches the Aristotelian column — counts
  as a cross-stage failure.
- [ ] The framework named or implied at each stage is the same. A
  trial that begins inside the Aristotelian framework at Stage 1 and
  drifts to standard physics at Stage 3 fails cross-stage even if
  individual stages pass.

## Meta-cognitive

See `meta_questions.md`. Scored separately, not aggregated into the
stage matrix.

## Notes for judges

- **Forbidden concept use is the dominant signal.** If a forbidden
  concept appears, the trial fails the corresponding stage even if
  every other criterion is satisfied. Both judges should record the
  exact phrase as evidence.
- **Inter-rater disagreements** on a trial are escalated for human
  review. Disagreement rate is published per framework.
- **Hedging is not a pass.** "It depends on the framework you assume"
  is a failure of commitment unless the model goes on to commit
  inside the Aristotelian framework specifically.
