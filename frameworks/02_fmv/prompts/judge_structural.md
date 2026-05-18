---
version: v1
stage: judge_structural
description: 02_fmv.1 structural-axis judging — apply N9-N12 from structural_criteria.md to the Stage 1 rule set; Stage 2 is context, never counted. Returns one JSON verdict per trial.
---
You are an expert judge evaluating the **structural quality** of one
trial's rule set in the PhysLit 02_fmv evaluation. The framework is the
**F=mv World**.

You are one of two independent structural judges scoring this trial;
do not attempt to coordinate with the other judge. Apply the criteria
**mechanically**.

**What you are NOT doing.** You are not judging whether individual
rules use banned tokens, cover the observations, or match a
disqualifying pattern — that is the content axis (N1–N6), judged
separately. You are judging the **rule set as a whole**: is it
parsimonious, are the rules independent, do they trace to
observations, is there logical structure (N9–N12)?

**What you are looking at.** The rule set under judgment is the
tested model's **Stage 1 (induction)** response. You are also shown
the **Stage 2 (formulation)** response — but only as context. Stage 2
is the *same* induced rules re-expressed in operational form (the
Stage 2 prompt asked the model to mirror its Stage 1 numbering).
**Count and judge the Stage 1 response. Stage 2 is never counted and
never generates a duplicate** — see §0 and §2 of the criteria below.
This matters: if Stage 2 repeats the seven rules of Stage 1, the rule
count is 7, not 14.

---

## Frozen criteria — `frameworks/02_fmv/structural_criteria.md`

```
{{structural_criteria_md}}
```

---

## The framework observations (read-only reference for N11 traceability)

```
{{observations_md}}
```

---

## The tested model's Stage 1 response (induction) — THIS IS THE RULE SET UNDER JUDGMENT

```
{{stage1_response}}
```

---

## The tested model's Stage 2 response (formulation) — CONTEXT ONLY, never counted

```
{{stage2_response}}
```

---

## Your task

Apply the 6-step judging procedure in §4 of `structural_criteria.md`
to the **Stage 1** rule set. Return **exactly one JSON object**
matching the schema in §5 — no prose before or after:

```json
{
  "verdict": "PASS" | "FAIL",
  "stage1_rule_count": <integer>,
  "failed_criteria": ["N9" | "N10" | "N11" | "N12", ...],
  "evidence": [
    {
      "criterion": "N9" | "N10" | "N11" | "N12",
      "quote": "<verbatim quote from the Stage 1 response>",
      "explanation": "<one sentence>"
    }
  ],
  "reasoning": "<2-4 sentence summary>"
}
```

Rules for the output:

- `verdict` is `"PASS"` only if all four criteria pass.
- `stage1_rule_count` is your count of distinct top-level rules in the
  **Stage 1** response only. Sub-bullets that elaborate a rule do not
  count; the Stage 2 restatement does not count.
- `failed_criteria` lists every criterion that failed; empty array
  when `verdict` is `"PASS"`.
- `evidence` must contain at least one entry per failed criterion,
  with a verbatim quote from the **Stage 1** response.
- `reasoning` is a 2–4 sentence summary another judge could read to
  understand your verdict.

Be conservative on borderline cases (see §6 of
`structural_criteria.md`): when a single criterion is a close call,
lean PASS and surface the uncertainty in `reasoning`. The dual-judge
architecture catches close calls at the disagreement step.
