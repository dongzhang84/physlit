# Ideal Induction

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-17
> **Framework ID:** 02_fmv
> **Stage:** 1 (Induction)

## 0. Design note — this file is written to be mechanical

The v0.1 Aristotelian criteria left their hardest call to judgment.
`ideal_induction.md` §3 banned "density (as a defined quantity)"; §5
said the bare word "denser" fails. Those pull apart, and a human
auditor (strict-literal) and an LLM resolver (interpretive) resolved
the gap in opposite directions — the main cause of the v0.2 Agent 1 /
Agent 2 disagreement with the human audit.

This file is written to remove that gap. **Every FAIL trigger below
is a check a judge applies the same way every time:** a literal token
match (§3) or a concrete, quoted claim pattern (§5). A judge does
**not** assess intent, charity, sophistication, or "how the concept
was used". If two judges read the same response and the criteria,
they should reach the same verdict.

## 1. Purpose

This file is **for judges only**. The tested model never sees it.
After the tested model reads `observations.md` and produces its own
induced rules, judges read its output alongside this file and apply
the checklist in §6.

The tested model is given **only** `observations.md`. It is not told
that this world is counterfactual, not told the name of any law, not
told what to avoid. It must induce the regularities itself.

This is **not** a reference answer. Many distinct rule sets pass.
This file states the *necessary conditions* an induction must satisfy
and the *banned moves* that disqualify it regardless of how well the
rest reads.

## 2. Necessary conditions

A passing induction must satisfy **all** of N1–N6. Failing any one
triggers FAIL. "The rules state X" means a stated rule asserts X in
any wording; equivalent phrasings are equivalent (see §7).

**N1 — Pace is set by the present push.**
The rules must state that a body's pace (how fast it moves) is
determined by the push acting on it *at that moment*: a present push
gives a present pace, and no push gives no pace. Required by
observations 1 and 6.

**N2 — More push, more pace.**
The rules must state that, for a given body, a greater push produces
a greater pace. Required by observation 4. (The *proportional* form —
doubling the push doubles the pace — is a Stage 2 formulation matter;
Stage 1 passes N2 with the monotone relation. A Stage 1 induction
that explicitly contradicts the doubling pattern of observation 4
FAILs.)

**N3 — More heaviness, less pace.**
The rules must state that, under one and the same push, a heavier
body moves at a smaller pace than a lighter one. Required by
observation 5.

**N4 — Motion is simultaneous with the push: no build-up, no
carry-over.**
The rules must state **both**:
(a) a body is at its full pace as soon as the push acts — the pace
does not build up gradually from rest (observation 2); and
(b) a body stops the instant the push ends — it does not coast,
drift, glide on, or otherwise continue (observations 3, 7, 11).
N4 is the load-bearing condition: it is where a "push builds up
speed, and speed then persists on its own" reading is excluded.

**N5 — Bodies fall at one common, unchanging pace.**
The rules must state that released bodies fall at a pace that is
(a) the same for a heavy body and a light body, and (b) unchanging
during the fall — it does not increase as the fall proceeds.
Required by observations 10 and 12.

**N6 — Pushes combine.**
The rules must state that two pushes acting on one body combine: same
direction adds, opposite directions subtract, and equal opposite
pushes leave the body at rest. Required by observations 8 and 9.

**General — consistency and coverage.** Beyond N1–N6: the rules must
be mutually consistent (no two rules make contradictory claims about
the same body in the same situation), and every observation must be
covered by at least one rule (see the coverage map, §4). Either
failing → FAIL.

## 3. Banned tokens — purely lexical test

If any token in the list below — **or a morphological variant of it**
(plural, `-ing`, `-ed`, `-al`, adjective/adverb form) — appears
**anywhere in the tested model's response**, the trial FAILs at
Step 1. No exceptions.

This is a **purely lexical test**. A judge does **not** assess whether
the model "defined" the concept, used it "only descriptively", used
it "correctly", used it in a subordinate clause, or named it "only to
deny that it applies". Presence of the token = FAIL. (Aristotelian
precedent, carried over: naming a concept only to deny its
applicability still counts as use.)

**Banned tokens:**

- `force`
- `velocity` (catches "terminal velocity")
- `acceleration` (and `accelerate`, `accelerating`, `decelerate`)
- `inertia` (and `inertial`)
- `momentum`
- `mass`
- `gravity` (and `gravitational`, `gravitate`)
- `friction` (and `frictional`)
- `energy` (in any compound: kinetic, potential, …)
- `Newton`, `Newtonian`, `Galileo`, or any physicist's proper name
- the equation `F = ma` (or `F=ma`) in any notation

**Why these and not others (for judges — not a loophole).** Every
banned token names a concept from standard (Newtonian) physics that a
model would import from its training data, not derive from the twelve
observations. The observations are written entirely in plain
phenomenological language and use **none** of these tokens; the model
therefore has, in the observations themselves, a complete vocabulary
for describing this world. Reaching for a banned token is by
construction reaching outside the given evidence.

**Allowed vocabulary** (non-exhaustive): push, pull, press, effort,
shove; pace, speed, fast, slow, quick, steady, unchanging; move,
travel, glide, halt, stop, stay, rest; heavy, light, heaviness,
weight; rise, fall, drop, descend; gather speed (allowed as a token;
see §5 P1 if a rule asserts build-up), build up, increase, add,
subtract.

**Phrasing the negations without a banned token.** The model must say
this world *lacks* a gradual speeding-up and *lacks* any coasting.
Allowed: "the pace does not increase / does not build up / stays
unchanging"; "the block stops at once and does not glide on". A
model that writes "there is no acceleration" or "the block has no
inertia" FAILs — the concept can and must be expressed in the plain
words above.

## 4. Coverage map

Every observation must be explained by at least one stated rule.
Judges check this mapping line by line.

| Obs | Phenomenon | Covered by |
|-----|------------|------------|
| 1  | Steady push → steady pace | N1, N4 |
| 2  | Full pace at once, no build-up | N4(a) |
| 3  | Push ends → stops at once | N4(b) |
| 4  | Twice the push → twice the pace | N2 |
| 5  | Twice as heavy → half the pace | N3 |
| 6  | Same behaviour in empty space, no contact | N1 |
| 7  | Crossing ground needs a push the whole way | N4(b) |
| 8  | Same-direction pushes add | N6 |
| 9  | Opposing pushes subtract / cancel | N6 |
| 10 | All bodies fall at one unchanging pace | N5 |
| 11 | Released body drops at the release point | N4(b) |
| 12 | Fall pace the same with or without air | N5 |

Any observation not covered by at least one stated rule → FAIL.

## 5. Disqualifying patterns — binding

Each pattern below is an automatic FAIL. They are stated as concrete
claims so a judge checks them by reading the rules, not by
interpretation. For each FAIL the judge quotes the offending rule
verbatim.

- **P1 — Build-up.** A rule stating that a push makes a body *speed
  up*, *gather speed*, or move *faster and faster* while the push
  continues. Contradicts observations 1 and 2 (pace is steady under a
  steady push).

- **P2 — Carry-over.** A rule stating that a body *keeps moving*,
  *coasts*, *drifts on*, or *continues* after the push is removed.
  Contradicts observation 3.

- **P3 — Hidden-resistance rescue.** A rule explaining the steady
  pace under a steady push, or the immediate stop, by positing a
  rubbing, a resistance, a drag, or an opposing agent that balances or
  cancels the push. Contradicts observations 6 (no contact) and 12
  (no air): there is nothing present to do the balancing. (The token
  `friction` is separately banned by §3.)

- **P4 — Heavier-falls-faster.** A rule stating that heavier bodies
  fall faster, or lighter bodies fall slower, or that fall pace
  depends on heaviness. Contradicts observation 10.

- **P5 — Falling speeds up.** A rule stating that a falling body
  gathers speed, falls faster the longer it falls, or speeds up as it
  descends. Contradicts observation 10.

- **P6 — Projectile arc.** A rule stating that a released or thrown
  body travels onward, sails forward, follows a curved or arcing
  path, or lands ahead of the point where it was released.
  Contradicts observation 11.

- **P7 — Refusal.** A response that declines to induce on the grounds
  that the observations are impossible, self-contradictory, or
  "not how motion works". The observations are to be taken as
  accurate and complete (see `observations.md`); the task is to
  induce their regularities, not to reject them.

## 6. Judge checklist

Apply in order. **Stop at the first FAIL.**

```
Step 1. Scan the whole response for banned tokens (§3).
        Any banned token present?            → FAIL.

Step 2. Check necessary conditions N1–N6 (§2).
        Any condition unmet?                 → FAIL.

Step 3. Check coverage (§4).
        Any observation uncovered?           → FAIL.

Step 4. Check mutual consistency (§2 General).
        Any two rules contradict?            → FAIL.

Step 5. Check disqualifying patterns P1–P7 (§5).
        Any pattern present?                 → FAIL.

Step 6. All checks passed.                   → PASS.
```

For each FAIL the judge records the step, the specific clause or
token, and a verbatim quote (e.g. "FAIL at Step 1: token 'inertia' in
rule 4" or "FAIL at Step 5: pattern P3 — rule 2 posits a balancing
resistance").

## 7. Notes for judges

- **Equivalent phrasings are equivalent — for the positive
  conditions only.** N1–N6 are checked by meaning: "a push sets the
  pace" and "how fast a thing goes follows the push on it" both
  satisfy N1. This charity applies to §2. It does **not** apply to
  §3: §3 is a literal token test, not a meaning test.
- **The model never sees this file.** It is not told the banned
  tokens. A model that avoids them does so by inducing from the
  observations' own vocabulary; a model that uses one has reached
  outside the evidence. That is the signal being measured.
- **§3 scope — author decision to confirm.** This draft scopes the
  banned-token test to the **whole response**, not only the "induced
  rules", because deciding what counts as a rule is itself a
  judgment call this file is trying to eliminate. v0.1 Aristotelian
  scoped it to the induced rules. This is stricter. **Author: confirm
  whole-response scope, or revert to rules-only.**
- **Structural criteria (the v0.2 N9–N12 axis) are deliberately not
  in this file.** If a structural axis is used for this framework it
  will be specified separately and mechanically; it is out of scope
  for this draft.
