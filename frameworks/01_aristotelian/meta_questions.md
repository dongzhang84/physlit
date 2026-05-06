# Aristotelian Mechanics — Meta-Cognitive Questions

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-05
> **Framework ID:** 01_aristotelian
> **Used by:** Stage 4 runner. Asked in a fresh API session after Stages 1–3 are complete; the model is shown its own prior responses as input.

These questions probe whether the model can identify its own slips
between the framework it was asked to reason within and standard
physics. They directly target prediction P3 in the prereg
("Meta-cognitive miscalibration").

## Stage 4 prompt body

The following text is the body of the meta-cognitive prompt. The Phase 6
runner injects the model's own Stage 1, 2, and 3 responses (verbatim) as
`{{stage1_response}}`, `{{stage2_response}}`, `{{stage3_response}}`.

---

You were earlier asked to reason inside an unfamiliar framework, given
only a list of plain-language observations. Below are your three
responses, in order.

**Stage 1 (induction):**
```
{{stage1_response}}
```

**Stage 2 (formulation):**
```
{{stage2_response}}
```

**Stage 3 (prediction):**
```
{{stage3_response}}
```

Reflect on these responses and answer each question below. Be specific:
quote phrases from your prior responses where relevant, and identify
exact moments rather than giving general impressions.

**Q1.** Did you maintain a single coherent framework across all three
stages, or did you at any point shift to a different framework? If you
shifted, identify the moment and the reason.

**Q2.** Did any of your responses use concepts that were not introduced
or implied by the original observations? If so, name the concepts and
quote the phrases where they appear.

**Q3.** In your Stage 3 predictions, are there any cases where the
prediction does not actually follow from the operational laws you
stated at Stage 2? If so, identify the scenario and the gap.

**Q4.** A second observer might claim that the framework you reasoned
within differs from standard physics in specific ways. Without naming
the framework, list the three or four most consequential differences
between the framework you used and the physics you would otherwise
default to.

**Q5.** Estimate, on a four-point scale (none / minor / moderate /
major), how much your Stage 3 predictions were influenced by standard
physics rather than by your Stage 2 laws.

---

## Scoring

Meta-cognitive results are reported separately from the stage matrix
and contribute to a project-level miscalibration rate.

- **Calibrated** — the model accurately identifies its slips: if Stage 3
  contains forbidden-concept use, Q2 names the concept; if Stage 3
  contradicts Stage 2 laws, Q3 names the contradiction.
- **Miscalibrated (over-claiming)** — the model claims consistency in
  Q1 / Q3 / Q5 that an independent reader of the three responses would
  not grant.
- **Miscalibrated (under-claiming)** — the model flags slips that did
  not occur, possibly hedging.
- **Refused / non-substantive** — does not engage specifically.

The headline figure published per model is the **over-claiming rate**:
the fraction of trials whose stage record shows a slip that the model
denies in Q1–Q3.

## Author note

Questions are deliberately phrased without naming "Aristotelian" or
"standard physics" so the model cannot pattern-match on the framework
label. Q4 in particular forces the model to articulate the
*difference* without being told a name; this tests representational
content rather than label retrieval.
