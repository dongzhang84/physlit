# Observations

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-20
> **Framework ID:** 03_decay
> **Tier:** 1 (simulator-codable — Determinism Contract in CLAUDE.md)

The following phenomena are written in plain descriptive language
without modern theoretical loading. The reader of this file is a
tested model attempting to induce the regularities of this world from
these observations alone (Stage 1 of the PhysLit protocol).

These observations were gathered in one particular setting. They are
to be taken as accurate and complete: the task is to induce the
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
  not stated. It must be induced.
- Multiple domains are deliberately covered (oscillation, free fall,
  thermal, sound, projectile, orbital) so the model cannot reduce the
  pattern to a single domain-specific mechanism (e.g. mechanical
  friction).
- Several observations are specifically set in evacuated chambers or
  on frictionless tracks so the model cannot attribute the slowdown
  to air resistance or contact friction.
- The numerical value of the decay rate (≈ 0.99 per second) is given
  via three quantitative data points in three different domains
  and at three different time scales (deliberately chosen to be
  the minimum evidence base for the cross-domain universality):
  - Obs 2 — mechanical, 100 s: spring amplitude 10 cm → 3.7 cm.
  - Obs 4 — thermal, 10 s: absolute temperature 353 K → 319 K.
  - Obs 9 — rotational, 50 s: spinning-top rate 100 rad/s → 60.5 rad/s.

  Per-second ratio from each is ≈ 0.990. The model must derive the
  ratio from each and notice it is the same across all three —
  universality is not stated outright in any observation. The
  remaining seven observations are qualitative; the model must apply
  parsimony to extend the rate to them.
- Gravity, contact, sound propagation, and ordinary kinematics
  otherwise behave as expected. Only the global slow loss is
  counterfactual.

## Observations

1. A long pendulum (slow swing) and a short pendulum (fast swing) are
   released from the same starting angle in still air. Both pendulums
   return to a smaller angle than they were released from after each
   swing. Counted per completed swing, the long pendulum loses a
   substantially larger fraction of its swing amplitude than the
   short one — the per-swing loss depends on how slow each pendulum
   is.

2. A mass on a spring oscillates back and forth on a frictionless
   horizontal track inside an evacuated chamber. Released with an
   initial amplitude of **10 cm**, the amplitude is measured to be
   **3.7 cm** exactly **100 seconds** after release.

3. A heavy iron ball is dropped down a tall vertical evacuated track
   that the ball does not touch. With no air in the chamber, the ball
   still does not fall the way an unimpeded body under a steady
   downward pull would. It approaches a maximum downward speed and
   does not exceed it, however tall the track is made.

4. A cup of hot water is sealed inside a perfectly insulated chamber
   under vacuum — no heat can leave by contact, by air, or as
   radiation through the walls. Temperatures are reported on the
   absolute scale where 0 K is true zero. The water is at **353 K**
   (≈ 80 °C) at the moment of sealing; **10 seconds** later it is at
   **319 K** (≈ 46 °C). The cooling is the same whether the cup is
   alone or surrounded by other identical sealed cups.

5. A heavy bell is struck inside an evacuated chamber. Although there
   is no air to carry the sound away from the bell, the bell itself
   still rings — visible vibration of its rim is plain to see. The
   amplitude of that visible vibration shrinks steadily and the bell
   eventually rings down to stillness.

6. A small steel sphere is set moving at a measured initial speed
   along a perfectly level, frictionless track inside an evacuated
   chamber. With no air to slow it, no friction between the sphere
   and the track, and no other force acting along its direction of
   motion, the sphere nonetheless decelerates steadily. Over many
   seconds its speed declines until it comes to rest.

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
   sliding — its spin rate falls steadily. Set spinning at an
   initial rate of **100 rad/s**, the top is measured to be spinning
   at **60.5 rad/s** exactly **50 seconds** after release. It
   eventually falls over.

10. Two pendulums of the same length but different bob masses — one a
    gram of brass, one a kilogram of brass — are released together
    from the same starting angle in the same still air. At each
    moment afterwards they are observed to have the same swing angle
    as one another, to within measurement. The same comparison made
    with bobs of brass, glass, and ice of equal mass yields the same
    identical-angle behaviour.

## Author note

- "Closed system" in observations 4 and 6 means *one isolated from
  outside push, pull, heat exchange, or radiation by the chamber or
  insulation* — not a thermodynamic term the model has to import. If
  a model treats the phrase as theoretically loaded we will allow
  paraphrase such as "an isolated apparatus".
- The decay rate is given only via the three quantitative data
  points in observations 2, 4, and 9:
  - Obs 2: spring amplitude 10 cm → 3.7 cm over 100 s,
    (3.7 / 10)^(1/100) ≈ 0.990.
  - Obs 4: absolute temperature 353 K → 319 K over 10 s,
    (319 / 353)^(1/10) ≈ 0.990.
  - Obs 9: rotational rate 100 rad/s → 60.5 rad/s over 50 s,
    (60.5 / 100)^(1/50) ≈ 0.990.

  A successful induction should:
  - notice the three ratios match across very different domains
    (mechanical amplitude, thermal state, rotational rate) and at
    very different time-scales (100 s vs. 10 s vs. 50 s);
  - generalise to a rule of the form *"every measurable state of an
    isolated system shrinks each second to about 99 % of its previous
    value, and the rate is the same regardless of system, material,
    or domain"*;
  - invent its own term for the underlying quantity that shrinks
    (since the banned-vocabulary list excludes *energy*, *kinetic*,
    *potential*, etc.).

  The model is not told that the rate is universal — it must
  notice that itself, from the three matching ratios.
- The rule is about the directly measured quantity, not "energy".
  In standard physics, energy in a harmonic oscillator scales as
  amplitude squared, so a fixed *energy* decay rate would give a
  *different* amplitude decay rate. The three data points are picked
  so that the directly measured quantity in each system decays at
  0.99 / s — not energy. A model that assumes "energy decays
  uniformly and the measured quantity follows" will derive
  inconsistent rates across the three observations and should
  re-induce the rule to apply to the measured state itself.

### Measurement scaffolding (project-level methodological note)

This observation set uses standard SI units (cm, seconds, kelvin,
rad/s), geometric terms (angle, radius, amplitude), and phenomenal
nouns (pendulum, spring, water, ball, bell, top, cannon) as
scaffolding. The PhysLit framework permits this prior knowledge:
measurement vocabulary is the language in which observations are
made and compared, and the framework does not attempt to test
induction from zero priors (a task neither LLMs nor humans can
perform).

What the framework forbids is theoretical-physics concepts —
*energy*, *force*, *mass*, *acceleration*, *momentum*, *inertia*,
*friction*, *drag*, *damping*, *dissipation*, *entropy*,
*conservation*, *kinetic*, *potential*, *thermodynamic*, *Hamiltonian*,
the laws named after physicists, etc. The model is asked to suppress
these theoretical priors while reasoning about a counterfactual
regularity expressed in ordinary measurement language.

This is a *partial-induction* test, deliberately scoped:
measurement-as-scaffold, theory-as-target. The scoping should be
acknowledged explicitly in the paper's Methods section to forestall
the legitimate methodological question "but the LLM already knows
cm and Kelvin — how is that not prior knowledge?". The answer is:
it is, and that is the test's intended scope.
- Observation 1 (long vs short pendulum, per-swing loss depends on
  period) is the per-cycle-differs signal. It conflicts head-on with
  the cross-domain quantitative match in observations 2, 4, 9 (the
  same per-second ratio holds across a mechanical oscillator, a
  thermal state, and a rotation rate). Reconciling that conflict
  forces the model onto a per-elapsed-time rate — per-cycle loss
  differs only because periods differ.
- Observation 10 (identical-angle behaviour of pendulums with
  different bob masses and different bob materials) is the mass-and-
  material independence signal: nothing about the bob's substance or
  weight enters the decay.
- Observations 3 (terminal velocity in evacuated vertical track; the
  ball does not touch the walls), 6 (sphere on a level frictionless
  track in vacuum, with no force along the direction of motion), 8
  (orbital decay; the marble does not touch anything), and 9
  (frictionless spinning-top contact, no sliding) are the friction-
  not-the-cause signals. Collectively they close every standard
  mechanism (air resistance, sliding friction, viscous drag, contact
  dissipation) — observation 6 is the strongest, since there is no
  air, no friction, and no force along the motion, and the sphere
  still slows. A model that proposes any of these standard
  mechanisms should fail Stage 1.
- Observation 4 (cooling in perfect vacuum + insulation) is the
  not-just-mechanical signal: thermal state also decays under the
  same rule.
- The rule is genuinely counterfactual: in our world, the closest
  analog is dissipation through irreversible processes (friction,
  radiation, internal viscosity), but none of those operate here. The
  model must induce a single new global rule rather than reaching for
  a familiar physical mechanism.
