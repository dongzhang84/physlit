# v0.3 Audit — Human Verdicts (Aristotelian Axiomatisation Treatment)

11 disagree cases audited: 8 content (IRR 17.78 %) + 3 structural (IRR 20.00 %).

## Part A — Content Axis (8 cases)

| Case | Trial | Stage | Claude | OpenAI | Human | Reason |
|------|-------|-------|--------|--------|-------|--------|
| C1 | Claude T0 | S1 | PASS | FAIL | **FAIL** | "denser" = density (banned concept). Same ruling as v0.1. |
| C2 | Claude T0 | S2 | PASS | FAIL | **FAIL** | "speeds up, slows down, or holds steady" — Newton leak. No observation mentions acceleration/deceleration; model imported the concept from training data. |
| C3 | Claude T0 | S3 | PASS | FAIL | **FAIL** | "I will not silently import a standard-physics answer (such as that the feather falls just like the iron ball)" — model exposed knowledge of Galileo's vacuum result. Naming to deny = use per §3. |
| C4 | Claude T1 | S3 | PASS | FAIL | **FAIL** | Scenario 4: model predicted "feather falls straight down" instead of rejecting the vacuum scenario. Aristotelian correct answer = vacuum cannot exist / outside scope. Model gave prediction first, hedged after. Decisive case. |
| C5 | Claude T2 | S2 | PASS | FAIL | **FAIL** | "heavier (per equal volume)" = operational definition of density. Stage 1 used "weight vs resistance"; Stage 2 introduced new concept. Decisive case. |
| C6 | Gemini T1 | S3 | PASS | FAIL | **FAIL** | Scenario 5: model predicted arrow "immediately falls strictly downward." Aristotelian answer = air sustains forward motion (antiperistasis). Model's Stage 1 lacked impetus/antiperistasis rule. Non-decisive. |
| C7 | Gemini T2 | S3 | PASS | FAIL | **FAIL** | Scenario 5: same as C6 — arrow "immediately falls strictly straight downward." Same missing antiperistasis. Non-decisive. |
| C8 | Gemini T4 | S2 | PASS | FAIL | **FAIL** | "constant, unchanging speeds" for celestial bodies — Stage 1 only said "endless, repeating circular paths." Fixed period + circular path does not logically require constant speed (could be non-uniform within each cycle). New information introduced in Stage 2. Non-decisive. |

**All 8 content cases → FAIL.**

## Part B — Structural Axis (3 cases)

All three resolve PASS under previously-established principles.

| Case | Trial | Rules | Claude | OpenAI | Human | Reason |
|------|-------|-------|--------|--------|-------|--------|
| S1 | GPT T1 | 7 (Stage 1) | FAIL | PASS | **PASS** | Stage 2 has explicit cross-rule references ("as in Rule 1", "requires Rule 5"). Claude verdict-field bug (reasoning self-corrects to PASS). |
| S2 | Gemini T3 | 4 (Stage 1) | PASS | FAIL | **PASS** | 4 rules < 5, N12 exempt. OpenAI counted 8 (Stage 1+2 combined) — same v0.2 double-counting bug. |
| S3 | Gemini T4 | 3 (Stage 1) | FAIL | PASS | **PASS** | 3 rules < 5, N12 exempt. Claude verdict-field bug ("Verdict should be PASS"). |

**All 3 structural cases → PASS.**

## Key findings

### 1. Content axis: all 8 disagrees resolved as FAIL

This is unusual — every single disagree case went against the Claude content judge (which judged PASS) and aligned with OpenAI (which judged FAIL). In prior rounds OpenAI had high false-positive rates (hallucinated banned tokens, verdict-field bugs). This time OpenAI's FAIL calls were substantively correct, though sometimes for wrong or incomplete reasons.

### 2. Three types of Newton leak detected

**Type A — Banned vocabulary derivatives (C1, C5):** "denser" and "heavier per equal volume" both encode the density concept. Consistent with v0.1 rulings on "denser" / "dense."

**Type B — Training-data concept import (C2, C8):** Model introduced concepts (acceleration, constant speed) that no observation supports. The "speeds up / slows down" in C2 is particularly diagnostic — no observation describes changing fall speed, yet the model spontaneously discussed it because F=ma predicts acceleration during free fall.

**Type C — Standard-physics knowledge exposure (C3, C4):** Model revealed it knows Galileo's vacuum experiment result (C3) and gave a quasi-Newtonian prediction for vacuum scenarios instead of rejecting them per Aristotelian framework (C4).

**Type D — Missing framework concept (C6, C7):** Gemini's Stage 1 never induced antiperistasis or impetus, so Stage 3 predictions for the arrow defaulted to "immediately falls" — neither Aristotelian nor Newtonian, but a consequence of incomplete induction.

### 3. Structural axis: all 3 disagrees resolved as PASS

Two systematic judge bugs recurred:

- **Claude verdict-field bug** (S1, S3): reasoning self-corrects to PASS but verdict field stays FAIL. Same defect seen across all prior audit rounds.
- **OpenAI double-counting bug** (S2): counts Stage 1 + Stage 2 combined, triggering false N10. Same v0.2 design flaw — third occurrence (v0.2 Aristotelian original, then 02_fmv.1 which fixed it via Stage-1-only criteria, now re-emerging in v0.3 because v0.3 reuses v0.2 criteria per the prereg's identical-baseline-judging commitment).

### 4. Claude content judge too lenient on this round

Claude content judge judged all 8 disagree cases PASS. It missed: density derivatives (C1, C5), training-data concept imports (C2, C8), standard-physics knowledge exposure (C3, C4), and missing framework predictions (C6, C7). This contrasts with `02_fmv` where the Claude content judge agreed with the human audit on 86 % of cases. The judge's lenient direction stayed the same across rounds (Claude tends toward PASS); what shifted is whether that leniency aligned with the human verdict — on `02_fmv` it did (most disputed cases truly were PASS); on `v0.3` it did not (every disputed case was a real Newton leak).

### 5. v0.1 → v0.3 comparison note

v0.1 had "denser" as a recurring FAIL. v0.3 treatment arm still has "denser" (C1) — the axiomatisation instruction did not eliminate this particular leak. It also introduced new leak types (C2 "speeds up / slows down", C3 standard-physics exposure) not seen in v0.1, suggesting the parsimony pressure may have *encouraged* the model to consolidate its account by reaching for the cleaner Newtonian language. A side effect of the cue, parallel to (but distinct from) the `02_fmv.2` Claude-t2 P3 fabrication. The structural axis still moved decisively up; the content side gained 1 trial (5 → 6) but the disputed cases that the Claude judge wanted to call PASS were every one of them content-FAIL by audit.

## Methodological notes (from this round)

Two known judge defects, both with established precedents elsewhere in the project, surfaced again on the structural axis:

1. **OpenAI Stage 1+2 double-count** (S2). The v0.2 structural criteria (`frameworks/01_aristotelian/structural_criteria.md` §2: "rule count means top-level numbered or bolded propositions in the Stage 1 + Stage 2 combined output") combined with the Stage 2 prompt's mirror-numbering instruction creates a built-in conflict: any well-formed Stage 2 will be a mirror restatement of Stage 1, and under the v0.2 criteria those mirrored rules get counted as "duplicates" → N10 false positive. `02_fmv.1` already removed this defect by scoping the count and the N10 check to Stage 1 only. `v0.3` reuses the v0.2 criteria (the prereg required identical judging to the v0.1/v0.2 baseline so the cross-framework comparison is valid), so the defect re-emerges here. Resolution: the audit applies the Stage-1-only principle as the canonical reading.

2. **Claude verdict-field self-contradiction** (S1, S3). The structured `verdict` field reports FAIL while the reasoning text explicitly concludes "this should be PASS" / "Verdict should be PASS". Same defect class as `02_fmv.1` Case 6 (Gemini t2). Resolution: the audit follows the reasoning over the structured field.

Both defects independently exist in published prior rounds and are documented as known limitations of LLM-as-judge methodology, not specific to this experiment.
