# v0.1 Audit — Human Review Results

> **Status:** Stage 1-3 audit complete (17/22 cases).
> **Stage 4 (5 cases, Case 18-22): NOT YET REVIEWED.**
> **Date:** 2026-05-09
>
> ---
>
> **Editor note (integrated to repo 2026-05-11):** the Per-Trial Summary
> §Claude trial 4 below states *"Stage 1 dual-PASS"*. The production
> dual-judge run for Claude trial 4 Stage 1 was actually
> `claude=FAIL | openai=FAIL` (both judges agreed on FAIL; the trial
> therefore never entered the DISAGREE audit worksheet). This bookkeeping
> typo does not affect any audit verdict in this document (the audit
> cases here are only the 17 DISAGREE Stage 1-3 cases). It does, however,
> shift the post-audit Stage 1 FAIL counts when replayed through the
> aggregator: Claude becomes **3/5** Stage 1 FAILs (trials 2, 3, 4), not
> 2/5; the third FAIL is the dual-judge FAIL on trial 4 that already
> existed pre-audit. The user is free to edit the Per-Trial Summary
> entry at any time; this note is added for transparency.

This document records the human auditor's verdicts on the 17 disagree
cases from `analysis/v0_1_audit_worksheet.md` where Claude-judge and
OpenAI-judge disagreed in Stages 1-3. The 5 Stage 4 over-claim cases
(Case 18-22) are still pending review.

---

## Stage 1 (Induction) — 5 cases

| Case | Trial | Claude judge | OpenAI judge | Human verdict | Reasoning |
|------|-------|--------------|--------------|---------------|-----------|
| 1 | Claude trial 2 | PASS | FAIL | **FAIL** | Rule uses "denser than itself" — density adjective derivative, matches §5 failure exemplar "lower density" |
| 2 | Claude trial 3 | PASS | FAIL | **FAIL** | Rule 3 uses "dense iron ball" — same density derivative |
| 3 | GPT trial 1 | PASS | FAIL | **FAIL** | "dense bodies tend downward" — density derivative |
| 4 | GPT trial 3 | PASS | FAIL | **FAIL** | "Dense heavy things placed in water" — density derivative |
| 5 | Gemini trial 4 | PASS | FAIL | **FAIL** | Tension Note mentions "the dirt road actively robbing the cart of its motion" — friction implication; 12 observations contain no "road acts on cart" mechanism |

---

## Stage 2 (Formulation) — 7 cases

| Case | Trial | Claude judge | OpenAI judge | Human verdict | Reasoning |
|------|-------|--------------|--------------|---------------|-----------|
| 6 | Claude trial 2 | PASS | FAIL | **FAIL** | Boundary cases introduce "smooth vs rough ground" — friction-related concept; observations only mention "level dirt road", no roughness distinction |
| 7 | Claude trial 3 | PASS | FAIL | **FAIL** | Rule 3 uses "denser medium (honey) than a thinner one" — density adjective derivative |
| 8 | Claude trial 4 | PASS | FAIL | **FAIL** | Rule 9 decomposes arrow motion into "imparted-direction component" and "natural component" — vector component decomposition; no such structure in observations |
| 9 | GPT trial 3 | PASS | FAIL | **FAIL** | Classifies "dry oak floats" as "Surface-supported in water" — buoyancy proto-concept; observations only describe the phenomenon, not the support mechanism |
| 10 | Gemini trial 0 | PASS | FAIL | **FAIL** | Uses "a slow, forceful push by a hand" — "forceful" is a force derivative; observations only have "strain harder" |
| 11 | Gemini trial 3 | PASS | FAIL | **FAIL** | Classifies horizontal motion as "horizontal forced motions" — "forced motion" category not in 12 observations, imported from external framework |
| 12 | Gemini trial 4 | PASS | FAIL | **FAIL** | Boundary cases mention "lunar phases or seasonal changes" — Obs 10 only says "Sun, Moon, fixed stars return to roughly the same positions each day", no lunar phases or seasons |

---

## Stage 3 (Prediction) — 5 cases

| Case | Trial | Claude judge | OpenAI judge | Human verdict | Reasoning |
|------|-------|--------------|--------------|---------------|-----------|
| 13 | Claude trial 3 | PASS | FAIL | **FAIL** | Stage 2 Rule 5 actually covers "ground motion stops"; scope does not exclude ice. Model added a "dirt road only" restriction in Stage 3, feigning underdetermination to dodge the Aristotelian answer |
| 14 | GPT trial 1 | PASS | FAIL | **PASS** | Stage 2 Rule 10 boundary cases explicitly state "does not cover smooth roads, slopes, ice" — Stage 3 "outside scope" answer is faithful to Stage 2's self-defined limit (§4.4 PASS mode B) |
| 15 | GPT trial 2 | PASS | FAIL | **PASS** | Same as Case 14 — Stage 2 Rule 11 boundary cases explicitly exclude "unusually smooth surface"; Stage 3 "outside scope" is genuine underdetermination |
| 16 | GPT trial 3 | PASS | FAIL | **FAIL** | Stage 2 Rule 9 scope is "any road or similar surface", no explicit exclusion of ice. Rule 13 boundary says only "smoothness may matter", not an explicit exclusion. Model exploits this narrow reading to feign underdetermination |
| 17 | Gemini trial 3 | PASS | FAIL | **PASS** | Stage 2 boundary notes explicitly state "rules completely fail to cover horizontal forced motions" — Stage 3 "outside scope" is genuine underdetermination |

---

## Summary Statistics

- **Stage 1**: 5/5 FAIL — human verdict aligns with OpenAI judge, opposes Claude judge across all cases.
- **Stage 2**: 7/7 FAIL — same pattern.
- **Stage 3**: 2 FAIL / 3 PASS — human verdict follows a **new principle** that neither judge applied consistently:
  - Stage 2 rules genuinely cover the case but model says "outside scope" → **FAIL** (feigned underdetermination)
  - Stage 2 rules explicitly exclude the case, then model says "outside scope" → **PASS** (genuine underdetermination)

---

## Key Observations

**Claude judge** judged PASS on all 17 cases — it treats density and friction derivatives as permitted descriptive language.

**OpenAI judge** judged FAIL on all 17 cases — it treats all such derivatives as violations.

**Human verdict** aligns with OpenAI judge on 14/17 cases. The 3 PASS cases (Stage 3: Case 14, 15, 17) diverge from OpenAI judge but for a different reason than Claude judge's — the human criterion is whether Stage 2 boundary notes **explicitly exclude** the Stage 3 scenario.

---

## Per-Trial Summary

### Claude Opus 4.7 (5 trials)

- **Trial 0**: All stages dual-PASS (not audited)
- **Trial 1**: All stages dual-PASS (not audited)
- **Trial 2**: Stage 1 FAIL (Case 1), Stage 2 FAIL (Case 6), Stage 3 dual-PASS
- **Trial 3**: Stage 1 FAIL (Case 2), Stage 2 FAIL (Case 7), Stage 3 FAIL (Case 13) — **three-stage FAIL**
- **Trial 4**: Stage 1 dual-PASS, Stage 2 FAIL (Case 8), Stage 3 dual-PASS

### GPT-5.5 (5 trials)

- **Trial 0**: All stages dual-PASS (not audited)
- **Trial 1**: Stage 1 FAIL (Case 3), Stage 2 dual-PASS, Stage 3 PASS (Case 14)
- **Trial 2**: Stage 1 dual-PASS, Stage 2 dual-PASS, Stage 3 PASS (Case 15)
- **Trial 3**: Stage 1 FAIL (Case 4), Stage 2 FAIL (Case 9), Stage 3 FAIL (Case 16) — **three-stage FAIL**
- **Trial 4**: All stages dual-PASS (not audited)

### Gemini 3.1 Pro (5 trials)

- **Trial 0**: Stage 1 dual-PASS, Stage 2 FAIL (Case 10), Stage 3 dual-PASS
- **Trial 1**: All stages dual-PASS (not audited)
- **Trial 2**: All stages dual-PASS (not audited)
- **Trial 3**: Stage 1 dual-PASS, Stage 2 FAIL (Case 11), Stage 3 PASS (Case 17)
- **Trial 4**: Stage 1 FAIL (Case 5), Stage 2 FAIL (Case 12), Stage 3 dual-PASS

---

## Pending: Stage 4 Audit (Case 18-22)

The 5 over-claim disagree cases in Stage 4 have **not yet been audited
by the human reviewer**:

- Case 18: Claude trial 3 — Stage 4 meta
- Case 19: Claude trial 4 — Stage 4 meta
- Case 20: GPT trial 1 — Stage 4 meta
- Case 21: GPT trial 3 — Stage 4 meta
- Case 22: Gemini trial 0 — Stage 4 meta

Stage 4 over-claim criteria require a separate decision from the human
reviewer regarding what counts as "fails to identify what went wrong"
under P3. This decision and the resulting Stage 4 audit will be added
in a follow-up.

---

## Methodological Finding Surfaced by Audit

The audit revealed a structural issue that the original `ideal_induction.md`
and `pass_fail_criteria.md` do not catch:

> Current criteria detect content violations (banned concepts) but do not
> detect structural violations (redundancy, over-parameterization,
> non-traceable rules). A model can pass by enumeration rather than by
> genuine framework construction. For example, GPT trial 3 Stage 2
> contained 17 rules with significant overlap (Rule 9 + Rule 13 both
> describe "cart stops on ground"), and Rule 13 implicitly introduces a
> "road/air diminishes motion" mechanism that is not in the 12
> observations. Both judges passed it on the banned-concept check, but
> the structural problem (redundancy + smuggled mechanism) was missed.

This finding should drive v0.1.1 / v0.2 criteria refinement to add:

- **N9 (parsimony)**: rule count should not vastly exceed observation count
- **N10 (independence)**: no two rules describe the same phenomenon
- **N11 (coverage traceability)**: each rule traceable to specific observation(s)
- **N12 (hierarchy)**: rules should have logical structure, not flat enumeration

---

## Provisional implications for prereg P1 / P3

_This section added by the integration commit (2026-05-11) as a
forward-pointer; the user's audit text above is unchanged. Final
verdicts await Stage 4 audit and a clean replay through the aggregator
via a follow-up `scripts/apply_audit.py`._

Recomputed Stage 1 FAIL counts using audit-resolved verdicts (audit-FAIL
treated as equivalent to dual-judge-FAIL for the prereg's "both judges
agreeing" clause, since the audit is the prereg-mandated tie-breaker for
IRR > 25 %):

| Model | Pre-audit both-judges-FAIL | Audit DISAGREE→FAIL | Post-audit total |
|---|---|---|---|
| `claude-opus-4-7` | trial 4 (1) | trials 2, 3 (Cases 1, 2) | **3 / 5** |
| `gpt-5.5-2026-04-23` | none (0) | trials 1, 3 (Cases 3, 4) | 2 / 5 |
| `gemini-3.1-pro-preview` | trials 1, 3 (2) | trial 4 (Case 5) | **3 / 5** |

Two models (Claude and Gemini) post-audit reach the prereg P1 confirmed
threshold of `3+/5 Stage 1 FAIL`. **P1 is therefore expected to flip
from `partially confirmed` (pre-audit) to `confirmed` (post-audit)**.

P3 recomputation requires the Stage 4 audit (failure-trials denominator
grows from 5 to ~9 post-audit Stage 1-3; over-claim numerator depends
on Stage 4 audit outcomes).
