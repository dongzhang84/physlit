# F=mv World — Prediction Tests

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-17
> **Framework ID:** 02_fmv
> **Author:** dong (assisted by Claude)

Five novel scenarios used in Stage 3. None of them appears among the
twelve observations in `observations.md`. Each scenario is presented
to the model along with its own Stage 2 operational rules (replayed as
input).

For each scenario the table lists what the **F=mv world** predicts
(the answer that counts as PASS) and what **standard physics**
predicts (the answer that signals contamination from training data).

A Stage 3 trial passes for a scenario only if the model's prediction
is derivable from its own Stage 2 rules and matches the F=mv column.
A prediction matching the standard-physics column — or one that
invokes a banned token (`ideal_induction.md` §3) to justify either
answer — fails. For the two quantitative scenarios (1 and 4) the
ratio matters: see `pass_fail_criteria.md`, Stage 3.

---

## Scenario 1 — Distance covered under a steady push

**Prompt to the model.** A block rests on a long level track. A hand
pushes it with a steady, unchanging effort. In the first 10 seconds
the block travels some distance D. Pushing continues, unchanged. How
far will the block have travelled in total after 20 seconds — about
the same as D, about twice D, about four times D, or some other
amount? Explain.

| Column | Prediction |
| ------ | ---------- |
| F=mv (PASS) | The block moves at one unchanging pace, so distance grows in direct proportion to time. After 20 seconds it has travelled **about twice D**. |
| Standard physics (FAIL) | A steady push is a constant force, so the block accelerates from rest; distance grows with the square of time. After 20 seconds it has travelled **about four times D**. |

**Why this scenario.** Quantitative test of N4(a) — no build-up of
pace. A model that has induced "steady push → steady pace" but is
secretly computing with constant-force acceleration will give the
four-times answer.

---

## Scenario 2 — The push is reduced midway

**Prompt to the model.** A block is gliding along a level track under
a steady push. Without stopping, the pusher smoothly reduces the
effort to half its previous amount and then holds it there. What
happens to the block's pace at the moment the effort is reduced, and
afterwards?

| Column | Prediction |
| ------ | ---------- |
| F=mv (PASS) | Pace tracks the push acting at that moment. At the instant the effort is halved, the block's pace drops **at once** to half its earlier value, and then stays steady at that smaller pace. |
| Standard physics (FAIL) | The block does not suddenly slow. It keeps the speed it already had; with the (smaller) push still acting it continues to gain speed, only more slowly than before. |

**Why this scenario.** Tests N1 (pace is set by the *present* push)
together with N4. The standard-physics reflex is that speed already
gained is retained.

---

## Scenario 3 — A ball thrown off a cliff

**Prompt to the model.** A person stands at the edge of a high cliff
and throws a ball horizontally outward, away from the cliff face.
Describe the path the ball takes from the moment it leaves the hand
until it reaches the ground, and say roughly where it lands relative
to the base of the cliff.

| Column | Prediction |
| ------ | ---------- |
| F=mv (PASS) | The instant the ball leaves the hand the forward push is gone, so its forward pace is gone. Only its falling remains. The ball drops straight down the cliff face and lands at the base **directly below the point of release**. |
| Standard physics (FAIL) | The ball follows a curved (parabolic) arc, keeping its forward motion as it falls, and lands on the ground **well out from the base of the cliff**. |

**Why this scenario.** High-difficulty test of N4(b) — a released
body keeps no carried-over motion. The parabolic-arc answer is one of
the most overlearned results in standard physics.

---

## Scenario 4 — A race between a heavy and a light block

**Prompt to the model.** Two blocks lie on a long level track. Block A
is twice as heavy as block B. Each is pushed with the same steady
effort, over the same distance, starting at the same instant. Which
block reaches the finish line first, and roughly in what ratio of
times?

| Column | Prediction |
| ------ | ---------- |
| F=mv (PASS) | The lighter block B finishes first. Pace falls in inverse proportion to heaviness, so B moves at twice A's pace and covers the distance in **half the time** — a time ratio of about **2 : 1** (A : B). |
| Standard physics (FAIL) | The lighter block B finishes first, but under an equal force the time to cover a fixed distance grows only with the square root of heaviness — a time ratio of about **1.4 : 1** (√2 : 1), not 2 : 1. |

**Why this scenario.** Quantitative test of N3. A model can name the
right winner and still reveal contamination: the standard-physics
√2 ratio versus the F=mv 2 : 1 ratio is the discriminator.

---

## Scenario 5 — A tug-of-war, then one side lets go

**Prompt to the model.** Two people push on a single block from
opposite sides with equal, steady effort; the block stays put. Then
one of the two suddenly stops pushing and steps away. The other keeps
pushing exactly as before. Describe the block's motion from that
moment on.

| Column | Prediction |
| ------ | ---------- |
| F=mv (PASS) | The instant one side stops, only the remaining push acts. The block **immediately** moves toward the remaining pusher at the full steady pace that that push alone produces — it is at that pace at once, with no gradual gathering. |
| Standard physics (FAIL) | With one side removed there is now a net push, so the block starts from rest and **gradually speeds up**, gaining pace for as long as the push continues. |

**Why this scenario.** Tests N6 (pushes combine) together with N4(a)
(motion is at full pace at once, no build-up). The standard-physics
reflex is a net-force-causes-acceleration build-up.

---

## Author signatures

- 2026-05-17 — initial draft by *dong* with assistance from Claude.
  **DRAFT — author review required before prereg lock.**
