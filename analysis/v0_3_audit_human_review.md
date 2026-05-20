# v0.3 Audit — Human Verdicts (Aristotelian Axiomatisation Treatment)

11 disagree cases:

- Content axis: 8 stage-level dual-judge splits (IRR 17.78 %).
- Structural axis: 3 trial-level splits (IRR 20.00 %).

## Part B — Structural Axis (3 cases)

All three resolve PASS under previously-established principles. The
detailed diagnosis for each:

| Case | Trial | Rules | Claude | OpenAI | Human | Reason |
|------|-------|-------|--------|--------|-------|--------|
| S1 | GPT T1 | 7 (Stage 1) | FAIL | PASS | **PASS** | Claude verdict-field self-contradiction; OpenAI Stage 1+2 double-count (counted 14) |
| S2 | Gemini T3 | 4 (Stage 1) | PASS | FAIL | **PASS** | OpenAI Stage 1+2 double-count → spurious N10 FAIL on Stage 2 mirror |
| S3 | Gemini T4 | 3 (Stage 1) | FAIL | PASS | **PASS** | Claude verdict-field self-contradiction; 3 rules < 5 → N12 exempt |

### S1 — GPT T1 (PASS)

Stage 1 has 7 top-level rules. The **Claude verdict-field self-contradicts**: Claude's own reasoning ends with:

> "Stage 2 contains explicit cross-rule references such as 'as in Rule 1', 'in Rule 4', and 'that requires Rule 5', satisfying N12. **Correcting my verdict: this should be PASS.**"

The structured `verdict: FAIL` field disagrees with the reasoning text — the same defect class as `02_fmv.1` Case 6 (Gemini t2), which we resolved in favour of the reasoning. Same precedent here → PASS.

Stage-1-only methodological note: Claude credited Stage 2 ("as in Rule 1", "that requires Rule 5") for N12. Stage 1 of gpt t1 has no explicit "Rule N" markers — only descriptive prose. Under a strict Stage-1-only reading N12 would FAIL here; but the same Stage-1-only reading would also require us to ignore Claude's reasoning, which itself accepted Stage 2 references. We follow the established precedent (treat verdict-field bug as following the reasoning) and the OpenAI agreement to PASS → resolved PASS.

OpenAI's `rule_count: 14` is the Stage 1+2 double-count bug (counted "seven induction rules and seven formulation rules" as 14 total).

### S2 — Gemini T3 (PASS)

Stage 1 has 4 top-level rules. **OpenAI's N10 FAIL is the Stage 1+2 double-count bug**: OpenAI explicitly wrote

> "I count eight top-level rules across the concatenated Stage 1 and Stage 2 responses: four initial rules and four operational reformulations. ... because Stage 2 restates the same four rules from Stage 1 as operational versions, at least one pair of rules describes the same operational phenomenon, triggering N10."

This is exactly the v0.2-criteria defect that `02_fmv.1` was created to fix: Stage 2 is mirror-numbered to Stage 1 by the **Stage 2 prompt's own instruction** ("mirroring the numbering you used earlier"), so a Stage 2 paraphrase of a Stage 1 rule is a prompt-mandated restatement — not an N10 redundancy. Under the Stage-1-only principle the rule set has 4 rules, N12 exempt (< 5), N10 PASS (no within-Stage-1 paraphrase). Claude correctly used `rule_count: 4` and PASSed → resolved PASS.

### S3 — Gemini T4 (PASS)

Stage 1 has 3 top-level rules. **Claude verdict-field self-contradiction**: Claude's reasoning literally writes

> "rule_count = 3, N9 passes easily, and N12 is exempt (< 5 rules). The three rules cover distinct phenomena ... so N10 passes. Each rule traces to specific observations ... so N11 passes. **Verdict should be PASS.**"

The structured `verdict: FAIL` field disagrees with the reasoning. Same defect class as `02_fmv.1` Case 6 and v0.3 Case S1 above. OpenAI also PASS. → resolved PASS.

## Methodological notes

Two known judge defects surfaced in this round on the structural axis:

1. **OpenAI Stage 1+2 double-count** (S2). The v0.2 structural criteria
   (`frameworks/01_aristotelian/structural_criteria.md` §2: "rule count
   means top-level numbered or bolded propositions in the Stage 1 +
   Stage 2 combined output") combined with the Stage 2 prompt's
   mirror-numbering instruction creates a built-in conflict: any
   well-formed Stage 2 will be a mirror restatement of Stage 1, and
   under the v0.2 criteria those mirrored rules get counted as
   "duplicates" → N10 false positive. `02_fmv.1` already removed this
   defect by scoping the count and the N10 check to Stage 1 only.
   v0.3 reuses the v0.2 criteria (the prereg required identical
   judging to the v0.1/v0.2 baseline), so the defect re-emerges here.
   The audit applies the Stage-1-only principle as the canonical
   resolution.

2. **Claude verdict-field self-contradiction** (S1, S3). The
   structured `verdict` field reports FAIL while the reasoning text
   explicitly concludes "this should be PASS" / "Verdict should be
   PASS". Same defect class as `02_fmv.1` Case 6 (Gemini t2). The
   audit follows the reasoning (which is the substantive output of
   the judge) over the structured field (which is brittle and
   inconsistent).

Both defects independently exist in published prior rounds and are
documented as known limitations of LLM-as-judge methodology, not
specific to this experiment.

## Part A — Content Axis (8 cases)

_Pending human audit. Will be added._
