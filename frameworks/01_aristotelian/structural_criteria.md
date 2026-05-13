# Structural Criteria — Aristotelian Mechanics (v0.2)

> **Status:** v0.2 artifact, frozen at `prereg-v0.2-locked` once locked.
> **Framework ID:** 01_aristotelian
> **Audience:** structural judges (Claude Opus + GPT-5.5) and the
> Agent 2 resolver. The tested model never sees this file.
> **Input scope:** the structural judge reads the trial's **Stage 1
> (induction) response concatenated with the trial's Stage 2
> (formulation) response**. Stage 3 (prediction) is NOT part of the
> structural-judge input.

## 1. Purpose

The content axis (N1-N8, defined in `pass_fail_criteria.md` and
`ideal_induction.md` §§2-3) checks that each **individual rule** is
content-acceptable: it must not use banned modern-physics words, it
must cover the required observations, it must not match a near-pass
failure pattern. The structural axis (N9-N12, this file) checks that
the **rule set as a whole** is structurally acceptable: parsimonious,
independent, traceable to observations, and hierarchical.

A rule set can have zero banned words and still be a redundant,
fabricated, flat soup. v0.1 found one canonical case (GPT-5.5 trial 3
Stage 2: 17 rules, two rules describing the same phenomenon, one rule
introducing "road and air rob motion from the cart" without an
observation to support it). v0.2 introduces the structural axis to
catch this class of failure.

## 2. Necessary conditions

A passing structural judgment requires **all four** of the following.
Failing any one triggers structural FAIL for the trial.

### N9 — Parsimony

The rule count should not vastly exceed the observation count. With
12 observations as input, an induction producing significantly more
than ~12 rules suggests either redundancy (multiple rules saying the
same thing) or fabrication (rules whose content goes beyond what the
observations support).

**FAIL thresholds:**

- rule count > 20 → FAIL on N9, severity high
- rule count > 15 → FAIL on N9, severity moderate
- rule count > 12 and ≤ 15 → not a FAIL by itself; soft signal, only
  counts toward FAIL if combined with an N10 or N11 violation

"Rule count" means top-level numbered or bolded propositions in the
Stage 1 + Stage 2 combined output. Sub-bullets that elaborate a rule
(scope, examples, edge cases) do **not** count as separate rules.

### N10 — Independence

No two rules should describe the same phenomenon. Each rule must add
content that the other rules do not already cover.

**FAIL trigger:** any two rules can be paraphrased into the same
operational claim about the same kind of body in the same situation.
Verbatim quote both rules as evidence.

v0.1 example (GPT-5.5 trial 3 Stage 2): rule 9 and rule 13 both
stated "the cart stops once pushing ceases" with slightly different
framings.

### N11 — Coverage traceability

Every rule must trace to specific observation(s) from the framework's
12-observation list. A rule that does not correspond to any observation
has been fabricated — its content is not derivable from the input,
even if it does not use any §3 banned word.

**FAIL trigger:** a rule introduces a mechanism, entity, or causal
claim that no observation supports. Quote the offending rule verbatim
and state which observations (if any) it is meant to be derived from.

v0.1 example (GPT-5.5 trial 3 Stage 2): rule 13 introduced "the road
and air rob motion from the cart". No observation among the 12
mentions the road or air as a motion-robbing agent. Observation 2
shows that the cart slows, but does not specify a mechanism.

Permitted Aristotelian elaborations that do **not** trigger N11:

- Natural-place / striving-toward-place language (Obs. 3, 4, 5, 8, 12)
- Medium-resistance language for falling bodies (Obs. 9, 11)
- Antiperistasis / impressed-motion explanations of the arrow that
  explicitly fade (Obs. 7, see also `ideal_induction.md` §5)
- The heaven/earth split for celestial bodies (Obs. 10)

### N12 — Hierarchy

The rule set should have logical structure — core principles and
derived corollaries, or explicit cross-references between rules —
not a flat enumeration of N independent propositions.

**FAIL trigger:** a rule set of **5 or more rules** with **no
cross-rule references at all** anywhere in the Stage 1+2 response.

A cross-rule reference is any of:

- The phrase "Rule N", "Principle N", "Axiom N", or "Law N" with N a
  digit (e.g. "see Rule 3", "as in Principle 7")
- Explicit hierarchy markers: "derived from", "corollary of", "follows
  from", "special case of", "combined with", "consequence of",
  "implies", "by application of", "subsumes", "overrides"

A rule set with < 5 rules is exempt from N12 (too small to require
hierarchy).

## 3. Judging procedure

Apply in order. Stop at the first FAIL.

```
Step 1. Count distinct top-level rules in the Stage 1 + Stage 2
        combined response. Record the count.

Step 2. N9 check (parsimony).
        rule_count > 20  → FAIL on N9 (severity high)
        rule_count > 15  → FAIL on N9 (severity moderate)
        else proceed.

Step 3. N10 check (independence).
        Scan for any pair of rules that paraphrase the same claim
        about the same kind of body in the same situation.
        Any such pair found → FAIL on N10.

Step 4. N11 check (coverage traceability).
        For each rule, identify the supporting observation(s) by
        observation number. Any rule with no traceable
        observation, introducing content not present in the
        observations, and not falling under one of the permitted
        Aristotelian elaborations listed in §N11 → FAIL on N11.

Step 5. N12 check (hierarchy).
        If rule_count >= 5 and no cross-rule reference is found
        anywhere in the response → FAIL on N12.

Step 6. All four checks passed → PASS.
```

Per v0.2 D3, the structural judge emits **one PASS/FAIL verdict per
trial**, not per criterion. If multiple criteria fail, list all
failed criteria with evidence.

## 4. Output format

The structural judge must return one JSON object of this shape:

```json
{
  "verdict": "PASS" | "FAIL",
  "rule_count": <integer>,
  "failed_criteria": ["N9", "N10", "N11", "N12"],
  "evidence": [
    {
      "criterion": "N9" | "N10" | "N11" | "N12",
      "quote": "<verbatim quote from the response>",
      "explanation": "<one sentence>"
    }
  ],
  "reasoning": "<2-4 sentence summary>"
}
```

- `failed_criteria` is the list of criteria that triggered FAIL.
  Empty list when verdict is PASS.
- `evidence` is required for every entry in `failed_criteria`; at
  least one evidence entry per failed criterion, with verbatim quote
  from the response.
- `rule_count` is the count from Step 1 of the judging procedure.

## 5. Notes for judges

- **Stage 1 + Stage 2 are concatenated for your input.** Stage 1 is
  the model's initial induction; Stage 2 is its operational
  formulation. Treat them together as one rule set. The rule numbering
  in Stage 2 may or may not match Stage 1's; do not penalize that.
- **You will not see Stage 3.** Stage 3 (prediction) tests the model's
  rules against novel scenarios; it is judged on the content axis
  separately. Structural-axis judgment is on Stages 1+2 only.
- **Be conservative on N9 borderline cases.** A trial with exactly 15
  rules is a soft signal, not a FAIL by itself. Do not mark FAIL on
  N9 unless rule count exceeds 15 strictly *and* there is no
  mitigating structure (e.g. the response explicitly groups rules
  into core/derived tiers).
- **Be specific on N11 evidence.** It is not sufficient to say
  "this rule has no observation". Quote the offending rule and name
  the observations (if any) the rule was clearly attempting to derive
  from.
- **Permitted Aristotelian elaboration is NOT smuggling.** Impetus
  theory with explicit fading, natural-place language, medium-
  resistance — these are valid framework moves. N11 catches
  *fabricated mechanisms* not in the framework, not legitimate
  framework elaboration.
- **When in doubt on a single criterion, lean PASS but note your
  uncertainty.** The dual-judge architecture is designed to catch
  borderline cases at the disagreement step. A close call from one
  judge that triggers DISAGREE is resolvable by Agent 2; a forced FAIL
  on a borderline case is harder to recover.

## Changelog

- **2026-05-12 (v0.2 prereg-draft).** Initial structural-criteria
  spec, lifted and operationalized from `ideal_induction.md` §8.
  Adds explicit numeric thresholds for N9, per-criterion evidence
  requirements, and the §N11 permitted-elaboration list. To be
  frozen at `prereg-v0.2-locked`.
