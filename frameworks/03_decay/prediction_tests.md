# Prediction Tests

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-21
> **Framework ID:** 03_decay

Five novel scenarios used in Stage 3. None of them appears among the
ten observations in `observations.md`. Each scenario is presented to
the model along with its own Stage 2 operational rules (replayed as
input).

For each scenario the table lists what the **Decay World** predicts
(the answer that counts as PASS) and what **standard physics**
predicts (the answer that signals contamination from training data).

A Stage 3 trial passes for a scenario only if the model's prediction
is derivable from its own Stage 2 rules and matches the Decay World
column. A prediction matching the standard-physics column — or one
that invokes a banned token (`ideal_induction.md` §3) to justify
either answer — fails. For the four quantitative scenarios (1, 2, 3,
4) the **ratio matters**: a prediction with the right sign but the
standard-physics ratio still fails. See `pass_fail_criteria.md`,
Stage 3.

The Stage 1 prompt that produced the Stage 2 rules carries the
axiomatisation cue used in 02_fmv.2 and v0.3:

> Aim for the smallest set of rules that still explains every
> observation. Do not state as a separate rule anything that
> already follows from rules you have given; if one rule is a
> special case or a consequence of another, say so instead of
> listing it on its own. Prefer a few general rules over a long
> list of specific ones.

Stage 3 carries no such cue — it is plain prediction.

---

## Scenario 1 — Pendulum amplitude after thirty seconds

**Prompt to the model.** A pendulum is released from rest at a swing
angle of 10° in still air. The pendulum is well-built and
well-supported; the pivot is smooth. The pendulum is allowed to
swing freely. What is its swing angle exactly 30 seconds after
release — still about 10°, about 7.4°, very close to 0°, or some
other value? Explain.

| Column | Prediction |
| ------ | ---------- |
| Decay World (PASS) | The measured quantity (swing angle) shrinks at about 0.99 per second, so after 30 seconds the angle is **about 10 × 0.99³⁰ ≈ 7.4°**. |
| Standard physics (FAIL) | An ideal pendulum is taken to be a conservative oscillator: with a smooth pivot and only light air around it, the swing angle is **essentially unchanged — still about 10°** — or, if the model invokes air damping, "a tiny bit less", but on the order of a fraction of a percent. |

**Why this scenario.** Quantitative test of N1 + N2 + N4 + N6 in
the mechanical-oscillation domain. The discriminator is the ratio:
the standard-physics reflex on a pendulum is *near-zero amplitude
loss in 30 seconds*; the Decay World prediction is *a quarter of
the amplitude already gone*. A model that says "the amplitude
drops a small amount" without committing to the 7.4° value has not
applied the rate it should have induced.

---

## Scenario 2 — Hot tea cooling for sixty seconds

**Prompt to the model.** A cup of tea is sealed at 400 K inside a
perfectly insulated chamber under vacuum — no heat can leave by
contact, by air, or by radiation. What is the temperature of the
tea exactly 60 seconds after sealing — still close to 400 K, about
360 K, about 220 K, about 293 K (room temperature), or some other
value? Explain.

| Column | Prediction |
| ------ | ---------- |
| Decay World (PASS) | The measured quantity (absolute temperature) shrinks at about 0.99 per second, so after 60 seconds the temperature is **about 400 × 0.99⁶⁰ ≈ 219 K** (≈ −54 °C) — *below* the surrounding room temperature. |
| Standard physics (FAIL) | Heat cannot leave a perfectly insulated chamber, so the temperature is **essentially unchanged — still close to 400 K**. (A model that smuggles in a leakage term will give "approaches the surrounding room temperature of about 293 K", which is also FAIL.) |

**Why this scenario.** Quantitative test of N1 + N2 + N4 + N6 in
the thermal domain. The diagnostic is that Decay-World cooling
goes *below* the ambient — the temperature trajectory is toward
absolute zero, not toward the room. A model that has induced the
universal multiplicative decay will give 219 K; a model that has
defaulted to standard insulated-cup reasoning will give either
"400 K, unchanged" or "approaches room temperature".

---

## Scenario 3 — Spinning flywheel after one hundred seconds

**Prompt to the model.** A heavy flywheel is set spinning at 200
rad/s on a smooth, polished, polished-tip pivot inside an evacuated
chamber. There is no air, and the pivot contact involves no rubbing
or sliding — nothing in contact with the flywheel that would slow
it by familiar mechanical means. What is its spin rate exactly 100
seconds after release — still about 200 rad/s, about 180 rad/s,
about 73 rad/s, or some other value? Explain.

| Column | Prediction |
| ------ | ---------- |
| Decay World (PASS) | The measured quantity (rotation rate) shrinks at about 0.99 per second, so after 100 seconds the rate is **about 200 × 0.99¹⁰⁰ ≈ 73 rad/s**. |
| Standard physics (FAIL) | In vacuum, with no contact rubbing, an isolated spinning body has no torque acting on it, so its angular rate is **essentially unchanged — still about 200 rad/s**. (A model that invokes "tiny imperfections in the pivot" will give "a slight reduction", which is also FAIL.) |

**Why this scenario.** Quantitative test of N1 + N2 + N4 + N6 in
the rotational domain. This is the closest scenario to a
textbook-perfect "no friction" setup; the standard-physics
prediction is "no change" with high confidence. A model that has
genuinely induced the universal rate will commit to 73 rad/s.

---

## Scenario 4 — Orbital radius shrinkage over sixty seconds

**Prompt to the model.** A small marble is set into a nearly
circular orbit at an initial radius of 1 metre around a heavy
fixed sphere that pulls it inward. The orbit is in vacuum, and
the marble does not touch the central sphere. What is the orbital
radius exactly 60 seconds after launch — still about 1 metre,
about 0.95 metres, about 0.55 metres, or some other value?
Explain.

| Column | Prediction |
| ------ | ---------- |
| Decay World (PASS) | The measured quantity (orbital radius) shrinks at about 0.99 per second, so after 60 seconds the radius is **about 1 × 0.99⁶⁰ ≈ 0.55 metres**. |
| Standard physics (FAIL) | A circular orbit in vacuum is stable (Keplerian, by conservation of angular momentum and energy), so the radius is **essentially unchanged — still about 1 metre**. |

**Why this scenario.** Quantitative test of N1 + N2 + N4 + N6 in
the orbital domain. The standard-physics reflex is "orbits in
vacuum are stable"; the Decay World prediction is a near-halving
of the radius in one minute. The diagnostic ratio 0.55 versus 1.0
is large enough that no measurement-noise argument can bridge it.

---

## Scenario 5 — Will an ideal pendulum ever stop?

**Prompt to the model.** A pendulum is built with a perfectly
smooth, frictionless pivot and is placed in a perfectly evacuated
chamber. (Idealised: no air, no contact rubbing.) It is released
from a 10° swing angle. Does it swing forever, or does it
eventually stop? If it eventually stops, roughly how long does it
take for its swing angle to fall to one-hundredth of the starting
angle (i.e. about 0.1°)?

| Column | Prediction |
| ------ | ---------- |
| Decay World (PASS) | The pendulum **eventually stops** even in idealised conditions: the swing angle shrinks at about 0.99 per second, so it falls to one-hundredth of the starting angle when 0.99ᵗ = 0.01, i.e. at **t ≈ 458 seconds (about 7 to 8 minutes)**. |
| Standard physics (FAIL) | An ideal pendulum with a frictionless pivot in perfect vacuum is a conservative oscillator and **swings forever** — its swing angle never falls. (A model that says "it would take an astronomical time" is also FAIL — it is making the same conservative-oscillator assumption with vague hedging.) |

**Why this scenario.** Qualitative + timescale test of N1 (the
decay is intrinsic; closed-system isolation does not stop it) and
N6 (the rate has a value, from which a timescale follows). The
yes/no question alone is enough to discriminate: the standard
answer is *"forever"*. A model that says *"eventually stops"* and
gives a timescale on the order of 458 seconds (anywhere in roughly
300–700 seconds) passes; a model that says *"forever"* — or that
hedges with "indefinitely" / "astronomical" — fails.

---

## Author signatures

- 2026-05-21 — initial draft. **DRAFT — author review required
  before prereg lock.**
