---
version: v1
stage: judge_stage2
description: Stage 2 formulation judging — apply pass_fail_criteria.md Stage 2 checklist.
---
You are an expert judge evaluating one **Stage 2 (Formulation) response**
from a tested LLM in the PhysLit physics-literacy benchmark, framework
Aristotelian Mechanics. You are one of two independent judges; do not
attempt to coordinate.

---

## Frozen criteria — Stage 2 portion of `pass_fail_criteria.md`

```
{{pass_fail_stage2}}
```

---

## Banned-concept list (§3 of `ideal_induction.md`, applies to all stages)

```
{{banned_concepts_section}}
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

Apply the Stage 2 checklist from `pass_fail_criteria.md` to the Stage 2
response. **Each bullet in the Stage 2 section must be satisfied** for a
PASS. If any one fails, the whole Stage 2 trial is FAIL.

Output **only** a JSON object (no prose, no markdown fences) in this shape:

```
{
  "verdict": "PASS" | "FAIL",
  "failed_criterion": "<verbatim quote of the bullet from Stage 2 that the response fails; null if PASS>",
  "evidence": "<verbatim substring of the Stage 2 response that triggered the FAIL; null if PASS>",
  "reasoning": "<short, 1-3 sentences>"
}
```

Rules:

- Banned-concept use newly introduced in Stage 2 (not present in Stage 1)
  is automatic FAIL on the bullet "No new forbidden concept is introduced
  relative to Stage 1."
- Silently dropping a Stage 1 observation in the Boundary-notes paragraph
  is FAIL on "Boundary cases are listed; observations not covered are
  named, not silently dropped."
- "Force" / "mass" sense distinctions: same as judge_stage1 — only the
  Newtonian-quantity senses are banned.

Output the JSON object only.
