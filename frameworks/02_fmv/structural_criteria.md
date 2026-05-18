# Structural Criteria — F=mv World (round `02_fmv.1`)

> **Status:** DRAFT — author review required before the `02_fmv.1`
> prereg lock.
> **Created:** 2026-05-18
> **Framework ID:** 02_fmv
> **Round:** `02_fmv.1` — the structural-axis layer, additive over the
> frozen `02_fmv` content-axis trials.
> **Audience:** structural judges (Claude Opus 4.7 + GPT-5.5) and the
> human auditor. The tested model never sees this file.

## 0. Design note — what this fixes, and the mechanical standard

This file is the **bug-fixed** structural criteria. The v0.2
Aristotelian structural criteria
(`frameworks/01_aristotelian/structural_criteria.md`) counted "rules"
across the **Stage 1 + Stage 2 combined** output. But the Stage 2
prompt instructs the tested model to restate its rules "mirroring the
numbering you used earlier" — so Stage 2 is the *same* induced rules,
re-expressed in operational form. Counting both:

- **doubled every rule count**, tripping N9 (parsimony) on rule sets
  that were in fact parsimonious; and
- made every (Stage 1 rule, its Stage 2 counterpart) pair look like an
  N10 (independence) duplicate.

The v0.2 Aristotelian structural **human audit confirmed this defect**
as the dominant cause of the 40 % structural-axis disagreement rate.
`02_fmv.1` fixes it (§2, §3):

- **The rule set under judgment is the Stage 1 induction.** N9 counts
  Stage 1 core rules only; the Stage 2 operational restatement is not
  counted.
- **N10 redundancy is judged within Stage 1.** A Stage 1 rule and its
  Stage 2 operational counterpart are the *same* rule — prompt-mandated
  mirroring — and are **not** an N10 violation.

Beyond that fix, this file follows the same **mechanical** standard as
`ideal_induction.md` §0: each FAIL trigger is a check applied the same
way every time — a count against a fixed threshold, or a concrete
quoted pattern — with no assessment of intent or sophistication.

## 1. Purpose

The content axis (N1–N6, in `ideal_induction.md`) checks each
**individual rule**: no banned token, covers the observations, no
disqualifying pattern. The structural axis (N9–N12, this file) checks
the **rule set as a whole**: is it parsimonious, are the rules
independent, do they trace to observations, is there logical
structure.

A rule set can have every individual rule content-clean and still be a
redundant, fabricated, flat soup. v0.1's canonical case was a model
producing 17 rules where two stated the same claim and one introduced
a mechanism no observation supports. The structural axis catches that
class of failure.

## 2. Input scope

The structural judge is shown the trial's **Stage 1 (induction)**
response and **Stage 2 (formulation)** response, clearly labelled as
two separate sections. Stage 3 and Stage 4 are not in scope.

**The rule set under judgment is the Stage 1 induced rules.** Stage 2
is the operational restatement of those same rules; it is shown only
as context (it can help confirm what a Stage 1 rule means and whether
the rule set has cross-references). Stage 2 **never adds rules** and is
**never counted**.

## 3. Necessary conditions

A passing structural judgment requires **all four** of N9–N12.
Failing any one triggers a structural FAIL for the trial.

### N9 — Parsimony

The Stage 1 rule count should not vastly exceed the observation count.
The F=mv World has **12 observations**; a Stage 1 induction producing
far more than ~12 rules suggests redundancy or fabrication.

**Rule count** = the number of **top-level numbered or bolded
propositions in the Stage 1 response**. Sub-bullets that elaborate a
rule (scope, examples, edge cases) do **not** count as separate rules.
The Stage 2 operational restatement is **not** counted — see §0, §2.

**FAIL thresholds (on the Stage 1 count):**

- count > 20 → FAIL on N9, severity high
- count > 15 → FAIL on N9, severity moderate
- count > 12 and ≤ 15 → not a FAIL by itself; soft signal, counts
  toward FAIL only if combined with an N10 or N11 violation

### N10 — Independence

No two **Stage 1** rules describe the same phenomenon. Each Stage 1
rule must add content the others do not already cover.

**FAIL trigger:** any two **Stage 1** rules can be paraphrased into
the same operational claim about the same kind of body in the same
situation. Quote both rules verbatim as evidence.

**Not an N10 violation:** a Stage 1 rule and its Stage 2 operational
counterpart stating the same thing. That is the prompt-mandated
mirroring (the Stage 2 prompt asks the model to restate its rules);
it is expected and correct, not redundancy. N10 is judged **within
the Stage 1 rule set only**.

### N11 — Coverage traceability

Every Stage 1 rule must trace to specific observation(s) from the
12-observation set. A rule that corresponds to no observation has been
fabricated — its content is not derivable from the input, even if it
uses no banned token.

**FAIL trigger:** a Stage 1 rule introduces a mechanism, entity, or
causal claim that no observation supports. Quote the offending rule
verbatim and name the observation(s) it was apparently meant to derive
from.

**Permitted, does NOT trigger N11:** a rule that *combines* or
*reconciles* observations into a more general statement — e.g. a rule
positing that a body's own downward push scales with its heaviness, to
reconcile observation 5 (heavier → slower under a hand-push) with
observation 10 (heavy and light fall alike). Tying observations
together is induction working as intended. N11 catches *fabricated
mechanisms with no observational basis at all*, not legitimate
generalisation.

### N12 — Hierarchy

The Stage 1 rule set should have logical structure — core principles
and derived corollaries, or explicit cross-references between rules —
not a flat enumeration of N unconnected propositions.

**FAIL trigger:** a Stage 1 rule set of **5 or more rules** with **no
cross-rule reference anywhere in the Stage 1 response**.

A cross-rule reference is any of:

- "Rule N", "Principle N", "Law N" with N a digit (e.g. "see Rule 3");
- explicit hierarchy markers: "derived from", "corollary of", "follows
  from", "special case of", "combined with", "consequence of",
  "implies", "by application of", "overrides".

A Stage 1 rule set with fewer than 5 rules is exempt from N12 (too
small to require hierarchy).

## 4. Judging procedure

Apply in order. **Stop at the first FAIL.** All steps operate on the
**Stage 1** rule set.

```
Step 1. Count the distinct top-level rules in the Stage 1 response.
        Record the count. (Stage 2 is not counted.)

Step 2. N9 check (parsimony).
        count > 20  → FAIL on N9 (severity high)
        count > 15  → FAIL on N9 (severity moderate)
        else proceed.

Step 3. N10 check (independence).
        Scan the Stage 1 rules for any pair that paraphrase the same
        claim about the same kind of body in the same situation.
        Any such pair → FAIL on N10. (A Stage 1 rule matching its
        Stage 2 counterpart is NOT such a pair.)

Step 4. N11 check (coverage traceability).
        For each Stage 1 rule, identify the supporting observation(s)
        by number. Any rule introducing content no observation
        supports, and not a legitimate generalisation → FAIL on N11.

Step 5. N12 check (hierarchy).
        If the Stage 1 rule count >= 5 and no cross-rule reference
        appears anywhere in the Stage 1 response → FAIL on N12.

Step 6. All four checks passed → PASS.
```

The structural judge emits **one PASS/FAIL verdict per trial**, not
one per criterion. If multiple criteria fail, list all of them with
evidence.

## 5. Output format

The structural judge returns one JSON object:

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

- `stage1_rule_count` is the count from Step 1 — of the **Stage 1**
  response only.
- `failed_criteria` is the list of criteria that triggered FAIL; empty
  when the verdict is PASS.
- `evidence` requires at least one entry per failed criterion, with a
  verbatim quote from the **Stage 1** response.

## 6. Notes for judges

- **Count the Stage 1 response, not Stage 1 + Stage 2.** This is the
  single most important instruction in this file — see §0. If Stage 2
  repeats the seven rules of Stage 1, the rule count is 7, not 14.
- **Stage 2 is context, not evidence to be counted.** Use it to
  understand what a Stage 1 rule means; do not let it inflate the
  count or generate spurious N10 duplicates.
- **Be conservative on N9 borderline cases.** A Stage 1 count of
  exactly 15 is a soft signal, not a FAIL by itself.
- **Be specific on N11.** Quote the offending rule and name the
  observations it was meant to derive from; legitimate generalisation
  that ties observations together is not a fabrication.
- **When a single criterion is a genuine close call, lean PASS and
  state the uncertainty in `reasoning`.** The dual-judge architecture
  catches close calls at the disagreement step; a forced FAIL on a
  borderline case is harder to recover.

## Changelog

- **2026-05-18 (`02_fmv.1` prereg-draft).** Initial structural criteria
  for the F=mv World. Fixes the v0.2 Stage 1 + Stage 2 double-count
  defect: the rule set under judgment, and the N9 count, are scoped to
  the Stage 1 induction; N10 redundancy is judged within Stage 1. To
  be frozen at `prereg-02_fmv.1-locked`.
