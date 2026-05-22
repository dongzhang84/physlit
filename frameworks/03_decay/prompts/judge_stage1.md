---
version: v1
stage: judge_stage1
description: Stage 1 (03_decay) induction judging — apply ideal_induction.md §6 checklist, return structured JSON verdict.
---
You are an expert judge evaluating one **Stage 1 (Induction) response**
from a tested LLM in the PhysLit physics-literacy benchmark. The
framework is the Decay World; the criteria you must apply are
reproduced verbatim below.

You are one of two independent judges scoring this response; do not
attempt to coordinate with the other judge. Apply the criteria
**mechanically** and stop at the first FAIL.

---

## Frozen criteria — `frameworks/03_decay/ideal_induction.md`

```
{{ideal_induction_md}}
```

---

## The tested model's Stage 1 response

```
{{stage1_response}}
```

---

## Your task

Apply the 6-step judge checklist in §6 of `ideal_induction.md`. Stop
at the first FAIL. Output **only** a JSON object (no prose around it,
no markdown fences):

```
{
  "verdict": "PASS" | "FAIL",
  "first_fail_step": <integer 1-6 or null if PASS>,
  "first_fail_clause": "<which token / N / P, e.g. 'banned: friction' or 'N3' or 'P2'; null if PASS>",
  "evidence": "<verbatim substring of the response that triggered the FAIL; null if PASS>",
  "reasoning": "<short, 1-3 sentences>"
}
```

Important rules:

- **§3 is a purely lexical test.** If any §3 banned token — or a
  morphological variant of it — appears anywhere in the response,
  the verdict is FAIL at Step 1. Do not assess part of speech,
  intent, whether the concept was "defined", whether it was used
  "only descriptively", or whether it was named only to deny that
  it applies. Token present → FAIL. (§3 of the criteria states
  this.)
- The positive conditions N1–N6 are judged by **meaning**:
  equivalent phrasings count as equivalent (§7). This charity
  applies to N1–N6 and the coverage / consistency checks — it does
  **not** apply to the §3 token test.
- The §5 disqualifying patterns P1–P7 are concrete claim patterns;
  quote the offending rule verbatim as evidence.
- The Decay World's most diagnostic disqualifying pattern is P2
  (energy-substrate framing). Be alert to phrasings that smuggle
  energy back in: "an underlying quantity decays at fixed rate, and
  the measured quantity follows from it" is P2 even if the literal
  token *energy* is avoided. (If the literal token appears, §3
  catches it; if a paraphrase is used, §5 P2 catches it.)
- When a necessary condition or a §5 pattern is genuinely
  borderline, see §7 of the criteria — but the §3 token test is
  never borderline.

**Anti-fabrication rules (load-bearing — read carefully):**

- The ``evidence`` field MUST be a **verbatim substring** of the
  tested model's response above. Before you write the ``evidence``
  field, find the exact substring in the response, copy it, and
  paste it. **Do not paraphrase, summarise, or reconstruct the
  evidence from memory.** A downstream mechanical check verifies
  that ``evidence`` appears in the response as a substring; if it
  does not, the verdict is flagged as judge-fabrication and sent
  to human audit, against you.
- For a §3 FAIL, the ``evidence`` field must be the literal banned
  token (or its morphological variant) as it appears in the
  response. Do not record an inferred or implied banned concept
  that the response does not contain as a literal substring. If you
  cannot find the banned token as a literal substring, the §3 test
  is PASS — proceed to Step 2.
- Your ``reasoning`` field must state a definite claim. **Do not
  use question marks, "perhaps", "I think", "it might be", or any
  self-doubting language. Do not pose alternatives to yourself.**
  If you are uncertain about a clause, that clause is PASS for the
  purpose of the mechanical checklist; record only the clauses you
  are certain of as FAILs.

Output the JSON object only.
