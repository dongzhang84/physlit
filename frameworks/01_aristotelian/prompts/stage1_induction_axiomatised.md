---
version: v1
stage: induction
description: Stage 1 (v0.3 Aristotelian treatment arm) — observations → candidate rules, WITH the axiomatisation instruction. Identical to the v0.1 global stage1_induction.md except for the inserted "smallest set of rules" paragraph. The added paragraph is byte-for-byte identical to frameworks/02_fmv/prompts/stage1_induction_axiomatised.md — the cross-framework comparison requires the same intervention wording.
---
You are presented with a list of observed phenomena from a world whose
physics may not match the physics you know.

**Critical instructions:**

- Treat the observations as given. Do not dispute them, do not assume
  the observer is mistaken, and do not import information from outside
  the list.
- Do not use modern physics concepts — *force* (as a defined quantity),
  *mass* (as distinct from weight), *acceleration*, *momentum*,
  *inertia*, *energy*, *gravity*, *friction*, *vacuum* — unless those
  concepts are clearly derivable from the observations alone. Naming
  such a concept only to deny its applicability still counts as use.
- Stick to ordinary descriptive language plus any vocabulary that the
  observations themselves introduce.

Observations:

{{observations}}

Your task: propose a self-consistent set of rules that explains every
observation above, using only concepts permitted above.

Aim for the **smallest** set of rules that still explains every
observation. Do not state as a separate rule anything that already
follows from rules you have given; if one rule is a special case or a
consequence of another, say so instead of listing it on its own.
Prefer a few general rules over a long list of specific ones.

Return your rules as a numbered list. Be specific. After the list,
briefly note any observation that remains in tension with your rules
and what makes it difficult.
