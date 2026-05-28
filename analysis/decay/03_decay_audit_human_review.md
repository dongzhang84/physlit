# 03_decay Audit — Human Verdicts (Canonical)

> **Status:** All 54 dual-judge disagreement cases reviewed (18 content + 32 Stage 3 per-scenario + 4 meta).
> **Date:** 2026-05-28.
> **Source worksheet:** [`03_decay_audit_worksheet.md`](./03_decay_audit_worksheet.md).
> **Non-canonical agent preview:** [`03_decay_agents_review.md`](./03_decay_agents_review.md).
> **Trigger:** Stage 1-3 dual-judge IRR 40.00 % > 25 % audit threshold (`CLAUDE.md`).
> Per `prereg-03_decay-locked` §1.4 these human verdicts are the **canonical** disagree resolution.

54 cases audited: 18 content (Part A) + 32 per-scenario (Part B) + 4 meta (Part C).
Headline: **P1, P2, P3, P4 all CONFIRMED.** Composite content PASS = **0/15**.

## Part A — Content axis (18 cases)

All 18 cases are non-decisive for P1 — every trial has at least one Stage 3 scenario consensus-FAIL, so composite content = FAIL on every trial. Resolved for the record and to feed the Stage 1 first-FAIL clause aggregation needed for P2.

| Case | Trial | Stage | Claude | OpenAI | **Human** | Agreed with | Reason |
|------|-------|-------|--------|--------|-----------|-------------|--------|
| C1 | Claude T0 | S2 | PASS | FAIL | **PASS** | Claude | OpenAI misclassified "pulled" as banned `force` |
| C2 | Claude T2 | S2 | PASS | FAIL | **PASS** | Claude | OpenAI misclassified "preserved" as banned `conservation` |
| C3 | Claude T3 | S2 | PASS | FAIL | **PASS** | Claude | OpenAI misclassified "preserved" as banned `conservation` |
| C4 | Claude T0 | S1 | PASS | FAIL | **PASS** | Claude | OpenAI hallucinated `resistance` (not in response) |
| C5 | Claude T1 | S1 | PASS | FAIL | **PASS** | Claude | OpenAI hallucinated `deceleration` |
| C6 | Claude T2 | S1 | PASS | FAIL | **PASS** | Claude | OpenAI hallucinated `resistance` |
| C7 | Claude T4 | S1 | PASS | FAIL | **PASS** | Claude | OpenAI misclassified "fired" as form of `force` |
| C8 | GPT T0 | S2 | PASS | FAIL | **FAIL** | OpenAI | §5 P2 — orbital radius framed as a "derived observed outcome"; sideways speed treated as the underlying decaying quantity |
| C9 | GPT T1 | S2 | PASS | FAIL | **FAIL** | OpenAI | N4 — separate τ values per system, no universal constant declared |
| C10 | GPT T2 | S2 | PASS | FAIL | **PASS** | Claude | Unified `e^{-t/100}`; orbital handled causally without making radius a downstream quantity |
| C11 | GPT T0 | S1 | PASS | FAIL | **PASS** | Claude | OpenAI misclassified "influences" as banned `force` |
| C12 | GPT T2 | S1 | PASS | FAIL | **PASS** | Claude | OpenAI cited "radiation"; not in §3 banned list |
| C13 | Gemini T0 | S2 | PASS | FAIL | **FAIL** | OpenAI | §5 P2 — scope omits radius; speed is the underlying decaying quantity |
| C14 | Gemini T1 | S2 | PASS | FAIL | **FAIL** | OpenAI | §5 P2 — sideways speed → radius (same pattern as C13) |
| C15 | Gemini T0 | S1 | PASS | FAIL | **PASS** | Claude | Response truncated but Rule 2 body complete; all six N1-N6 conditions stated |
| C16 | Gemini T1 | S1 | PASS | FAIL | **FAIL** | OpenAI | §5 P2 — scope omits radius; sideways speed → radius |
| C17 | Gemini T2 | S1 | PASS | FAIL | **FAIL** | OpenAI | Response truncated; obs 8 coverage incomplete (§6.3) |
| C18 | Gemini T4 | S3 | PASS | FAIL | **PASS** | Claude | All 5 scenarios within PASS ranges; Scenario 4 correctly applies the decay rule to radius |

**Post-audit Part A distribution:** 11 PASS / 7 FAIL.
**Per model:** Claude 7/7 PASS · GPT 2/4 PASS (2 FAIL: P2, N4) · Gemini 2/7 PASS (3 P2, 1 truncation, 1 coverage).

### FAIL-type distribution (Part A only)

| FAIL type | Count | Cases |
|-----------|-------|-------|
| §5 P2 (hidden-substrate / orbital-radius framing) | 4 | C8, C13, C14, C16 |
| §4 N4 (per-system τ, no universal constant) | 1 | C9 |
| §6.3 coverage (truncation, obs 8 incomplete) | 1 | C17 |

Note: C18 covers Stage 3, not first-FAIL aggregation. The §5 P2 hits in C8 / C13 / C14 are at Stage 2 (formulation), so they do **not** enter the Stage 1 §5 distribution that scores P2 in the prereg. Only C16 is a Stage 1 §5 hit.

## Part B — Stage 3 per-scenario (32 cases)

Collectively decisive for P3. Each case is classified into one of three buckets per `prereg-03_decay-locked` §2 P3: **decay-correct**, **direction-correct / ratio-leaked**, or **direction-wrong**. Per the prereg, decline-to-commit responses (no quantitative value supplied) land in the **ratio-leaked** bucket.

| Case | Trial | Scenario | Claude | OpenAI | **Human** | Direction | Bucket | Reason |
|------|-------|----------|--------|--------|-----------|-----------|--------|--------|
| B1 | Claude T0 | s1 | PASS | FAIL | **FAIL** | correct | ratio-leaked | §3 "forced" appears in Scenario 4 and pollutes the full response (§3 scope is the whole response) |
| B2 | Claude T0 | s2 | PASS | FAIL | **FAIL** | correct | ratio-leaked | same §3 pollution |
| B3 | Claude T0 | s3 | PASS | FAIL | **FAIL** | correct | ratio-leaked | same §3 pollution |
| B4 | Claude T1 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B5 | Claude T1 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B6 | Claude T1 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B7 | Claude T3 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B8 | Claude T3 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B9 | Claude T3 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B10 | Claude T4 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B11 | Claude T4 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B12 | Claude T4 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B13 | GPT T2 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B14 | GPT T2 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B15 | GPT T3 | s1 | PASS | FAIL | **FAIL** | correct | ratio-leaked | decline-to-commit (Scenario 1 scope issue) |
| B16 | GPT T4 | s1 | FAIL | FAIL | **FAIL** | correct | ratio-leaked | decline-to-commit (no r_pendulum value supplied) |
| B17 | Gemini T0 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B18 | Gemini T0 | s4 | FAIL/wrong | FAIL/correct | **FAIL** | correct | ratio-leaked | orbital outside model's declared scope → decline-to-commit |
| B19 | Gemini T1 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B20 | Gemini T1 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B21 | Gemini T1 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B22 | Gemini T2 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B23 | Gemini T2 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B24 | Gemini T2 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B25 | Gemini T3 | s1 | FAIL/n/a | FAIL/correct | **FAIL** | n/a | ratio-leaked | decline-to-commit (Scenario 1 scope issue) |
| B26 | Gemini T3 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B27 | Gemini T3 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B28 | Gemini T3 | s4 | FAIL/n/a | FAIL/correct | **FAIL** | correct | ratio-leaked | orbital outside scope → decline-to-commit |
| B29 | Gemini T4 | s1 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B30 | Gemini T4 | s2 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B31 | Gemini T4 | s3 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |
| B32 | Gemini T4 | s4 | PASS | FAIL | **PASS** | correct | decay-correct | within PASS range |

**Post-audit Part B distribution:** 24 decay-correct · 8 ratio-leaked · 0 direction-wrong.

**Combined with pre-audit consensus (13 decay-correct + 15 ratio-leaked + 0 direction-wrong):**
**P3 final tally: 37 decay-correct / 23 ratio-leaked / 0 direction-wrong** across 60 quantitative predictions.

### FAIL reasons (Part B only)

| Reason | Count | Cases |
|--------|-------|-------|
| §3 "forced" in Scenario 4 polluting the entire response | 3 | B1, B2, B3 |
| Decline to commit (Scenario 1 scope issue) | 2 | B15, B25 |
| Decline to commit (Scenario 4 orbital outside model's scope) | 2 | B18, B28 |
| Decline to commit (no r_pendulum value supplied) | 1 | B16 |

The §3 banned-token rule's "whole-response scope" turns one banned token in one scenario (Claude T0 Scenario 4) into three additional Scenario-level FAILs — a sharp cost for a single lexical slip.

## Part C — Stage 4 meta over-claim (4 cases)

Decisive for P4. Pre-audit consensus across 11 trials: 6 yes, 5 no. The 4 audit-pending cases all resolved **yes**, giving the final tally **10 yes vs 5 no → P4 CONFIRMED**.

| Case | Trial | Claude | OpenAI | **Human** | Reason |
|------|-------|--------|--------|-----------|--------|
| M1 | Claude T0 | no | yes | **yes** | Stage 3 FAIL but Q5 self-assessment says "minor"; the model does not acknowledge the Stage 3 slip |
| M2 | Claude T3 | no | yes | **yes** | Stage 1 (N4) + Stage 3 FAIL; Q5 says "minor" |
| M3 | GPT T0 | no | yes | **yes** | Stage 2 (§5 P2) + Stage 3 FAIL; Q5 says "minor to moderate"; model does not identify the P2 hidden-substrate framing |
| M4 | GPT T4 | no | yes | **yes** | Stage 1 + 2 + 3 all FAIL (N4 across the board); Q5 says "minor to moderate"; model does not identify the N4 universal-constant failure |

## Agreement rates

| Source | Cases scored | Agreement | Notes |
|--------|--------------|-----------|-------|
| Claude judge — Part A | 18 | **12/18 (67%)** | the more reliable judge on this framework |
| OpenAI judge — Part A | 18 | **6/18 (33%)** | systematic §3 fabrication / misclassification |
| Claude judge — Part B | 32 | **26/32 (81%)** | |
| OpenAI judge — Part B | 32 | **7/32 (22%)** | one direction-correct citation away from chance |
| Claude judge — Part C | 4 | **2/4 (50%)** | |
| OpenAI judge — Part C | 4 | **2/4 (50%)** | |
| Agent 1 (`gemini-3.1-pro-preview`) — Part A | 17 (one unparseable verdict) | **14/17 (82%)** | non-canonical; ran against the locked 03_decay criteria |
| Agent 2 (`gemini-3.1-pro-preview`) — Part B | 32 | **31/32 (97%)** | non-canonical; the lone disagreement was B25 (Agent 2 graded direction-wrong; audit graded n/a) |

## OpenAI judge — systematic §3 failure on the Decay World

OpenAI judge fabricated or misclassified banned tokens in nearly every Part A case (16/18 = 89% of OpenAI's FAIL clauses were defective). The Decay World §3 banned-token list is 20+ tokens long, and the response topics semantically overlap with the banned vocabulary (decay ↔ damping, slow ↔ deceleration, no-contact ↔ resistance). The OpenAI judge appears to perform semantic association rather than substring matching, even though §3 is explicitly defined as a purely lexical test (`ideal_induction.md` §3, second paragraph).

The `evidence_check.py` post-processor caught most fabricated citations (tokens cited that don't appear as substrings in the response) — those are the `FAB` flags in the worksheet. It cannot catch misclassification — where the judge found a real word in the response but incorrectly labelled it as banned.

### Fabricated tokens (cited word does not appear in the response)

- `resistance` — C4 (Claude T0 S1), C6 (Claude T2 S1)
- `deceleration` — C5 (Claude T1 S1)
- `frictionless` — B19, B20, B21 (Gemini T1 prediction)
- `damping` — B7, B8, B9 (Claude T3 prediction)
- `force` from "Reinforcing" — C16 (the word "Reinforcing" is in the response but does **not** contain the banned token `force` as a morphological component; the substring match is spurious)

### Misclassified tokens (word is present but not banned)

- `fired` → `force` (C7)
- `influences` → `force` (C11)
- `preserved` → `conservation` (C2, C3)
- `radiation` → §3 ban (C12; `radiation` is not on the §3 list)
- `factor` → `force` (B22, B23, B24)
- `continuous` → `conservation` (B29, B30, B31, B32)
- `weight` → `mass` (B4, B5, B6)
- `insulation` → `inertia` (B10, B11)
- `heating` → `heat` (C12; `heat` is not on the §3 list)
- `pulled` → `force` (C1)
- `imported` → `momentum` (C14)
- `smooth` → §3 ban (B13, B14)
- `adding` → `acceleration` (C15)

## Key findings

**1. Judge reliability re-reverses across frameworks (now three data points).**
- v0.1 Aristotelian: OpenAI 68%, Claude 32%.
- 02_fmv F=mv: Claude 79%, OpenAI 21%.
- 03_decay: Claude 67% (Part A) / 81% (Part B) / 50% (Part C); OpenAI 33% / 22% / 50%.

The pattern is now systematic: the relatively more reliable judge depends on the framework. On the Decay World, the OpenAI judge's failure is a single mechanism — §3 banned-token fabrication / misclassification at a degraded rate when the ban list is long and topic overlap is high. This is not random model variance.

**2. §3 banned-token "long list with topic overlap" is a stress test the OpenAI judge fails.**
The Decay World §3 list has 20+ tokens spanning mechanism, mechanics, physicist names, and equation forms. The Decay phenomena are inherently overlapping with that vocabulary (the world is about *not*-damping, *not*-dissipation, *not*-friction — but the response naturally describes the *absence* of those mechanisms). OpenAI's degradation here suggests a methodology guardrail for future rounds: when the §3 list is long, audit a sample of pre-audit consensus FAILs to verify the OpenAI judge isn't fabricating in bulk.

**3. Single-word lexical pollution can cost a trial 3 scenario PASSes.**
B1 / B2 / B3 are all FAIL solely because Scenario 4's response contains "forced". §3 scope is the whole response (carried in from 02_fmv), so a single banned token outside any specific scenario's text disqualifies the whole prediction stage. This is not a defect — it is the literal definition of the scope rule — but it warrants noting in the report as a sharp, possibly excessive, sensitivity.

**4. The Stage 1 §5 P2 sample is small but the pattern at Stage 2 is consistent.**
Only **one** Stage 1 trial (Gemini T1) FAILs on a §5 pattern, and it is P2. Three of the four Stage 2 §5 hits (C8 GPT T0, C13 Gemini T0, C14 Gemini T1) are also P2. The hidden-substrate framing — treating speed (or some other measured quantity) as the underlying decaying thing and deriving the others from it — is the only §5 pattern that fired in the entire experiment. P2 is technically confirmed (1 > 0 in the Stage 1 denominator), but the strongest evidence for the design hypothesis comes from Stage 2, where it is not in the prereg scoring window. A future round should consider widening the P2 first-FAIL aggregation to Stage 1 + Stage 2 combined.

**5. Agent 2 nearly matches the human audit on per-scenario classification.**
31/32 = 97% agreement is the highest agent-vs-human number across the entire PhysLit programme to date. The Decay World per-scenario judging task (numeric range check + direction call) appears to be tractable for a frontier LLM resolver. Agent 1 on the content axis ran at 82%, dragged down by the same OpenAI-side §3 fabrications that the human audit had to unwind.

**6. P4 over-claim rate climbs to 67% on a harder framework.**
v0.1 Aristotelian post-audit: 70%. 02_fmv F=mv: 66.7%. 03_decay: 10/15 = 67%. Three rounds in three different frameworks now converge on a 65–70% over-claim rate among failure-containing trials. This is a publishable behavioural regularity in its own right and is independent of P1 / P2 / P3.
