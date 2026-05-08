# Dry Run Findings — Phase 1.5

> **Status:** v1 — written 2026-05-08 immediately after the run.
> **Scope:** exploratory, single-trial, single-model. **Not v0.1 data.**
> **Run identifier:** `results/_dryrun/20260508T083204Z/01_aristotelian/`

## 1. What we did

Ran Claude Opus 4.7 once through the four-stage protocol on the
Aristotelian phenomenon set (12 observations), with a fresh API client
and new session UUID per stage. Total spend ≈ **$0.53** (estimated;
Anthropic invoice authoritative). Output is four `trial_0_t0.0.json`
files under the run-identifier directory above.

Pre-run gate: `ruff check`, `ruff format`, `mypy --strict`,
`pytest` (19 tests) — all green. The runner enforces the methodology
contract from `CLAUDE.md` (fresh client per call, response-model
verification).

## 2. Stage-by-stage assessment

Applied the lean `ideal_induction.md` checklist (§6) informally — one
human reviewer, no judge LLMs. **Provisional verdict:**

| Stage | Verdict | Notes |
| ----- | ------- | ----- |
| 1. Induction | **PASS** | All 8 necessary conditions (N1–N8) met. Coverage map: every observation explicitly cited under at least one rule. No banned concepts (no inertia, momentum, mass, gravity, friction, density, vacuum, F=ma). Tensions section is honest about gaps. |
| 2. Formulation | **PASS** | Each rule restated operationally. Scope, preserved-quantities, and boundary cases stated for every rule. No new concepts smuggled in beyond Stage 1. Boundary-case discipline is genuinely impressive (e.g. rule 2 explicitly says it gives "only a ranking, not a numerical relation"). |
| 3. Prediction | **PASS** on all 5 scenarios | Notably, Claude **refused to import inertia** in Scenario 2 (frictionless ice) and **refused to predict** in Scenario 4 (evacuated chamber), explicitly citing scope limits of its own Stage 2 rules. This is the strongest framework-fidelity signal we could ask for. |
| 4. Meta | **Calibrated** | Self-identified three concepts as borrowed terminology ("earthy/fiery", "impressed motion", "natural place"). Self-graded its standard-physics influence as "minor" — judgment that matches what an outside reader would assign. |
| Cross-stage | **PASS** | Stage 3 predictions all derive from Stage 2 rules; no drift. |

## 3. Provisional implication for prereg P1

P1 (induction failure under training-data conflict) predicts that "at
least one frontier model will, in at least 3 of 5 trials on a
Category A set, introduce real-physics concepts." On this single
Aristotelian trial, **Claude introduced none of the explicitly banned
concepts**, even when prompted with high-pressure scenarios designed
to elicit them.

A single trial doesn't refute P1 (P1 is across N=5 × 3 models). But
it's a calibration update: P1 may be wrong for Claude on Aristotelian.
We will not adjust P1 — pre-registration is the whole point — but we
should expect this to be the relevant headline if v0.1 confirms.

## 4. Methodology issues surfaced — must resolve before prereg lock

> **Update 2026-05-08 (post-decisions):** all seven items below are
> RESOLVED, per author decisions on the dry-run punch list. See
> per-item updates inline. The prereg-lock blockers in §7 are now
> complete; the prereg draft is at `predictions/v0_1_prereg.md`.

### 4.1 [RESOLVED] Opus 4.7 has deprecated the `temperature` parameter

The API returns 400 with `temperature is deprecated for this model`.
This breaks `product-spec.md` §4.5, which specifies `temperature=0`
headline + `temperature=0.7` secondary pass. The dry-run runner now
omits `temperature` from the request; the requested value is still
recorded on the `TrialRecord` for traceability, but the API uses its
own (undocumented) default sampling.

**Decisions needed before v0.1 prereg lock**, in order of preference:

1. Accept "Opus 4.7 default sampling" as the single sampling regime
   for v0.1, and explicitly retire the temperature=0/0.7 dual-pass
   from the prereg. (Keeps Claude 4.7 in scope.)
2. Substitute Opus 4.6 (which probably still respects `temperature`)
   for the Claude line of v0.1.
3. Drop Claude entirely from v0.1 in favour of a sampling-controlled
   model.

Current recommendation: option 1, with a methodology footnote in
`product-spec.md` §4.5.

**Resolution (2026-05-08):** option 1 chosen. `docs/product-spec.md`
§4.5 / §6.1 / §8.1 / §8.3 (and zh mirror) updated; the dual-pass is
retired for v0.1 and `TrialRecord.temperature` continues to record the
requested value for traceability. Stochasticity-sensitivity testing is
now §8.3 future-work.

### 4.2 [RESOLVED] Initial CLAUDE.md model-version pin was wrong

CLAUDE.md cited `claude-opus-4-7-20260101` as the example pinned
version. That string returns 404 on the Anthropic API today. The
correct pin is the bare alias `claude-opus-4-7` (Anthropic has not
published a date-stamped 4.7 variant yet). CLAUDE.md and
`runners/claude.py` updated as part of the dry-run commit. The
strict response-model verification still works: it matches the bare
alias against itself.

### 4.3 [RESOLVED] "Impressed motion" is a borderline N7-vs-near-pass case

`ideal_induction.md` §5 says: introducing "retained motion" as a
named quantity is FAIL "if formalized as a conserved quantity."
Claude introduced *impressed motion* (Buridan-style impetus theory),
which is medieval Aristotelian and explicitly described as fading
rather than conserved. The current criteria are ambiguous about
this case. **Recommended edit:** add an explicit clause to §5
permitting historical impetus-style accounts, since they fall within
the Aristotelian-extended framework rather than slipping into modern
momentum.

**Resolution (2026-05-08):** clause added to `ideal_induction.md` §5.
Buridan/Oresme-style impressed motion (described as fading rather
than conserved) is now explicitly PASS; "retained motion formalised
as conserved quantity" remains FAIL even if "momentum" is not named.

### 4.4 [RESOLVED] Scenario 4 (vacuum) — two valid PASS modes

The `prediction_tests.md` "Aristotelian (PASS)" column expects the
model to assert that vacuum "cannot occur in this framework." Claude
gave a different but defensible answer: "my rules underdetermine the
answer; I decline to guess." Both refuse to import standard physics,
which is the diagnostic test. **Recommended edit:**
`pass_fail_criteria.md` Stage 3 should treat both responses as PASS
(framework-fidelity refusal), not just the rejection-of-vacuum mode.

**Resolution (2026-05-08):** new "Scenario-specific notes" subsection
added to `pass_fail_criteria.md` Stage 3. Scenario 4 now has two
explicit PASS modes (reject-the-scenario / refuse-on-scope-grounds);
standard-physics answer is FAIL.

### 4.5 [RESOLVED] Scenario 3 (numerical ratio) — Claude declined to commit

Claude predicted "A reaches the bottom first, B second" without a
ratio, citing its own boundary-note that rule 2 gives "only a
ranking, not a numerical relation." `pass_fail_criteria.md` Stage 3
currently allows "qualitative direction; exact ratio not required."
This is fine, but a stricter judge might mark Claude down for
declining to give the 2:1 ratio that strict Aristotelian implies.
**Recommended decision:** keep current criterion (qualitative is
sufficient); add an explicit example to `pass_fail_criteria.md` §3
showing this case as PASS.

**Resolution (2026-05-08):** added to the new "Scenario-specific
notes" subsection of `pass_fail_criteria.md` Stage 3. Concrete dry-run
example included verbatim ("A first, B second; my rules give only a
ranking, not a numerical relation, so I cannot give a ratio" → PASS).

### 4.6 [RESOLVED] Framework-specific prompt files are unused

`frameworks/01_aristotelian/formulation_template.md` and
`meta_questions.md` were drafted to be the body of Stages 2 and 4,
but the dry-run runner uses the global `prompts/stage{2,4}_*.md`
self-contained templates instead. Two rationalisation paths:

1. Keep global templates self-contained; demote the framework-specific
   files to documentation-only.
2. Refactor: framework files own Stage 2/4 wording, global templates
   become thin wrappers with `{{framework_body}}` placeholders.

Current recommendation: option 1 for v0.1 (less code), with the
framework-specific files re-cast as "what each stage would look like
for this framework if we ever needed framework-specific overrides."

**Resolution (2026-05-08):** option 1 chosen.
`frameworks/01_aristotelian/formulation_template.md` and
`meta_questions.md` got a status frontmatter explicitly marking them
"DOCUMENTATION-ONLY for v0.1", with a pointer to the global templates
that the v0.1 protocol actually uses.

### 4.7 [RESOLVED] Stage 3 scenarios are duplicated (`prediction_tests.md` ↔ script)

The five Stage 3 scenario prompts are hand-written in
`scripts/dryrun_aristotelian.py` AND in
`frameworks/01_aristotelian/prediction_tests.md`. Drift will bite
us. Action: before v0.1 prereg lock, parse the
"**Prompt to the model.**" sections from `prediction_tests.md`
directly so there's one source of truth.

**Resolution (2026-05-08):** new module `src/physlit/scenarios.py`
parses scenarios from `prediction_tests.md` (single source of truth);
`scripts/dryrun_aristotelian.py` now uses
`load_scenarios(...) + render_scenarios_block(...)` instead of a
hardcoded constant. `tests/test_scenarios.py` enforces parity:
expected substrings present, judge columns and "Why this scenario"
commentary stripped, indices contiguous. Future edits to
`prediction_tests.md` that break the parser fail CI.

## 5. Cost calibration for v0.1

Single-trial Claude cost on Aristotelian: ≈ **$0.53** (4 stages).

For full v0.1: 3 models × 5 trials × 1 temperature × 4 stages
= 60 tested-model trials. Assuming GPT-5 and Gemini 3 are roughly
in the same ballpark as Claude (probably cheaper per token),
tested-model spend ≈ **$25–35**. Adding dual-judge (Claude + GPT
scoring 60 × 4 = 240 stage-records, ~$0.04 per judge call × 2
judges = ~$20), grand total ≈ **$45–55**.

That puts us right at or slightly above the **$50 cap** committed
in `product-spec.md` §8.1. **Recommendation:** before v0.1, run a
single GPT-5 and a single Gemini 3 trial through the same
infrastructure (Phase 1.5 extension) to calibrate per-model cost,
and revise the cap if needed.

## 6. Verbatim links to the four trial JSONs

- [Stage 1 — induction](../results/_dryrun/20260508T083204Z/01_aristotelian/induction/trial_0_t0.0.json)
- [Stage 2 — formulation](../results/_dryrun/20260508T083204Z/01_aristotelian/formulation/trial_0_t0.0.json)
- [Stage 3 — prediction](../results/_dryrun/20260508T083204Z/01_aristotelian/prediction/trial_0_t0.0.json)
- [Stage 4 — meta](../results/_dryrun/20260508T083204Z/01_aristotelian/meta/trial_0_t0.0.json)

Each file contains the verbatim prompt, the verbatim response,
the model version returned by the API, the per-trial UUID, the
UTC timestamp, and the cost estimate. They are committed
unchanged; the dry run does not pre-judge any response.

## 7. Recommended punch list before v0.1 prereg lock

> **Status (2026-05-08):** all five hard blockers below are now
> RESOLVED — see the per-section [RESOLVED] tags in §4. The prereg
> draft is at `predictions/v0_1_prereg.md`; the lock infrastructure
> is at `scripts/lock_prereg.py` and `scripts/verify_prereg_integrity.py`.

Hard blockers (must do):

1. Resolve §4.1 — pick one of the three temperature options.
2. Edit `ideal_induction.md` §5 per §4.3 (impetus-as-fading is PASS).
3. Edit `pass_fail_criteria.md` per §4.4 + §4.5 (Scenario 4 dual
   PASS modes; Scenario 3 qualitative-is-enough explicit).
4. Resolve §4.6 — framework-specific files: documentation-only or
   refactor.
5. De-duplicate Stage 3 scenarios per §4.7.

Soft items (recommended):

6. Run Phase 1.5 extensions for GPT-5 and Gemini 3 to calibrate
   cost (§5).
7. Keep this findings file under version control as the historical
   record of what changed and why between draft markdown and
   prereg-locked v1.0.
