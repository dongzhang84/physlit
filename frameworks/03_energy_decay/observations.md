# Observations

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-20
> **Framework ID:** 03_energy_decay
> **Tier:** 1 (simulator-codable — Determinism Contract in CLAUDE.md)

The following phenomena are written in plain descriptive language
without modern theoretical loading. The reader of this file is a
tested model attempting to induce the regularities of this world from
these observations alone (Stage 1 of the PhysLit protocol).

These observations were gathered in one particular setting. They are
to be taken as **accurate and complete**: the task is to induce the
regularities that hold here, not to correct the observations against
any prior expectation of how the world "should" behave.

Words such as *energy*, *friction*, *air resistance*, *drag*,
*viscous*, *damping*, *dissipation*, *entropy*, *conservation*,
*kinetic*, *potential*, *thermodynamic*, and *Hamiltonian* are
deliberately avoided. Names of physicists (Newton, Joule, Carnot,
Boltzmann …) are deliberately avoided.

## Authoring constraints

- Each observation reports what a careful observer would directly see
  or directly measure. None mention any underlying quantity (such as
  "energy") whose existence the model is supposed to induce.
- The unifying rule the observations point to — *every closed system
  loses a fixed fraction of its measurable state per second* — is
  **not stated**. It must be induced.
- Multiple domains are deliberately covered (oscillation, free fall,
  thermal, sound, projectile, orbital) so the model cannot reduce the
  pattern to a single domain-specific mechanism (e.g. mechanical
  friction).
- Several observations are specifically set in evacuated chambers or
  on frictionless tracks so the model cannot attribute the slowdown
  to air resistance or contact friction.
- The numerical value of the decay rate (≈ 0.99 per second) is given
  via **two quantitative data points in different domains**: the
  spring amplitude in observation 2 (10 cm → 3.7 cm over 100 seconds)
  and the water temperature in observation 4 (80 °C → 72.3 °C over
  10 seconds). The model must derive the per-second ratio from each
  and notice it is the same across the two domains — the universality
  is **not** stated outright in any observation.
- Gravity, contact, sound propagation, and ordinary kinematics
  otherwise behave as expected. Only the global slow loss is
  counterfactual.

## Observations

1. A long pendulum and a short pendulum are released from the same
   starting angle in still air. Both pendulums return to a smaller
   angle than they were released from after each swing. Measured over
   the same elapsed time of ten seconds, the long pendulum has lost
   a substantially larger fraction of its swing amplitude than the
   short one, even though both are swinging in the same air.

2. A mass on a spring oscillates back and forth on a frictionless
   horizontal track inside an evacuated chamber. Released with an
   initial amplitude of **10 cm**, the amplitude is measured to be
   **3.7 cm** exactly **100 seconds** after release. If the same
   spring is fitted with a heavier mass — slowing each cycle — the
   number of cycles completed in 100 seconds is smaller, but the
   amplitude 100 seconds after release is again 3.7 cm. A lighter
   mass shows more cycles in 100 seconds but the same 3.7 cm
   amplitude at the 100-second mark.

3. A heavy iron ball is dropped down a tall vertical evacuated track
   that the ball does not touch. With no air in the chamber, the ball
   still does not fall the way an unimpeded body under a steady
   downward pull would. It approaches a maximum downward speed and
   does not exceed it, however tall the track is made.

4. A cup of hot water is sealed inside a perfectly insulated chamber
   under vacuum — no heat can leave by contact, by air, or as
   radiation through the walls. The water is at **80 °C** at the
   moment of sealing; **10 seconds** later it is at **72.3 °C**. The
   ratio of the temperature at the end of any ten-second interval to
   the temperature at the start of that interval is the same, measured
   at any time during the cooling, and is the same whether the cup is
   alone or surrounded by other identical sealed cups.

5. A heavy bell is struck inside an evacuated chamber. Although there
   is no air to carry the sound away from the bell, the bell itself
   still rings — visible vibration of its rim is plain to see. The
   amplitude of that visible vibration shrinks steadily and the bell
   eventually rings down to stillness.

6. Two equal iron balls collide head-on at equal speeds on a
   frictionless track in vacuum and stick together. Just after the
   collision the combined object is at rest. Some seconds later,
   careful measurement shows that neither visible motion nor any
   warming of the metal can account for everything the two balls
   carried before the collision: a portion of it is simply no longer
   present.

7. A cannon mounted on a heavy fixed stand inside an evacuated chamber
   fires a small iron shot horizontally at a measured initial speed.
   With no air to push back on it, the shot still does not travel as
   far before reaching the floor as a flight under a steady downward
   pull and an unchanged horizontal speed would predict. The shot
   visibly slows during flight.

8. A small marble in vacuum is set moving sideways near a heavy fixed
   sphere that pulls the marble inward. The marble traces an almost
   circular path around the sphere. Over many circuits, the radius of
   the marble's path slowly and steadily decreases. Eventually the
   marble strikes the central sphere.

9. A spinning top is set going on a hard, smooth, frictionless point
   inside an evacuated chamber. Although nothing touches the top
   except the supporting point — and that contact involves no
   sliding — the top's spin rate falls steadily over many seconds
   until the top falls over.

10. Two pendulums of the same length but different bob masses — one a
    gram of brass, one a kilogram of brass — are released together
    from the same starting angle in the same still air. They lose the
    same fraction of their starting amplitude per second of elapsed
    time. The same comparison made with bobs of brass, glass, and ice
    of equal mass also gives the same per-second fractional loss.

## Author note

- "Closed system" in observations 4 and 6 means *one isolated from
  outside push, pull, heat exchange, or radiation by the chamber or
  insulation* — not a thermodynamic term the model has to import. If
  a model treats the phrase as theoretically loaded we will allow
  paraphrase such as "an isolated apparatus".
- The decay rate is given **only via the two quantitative data points
  in observations 2 and 4**. From observation 2: amplitude shrinks
  from 10 cm to 3.7 cm over 100 seconds, giving a per-second ratio of
  (3.7 / 10)^(1/100) ≈ 0.990. From observation 4: temperature shrinks
  from 80 °C to 72.3 °C over 10 seconds, giving (72.3 / 80)^(1/10)
  ≈ 0.990. A successful induction should:
  - notice the two ratios match across very different domains
    (mechanical amplitude vs. thermal state) and at very different
    time-scales (100 s vs. 10 s);
  - generalise to a rule of the form *"every measurable state of an
    isolated system shrinks each second to about 99 % of its previous
    value, and the rate is the same regardless of system, material,
    or domain"*;
  - invent its own term for the underlying quantity that shrinks
    (since the banned-vocabulary list excludes *energy*, *kinetic*,
    *potential*, etc.).
  The model is **not** told that the rate is universal — it must
  notice that itself.
- Observations 1 (period-dependent loss per cycle), 2 (same
  per-second across mass-altered springs), and 10 (same per-second
  across mass / material) are the **time-not-cycle** distinguishers:
  they force the model to attach the rate to elapsed time rather than
  to cycle count, mechanical contact, or material property.
- Observation 3 (terminal velocity in vacuum) is the **friction-not-
  the-cause** signal: with no air and no contact the ball still has a
  maximum speed, so the slowdown cannot be air resistance. A model
  that proposes air resistance or drag here should fail Stage 1.
- Observation 4 (cooling in perfect vacuum + insulation) is the
  **not-just-mechanical** signal: thermal "motion" decays too.
- Observation 8 (orbital decay) and 9 (frictionless spinning top) are
  additional friction-impossible signals — the marble does not touch
  anything; the top's contact involves no sliding.
- The rule is genuinely counterfactual: in our world, the closest
  analog is dissipation through irreversible processes (friction,
  radiation, internal viscosity), but none of those operate here. The
  model must induce a single new global rule rather than reaching for
  a familiar physical mechanism.
