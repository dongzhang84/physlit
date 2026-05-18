---
version: v1
stage: judge_stage2
description: Stage 2 (02_fmv) formulation judging — apply pass_fail_criteria.md Stage 2 checklist + ideal_induction.md §3/§5.
---
You are an expert judge evaluating one **Stage 2 (Formulation)
response** from a tested LLM in the PhysLit physics-literacy
benchmark, framework the F=mv World. You are one of two independent
judges; do not attempt to coordinate. Apply the criteria
**mechanically**.

---

## Frozen criteria — `frameworks/02_fmv/pass_fail_criteria.md`

```
{{pass_fail_criteria_md}}
```

---

## Frozen criteria — `frameworks/02_fmv/ideal_induction.md` (for the §3 banned tokens and §5 patterns)

```
{{ideal_induction_md}}
```

---

## The tested model's Stage 1 response (context)

```
{{stage1_response}}
```

## The tested model's Stage 2 response (under judgment)

```
{{stage2_response}}
```

---

## Your task

Apply the **Stage 2** checklist from `pass_fail_criteria.md` to the
Stage 2 response. Every checkbox must be satisfied for a PASS; if any
one fails, the whole Stage 2 trial is FAIL.

Output **only** a JSON object (no prose, no markdown fences):

```
{
  "verdict": "PASS" | "FAIL",
  "failed_criterion": "<verbatim quote of the Stage 2 checkbox the response fails; null if PASS>",
  "evidence": "<verbatim substring of the Stage 2 response that triggered the FAIL; null if PASS>",
  "reasoning": "<short, 1-3 sentences>"
}
```

Rules:

- **§3 is a purely lexical test, applied to the whole response.** If
  any §3 banned token — or a morphological variant — appears anywhere
  in the Stage 2 response, that is an automatic FAIL on the checkbox
  "No banned token appears anywhere in the response". Do not assess
  intent or part of speech.
- A §5 disqualifying pattern P1–P7 present in the Stage 2 operational
  rules is a FAIL.
- Silently dropping a Stage 1 observation — not naming it in the
  *Boundary notes* — is a FAIL on the boundary-cases checkbox.
- The positive checkboxes are judged by meaning; equivalent phrasings
  count as equivalent. This charity does **not** apply to the §3
  token test.

Output the JSON object only.
