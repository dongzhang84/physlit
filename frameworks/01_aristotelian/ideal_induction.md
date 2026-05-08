# Ideal Induction — Aristotelian Mechanics

> **Status:** DRAFT v0.1 (lean) — 2026-05-08
> **Framework ID:** 01_aristotelian
> **Stage:** 1 (Induction)

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

## Changelog

- **v0.1 (2026-05-08)** — Initial lean draft. Necessary-conditions style
  per project decision (selecting option 2 over single-answer style).
  Banned terms include quantitative concepts (mass, density, momentum,
  force-as-quantity); descriptive terms (heavy, thick, fast) allowed.
  Projectile tension required to be acknowledged but not resolved.
