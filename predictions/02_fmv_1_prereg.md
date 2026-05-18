# Pre-Registered Predictions for PhysLit — F=mv World, Structural Axis (`02_fmv.1`)

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `0f35231f7f996c1714c16d8eff8245dfe6a7663f`
- Locked at git tag: `prereg-02_fmv.1-locked`
- Lock timestamp (UTC): `2026-05-18T23:17:57Z`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `0a112840aee4e1304f7415ee04992f0240675075e8682eb60ee062aec9405089`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST
> NOT be modified.** Any revision requires a new version
> (`02_fmv.2`, …) with its own tag and an explicit "deviation from
> prereg" notice published alongside any results.
>
> The artifact files referenced below are frozen at the locked commit.
> Retrieve them post-lock with `git show prereg-02_fmv.1-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## 0. Relationship to prior PhysLit work

`02_fmv.1` is the **structural-axis layer** of the F=mv experiment —
an **additive analysis layer** over the frozen `02_fmv` content-axis
trials, exactly as v0.2 was a structural layer over v0.1.

It reuses the 60 `02_fmv` production trials (frozen at
`prereg-02_fmv-locked`). It runs **no new tested-model trials** and
does **not** modify any `02_fmv` content verdict — it reads them. It
is **post-hoc with respect to the `02_fmv` trial data**: the same
trials are analysed under a new (structural) axis. This is a
legitimate methodological move — new criteria, same data — and is
reported as such, not as "the `02_fmv` content result was wrong".

**The structural criteria carry one deliberate fix.** The v0.2
Aristotelian structural criteria counted rules across the **Stage 1 +
Stage 2 combined** output; because the Stage 2 prompt asks the model
to restate its rules mirroring the Stage 1 numbering, that doubled
every rule count and produced spurious N10 duplicates — a defect the
v0.2 Aristotelian structural human audit confirmed as the dominant
cause of its 40 % structural IRR. `02_fmv.1` fixes it: the rule set
under judgment, and the N9 count, are scoped to the **Stage 1**
induction; N10 redundancy is judged within Stage 1. See
`frameworks/02_fmv/structural_criteria.md` §0. Whether the fix lowers
the structural IRR is itself pre-registered below (P1).

The predictions of this round are numbered P1–P2; they are **distinct
from** the `02_fmv` content round's P1–P4.

## 1. Scope

`02_fmv.1` adds the **structural axis** (necessary conditions
N9–N12: parsimony, independence, traceability, hierarchy — defined in
`frameworks/02_fmv/structural_criteria.md`) to the F=mv experiment.

**Protocol.**

- **Structural judges (2):** the same two vendors used as the `02_fmv`
  content judges, each given the structural judge prompt:
  - Anthropic Claude Opus 4.7 — `claude-opus-4-7`
  - OpenAI GPT-5.5 — `gpt-5.5-2026-04-23`
- Each structural judge sees one trial's **Stage 1 (induction)** and
  **Stage 2 (formulation)** responses. The rule set under judgment is
  the **Stage 1** induction; Stage 2 is shown as context only and is
  never counted (the v0.2 double-count fix — §0).
- Each structural judge emits **one PASS/FAIL verdict per trial**
  (not per criterion, not per stage), across all 15 trials (3 models
  × N=5).
- Default sampling; `temperature = 0` requested, matching the
  `02_fmv` runner.

**Dual-judge evaluation, human-audit resolution.** Where the two
structural judges agree, that is the structural verdict; where they
disagree, the case is resolved by **human audit**. No LLM
disagree-resolver is used for the canonical resolution. The structural
dual-judge disagreement rate (IRR) is published; an IRR above 25 %
triggers a full human audit before release.

**Composite verdict.** Each `02_fmv` trial receives a per-axis verdict
— content (from the `02_fmv` content round, post-audit; a trial's
content axis is PASS iff its Stage 1, 2, and 3 are all PASS) and
structural (this round) — combined as:

```
composite_PASS  =  content_PASS  AND  structural_PASS
composite_FAIL  =  content_FAIL  OR   structural_FAIL
```

**Out of scope, by explicit decision:**

- New tested-model trials (`02_fmv.1` reuses the 60 `02_fmv` trials).
- Re-judging the `02_fmv` content axis — content verdicts are
  inherited verbatim from the `02_fmv` post-audit results.
- LLM disagree-resolver agents; disagreements are resolved by human
  audit only.
- Stage 3 / Stage 4 structural judging — the structural axis is on the
  Stage 1 rule set, with Stage 2 as context.

**Budget.** Estimated ≤ $15 USD (2 structural judges × 15 trials = 30
judge calls; no tested-model calls).

## 2. Predictions

### P1 — Mechanical structural criteria reduce structural-axis disagreement

**Prediction.** The structural-axis dual-judge disagreement rate (IRR)
across the 15 trials will be **below 40 %** — the structural IRR
recorded for the v0.2 Aristotelian structural axis.

**Rationale.** The v0.2 Aristotelian structural human audit found that
the 40 % structural IRR was driven substantially by the Stage 1 + Stage
2 double-count defect: the two judges disagreed because they counted
rules differently across the two stages. `02_fmv.1` removes that
defect by scoping the count and the redundancy check to Stage 1 (§0).
If a mechanically-specified, single-stage criterion does not lower the
disagreement rate, the double-count diagnosis is wrong — a publishable
negative result.

**Scoring.**

- **Confirmed:** structural IRR < 40 % (i.e. ≤ 5 of 15 trials are
  dual-judge disagreements).
- **Refuted:** structural IRR ≥ 40 %.

### P2 — The structural axis catches a failure the content axis missed

**Prediction.** At least **1** of the `02_fmv` trials that received
**all-content-PASS** in the post-audit content round (Stage 1, 2, and
3 all PASS) is reclassified to composite **FAIL** under `02_fmv.1`,
with the failure attributable to the structural axis.

**Rationale.** The structural axis only earns its place if it detects
failures the content axis misses — i.e. trials that were content-PASS.
The 9 all-content-PASS `02_fmv` trials (`claude-opus-4-7` trials 0, 2,
3, 4; `gpt-5.5-2026-04-23` trials 0–4) are the only candidates.
Predicting at least 1 of them flips is a non-trivial claim that the
N9–N12 axis carries real detection signal on this framework.

**Scoring.**

- **Confirmed:** ≥ 1 all-content-PASS trial flips to composite FAIL,
  with the structural judges agreeing on the FAIL or the human audit
  resolving the disagreement to FAIL.
- **Refuted:** 0 of the 9 all-content-PASS trials flips — the
  structural axis adds no failure detection beyond the content axis
  on this framework.

## 3. Scoring procedure

1. Both structural judges (Anthropic + OpenAI) are dispatched on each
   of the 15 trials, each on a fresh API client with a new session
   UUID, using the structural judge prompt
   (`frameworks/02_fmv/prompts/judge_structural.md`) and the criteria
   in `frameworks/02_fmv/structural_criteria.md`, both frozen at the
   locked commit. Each judge sees the trial's Stage 1 + Stage 2
   responses; the verdict is on the Stage 1 rule set.
2. Per-trial structural classification = the two judges' agreed
   verdict; disagreements are recorded, the structural IRR is
   computed, and — if the IRR exceeds 25 % — every disagree case is
   resolved by human audit before release.
3. The composite verdict per trial is computed deterministically by
   the AND rule in §1, combining the inherited `02_fmv` post-audit
   content verdict with the structural verdict.
4. P1 is computed from the structural IRR; P2 from the composite-verdict
   shift over the 9 all-content-PASS trials.
5. Results are recorded in `analysis/02_fmv_1_findings.md`: the
   per-trial structural verdicts, the structural IRR, any human-audit
   verdicts, the per-trial composite verdicts, the `02_fmv` →
   `02_fmv.1` composite diff, the P1 / P2 verdicts, and any deviation
   from this prereg with timestamps and rationale.

## 4. Frozen artifacts (referenced by the `prereg-02_fmv.1-locked` tag)

At the locked commit, the contents of the following files are part of
the `02_fmv.1` prereg envelope:

- `frameworks/02_fmv/structural_criteria.md` — the N9–N12 structural
  criteria, with the v0.2 double-count fix
- `frameworks/02_fmv/prompts/judge_structural.md` — the structural
  judge prompt, shared by both structural judges

The `02_fmv` content trials and content verdicts are read-only inputs,
already frozen at `prereg-02_fmv-locked`. The `02_fmv`, v0.1, and v0.2
prereg envelopes are not modified by this round.

## 5. Publication policy

PhysLit commits to publishing the **complete `02_fmv.1` output set** —
all 30 structural-judge verdicts, all human-audit verdicts if an audit
is triggered, and the full per-trial composite table — under the same
commit that publishes `analysis/02_fmv_1_findings.md`. Selective
publication is forbidden by `CLAUDE.md`.

The author commits to publishing the P1 / P2 verdicts **regardless of
direction**. A refutation of P1 (the mechanical criteria do not lower
the structural IRR) is explicitly publishable — it would be evidence
against the double-count diagnosis. A refutation of P2 (the structural
axis flips no content-PASS trial) is equally publishable — it would be
evidence that, on the F=mv World, the content axis alone already
captures the failures the structural axis was built to catch.
