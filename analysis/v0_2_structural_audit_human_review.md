# v0.2 Structural Audit — Human Verdicts (Canonical)

> **Status:** All 6 structural-axis (N9-N12) disagree cases reviewed.
> **Date:** 2026-05-17.
> **Source worksheet:** [`v0_2_structural_audit_worksheet.md`](./v0_2_structural_audit_worksheet.md).
> **Scope:** structural axis only. Content axis (N1-N8) is unchanged.
> The prereg-locked `predictions/v0_2_1_prereg.md` is unchanged; this
> audit lives entirely in the analysis layer per CLAUDE.md
> "Inter-rater reliability".

6 disagree cases audited. Structural-axis dual-judge IRR 40 % (6/15).

## Verdicts

| Case | Trial | Claude judge | OpenAI judge | Agent 2 | Human verdict | Agent 2 correct? |
|------|-------|-------------|-------------|---------|--------------|-----------------|
| 1 | Claude trial 3 | PASS (7) | FAIL (14) | FAIL (14) | **PASS** | ❌ |
| 2 | Claude trial 4 | PASS (10) | FAIL (20) | PASS (10) | **PASS** | ✅ |
| 3 | Gemini trial 0 | FAIL→PASS (7) | PASS (14) | PASS (7) | **FAIL** | ❌ |
| 4 | Gemini trial 1 | FAIL→PASS (7) | PASS (7) | PASS (7) | **PASS** | ✅ |
| 5 | Gemini trial 2 | PASS (7) | FAIL (14) | FAIL (14) | **PASS** | ❌ |
| 6 | Gemini trial 4 | FAIL→PASS (7) | PASS (7) | PASS (7) | **PASS** | ✅ |

Agent 2 agreement with human: **3/6 (50 %)**.

## Reasoning

### Cases 1, 2, 5: Stage 2 mirror ≠ redundancy

The Stage 2 prompt (`prompts/stage2_formulation.md`) explicitly
instructs: "Return your operational rules as a numbered list,
**mirroring the numbering you used earlier**."

The models correctly followed this instruction — Stage 2 is an
operational expansion of Stage 1, not a new set of rules. Counting
Stage 1 + Stage 2 combined and calling the result N10 redundancy
penalizes correct prompt compliance.

The human audit counts **core rules only** (the Stage 1 count). Stage 2
mirroring is not an N10 redundancy.

- Case 1: 7 core rules → PASS
- Case 2: 10 core rules → PASS
- Case 5: 7 core rules → PASS

### Case 3: Stage 1 internal redundancy → FAIL

Gemini trial 0 has 7 rules, but Rule 1 and Rule 7 both describe
celestial circular motion:

- Rule 1: "Celestial bodies naturally travel in continuous, unending circles"
- Rule 7: "The Sun, Moon, and fixed stars… naturally travel in continuous horizontal circular paths"

This is **Stage 1 internal redundancy** (the same phenomenon stated in
two rules), not Stage 2 mirroring — a genuine N10 violation. All three
judges and Agent 2 missed it.

### Cases 4, 6: Clean 7 rules → PASS

- Case 4: Rule 1 packs celestial motion together with earthly and
  fiery directions. No separate celestial rule, no internal
  redundancy.
- Case 6: Rule 1 covers only earthly and fiery directions; Rule 7
  separately covers celestial motion. No overlap, no internal
  redundancy.

## Known defect: Claude structural-judge verdict-field bug

Cases 3, 4, 6: the Claude structural judge's `verdict` field says
`FAIL`, but the `reasoning` text self-corrects to PASS. The verdict
field is wrong; the reasoning is right. This is a systematic
data-entry bug in the Claude structural judge — not a genuine
judgment, and a contributor to the inflated 40 % IRR.

## Criteria design bug to disclose in the paper

`frameworks/01_aristotelian/structural_criteria.md` §2 says: "Rule
count means top-level numbered or bolded propositions in the Stage 1 +
Stage 2 **combined** output."

`prompts/stage2_formulation.md` says: "Return your operational rules
as a numbered list, **mirroring the numbering you used earlier**."

These two instructions conflict. Any model that correctly follows the
Stage 2 prompt has its rule count mechanically doubled, which then
trips N9 (parsimony) or N10 (independence). This must be disclosed as
a v0.2 criteria design limitation.

**Fix for v0.3:** `structural_criteria.md` should specify — "Count
core principles (the Stage 1 count). Stage 2 operational expansions
of the same rules do not count as additional rules. N10 redundancy is
assessed *within* the Stage 1 core set."
