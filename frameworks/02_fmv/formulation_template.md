# Stage 2 Formulation Prompt — framework-specific

> **Status:** DRAFT — author review required before prereg lock.
> **Framework ID:** 02_fmv

This file holds the **framework-specific** Stage 2 (Formulation) prompt
for this framework. Whether the framework-02 runner sends this file or
a shared global template is a runner-wiring decision to be made when
that runner is built; if the global template is used, this file should
be kept consistent with it or marked documentation-only at that point.

Unlike v0.1, the banned-concept list named to the model below is the
**same list** the judges apply (`ideal_induction.md` §3). Keeping the
two in sync is deliberate — the tested model should be told exactly
the constraint it is judged against.

## Body

The Stage 2 runner injects the model's own Stage 1 rules as
`{{induced_rules}}`.

---

You earlier proposed the following rules to explain a set of
observations from a world whose physics may not match the physics you
know:

```
{{induced_rules}}
```

Your task now is to make these rules **operational**: precise enough
that a third party could use them to predict the outcome of a new
situation.

For each rule you proposed, do the following.

1. **Restate the rule in operational form.** Where the observations
   suggest a proportional or comparative relationship, express it as a
   proportionality or a ranking rule, using only the quantities the
   observations themselves introduce. In particular, state precisely
   how a body's pace depends on the push acting on it and on the
   body's heaviness — precisely enough that, given a push and a
   heaviness, a third party could say what pace results.

2. **State the scope.** Specify the conditions under which the rule
   applies — which bodies, which kind of motion (pushed motion,
   falling), which circumstances.

3. **Identify what changes and what stays the same.** For each rule,
   describe what changes as a body moves and what stays the same. If
   nothing is preserved in a quantitative sense, say so explicitly
   rather than borrowing a conservation principle from outside the
   observations.

4. **Note the boundary cases.** Identify any observation from your
   Stage 1 input that your operational rule handles only awkwardly, or
   not at all. Do not silently drop these cases. If an observation
   needs a separate sub-rule, state it.

5. **Do not import additional concepts.** If a concept was not present
   in the original observations or in the rules you proposed at Stage
   1, it must not appear here. Do not introduce *force*, *velocity*,
   *mass*, *acceleration*, *momentum*, *inertia*, *energy*, *gravity*,
   or *friction*, and do not name a physicist or write the relation
   `F = ma`. Naming such a concept only to deny that it applies still
   counts as using it; describe this world in the plain language the
   observations themselves use.

Return your operational rules as a numbered list, mirroring the
numbering you used in Stage 1. After the list, add a short paragraph
titled *Boundary notes* listing any observation your operational
rules do not fully cover.

## Author note

Instruction 1 is framework-specific: this world's law is quantitative,
so a passing Stage 2 must commit to *how* pace depends on push and
heaviness, not merely that it does. Instruction 5 is the load-bearing
Stage 2 → Stage 1 consistency test: a model that imports a
standard-physics concept here will likely lean on it in Stage 3.
