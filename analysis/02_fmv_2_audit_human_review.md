# 02_fmv.2 Audit — Human Verdicts (Treatment Arm)

16 disagree cases audited: 10 content (IRR 22.22%) + 6 structural (IRR 40.00%).

## Part A — Content Axis (10 cases)

| Case | Trial | Stage | Human | Reason |
|------|-------|-------|-------|--------|
| C1 | Claude T1 | S2 | **FAIL** | "inert" contains inertia word root; §3 lexical |
| C2 | Claude T2 | S2 | **FAIL** | P3: track pushes upward to cancel downward pull |
| C3 | Claude T3 | S1 | **PASS** | "proportional" not in banned list; N1-N6 all covered |
| C4 | Claude T4 | S1 | **PASS** | "pull ∝ heaviness" is logical necessity from Rule 2 + obs 10; not P3 |
| C5 | GPT T4 | S1 | **PASS** | "air" not in banned list; N1-N6 all covered |
| C6 | Gemini T0 | S1 | **FAIL** | Response truncated mid-Rule 4; incomplete rule set |
| C7 | Gemini T1 | S2 | **FAIL** | P3: "solid surfaces actively provide upward push" (non-decisive) |
| C8 | Gemini T2 | S2 | **FAIL** | P3: "solid surface contributes upward push" (non-decisive) |
| C9 | Gemini T3 | S1 | **PASS** | "Unless adrift in open space" correctly distinguishes ground vs space per observations |
| C10 | Gemini T4 | S2 | **PASS** | "vacuum" not in banned list (non-decisive) |

## Part B — Structural Axis (6 cases)

| Case | Trial | Rules | Human | Reason |
|------|-------|-------|-------|--------|
| S1 | GPT T0 | 6 | **PASS** | "as in rule 2" in tension note satisfies N12 |
| S2 | GPT T1 | 6 | **PASS** | "as in rule 2" in Rule 3 satisfies N12 |
| S3 | GPT T3 | 6 | **FAIL** | N12: 6 rules, zero cross-references |
| S4 | GPT T4 | 5 | **FAIL** | N12: 5 rules, zero explicit cross-references |
| S5 | Gemini T0 | 3 | **PASS** | 3 rules < 5, N12 exempt |
| S6 | Gemini T2 | 3 | **PASS** | 3 rules < 5, N12 exempt |

## Reasoning

### C1 — "inert" (FAIL)

"Inert" shares its root with "inertia" (Latin "iners"). §3 bans "inertia (and inertial)" and specifies "or a morphological variant." Consistent with prior rulings on "massless" and "massive" (both FAIL for containing "mass"), "inert" fails the lexical test.

### C2, C7, C8 — P3 "surface pushes upward" (all FAIL)

Three trials wrote variants of: "the track/ground/solid surface provides an upward push that perfectly cancels the downward pull." P3 bans "positing an opposing agent that balances or cancels the push." No observation says the ground pushes anything — obs 10 says objects "strike the ground." The model could simply treat "object on ground = stationary" as a brute fact without inventing the ground-push mechanism. This is an extra mechanism not required by observations — an alternative explanation (e.g. downward pull ceases upon contact with ground) is equally valid and doesn't require fabricating a new force.

### C4 — "pull ∝ heaviness" (PASS)

If pace = effort/heaviness (Rule 2) and all objects fall at the same pace (obs 10), then effort must be proportional to heaviness. This is framework-internal logical necessity, not a hidden balancing agent. The downward pull is not "opposing" anything; it IS the primary cause of falling.

### C6 — Truncation (FAIL)

Response cut off mid-sentence at Rule 4 ("Invisible surroundings—"). Only 328 output tokens. Obs 6 and obs 12 not explicitly covered. Incomplete rule set.

### C9 — "Unless adrift in open space" (PASS)

Rule 3 correctly distinguishes two environments: ground (has pull → objects fall) and open space (no pull → objects only respond to direct pushes). All falling observations (obs 10-12) occur near the ground ("strike the ground"). Obs 6 occurs in open space and shows no falling. The model correctly induced from observations that the downward pull is location-dependent.

### S1, S2 — Cross-references present (PASS)

Both contain "with heaviness still dividing the result as in rule 2" — explicit cross-rule reference satisfying N12.

### S3, S4 — No cross-references (FAIL)

6 and 5 rules respectively, all flat. Conceptual connections exist but no explicit "Rule N" digits or hierarchy markers. Strict N12 standard consistent with all prior audits.

### S5, S6 — Small rule sets (PASS)

3 rules < 5 → N12 exempt. N9/N10/N11 all PASS.
