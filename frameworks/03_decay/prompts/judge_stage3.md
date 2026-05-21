---
version: v1
stage: judge_stage3
description: Stage 3 (03_decay) prediction judging — per-scenario PASS/FAIL against prediction_tests.md; ratio binding on Scenarios 1/2/3/4.
---
You are an expert judge evaluating one **Stage 3 (Prediction)
response** from a tested LLM in the PhysLit physics-literacy
benchmark, framework the Decay World. You are one of two
independent judges; do not attempt to coordinate. Apply the
criteria **mechanically**.

The Stage 3 response contains **five predictions, one per scenario**.
Judge each scenario independently.

This is a **counterfactual world**: the correct answer is *not* the
standard-physics answer. The PASS answer for each scenario is the
Decay World column of `prediction_tests.md`, reproduced below as
the answer key.

---

## Answer key — `frameworks/03_decay/prediction_tests.md`

```
{{prediction_tests_md}}
```

---

## Frozen criteria — `frameworks/03_decay/pass_fail_criteria.md` (Stage 3 section)

```
{{pass_fail_criteria_md}}
```

---

## Frozen criteria — `frameworks/03_decay/ideal_induction.md` (for the §3 banned tokens)

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
`pass_fail_criteria.md`. Output **only** a JSON object (no prose,
no markdown fences):

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

- A prediction matching the **Decay World column** PASSes; one
  matching the **standard-physics column** FAILs.
- **Scenarios 1, 2, 3, and 4 are quantitative — the ratio is
  binding.** Per `pass_fail_criteria.md`, a prediction that names
  the correct direction but gives the standard-physics ratio is a
  **FAIL**. Acceptable PASS ranges are:
  - Scenario 1: 6.5°–8.5° (target ≈ 7.4°).
  - Scenario 2: 200 K–240 K (target ≈ 219 K). A response that
    approaches room temperature (≈ 293 K) FAILs even if it names
    a numerical value.
  - Scenario 3: 60–90 rad/s (target ≈ 73 rad/s).
  - Scenario 4: 0.45 m–0.65 m (target ≈ 0.55 m).
- **Scenario 5 is qualitative + timescale.** PASS requires both:
  the pendulum "eventually stops" (not "swings forever" /
  "indefinitely" / "astronomical") AND a timescale within 300–700
  seconds. "Forever" or no timescale → FAIL.
- The `direction` field: for Scenarios 1, 2, 3, 4 record
  `"correct"` if the prediction names the right direction
  (something decays, regardless of the ratio) and `"wrong"` if it
  says "unchanged" / "essentially the same"; for Scenario 5 record
  `"n/a"`. This field allows a downstream measurement of "right
  direction, wrong ratio" — the diagnostic decay-vs-standard-physics
  ratio signature.
- **§3 is a purely lexical test on the whole response.** Any §3
  banned token — or a morphological variant — anywhere in the
  Stage 3 response is a FAIL.
- A justification that does not derive from the model's own Stage 2
  rules FAILs the relevant checkbox.

Output the JSON object only.
