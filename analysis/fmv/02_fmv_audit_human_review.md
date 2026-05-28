# 02_fmv Audit — Human Verdicts (Canonical)

> **Status:** All 14 dual-judge disagreement cases reviewed (12 content + 2 meta).
> **Date:** 2026-05-18.
> **Source worksheet:** [`02_fmv_audit_worksheet.md`](./02_fmv_audit_worksheet.md).
> **Trigger:** Stage 1-3 dual-judge IRR 26.67 % > 25 % audit threshold.
> Per `prereg-02_fmv-locked`, these human verdicts are the **canonical**
> disagree resolution; they replace the DISAGREE rows in P1 / P2 / P4.
>
> **Editor note:** the "Agreement rates" section below originally read
> "Claude judge vs human: 12/14"; the case-by-case "Agreed with" column
> sums to **11 Claude / 3 OpenAI** (= 14). Corrected to 11/14 here; the
> case table is authoritative.

14 disagree cases audited. Pre-audit IRR = 26.67% (12/45 Stage 1-3 + 2 meta).

## Verdicts

| Case | Trial | Stage | Claude | OpenAI | Human | Agreed with |
|------|-------|-------|--------|--------|-------|-------------|
| 1 | Claude T3 | S1 | PASS | FAIL | **PASS** | Claude |
| 2 | Claude T4 | S1 | PASS | FAIL | **PASS** | Claude |
| 3 | Gemini T0 | S1 | PASS | FAIL | **PASS** | Claude |
| 4 | Gemini T3 | S1 | FAIL | PASS | **FAIL** | Claude |
| 5 | Claude T0 | S2 | PASS | FAIL | **PASS** | Claude |
| 6 | Claude T1 | S2 | PASS | FAIL | **FAIL** | OpenAI |
| 7 | Claude T3 | S2 | PASS | FAIL | **PASS** | Claude |
| 8 | Claude T4 | S2 | PASS | FAIL | **PASS** | Claude |
| 9 | GPT T2 | S2 | PASS | FAIL | **PASS** | Claude |
| 10 | Gemini T0 | S2 | PASS | FAIL | **FAIL** | OpenAI |
| 11 | Gemini T4 | S2 | PASS | FAIL | **PASS** | Claude |
| 12 | Claude T4 | S3 | PASS | FAIL | **PASS** | Claude |
| 13 | Claude T0 | Meta | no | yes | **no** | Claude |
| 14 | Gemini T0 | Meta | no | yes | **yes** | OpenAI |

## Agreement rates

- Claude judge vs human: **11/14 (79%)**
- OpenAI judge vs human: **3/14 (21%)**

## OpenAI judge failure analysis

OpenAI judge performed far worse than in v0.1 Aristotelian (where it agreed with human audit 15/22 = 68%). Three distinct failure modes:

**1. Verdict-field self-contradiction (Cases 3, 7, 8, 9, 12)**
OpenAI's reasoning text explicitly concludes "this should pass" or "no listed banned token appears," but the verdict field says FAIL. This is the same bug observed in v0.2 Aristotelian structural audit with Claude's structural judge. Five of 14 cases (36%) have this defect.

**2. Hallucinated banned tokens (Cases 1, 2, 5)**
OpenAI claims to find banned tokens that do not exist in the response:
- Case 1: claims "air" is banned (it is not in §3)
- Case 2: claims "glides" is a morphological variant of "gravity" (it is not)
- Case 5: claims "inertia" appears in Rule 1 heading (it does not; heading is "Effort produces pace directly")

**3. Correct banned-token detection (Cases 6, 10)**
OpenAI correctly identified "massless" (Case 6) and "massive" (Case 10) as containing the banned substring "mass." These are the only two cases where OpenAI agreed with the human verdict on a FAIL.

**Summary**: OpenAI judge's accurate detections were limited to substring matches of "mass." It hallucinated tokens in 3 cases, self-contradicted in 5 cases, and had confused reasoning in the remainder. This is a complete reversal from v0.1 Aristotelian where OpenAI was the more reliable judge.

## Reasoning for each case

**Cases 1, 2, 3 (S1 PASS):** No banned tokens in response. OpenAI hallucinated "air", "glides"→"gravity", and self-contradicted respectively. Full content check (N1-N6, P1-P7) also PASS.

**Case 4 (S1 FAIL):** Response is a truncated fragment — only the second half of a reasoning trace, with no actual rules stated. Claude correctly identified this; OpenAI ignored it and judged on fragments.

**Case 5 (S2 PASS):** No banned tokens. OpenAI hallucinated "inertia." Full content check PASS (operational rules with P=E/H, scope, boundary notes).

**Case 6 (S2 FAIL):** "massless" in Rule 4 boundary cases ("the observations include no massless bodies"). §3 pure lexical: "mass" substring present → FAIL. Model could have written "bodies of zero heaviness."

**Cases 7, 8 (S2 PASS):** No banned tokens. OpenAI self-contradicted. Full content check PASS.

**Case 9 (S2 PASS):** No banned tokens. OpenAI self-contradicted. Full content check PASS — GPT wrote 15 operational rules with quantitative S = S₀ × (P/P₀) × (H₀/H), all N1-N6 covered, no P1-P7.

**Case 10 (S2 FAIL):** "massive" in Rule 4 boundary cases ("creates a massive boundary case"). §3 pure lexical: "mass" substring present → FAIL. Model could have written "severe" or "profound."

**Case 11 (S2 PASS):** No banned tokens. OpenAI had confused reasoning (claimed "medium" then pivoted to content objection). Full content check PASS.

**Case 12 (S3 PASS):** All 5 scenarios answered correctly with F=mv ratios (2D, 2T, straight down, 2:1, immediate full pace). No banned tokens. OpenAI self-contradicted on Scenario 3 ("physics" not in banned list).

**Case 13 (Meta — no over-claim):** Claude T0, Stage 1-3 all PASS (after audit). Model's self-assessment ("maintained coherent framework", Q5 "Minor") is proportionate. OpenAI judged yes based on "possible Stage 2 failure" that was resolved as PASS.

**Case 14 (Meta — yes over-claim):** Gemini T0, Stage 2 FAIL ("massive"). Model claims "None" standard-physics influence and full coherence. Does not acknowledge "massive" slip. Additionally, Q4 point 4 contradicts model's own Stage 1 rules (claims "falling speed is dependent on mass" when own Rule 5 says all objects fall at identical pace).

## Key findings

**1. Judge reliability does not transfer across frameworks.**
v0.1 Aristotelian: OpenAI 68% agreement, Claude 32%. F=mv: Claude 79%, OpenAI 21%. Same judge prompts, same models, completely reversed performance. This is a paper-level finding.

**2. "mass" derivatives are the only real banned-token violations.**
Of 14 disagree cases, only 2 are genuine FAIL (Cases 6, 10) — both for "mass" substrings ("massless", "massive") in boundary-note parentheticals. No model used a banned token in an actual rule or prediction. The F=mv banned-token list is effective: models successfully avoid banned vocabulary in their core reasoning.

**3. OpenAI judge verdict-field bug is systematic.**
5/14 cases have verdict ≠ reasoning. This is not random error — it's a systematic defect where the model fills the verdict JSON field before completing its reasoning chain, then the reasoning overrides the verdict but doesn't update the field.
