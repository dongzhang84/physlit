---
version: v1
stage: judge_stage3
description: Stage 3 (02_fmv) prediction judging — per-scenario PASS/FAIL against prediction_tests.md; ratio binding on Scenarios 1/2/4.
---
You are an expert judge evaluating one **Stage 3 (Prediction)
response** from a tested LLM in the PhysLit physics-literacy
benchmark, framework the F=mv World. You are one of two independent
judges; do not attempt to coordinate. Apply the criteria
**mechanically**.

The Stage 3 response contains **five predictions, one per scenario**.
Judge each scenario independently.

This is a **counterfactual world**: the correct answer is *not* the
standard-physics answer. The PASS answer for each scenario is the
F=mv column of `prediction_tests.md`, reproduced below as the answer
key.

---

## Answer key — `frameworks/02_fmv/prediction_tests.md`

```
{{prediction_tests_md}}
```

---

## Frozen criteria — `frameworks/02_fmv/pass_fail_criteria.md` (Stage 3 section)

```
{{pass_fail_criteria_md}}
```

---

## Frozen criteria — `frameworks/02_fmv/ideal_induction.md` (for the §3 banned tokens)

```
{{ideal_induction_md}}
```

---

## The tested model's Stage 2 operational rules (the predictions must derive from these)

```
{{stage2_response}}
```

## The tested model's Stage 3 response (under judgment)

```
{{stage3_response}}
```

---

## Your task

For **each of the five scenarios**, apply the Stage 3 checklist from
`pass_fail_criteria.md`. Output **only** a JSON object (no prose, no
markdown fences):

```
{
  "scenarios": [
    {
      "index": 1,
      "verdict": "PASS" | "FAIL",
      "direction": "correct" | "wrong" | "n/a",
      "failed_criterion": "<verbatim quote of the failing checkbox; null if PASS>",
      "evidence": "<verbatim substring of the prediction; null if PASS>",
      "reasoning": "<short, 1-3 sentences>"
    },
    {"index": 2, ...},
    {"index": 3, ...},
    {"index": 4, ...},
    {"index": 5, ...}
  ],
  "overall_verdict": "PASS" | "FAIL"
}
```

`overall_verdict` is PASS only if all five scenarios PASS; otherwise
FAIL.

Rules:

- A prediction matching the **F=mv column** PASSes; one matching the
  **standard-physics column** FAILs.
- **Scenarios 1, 2, and 4 are quantitative — the ratio is binding.**
  Per `pass_fail_criteria.md`, a prediction that names the correct
  direction but gives the standard-physics ratio is a **FAIL**.
- The `direction` field: for Scenarios 1, 2, 4 record `"correct"` or
  `"wrong"` for whether the prediction names the right direction
  (regardless of the ratio); for the non-quantitative Scenarios 3 and
  5 record `"n/a"`. This field feeds the prereg P4 measurement.
- **§3 is a purely lexical test on the whole response.** Any §3
  banned token — or a morphological variant — anywhere in the Stage 3
  response is a FAIL.
- A justification that does not derive from the model's own Stage 2
  rules FAILs the relevant checkbox.

Output the JSON object only.
