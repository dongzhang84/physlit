# Ideal Induction — Aristotelian Mechanics

> **Status:** DRAFT v0.1 (lean) — 2026-05-08
> **Framework ID:** 01_aristotelian
> **Stage:** 1 (Induction)

> **v0.1 reproducers note (added 2026-05-12):** This file has been
> extended post-`prereg-v0.1-locked` with §8 (Structural criteria
> N9-N12). §8 is **documentation only** and does NOT modify the
> v0.1 judge checklist (§6) or N1-N8 in §2. The judge prompts at
> the locked tag (`prompts/judge_stage*.md`) score only against
> N1-N8. To reproduce v0.1 verdicts byte-for-byte, run from the
> locked tag: `git checkout prereg-v0.1-locked`. N9-N12 will be
> operationalized as flags by the v0.2 Structural Auditor agent
> (see `analysis/aristotelian/v0_1_report.md` §3.5 and §4).

## 1. Purpose

This file is **for judges only**. The tested model never sees it. After the
tested model reads `observations.md` and produces its own induced
regularities, judges read its output alongside this file and apply the
checklist in §6 to assign PASS or FAIL.

This is **not** a reference answer. There is no single correct induction.
Many distinct rule sets can pass. This file specifies the *necessary
conditions* an induction must satisfy and the *banned moves* that disqualify
it regardless of how elegant the rest is.

## 2. Necessary conditions

A passing induction must satisfy **all** of the following. Failing any one
condition triggers FAIL.

**N1 — Two-regime distinction for terrestrial motion.**
The induction must distinguish between (a) motion that requires a sustained
external cause and ceases when the cause is removed, and (b) motion or rest
that is the body's "default" state. Without this distinction, observation 2
(cart slowing) cannot be explained.

**N2 — Heavier-falls-faster ordering.**
The induction must include a rule that heavier bodies reach the ground
sooner than lighter bodies released from the same height. Required to
account for observations 1 and 12.

**N3 — Medium-resistance dependence.**
The induction must include a rule that the speed at which a body falls or
moves through a substance depends on the substance: thicker substances slow
the body more. Required for observation 9.

**N4 — Shape dependence.**
The induction must include a rule that, for bodies of equal weight, shape
affects rate of fall (compact vs. extended). Required for observation 11.

**N5 — Directional preference of certain substances.**
The induction must explain why some substances move upward of their own
accord (smoke, flame) and others move downward (water, stone, iron),
independently of how the surrounding object is oriented. Required for
observations 3, 4, 8.

**N6 — Heaven/earth split (or equivalent).**
The induction must recognize that observation 10 (Sun, Moon, stars on
unending circular paths) does not fit the same rules as terrestrial
observations. Either by explicitly proposing two regimes, or by flagging
the celestial case as outside the scope of the terrestrial rules.

**N7 — Acknowledgment of the projectile tension.**
Observation 7 (arrow continuing after leaving the bow) is in tension with
N1: the arrow keeps moving with no visible mover. The induction must
acknowledge this tension. **A specific resolution is not required** — it is
sufficient to flag the case as a difficulty for the otherwise-stated rules.
Pretending observation 7 is not problematic is FAIL.

**N8 — Some account of floating.**
The induction must give *some* explanation for observation 5 (oak floats,
stone sinks). The explanation does not need to match Aristotle's; it can be
in terms of weight, of natural directional preference, or of substance
type. Leaving the observation unexplained is FAIL.

## 3. Banned concepts

Use of any of the following terms or their direct equivalents in the
induced rules is automatic FAIL — regardless of whether the rest of the
induction is well-formed:

- inertia
- acceleration
- force (as a defined quantity, e.g. F = ma)
- momentum, momentum conservation
- energy, energy conservation
- mass (as distinct from weight)
- density (as a defined quantity)
- gravity, gravitational force, universal gravitation
- vacuum (except as a hypothetical to be argued against)
- friction, frictional force
- Newton, Galileo, Archimedes, or any post-Aristotelian physicist by name
- references to controlled experiments unavailable to the observer
  (evacuated chambers, low-friction tracks, inclined-plane timing)

**Allowed**: ordinary descriptive language including "heavy," "light,"
"thick," "thin," "fast," "slow," "pushes," "pulls," "rises," "sinks,"
"resists." The line between description and theoretical loading is: words
that any non-physicist would use to describe what is seen are allowed;
words that import a measurement scheme or a quantitative law are not.

## 4. Coverage map

A passing induction must produce at least one rule that explains each
observation. Judges check this mapping line by line.

| Obs | Phenomenon                          | Must be explained by a rule covering... |
|-----|-------------------------------------|------------------------------------------|
| 1   | Iron ball vs. dried pea fall        | weight ordering (N2)                     |
| 2   | Cart pushed, then stops             | two-regime motion (N1)                   |
| 3   | Smoke rises                         | upward preference (N5)                   |
| 4   | Rain falls and pools                | downward preference (N5)                 |
| 5   | Stone sinks, oak floats             | some account of floating (N8)            |
| 6   | Loaded cart needs more pull         | weight–effort relation (related to N1, N2) |
| 7   | Arrow continues after release       | projectile tension acknowledged (N7)     |
| 8   | Flame upward regardless of tilt     | upward preference, body-independent (N5) |
| 9   | Pebble in honey vs. air             | medium dependence (N3)                   |
| 10  | Sun, Moon, stars on circular paths  | heaven/earth split (N6)                  |
| 11  | Flat sheet vs. ball, equal weight   | shape dependence (N4)                    |
| 12  | Iron bar straight, down vs. drifting| weight-vs-medium interplay (N2 + N3)     |

Any observation not covered by at least one stated rule → FAIL.

## 5. Common near-passes that fail

These patterns look reasonable on first reading but trigger FAIL. Judges
should be alert to them.

- **"Heavier falls faster because of greater gravitational force."**
  FAIL — "gravitational force" is banned (§3). The model has imported a
  concept not derivable from observations.

- **"The arrow continues because of momentum / inertia carried from the bow."**
  FAIL — "momentum" and "inertia" are banned (§3).

- **"Flame rises because hot air is less dense."**
  FAIL — "density" is banned as a defined quantity. Note: "thin air rises"
  is allowed; "lower density" is not.

- **"The cart stops because friction acts against its motion."**
  FAIL — "friction" is banned. Allowed paraphrase: "the road resists the
  cart, and once nothing pushes it, the resistance stops it."

- **"I cannot induce a unified law from these observations."**
  FAIL — induction is not required to be unified across all 12
  observations. The model must still produce *some* rules that cover the
  observations. Refusing to induce is FAIL.

- **"Heavier bodies fall faster, and this is because they have more mass
  pulling them down."**
  FAIL — "mass" is banned as a distinct concept; "pulling them down" is
  acceptable phrasing only if no further quantitative apparatus is
  introduced.

- **"Observation 7 (arrow) shows that bodies retain motion once given to
  them."**
  PASS if the induction explains observation 7 via a Buridan / Oresme-style
  *impetus* — an *impressed motion* or *impressed force* that is explicitly
  described as **fading** with time and/or with medium-resistance, rather
  than as conserved. This is medieval scholastic Aristotelianism (impetus
  theory), and is consistent with the framework's permitted elaboration
  policy in §"Note on framework extrapolation" above.
  PASS also if the induction merely flags observation 7 as a
  noted-but-unresolved feature.
  FAIL if "retained motion" is formalized as a conserved quantity — that
  slips into Newtonian momentum and trips §3 even if the word "momentum"
  is never used.

## 6. Judge checklist

Apply in order. Stop at the first FAIL.

```
Step 1. Scan induced rules for banned concepts (§3).
        Any banned concept present?  → FAIL.

Step 2. Check necessary conditions N1–N8 (§2).
        Any condition unmet?         → FAIL.

Step 3. Check coverage map (§4).
        Any observation uncovered?   → FAIL.

Step 4. Check near-pass patterns (§5).
        Any pattern present?         → FAIL.

Step 5. All checks passed.            → PASS.
```

The judge records, for each FAIL, the specific step and clause that
triggered it (e.g., "FAIL at Step 1: 'inertia' appears in rule 3" or "FAIL
at Step 2: condition N6 unmet — heaven/earth distinction not made").

## 7. Notes for judges

- **Equivalent phrasings are equivalent.** "Motion needs a continuous
  cause" and "moving things stop unless something keeps moving them" mean
  the same thing. Both pass N1.

- **The model may invent new vocabulary.** If the model says "all bodies
  carry an inner urge toward their proper region," do not FAIL it for
  introducing "inner urge" — that is induced vocabulary, not imported
  physics. FAIL only on §3 banned terms or on rules whose content is
  Newtonian/modern regardless of label.

- **Length is not quality.** A three-sentence induction that satisfies all
  conditions passes. A three-page induction that violates §3 fails.

- **When in doubt, FAIL with explicit reasoning.** A FAIL with a clear
  citation to §2/§3/§4 is more useful for the project than a charitable
  PASS that lets a near-miss through.

## 8. Structural criteria (post-v0.1 documentation)

> **Documentation only.** These criteria were surfaced during the v0.1
> human audit (see [`analysis/aristotelian/v0_1_audit_human_review.md`](../../analysis/aristotelian/v0_1_audit_human_review.md)
> and [`analysis/aristotelian/v0_1_report.md`](../../analysis/aristotelian/v0_1_report.md) §3.5).
> They are **not** part of the v0.1 judge checklist in §6 and were
> **not** applied to any v0.1 verdict. In v0.2 they will be
> operationalized as **flags** emitted by the Structural Auditor agent
> (Agent 2), not as criteria scored by the dual judges, to avoid
> amplifying inter-judge disagreement on threshold-laden questions.

### Motivation

The v0.1 dual-judge architecture detects **content violations** (banned
words, missing rules, individual-rule failures) but not **structural
violations** of the rule set as a whole — redundancy,
over-parameterisation, fabricated mechanism, flat enumeration. Both
judges can silently PASS a structurally broken rule set if every
individual rule clears N1-N8 and avoids §3 banned words. The v0.1 audit
surfaced one clear case of this (GPT trial 3) and indications of milder
versions in others.

N9-N12 close that gap.

### N9 — Parsimony

The total rule count should not vastly exceed the observation count.
With 12 observations as input, an induction producing significantly
more than ~12 rules suggests either redundancy or fabrication beyond
what the observations support.

**Proposed v0.2 thresholds (Agent 2):**
- `rule_count > 15` → Tier-2 structural flag.
- `rule_count > 20` → Tier-1 structural flag.

**Trigger case (v0.1):** GPT trial 3 Stage 2 produced 17 rules from 12
observations. Both judges PASSed it because parsimony is not in N1-N8.

### N10 — Independence

No two rules should describe the same phenomenon. Each rule must add
content the other rules do not already cover.

**Operationalization:** Agent 2 clusters rule statements by semantic
similarity (LLM judgment, low temperature). Any cluster with > 1
member → flag, with the cluster members listed verbatim for human
review.

**Trigger case (v0.1):** GPT trial 3 Stage 2 — rule 9 and rule 13 both
stated "the cart stops once pushing ceases" with slightly different
framings.

### N11 — Coverage traceability

Each rule must trace to specific observation(s). A rule that does not
trace to any observation has been fabricated. This is functionally
equivalent to introducing a banned concept: the rule content is not
derivable from the input, even if no §3 word appears.

**Operationalization:** Agent 2 prompts the model output (or applies a
post-hoc trace) for an observation-id citation per rule. Any rule with
no traceable source → flag.

**Trigger case (v0.1):** GPT trial 3 Stage 2 rule 13 introduced "the
road and air rob motion from the cart." No observation among the 12
mentions the road or air as a motion-robbing mechanism. The mechanism
is fabricated and conceptually equivalent to Newtonian friction, but
does not trip §3 because the word "friction" is never used.

### N12 — Hierarchy

The rule set should have logical structure — core principles and
derived corollaries — not a flat enumeration. A list of N rules with
no explicit relations between them is a sign of pattern-matching
rather than theory-building.

**Operationalization:** Agent 2 scans for hierarchy markers (`derived
from`, `corollary of`, `combined with`, `special case of`, `follows
from rule N`, etc.). Total absence in a rule set of size ≥ 5 → Tier-2
flag.

### Why these are not in §2 or §6

N1-N8 (§2) check that each individual rule is *content-acceptable* —
no banned words, covers the required phenomena. N9-N12 check that the
rule *set* is *structurally acceptable* — parsimonious, independent,
traceable, hierarchical. The two axes are orthogonal: a rule set can
have zero banned words and still be a redundant, fabricated, flat soup.

The v0.1 prereg locked N1-N8 only. Bolting N9-N12 into §6 (the judge
checklist) would require the dual LLM judges to score on
threshold-laden criteria ("how many rules is too many?", "are these
two rules really saying the same thing?"), which is the class of
question where inter-judge IRR is hardest to control. v0.2 keeps the
axes separate: dual judges apply N1-N8, Agent 2 emits N9-N12 flags,
and human review is the tie-breaker on both pathways.

## Changelog

- **v0.1 (2026-05-08)** — Initial lean draft. Necessary-conditions style
  per project decision (selecting option 2 over single-answer style).
  Banned terms include quantitative concepts (mass, density, momentum,
  force-as-quantity); descriptive terms (heavy, thick, fast) allowed.
  Projectile tension required to be acknowledged but not resolved.

- **2026-05-12 — post-v0.1 documentation expansion.** Added §8
  Structural criteria (N9-N12). Documentation-only; does NOT modify
  §2 (N1-N8) or §6 (judge checklist) used at the
  `prereg-v0.1-locked` tag. v0.1 reproducers should checkout the
  locked tag for the original file. N9-N12 will be operationalized
  as flags by the v0.2 Structural Auditor agent (Agent 2).
