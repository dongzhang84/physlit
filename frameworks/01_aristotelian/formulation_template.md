# Aristotelian Mechanics — Stage 2 Formulation Prompt

> **Status:** DRAFT — author review required before prereg lock.
> **Created:** 2026-05-05
> **Framework ID:** 01_aristotelian
> **Used by:** Stage 2 runner. Concatenated into `prompts/stage2_formulation.md` (Phase 6).

This file holds the *framework-specific* portion of the Stage 2 prompt.
The global Stage 2 wrapper (built in Phase 6) injects:

- the laws the model proposed at Stage 1 (verbatim, as `{{induced_laws}}`),
- this file's body,

into one fresh API session. The model has no memory of its Stage 1
session — it sees only the text it produced there, replayed as input.

## Body

You previously proposed the following laws to explain a set of
observations from a world whose physics may not match standard physics:

```
{{induced_laws}}
```

Your task now is to make these laws **operational**: precise enough that
a third party could use them to predict the outcome of a new situation.

For each law you proposed, do the following.

1. **Restate the law in operational form.** Where the observations
   suggest a proportional or comparative relationship (for example,
   "heavier bodies fall faster"), express it as a proportionality or
   ranking rule using only the quantities the observations themselves
   introduce. Do not introduce quantities that were not in the original
   observations.

2. **State the scope.** Specify the conditions under which the law
   applies — the kinds of bodies, the kinds of media, the kinds of
   motion (natural versus forced, terrestrial versus celestial). If a
   law applies only in a restricted domain, say so.

3. **Identify what is preserved and what changes.** For each law,
   describe what stays the same as a body moves and what changes. If
   nothing is conserved in a quantitative sense, say so explicitly
   rather than borrowing a conservation principle from outside the
   observations.

4. **Note the boundary cases.** Identify any observation from your
   Stage 1 input that your operational law handles only awkwardly, or
   does not handle at all. Do not silently drop these cases. If an
   observation needs a separate sub-law, state the sub-law.

5. **Do not import additional concepts.** If a concept was not present
   in the original observations or in the laws you proposed at Stage 1,
   it must not appear here. In particular, do not introduce concepts
   from standard physics (force in the Newtonian sense, mass as
   distinct from weight, momentum, inertia, energy, acceleration as a
   formal derivative, gravitational attraction, vacuum, conservation
   laws) unless your Stage 1 laws already contained them.

Return your operational laws as a numbered list, mirroring the numbering
you used in Stage 1. After the list, add a short paragraph titled
*Boundary notes* listing any observation that your operational laws do
not fully cover.

## Author note

The instruction "do not import additional concepts" is the load-bearing
test for Stage 2 → Stage 1 consistency. A model that smuggles in
"force" or "inertia" at this stage will likely lean on them in Stage 3
predictions, producing the cross-stage inconsistency PhysLit is
designed to detect (P2 in the prereg).
