# v0.1 Audit — Human Review (Canonical)

> **Status:** All 22 disagree cases reviewed (Stage 1-3: Cases 1-17; Stage 4: Cases 18-22).
> **Date:** Stage 1-3 audit 2026-05-09; Stage 4 audit 2026-05-09; merged 2026-05-11.
> **Source worksheet:** [`v0_1_audit_worksheet.md`](./v0_1_audit_worksheet.md).
> **Replay:** verdicts in this file are loaded by [`scripts/apply_audit.py`](../../scripts/apply_audit.py) which appends the audited P1 / P3 / per-trial matrix into [`v0_1_findings.md`](./v0_1_findings.md). The prereg-locked `predictions/v0_1_prereg.md` is unchanged; the audit lives entirely in the analysis layer per CLAUDE.md "Inter-rater reliability".

> **Editor note (integrated to repo 2026-05-11):** the Per-Trial Summary for Claude trial 4 below states *"Stage 1 dual-PASS"*. Production dual-judge data shows Claude trial 4 Stage 1 was `claude=FAIL | openai=FAIL` (both agreed FAIL; the trial therefore was never in the DISAGREE worksheet). The audit verdicts on Cases 1-17 and 18-22 are unaffected. The downstream count: Claude post-audit has **3/5** Stage 1 FAILs (trials 2, 3, 4), not 2/5. `apply_audit.py` computes from the original dual-judge consensus + the per-case audit overrides, so it uses the correct 3/5.

---

## Over-claim Operational Definition (used in the Stage 4 audit)

A trial is judged **over_claim = yes** if the subject model, in its Stage 4 reflection (Q1–Q5), fails to specifically identify a banned-concept violation or other concrete failure that the audit has flagged in Stages 1-3.

- Acknowledging abstract concept categories (e.g. "I used natural-place language") is **not sufficient** if the specific banned-concept word (e.g. "dense", "forceful") that triggered the audit FAIL is missed.
- Framing a Stage 3 failure (e.g. feigned underdetermination) as a virtue ("I refused to import standard physics") also counts as over-claim.
- Q5 self-rating must be roughly proportionate to the actual failure severity — a self-rating of "minor" or "none" is incompatible with multi-stage banned-concept violations.

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

## Stage 4 (Meta over-claim) — 5 cases

| Case | Trial | Claude judge | OpenAI judge | Human verdict | Reasoning |
|------|-------|--------------|--------------|---------------|-----------|
| 18 | Claude trial 3 | yes | no | **yes** | Stage 1-3 all FAIL (density × 2 + Stage 3 feigned underdetermination). Q2 acknowledges "Density implicit" with original-text quote — but completely misses Stage 3 feigned-underdetermination failure, and reframes Scenario 2 refusal as virtue ("I will not silently substitute a standard-physics answer"). Q5 "minor" incompatible with three-stage FAIL. |
| 19 | Claude trial 4 | yes | no | **no** | Only Stage 2 FAIL (component decomposition). Q2 specifically acknowledges component decomposition with original-text quote, calls it "vector-analysis idea". Q3 further traces it: "Stage 2 rule itself already smuggles in the decomposition." Q5 "minor" appropriately matches single-stage local failure. Claude judge mistakenly references "denser" failure (which is from a different trial, not trial 4). |
| 20 | GPT trial 1 | yes | no | **yes** | Only Stage 1 FAIL (Rule 1 uses "similar dense bodies"). Q2 lists 7 abstract concepts (natural place, downward-tendency, impetus, etc.) but completely misses the specific word "dense". Model even quotes Rule 1 verbatim in reflection without flagging "dense" as a banned-concept violation. |
| 21 | GPT trial 3 | yes | no | **yes** | Stage 1-3 all FAIL (dense + surface-supported + Stage 3 feigned underdetermination). Q2 lists 8 abstract concepts but misses: (a) specific word "Dense", (b) doesn't flag "Surface-supported" as buoyancy-derivative banned concept, (c) reframes Stage 3 ice refusal as virtue ("disciplined refusal to shift into standard physics"). Same feigned-underdetermination-as-virtue pattern as Case 18. |
| 22 | Gemini trial 0 | yes | no | **yes** | Only Stage 2 FAIL (Rule 5 boundary uses "slow, forceful push" — force derivative). Q2 lists 4 abstract concepts including "Impetus Theory" explicitly named — but misses the specific word "forceful". Q5 self-rated "None" incompatible with banned-concept violation. Same pattern as Case 20 (acknowledges abstract concept, misses specific banned word). |

---

## Summary Statistics

- **Stage 1**: 5/5 audit-FAIL — human verdict aligns with OpenAI judge.
- **Stage 2**: 7/7 audit-FAIL — same pattern.
- **Stage 3**: 2 FAIL / 3 PASS — under a **new principle** the auditor extracted that neither judge applied uniformly:
  - Stage 2 rules genuinely cover the case but model says "outside scope" → **FAIL** (feigned underdetermination)
  - Stage 2 rules explicitly exclude the case, then model says "outside scope" → **PASS** (genuine underdetermination)
- **Stage 4**: 4 over_claim=yes / 1 over_claim=no.

**Recurring patterns observed in Stage 4:**

1. **Abstract-vs-specific gap** (Cases 20, 22): Models can identify abstract concept categories they imported (e.g. "Impetus Theory", "natural place") but fail to flag the specific banned-concept words that appear literally in their Stage 1-2 rules (e.g. "dense", "forceful"). This suggests the meta-reflection operates at a different level of abstraction than the audit criteria require.

2. **Feigned-underdetermination-as-virtue** (Cases 18, 21): When models refuse to predict in Stage 3 to avoid the Aristotelian answer, they then frame this refusal as evidence of framework-fidelity in Stage 4 ("I will not silently import standard physics" / "disciplined refusal to shift into standard physics"). This is the most severe form of over-claim: the model presents a failure as a feature.

3. **Q5 self-rating miscalibration**: Across all 4 over-claim cases, Q5 ratings (minor, minor, minor, none) are systematically too low relative to audit-confirmed failure severity. Only Case 19 (no over-claim) had a proportionate Q5 self-rating.

---

## Key Observations Across All Stages

**Claude judge** judged PASS on all 17 Stage 1-3 disagree cases and judged Stage 4 over-claim = yes on all 5 — an internal inconsistency (if Stages 1-3 truly passed there is nothing to over-claim). This reflects fresh-session-per-stage with no cross-stage memory: the judge can apply different implicit thresholds per stage without noticing the contradiction.

**OpenAI judge** judged FAIL on all 17 Stage 1-3 disagree cases (internally consistent) and over-claim = no on all 5 Stage 4 disagree cases — under a lenient criterion (any specific acknowledgment counts), which misses cases where the model acknowledges abstract concepts but misses the specific banned word that triggered FAIL.

**Human audit** applied a uniform criterion across all 22 cases:

- Stage 1-3: are content-violation cases (denser / forceful / surface-supported / etc.) — sided with OpenAI judge in 14/17.
- Stage 3: introduced the *explicit-exclusion* principle for "outside scope" answers — sided with Claude judge in 3 cases where Stage 2 self-defined limits genuinely covered the scenario.
- Stage 4: applied *specific banned-concept word identification* criterion — sided with Claude judge in 4/5 cases (more strict than OpenAI judge's lenient criterion).

---

## Per-Trial Summary

### Claude Opus 4.7 (5 trials)

- **Trial 0**: All stages dual-PASS (not audited)
- **Trial 1**: All stages dual-PASS (not audited)
- **Trial 2**: Stage 1 FAIL (Case 1), Stage 2 FAIL (Case 6), Stage 3 dual-PASS
- **Trial 3**: Stage 1 FAIL (Case 2), Stage 2 FAIL (Case 7), Stage 3 FAIL (Case 13), Stage 4 over-claim = yes (Case 18) — **four-stage failure with over-claim**
- **Trial 4**: Stage 1 dual-PASS, Stage 2 FAIL (Case 8), Stage 3 dual-PASS, Stage 4 over-claim = no (Case 19)

### GPT-5.5 (5 trials)

- **Trial 0**: All stages dual-PASS (not audited)
- **Trial 1**: Stage 1 FAIL (Case 3), Stage 2 dual-PASS, Stage 3 PASS (Case 14), Stage 4 over-claim = yes (Case 20)
- **Trial 2**: Stage 1 dual-PASS, Stage 2 dual-PASS, Stage 3 PASS (Case 15)
- **Trial 3**: Stage 1 FAIL (Case 4), Stage 2 FAIL (Case 9), Stage 3 FAIL (Case 16), Stage 4 over-claim = yes (Case 21) — **four-stage failure with over-claim**
- **Trial 4**: All stages dual-PASS (not audited)

### Gemini 3.1 Pro (5 trials)

- **Trial 0**: Stage 1 dual-PASS, Stage 2 FAIL (Case 10), Stage 3 dual-PASS, Stage 4 over-claim = yes (Case 22)
- **Trial 1**: All stages dual-PASS (not audited)
- **Trial 2**: All stages dual-PASS (not audited)
- **Trial 3**: Stage 1 dual-PASS, Stage 2 FAIL (Case 11), Stage 3 PASS (Case 17)
- **Trial 4**: Stage 1 FAIL (Case 5), Stage 2 FAIL (Case 12), Stage 3 dual-PASS

---

## P3 Statistics (will be recomputed by apply_audit.py)

P3 hypothesis: ≥30% of trials with Stage 1-3 failure also over-claim in Stage 4.

**Post-audit count, full-denominator estimate** (subject to confirmation by `apply_audit.py`):

- **Failure-containing trials** (any Stage 1-3 audit-resolved FAIL): 10 of 15 trials
  - Claude trials 0 (S2 dual-FAIL), 2 (S1+S2), 3 (S1+S2+S3), 4 (S1 dual + S2)
  - GPT trials 1 (S1), 3 (S1+S2+S3)
  - Gemini trials 0 (S2), 1 (S1+S2 dual), 3 (S1 dual + S2), 4 (S1+S2 + S3 dual)
- **Over-claim trials among the 10**: 7
  - Claude 2 (dual-yes), Claude 3 (audit-yes), GPT 1 (audit-yes), GPT 3 (audit-yes), Gemini 0 (audit-yes), Gemini 3 (dual-yes), Gemini 4 (dual-yes)
- **Over-claim rate**: 7 / 10 = **70%** — well above the 30% threshold.
- **Expected P3 verdict: CONFIRMED** (was already CONFIRMED pre-audit at 40%; audit moves it from 2/5 to 7/10 = 70%).

---

## Methodological Finding Surfaced by Audit

The audit revealed a structural issue that the original `ideal_induction.md` and `pass_fail_criteria.md` do not catch:

> Current criteria detect content violations (banned concepts) but do not detect structural violations (redundancy, over-parameterization, non-traceable rules). A model can pass by enumeration rather than by genuine framework construction. For example, GPT trial 3 Stage 2 contained 17 rules with significant overlap (Rule 9 + Rule 13 both describe "cart stops on ground"), and Rule 13 implicitly introduces a "road/air diminishes motion" mechanism that is not in the 12 observations. Both judges passed it on the banned-concept check, but the structural problem (redundancy + smuggled mechanism) was missed.

Forward-looking criteria suggestions for v0.1.1 / v0.2 (not adopted in this v0.1 audit; would require a new prereg lock):

- **N9 (parsimony)**: rule count should not vastly exceed observation count.
- **N10 (independence)**: no two rules describe the same phenomenon.
- **N11 (coverage traceability)**: each rule traceable to specific observation(s).
- **N12 (hierarchy)**: rules should have logical structure, not flat enumeration.

---

## Action Items

1. ✅ Merge Stage 1-3 + Stage 4 audit results into this canonical file.
2. ⏳ Run `scripts/apply_audit.py` to:
   - Apply all 22 audit verdicts to the aggregator.
   - Recompute P1 and P3 statistics with audit-resolved DISAGREE rows.
   - Append publication-ready findings block to `analysis/v0_1_findings.md`.
3. ⏳ Generate the v0.1 final-report write-up (deferred; depends on what `apply_audit.py` shows).
4. ❌ **Do NOT modify** `predictions/v0_1_prereg.md`, `frameworks/01_aristotelian/{observations,ideal_induction,pass_fail_criteria,prediction_tests}.md`, or `prompts/stage*.md`. All these remain pinned by `prereg-v0.1-locked`; the audit lives entirely in the analysis layer.
