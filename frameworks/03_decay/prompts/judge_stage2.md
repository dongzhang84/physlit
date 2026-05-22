---
version: v1
stage: judge_stage2
description: Stage 2 (03_decay) formulation judging — apply pass_fail_criteria.md Stage 2 checklist + ideal_induction.md §3/§5.
---
You are an expert judge evaluating one **Stage 2 (Formulation)
response** from a tested LLM in the PhysLit physics-literacy
benchmark, framework the Decay World. You are one of two independent
judges; do not attempt to coordinate. Apply the criteria
**mechanically**.

---

## Frozen criteria — `frameworks/03_decay/pass_fail_criteria.md`

```
{{pass_fail_criteria_md}}
```

---

## Frozen criteria — `frameworks/03_decay/ideal_induction.md` (for the §3 banned tokens and §5 patterns)

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
Stage 2 response. Every checkbox must be satisfied for a PASS; if
any one fails, the whole Stage 2 trial is FAIL.

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

- **§3 is a purely lexical test, applied to the whole response.**
  If any §3 banned token — or a morphological variant — appears
  anywhere in the Stage 2 response, that is an automatic FAIL on
  the checkbox "No banned token appears anywhere in the response".
  Do not assess intent or part of speech.
- A §5 disqualifying pattern P1–P7 present in the Stage 2
  operational rules is a FAIL. Be especially alert to P2 (energy-
  substrate framing): a Stage 2 rule of the form "an underlying
  quantity decays at fixed rate and the measured quantity follows
  from it" is P2 even when the literal token *energy* is avoided.
- The Stage 2 quantitative-rate checkbox requires that the per-time
  ratio is operational — a third party should be able to compute a
  later value from an initial value and an elapsed time. The
  number must be within ~1 percentage point of 0.99 / s.
- Silently dropping a Stage 1 observation — not naming it in the
  *Boundary notes* — is a FAIL on the boundary-cases checkbox.
- The positive checkboxes are judged by meaning; equivalent
  phrasings count as equivalent. This charity does **not** apply
  to the §3 token test.

**Anti-fabrication rules (load-bearing — read carefully):**

- The ``evidence`` field MUST be a **verbatim substring** of the
  tested model's Stage 2 response above. Before writing
  ``evidence``, find the exact substring in the response, copy it,
  and paste it. **Do not paraphrase, summarise, or reconstruct
  evidence from memory.** A downstream mechanical check verifies
  that ``evidence`` appears in the Stage 2 response as a substring;
  if it does not, the verdict is flagged as judge-fabrication and
  sent to human audit, against you.
- For a §3 FAIL, ``evidence`` must be the literal banned token (or
  morphological variant) as it appears. Do not record an inferred
  or implied banned concept that the response does not contain as
  a literal substring. Do not claim a string contains another
  string as a substring unless you can demonstrate the character
  positions; if uncertain, the §3 test is PASS for that token.
- Your ``reasoning`` field must state a definite claim. **Do not
  use question marks, "perhaps", "I think", "it might be", or any
  self-doubting language. Do not pose alternatives to yourself.**
  If you are uncertain about a clause, that clause is PASS for the
  purpose of the mechanical checklist; record only the clauses you
  are certain of as FAILs.

Output the JSON object only.
