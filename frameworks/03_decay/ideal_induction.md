# Ideal Induction

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-21
> **Framework ID:** 03_decay
> **Stage:** 1 (Induction)

## 0. Design note — this file is written to be mechanical

The v0.1 Aristotelian criteria left their hardest call to judgment.
`ideal_induction.md` §3 banned "density (as a defined quantity)"; §5
said the bare word "denser" fails. Those pulled apart, and a human
auditor (strict-literal) and an LLM resolver (interpretive) resolved
the gap in opposite directions — the dominant cause of v0.2's
Agent 1 / Agent 2 disagreement with the human audit. `02_fmv` and
`v0.3` carried the corrected mechanical style; this file continues
it.

Every FAIL trigger below is a check a judge applies the same way
every time: a literal token match (§3) or a concrete, quoted claim
pattern (§5). A judge does **not** assess intent, charity,
sophistication, or "how the concept was used". If two judges read
the same response and the criteria, they should reach the same
verdict.

## 1. Purpose

This file is **for judges only**. The tested model never sees it.
After the tested model reads `observations.md` and produces its own
induced rules, judges read its output alongside this file and apply
the checklist in §6.

The tested model is given `observations.md` and **one paragraph of
axiomatisation guidance** appended to the Stage 1 prompt, identical
to the cue used in `02_fmv.2` and `v0.3`:

> Aim for the smallest set of rules that still explains every
> observation. Do not state as a separate rule anything that already
> follows from rules you have given; if one rule is a special case
> or a consequence of another, say so instead of listing it on its
> own. Prefer a few general rules over a long list of specific ones.

This framework bakes the cue in from the start (rather than running
a no-cue control arm first and a cued arm second, as the F=mv and
Aristotelian arcs did). The reason: `02_fmv.2` and `v0.3` have
already established that the cue lifts the structural pass rate
substantially without degrading content; the question for the
03_decay framework is whether the *cued* induction can clear the
content axis on a deliberately harder counterfactual.

The model is **not** told that this world is counterfactual, not
told the name of any law, not told what to avoid (beyond the
explicit banned-vocabulary list quoted in the Stage 1 prompt). It
must induce the regularities itself.

This is **not** a reference answer. Many distinct rule sets pass.
This file states the *necessary conditions* an induction must
satisfy and the *banned moves* that disqualify it regardless of how
well the rest reads.

## 2. Necessary conditions

A passing induction must satisfy **all** of N1–N6. Failing any one
triggers FAIL. "The rules state X" means a stated rule asserts X in
any wording; equivalent phrasings are equivalent (see §7).

**N1 — Closed systems lose their measurable state over time.**
The rules must state that every closed system in this world — one
isolated from outside push, pull, heat exchange, or radiation — has
its directly observed quantity (amplitude, temperature, rotation
rate, etc.) decline over time on its own, with no external mechanism
required to cause the decline. Required by all ten observations.

**N2 — The decline is multiplicative.**
The rules must state that the decline is multiplicative: the
measured quantity at time t + Δ is a constant ratio of the quantity
at time t for any fixed Δ. This rules out a purely additive
("subtract a fixed amount per second") decline. Required by
observations 2, 4, 9: only a multiplicative decline yields a
per-second ratio that is consistent across systems of different
units and time scales. A linear-subtraction rule would give a
different rate constant for each system, which contradicts the
matching numerical ratios in those three observations.

**N3 — The rate is fixed by elapsed time.**
The rules must state that the rate of the decline is attached to
**elapsed time** — not to cycle count, not to mechanical contact,
not to material composition, not to the kind of motion or process.
Required by:
(a) observation 1, where the per-cycle loss differs between long
and short pendulums (so cycle count is not the time-keeper); in
conjunction with
(b) observations 2, 4, 9, where the per-second ratio matches across
three different systems at three different time scales (100 s, 10 s,
50 s).
A rule attaching the rate to anything other than elapsed time
(e.g. "amplitude loses a fixed fraction per cycle", "thermal motion
loses a fixed fraction per molecular collision") FAILs N3.

**N4 — The rate is the same across all closed systems
(universality).**
The rules must state that the per-time rate of decline is a single
number applied to every closed system in this world, regardless of
the system's domain, kind of motion, or measured quantity.
Required by observations 2, 4, 9: a mechanical oscillator, a
thermal cup, and a rotating top all show the same per-second
ratio. A rule that gives a different rate per system, or that
treats some systems as exempt, FAILs N4.

**N5 — The rate is independent of weight, material, and composition.**
The rules must state that the rate does not depend on the weight,
material composition, size, colour, or any other physical property
of the system. Required by observation 10: a one-gram brass bob
and a one-kilogram brass bob — and bobs of brass, glass, or ice —
all show identical behaviour. A rule that makes the rate depend on
weight, material, or composition FAILs N5.

**N6 — The rate is approximately 0.99 per second (≈ 1 % loss per
second).**
The rules must state the numerical value of the rate, accurate to
about one percentage point. Acceptable forms include
*"the measured quantity retains about 99 % of its previous value
each second"*; *"each second the quantity falls by about 1 %"*;
*"the ratio of one second's measurement to the next is about
99 : 100"*; *"the halving time is about 69 seconds"*; or any
equivalent statement. A rule that asserts decay without giving a
rate, or that gives a rate badly off the value derivable from
observations 2, 4, 9 (e.g. 10 % per second, 0.01 % per second),
FAILs N6.

**General — consistency and coverage.** Beyond N1–N6: the rules
must be mutually consistent (no two rules make contradictory claims
about the same system in the same situation), and every observation
must be covered by at least one rule (see the coverage map, §4).
Either failing → FAIL.

## 3. Banned tokens — purely lexical test

If any token in the list below — **or a morphological variant of
it** (plural, `-ing`, `-ed`, `-al`, adjective / adverb form) —
appears **anywhere in the tested model's response**, the trial
FAILs at Step 1. No exceptions.

This is a **purely lexical test**. A judge does **not** assess
whether the model "defined" the concept, used it "only
descriptively", used it "correctly", used it in a subordinate
clause, or named it "only to deny that it applies". Presence of
the token = FAIL. (Aristotelian / 02_fmv precedent, carried over:
naming a concept only to deny its applicability still counts as
use.)

**Banned tokens — core (energy & thermodynamics):**

- `energy` (catches all compounds: kinetic energy, potential energy,
  thermal energy, …)
- `kinetic`
- `potential` (as the energy-physics noun; everyday adjective use
  like "potential outcome" still falls under the lexical rule and
  also fails — the model has no need to use the word in induction)
- `conservation` (catches `conserve`, `conserved`)
- `entropy`
- `thermodynamic` (catches `thermodynamics`)
- `Hamiltonian`
- `Lagrangian`

**Banned tokens — mechanism (decay-specific):**

- `friction` (catches `frictional`, `frictionless`)
- `drag`
- `damping` (catches `damp`, `damped`, `dampen`, `dampening`)
- `dissipation` (catches `dissipate`, `dissipative`)
- `viscous` (catches `viscosity`)
- the phrase `air resistance`
- `resistance` (catches `resistive`)
- `attenuation` (catches `attenuate`, `attenuated`)

**Banned tokens — mechanics:**

- `force` (catches `forces`, `forcing`)
- `mass` (catches `massive`, `masses`)
- `acceleration` (catches `accelerate`, `accelerating`, `decelerate`,
  `decelerating`)
- `momentum`
- `inertia` (catches `inertial`)

**Banned tokens — physicist names:**

- `Newton`, `Newtonian`
- `Joule`
- `Carnot`
- `Boltzmann`
- `Clausius`
- `Helmholtz`
- `Galileo`, `Galilean`
- `Maxwell`
- `Lagrange`, `Hamilton`
- any other physicist's proper name introduced to invoke a named law

**Banned equation forms:**

- `F = ma` (or `F=ma`, in any notation)
- `E = mc²` (or `E=mc^2`)
- any equation explicitly named (e.g. "the Hamiltonian equation",
  "Newton's law of cooling")

**Why these and not others (for judges — not a loophole).** Every
banned token names a concept from standard physics or a named
mechanism that a model would import from its training data, not
derive from the ten observations. The observations are written
entirely in plain language and use **none** of these tokens; the
model therefore has, in the observations themselves, a complete
vocabulary for describing this world. Reaching for a banned token
is by construction reaching outside the given evidence.

**Allowed vocabulary** (non-exhaustive): the directly observed
phenomena and quantities — pendulum, amplitude, swing, spring,
oscillation, water, temperature, kelvin, bell, vibration, rim,
sphere, ball, track, marble, orbit, radius, top, spin, rotation,
rate; pull, push, tug, press, effort, support; smooth, polished,
contact, contactless, evacuated, sealed, insulated; rubbing,
scraping, sliding; weight, heavy, light, heavier, lighter; second,
minute, time, elapsed; ratio, fraction, percent, hundredth,
multiplicative, exponential (as a curve shape), constant, steady;
decay, decline, decrease, shrink, diminish, fade, wane, retain,
remain, lose.

The model is free — and indeed expected — to invent its own term
for the underlying quantity that is observed to shrink across all
systems (the framework rule talks about *the directly measured
quantity*, not about energy). Acceptable invented terms include
"the carried amount", "the held quantity", "the system's
persistence", "vigour", "the running level", and similar — any
unifying noun that is not a banned token. A model that does not
invent such a unifying term, but instead applies the per-second
decay to each measured quantity separately (amplitude shrinks at
0.99/s, temperature shrinks at 0.99/s, rate shrinks at 0.99/s, …)
also satisfies N4 if it states the rate is the same across all of
them.

**Phrasing the negations without a banned token.** The model
must describe what causes the decay (an intrinsic property of
isolated systems in this world) without reaching for friction,
drag, damping, dissipation, or any standard-physics mechanism.
Allowed phrasings: "the measured quantity shrinks on its own,
without anything outside the system acting on it"; "every isolated
system loses a fixed fraction of its current value each second,
by its own nature"; "the rate of the loss is set by elapsed time,
not by any contact or material". A model that writes "this is not
friction" or "this is not damping" or "energy is not conserved"
FAILs §3 by naming the banned concept to deny it.

## 4. Coverage map

Every observation must be explained by at least one stated rule.
Judges check this mapping line by line.

| Obs | Phenomenon | Covered by |
|-----|------------|------------|
| 1   | Per-swing loss depends on period (long pendulum loses more per swing) | N3 |
| 2   | Spring amplitude 10 cm → 3.7 cm over 100 s | N1, N2, N4, N6 |
| 3   | Heavy ball in vacuum approaches a maximum downward speed | N1 (against a steady downward pull) |
| 4   | Water 353 K → 319 K over 10 s in insulated vacuum | N1, N2, N4, N6 |
| 5   | Bell vibration in vacuum rings down to stillness | N1 |
| 6   | Sphere on smooth, level track in vacuum slows to rest | N1 |
| 7   | Projectile horizontal speed declines during flight in vacuum | N1 |
| 8   | Marble's orbital radius shrinks over many circuits | N1 |
| 9   | Top spin rate 100 rad/s → 60.5 rad/s over 50 s | N1, N2, N4, N6 |
| 10  | Different bob weights and materials show identical behaviour | N5 |

Any observation not covered by at least one stated rule → FAIL.

## 5. Disqualifying patterns — binding

Each pattern below is an automatic FAIL. They are stated as
concrete claims so a judge checks them by reading the rules, not by
interpretation. For each FAIL the judge quotes the offending rule
verbatim.

- **P1 — Contact-mechanism rescue.** A rule attributing the
  decline to a friction, drag, damping, viscous, dissipative,
  rubbing, or contact-resistive mechanism — i.e. positing some
  agent in contact with the system as the cause. Contradicts
  observations 3 (ball not touching track), 6 (smooth track, no
  rubbing, no force along motion), 8 (marble in vacuum), 9
  (polished point, no rubbing). The relevant standard-physics
  tokens are also banned by §3.

- **P2 — Hidden-substrate framing.** A rule structured as *"some
  underlying quantity X is the substrate that decays at the fixed
  per-second rate, and each system's measured quantity is derived
  from X"* — **regardless of what X is named** (*energy*, *the
  underlying state*, *vigour*, *the system's persistence*, *the
  carried amount*, …). The framework's rule is that the **directly
  measured quantity itself** is the object of the decay rule;
  introducing a hidden layer beneath it adds structure not derivable
  from any observation.

  The most common instance is the energy-substrate framing the model
  is expected to reach for. Under energy-decay-as-substrate with
  standard-physics derivations (amplitude scales as the square root
  of energy in a harmonic oscillator, temperature scales linearly
  with thermal energy in a fixed heat-capacity system, rotational
  rate scales as the square root of rotational energy), the
  per-second rate of the measured quantity would *differ across
  systems*, but observations 2, 4, 9 give the *same* per-second
  ratio for the measured quantity directly — this case FAILs on
  numerical grounds (the rates won't reconcile across the three
  observations).

  An ad-hoc substrate with arbitrary-exponent derivations that
  *does* give a consistent per-system rate by construction (e.g.
  "X decays at 0.9801 / s, every measured quantity = √X") **also
  FAILs P2**: it is a relabelling that adds an unwarranted layer.
  It violates both the framework's "measured quantity directly"
  rule and the Stage 1 axiomatisation cue's prohibition on stating
  any rule that already follows from rules already given (since X
  is derivable from each measured quantity, the X-as-substrate rule
  is a layer added on top, not below). The token `energy` is also
  banned by §3.

- **P3 — Additive (linear) decay.** A rule stating that the
  decline is a fixed amount subtracted per unit time (e.g.
  "amplitude loses 0.063 cm per second", "temperature loses 3.4 K
  per second"). Under additive decay the per-system rate constant
  is dimensioned and incomparable across systems — N4
  (universality) cannot then be stated. Contradicts the matching
  unitless per-second ratios in observations 2, 4, 9.

- **P4 — Per-cycle rate.** A rule stating that the decay rate is
  attached to oscillation cycles, swings, periods, collisions, or
  any cyclic event, rather than to elapsed time. Contradicts the
  cross-domain consistency in observations 2, 4, 9 (the time
  scales differ but the per-time ratio is the same), and
  contradicts the per-cycle period-dependence in observation 1.

- **P5 — Material- or weight-dependent decay.** A rule stating
  that the decay rate depends on the weight, mass, material,
  colour, size, or any physical property of the system.
  Contradicts observation 10.

- **P6 — Decay without a rate.** A response that lists qualitative
  decay phenomena and states the rate is universal, but does not
  state a numerical value for the rate (or a ratio, fractional
  loss, or half-life equivalent to it). The three quantitative
  data points are given precisely so the rate can be derived.
  Failing N6 (no rate stated, or a rate badly off ~ 0.99 / s)
  triggers this pattern.

- **P7 — Refusal of the world.** A response that declines on the
  grounds that the observations are physically impossible, violate
  conservation of energy, contradict the second law of
  thermodynamics, or "are not how physics works". The observations
  are to be taken as accurate and complete (see `observations.md`);
  the task is to induce their regularities, not to reject them.
  A model that mentions the conservation-of-energy or second-law
  concerns also FAILs §3 (banned tokens).

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
token, and a verbatim quote (e.g. "FAIL at Step 1: token
'friction' in rule 3" or "FAIL at Step 5: pattern P2 — rule 1
posits energy as the underlying decaying quantity, citing 'energy
loss at 1 % per second'").

## 7. Notes for judges

- **Equivalent phrasings are equivalent — for the positive
  conditions only.** N1–N6 are checked by meaning: "the measured
  quantity falls to about 99 % of its previous value each second"
  and "every isolated system retains about 99 hundredths of what
  it had a second earlier" both satisfy N2 + N6. This charity
  applies to §2 only. It does **not** apply to §3: §3 is a literal
  token test, not a meaning test.
- **The model never sees this file.** It is told the banned-token
  list in the Stage 1 prompt (the same list as §3), but it is not
  told the necessary conditions, the coverage map, or the
  disqualifying patterns. A model that avoids the banned tokens
  and satisfies N1–N6 does so by inducing from the observations'
  own vocabulary; a model that uses one has reached outside the
  evidence. That is the signal being measured.
- **§3 scope is the whole response.** Carrying over from 02_fmv:
  the banned-token test applies to the entire model response, not
  only to a section labelled "induced rules". Deciding what counts
  as a rule is itself a judgment call this file is trying to
  eliminate.
- **Structural criteria (the v0.2 N9–N12 axis) are deliberately
  not in this file.** If a structural axis is used for this
  framework it will be specified separately and mechanically; it
  is out of scope for this file.
- **Author note on the axiomatisation cue.** The Stage 1 prompt
  includes the cue quoted in §1 (the same wording as 02_fmv.2 and
  v0.3). Judges should expect a tighter, more consolidated rule
  set than under a no-cue prompt; this does **not** lower the
  threshold for N1–N6 or §3. A consolidated rule set is welcome,
  but if it consolidates by reaching for a banned mechanism (e.g.
  "everything loses energy at the same rate"), it FAILs.
