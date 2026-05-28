# 02_fmv.1 Structural Audit — Human Verdicts

7 disagree cases audited. Pre-audit structural IRR = 46.67% (7/15).

## Verdicts

| Case | Trial | Rules | Claude | OpenAI | Human | Failed | Agreed with |
|------|-------|-------|--------|--------|-------|--------|-------------|
| 1 | Claude T2 | 10 | PASS | FAIL | **FAIL** | N11 | OpenAI |
| 2 | Claude T3 | 11 | PASS | FAIL | **FAIL** | N10 | OpenAI |
| 3 | Claude T4 | 10 | PASS | FAIL | **FAIL** | N10 | OpenAI |
| 4 | GPT T2 | 15 | PASS | FAIL | **FAIL** | N10 | OpenAI |
| 5 | GPT T4 | 14 | PASS | FAIL | **FAIL** | N10 | OpenAI |
| 6 | Gemini T2 | 4 | FAIL | PASS | **PASS** | — | OpenAI |
| 7 | Gemini T4 | 5 | FAIL | PASS | **FAIL** | N12 | Claude |

## Agreement rates

- Claude structural judge vs human: **1/7 (14%)**
- OpenAI structural judge vs human: **6/7 (86%)**

## Complete reversal pattern across axes

| Axis | Claude judge | OpenAI judge |
|------|-------------|-------------|
| Content (02_fmv) | **86%** (12/14) | **21%** (3/14) |
| Structural (02_fmv.1) | **14%** (1/7) | **86%** (6/7) |

Same models, same framework, different judgment task — completely reversed reliability. Judge performance is task-dependent, not model-dependent. This is a paper-level finding.

## Reasoning for each case

### Case 1 — Claude T2 — FAIL (N11)

Rule 10 states: "The fall halts on contact. When the falling object reaches the ground, the downward pull is opposed and the object stops, in keeping with rule 5."

This introduces "ground provides upward push" — a fabricated mechanism. No observation says the ground pushes anything. Obs 10 only says objects "strike the ground together." The model could simply state "objects stop when they reach the ground" as a brute fact from observation, without inventing a ground-push mechanism.

Additionally, obs 6 states that the track plays no part in the block's behavior — yet Rule 10 assigns the ground an active pushing role, creating an internal contradiction.

N11: fabricated mechanism with no observational basis. FAIL.

### Case 2 — Claude T3 — FAIL (N10)

Rule 1: "how fast a thing moves is fixed by the push acting on it at that very moment. When the push stops, the pace stops."
Rule 2: "The present push alone sets the present pace; with no push, there is no motion."

These are the same operational claim stated positively (Rule 1) and negatively (Rule 2). Both reduce to: current push alone determines current pace; no push = no motion.

N10: paraphrase into the same operational claim. FAIL.

### Case 3 — Claude T4 — FAIL (N10)

Rule 1: "A thing moves only while it is being pushed or pulled. The moment any push or pull ceases, the thing halts in place."
Rule 10: "To transport a load, one must push the whole way. Since releasing the push halts the load at once (Rule 1)..."

The model itself cites "(Rule 1)" in Rule 10 — acknowledging Rule 10 is a restatement of Rule 1 applied to transport. Same operational claim: no push → no motion.

N10: self-acknowledged restatement. FAIL.

### Case 4 — GPT T2 — FAIL (N10)

15 rules with multiple redundant pairs:

- Rule 1 ("halts the instant that help stops") vs Rule 4 ("stops immediately at that place") — same claim
- Rule 4 vs Rule 8 ("Pushing hard only at the start cannot make the load continue by itself") — same claim applied to transport
- Rule 11 ("forward motion ends... drops straight down") vs Rule 15 ("forward push gives forward motion only while it continues... drops straight down") — same claim

15 rules = N9 soft signal. Combined with N10 violations = FAIL.

### Case 5 — GPT T4 — FAIL (N10)

Rule 3: "twice the effort gives twice the pace, three times the effort gives three times the pace"
Rule 5: "the pace equals the applied effort divided by the object's heaviness"

Rule 5 = Rule 3 + Rule 4 merged into one formula. Rule 3's proportionality information is entirely contained within Rule 5. The model wrote the general formula (Rule 5) while keeping the specific case (Rule 3) as a separate rule.

14 rules = N9 soft signal. Combined with N10 = FAIL.

### Case 6 — Gemini T2 — PASS

4 rules. N9 PASS (well under 12). N10 PASS (no duplicates). N11 PASS (each traces to observations). N12 exempt (< 5 rules).

Claude structural judge verdict = FAIL but reasoning self-corrects to PASS ("N12 exempts rule sets with fewer than 5 rules, so this does not trigger FAIL"). This is the verdict-field bug seen across multiple audit rounds.

### Case 7 — Gemini T4 — FAIL (N12)

5 rules. N9/N10/N11 all PASS. But 5 rules = N12 applicable (≥ 5 requires cross-rule references).

All 5 rules are independently stated with no cross-references — no "Rule N", no "as stated above", no "follows from", no hierarchy markers. Each rule stands alone.

N12: ≥ 5 rules with zero cross-references. FAIL.

## Claude structural judge failure analysis

Claude structural judge agreed with human on only 1/7 cases. Its systematic error: **too lenient on N10 and N11**.

In Cases 1-5, Claude judged PASS where the human found genuine redundancy (N10) or fabrication (N11). Claude's reasoning consistently treated borderline cases as PASS — "lean PASS" guidance taken too far.

In Case 6, Claude had a verdict-field bug (verdict = FAIL, reasoning = PASS).

Only in Case 7 did Claude correctly identify N12 failure.

## P1 / P2 status

**P1 (IRR < 40%):** Structural-axis dual-judge IRR = 46.67% (7/15). The IRR is audit-invariant — it counts trials where the two structural judges disagreed, which the human audit does not change. 46.67% ≥ 40%. **P1 REFUTED.**

**P2 (≥ 1 content-PASS trial flipped by structure):** 8 of the 9 all-content-PASS trials are reclassified to composite FAIL by the structural axis. **P2 CONFIRMED.**

## Design note for paper

N12 may be overly strict for small rule sets at the boundary (exactly 5 rules). A rule set of 5 clean, independent rules is arguably good induction without requiring explicit cross-references. The < 5 exemption threshold could be raised to < 7 in future versions. This does not affect the current verdict (prereg locked), but should be disclosed as a design limitation.
