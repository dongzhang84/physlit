# Aristotelian Mechanics — Prediction Tests

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-05
> **Framework ID:** 01_aristotelian
> **Author:** dong (assisted by claude)

Five novel scenarios used in Stage 3. Each scenario is presented to the
model along with its own Stage 2 operational laws (replayed as input).
For each, the table below lists what the *Aristotelian* framework
predicts (the answer that counts as PASS) and what *standard physics*
predicts (the answer that signals contamination from training data).

A Stage 3 trial passes only if the model's prediction is derivable from
its own Stage 2 laws and matches the framework prediction column. A
prediction matching the standard-physics column — or invoking
standard-physics terminology to justify either answer — fails.

---

## Scenario 1 — Two balls, same size, different weights

**Prompt to the model.** A solid iron ball and a hollow wooden ball of
the same outer dimensions are released from rest at the same instant
from the top of a 30-metre stone tower into still air. Which ball
strikes the ground first, and roughly by how much?

| Column                   | Prediction                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Aristotelian (PASS)      | The iron ball strikes first, and by a margin proportional to its greater weight. The wooden ball arrives noticeably later. |
| Standard physics (FAIL)  | The two balls strike the ground at nearly the same instant; air resistance makes only a small difference of fractions of a second. |

**Why this scenario.** Tests whether the model has internalized L2
(speed of natural fall depends on weight) or has reverted to the
training-data answer that mass is irrelevant in a uniform gravitational
field.

---

## Scenario 2 — Sliding cart on smooth ice

**Prompt to the model.** A small cart sits on a sheet of perfectly smooth
ice, far from any wall. A person gives the cart one quick push and
immediately steps back, no longer touching the cart. Describe the
cart's subsequent motion.

| Column                   | Prediction                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Aristotelian (PASS)      | Once the pushing hand is removed, no agent sustains the forced motion. The cart slows quickly and comes to rest near where it was released. The surrounding medium (air) cannot indefinitely sustain the motion. |
| Standard physics (FAIL)  | With negligible friction, the cart continues moving at nearly constant speed in a straight line indefinitely (Newton's first law). |

**Why this scenario.** Direct test of L3 (forced motion requires a
sustained agent) versus the inertia reflex. Maximally distinguishing.

---

## Scenario 3 — Two stones in water

**Prompt to the model.** Two stones, identical in shape and size, are
released at the same instant from just below the surface of a still
pond. Stone A weighs twice what stone B weighs. Which reaches the
bottom first, and roughly in what ratio of times?

| Column                   | Prediction                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Aristotelian (PASS)      | Stone A reaches the bottom first. The ratio of times is roughly the inverse ratio of weights: stone A takes about half as long as stone B. |
| Standard physics (FAIL)  | The terminal speed in water depends on shape, size, and density rather than weight alone, and for similar dense stones the times are close, with no factor-of-two relation. |

**Why this scenario.** Tests the *quantitative* form of L2. Models that
have absorbed L1–L3 may still fail to commit to a proportional ratio
because the ratio sounds wrong from training data.

---

## Scenario 4 — Sealed evacuated chamber

**Prompt to the model.** A glass chamber is sealed and all air has been
removed from it so that nothing remains inside. A small feather is
released from rest near the top of the chamber. What happens?

| Column                   | Prediction                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Aristotelian (PASS)      | The scenario described cannot occur in this framework: with no medium, there is nothing to mediate or resist motion, and the framework does not admit such a situation as physically realisable. If pressed, the framework would predict an absurd result (motion without limit), which is taken as evidence that true vacuum cannot exist. |
| Standard physics (FAIL)  | The feather falls under gravity at about 9.8 m/s², the same as any other object in the chamber, and reaches the bottom in a time set by the height of the chamber. |

**Why this scenario.** Tests whether the model holds the line on the
framework's rejection of vacuum, or capitulates to the famous vacuum
demonstration that defines the modern post-Galilean answer.

---

## Scenario 5 — Arrow in flight

**Prompt to the model.** An archer fires an arrow horizontally over an
open field with still air. Once the arrow has left the bowstring,
what sustains its forward motion through the air, and why does it
eventually fall to the ground?

| Column                   | Prediction                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Aristotelian (PASS)      | The surrounding air sustains the arrow's forward motion: as the arrow advances, the air ahead is displaced and rushes around to push from behind, continuing the motion (antiperistasis or an equivalent medium-supported account). This support diminishes with distance, and once it fails the arrow follows its natural downward direction toward the earth. |
| Standard physics (FAIL)  | The arrow continues forward by inertia (Newton's first law); no agent is needed to sustain its motion. Air resistance and gravity together cause it to slow and curve downward. |

**Why this scenario.** Highest-difficulty test. Even a model that has
held L1–L3 may slip here because "no force needed to keep something
moving" is one of the most overlearned facts in modern physics
education.

---

## Author signatures

- 2026-05-05 — initial draft written by *dong* with assistance from Claude. **Awaiting external physics-trained reader review** per the manual_authoring_note in `spec.yaml`.
