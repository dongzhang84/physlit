# Pre-Registered Predictions for PhysLit v0.2

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `3e42ff1ecc78e51cf4d60c7783da64211595cf40`
- Locked at git tag: `prereg-v0.2-locked`
- Lock timestamp (UTC): `2026-05-13T08:13:30Z`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `e6682e02e9805ece4f611dfd060754a889d56a8fc6c9b3ab012bd4a1f7d69f5a`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST NOT
> be modified.** Any revision requires a new version (`v0.2.1`,
> `v0.2.2`, …) with its own tag and an explicit "deviation from prereg"
> notice published alongside any results.
>
> The artifact files referenced below (structural criteria + the new
> v0.2 prompt files) are likewise frozen at the locked commit. Retrieve
> any of them post-lock with:
> `git show prereg-v0.2-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## Scope (PhysLit v0.2)

PhysLit v0.2 is an **additive analysis layer** on top of the v0.1
Aristotelian dataset. It introduces two methodological elements that
were not part of v0.1:

1. A **structural-judging axis** (criteria N9-N12: parsimony,
   independence, traceability, hierarchy) operating in parallel with
   the v0.1 content axis (criteria N1-N8). The two axes are combined
   into a per-trial composite verdict.
2. Two **disagree-resolver agents** that replace the v0.1 human-audit
   pathway: one for the content axis (Agent 1) and one for the
   structural axis (Agent 2). Their agreement with the v0.1 human-audit
   verdicts on the 17 content disagree cases is the central
   methodology measurement of v0.2.

v0.2 does **not** rerun any v0.1 production trial. It does **not**
modify any v0.1 verdict. It does **not** test any framework beyond
Aristotelian Mechanics.

**Reused v0.1 artifacts (read-only):**

- 60 v0.1 production trial responses across the three tested models
  (Claude Opus 4.7, GPT-5.5, Gemini 3.1 Pro) and four stages
- 360 v0.1 content-judge verdicts (Stages 1-3 × 2 judges)
- 22 v0.1 human-audit verdicts on dual-judge DISAGREE cases (5 Stage 1
  + 7 Stage 2 + 5 Stage 3 + 5 Stage 4 over-claim)

**New protocol additions (committed in this prereg):**

- **Structural judges.** The same two vendors used as v0.1 content
  judges, each given a new structural prompt:
  - Anthropic Claude Opus 4.7 — pinned to `claude-opus-4-7`
  - OpenAI GPT-5.5 — pinned to `gpt-5.5-2026-04-23`

  Each structural judge sees the trial's Stage 1 (induction) and
  Stage 2 (formulation) responses concatenated, plus the structural
  criteria committed at this prereg lock
  (`frameworks/01_aristotelian/structural_criteria.md`). Stage 3
  (prediction) is **not** part of the structural-judge input — the
  rule set being audited lives in Stages 1+2 only.

  Each structural judge emits **one PASS/FAIL verdict per trial**,
  not per criterion. Evidence quotes are required for every FAIL.

- **Disagree-resolver agents.** Both Agent 1 (content axis) and
  Agent 2 (structural axis) are Google Gemini 3.1 Pro, pinned to
  `gemini-3.1-pro-preview` — the same identifier verified in v0.1's
  Phase 1.5 dry-run paper trail. Each agent receives the disagree
  case's response text, both judges' verdicts and reasoning verbatim,
  and the relevant criteria file. The agent emits PASS/FAIL plus
  a written rationale.

  **Why not GPT-5.5 as resolver.** Using GPT-5.5 in the resolver role
  would put OpenAI in three of the six LLM seats in the v0.2 pipeline
  (content judge + structural judge + resolver), against two each for
  Anthropic and Google. Same-vendor judge+resolver compounds any
  OpenAI-specific systematic bias: the vendor whose model produced
  one of the conflicting judgments would also be the vendor
  adjudicating the conflict, and that bias is not observable from the
  pipeline output (the resolver effectively agrees with itself across
  roles, so cross-vendor cross-checks fail silently). Gemini-as-resolver
  carries a different risk — same-vendor-with-tested-model on the 5 of
  17 content disagree cases where Gemini was the v0.1 tested model —
  but that risk is bounded (small known subset), visible (subset
  identity known before running), and analyzable (the V1 scoring step
  below requires a separately-tabulated same-vendor vs cross-vendor
  cross-check). The same-vendor judge+resolver risk has no equivalent
  mitigation.

  **Same-vendor judging disclosure.** Gemini 3.1 Pro was the v0.1
  *tested* model for 5 of the 17 content disagree cases (and an
  unknown number of structural disagree cases, which will be reported
  post-run). For those cases, the resolver is the same vendor as the
  tested model. v0.2 will publish those cases as a separately tabulated
  subset; if Agent 1 / Agent 2 verdicts on the same-vendor subset
  systematically differ from those on the cross-vendor subset, this
  will be flagged in the v0.2 findings as a methodology caveat.

- **Composite verdict aggregation.** Each v0.1 trial receives a
  per-axis verdict (content PASS/FAIL, structural PASS/FAIL) and a
  composite verdict computed as:

  ```
  composite_PASS  =  content_PASS  AND  structural_PASS
  composite_FAIL  =  content_FAIL  OR   structural_FAIL
  ```

  Stage 4 (meta over-claim) is **out of scope** for v0.2 and is not
  re-processed; v0.1 Stage 4 verdicts are inherited verbatim.

**Pinned models, summary:**

| Role | Vendor | Pinned ID |
| --- | --- | --- |
| Content judge A | Anthropic | `claude-opus-4-7` |
| Content judge B | OpenAI | `gpt-5.5-2026-04-23` |
| Structural judge A | Anthropic | `claude-opus-4-7` |
| Structural judge B | OpenAI | `gpt-5.5-2026-04-23` |
| Agent 1 (content resolver) | Google | `gemini-3.1-pro-preview` |
| Agent 2 (structural resolver) | Google | `gemini-3.1-pro-preview` |

Runner enforces strict equality between the request's model field and
the response's identity field on every call. Identity-drift behaviour
follows the v0.1 R1 requirements (per-call capture + post-trial-set
re-ping) committed in `docs/v0_1_runner_requirements.md`.

**Sampling.** Default sampling for all three vendors (Anthropic Opus
4.7 still rejects the `temperature` parameter as of lock time; the
v0.1 convention of "default sampling, no temperature override"
carries forward).

**Predictions in scope of this lock:** V1 (Agent 1 calibration) and V2
(structural axis adds detection). v0.2 does not relock v0.1's P1 / P3
predictions — those remain verdicts of the v0.1 prereg envelope.

**Out of scope of v0.2, by explicit decision:**

- New production trials (v0.2 reuses v0.1 trials verbatim)
- New frameworks (Aristotelian only; multi-framework expansion deferred
  to v0.3+)
- Stage 4 (meta over-claim) re-processing
- Temperature variation
- Per-criterion (N9 / N10 / N11 / N12 separately) structural verdicts —
  the structural judge emits one combined verdict per trial
- Per-stage structural verdicts — the structural judge sees Stage 1+2
  combined and emits one verdict for that combined input

## V1 — Agent 1 calibration against the v0.1 human audit

**Prediction.** Agent 1, run on the 17 content-axis disagree cases
that v0.1's human audit resolved (5 Stage 1 + 7 Stage 2 + 5 Stage 3),
will produce verdicts that agree with the human-audit verdict in at
least **12 of 17 cases (≈ 70 %)**.

**Rationale.** v0.1's two LLM judges agreed on ~ 63 % of all
classifications (IRR 36.67 %); Agent 1, given both judges' reasoning
plus the criteria, has strictly more information than either judge
alone. If its verdicts on disagree cases do not exceed the
two-judges-blind agreement rate, the resolver design is not adding
value over a single fresh judge.

**Scoring.**

- **Confirmed:** Agent 1 agrees with the v0.1 human audit on ≥ 12 of
  17 cases.
- **Partially confirmed:** agreement on 9-11 of 17 cases (≈ 53-65 %).
- **Refuted:** agreement on ≤ 8 of 17 cases.

A subset breakdown will be published alongside the headline rate:
agreement on the 5 cases where Gemini was the tested model (the
same-vendor subset) will be reported separately from the 12
cross-vendor cases.

## V2 — Structural axis adds detection over content-only

**Prediction.** When the v0.2 composite verdict is computed across all
60 v0.1 trials, at least **2** of the 5 trials that received
all-stages-PASS in v0.1's content axis (Claude trial 1, GPT-5.5 trials
0, 2, 4, Gemini trial 2) will be reclassified as composite **FAIL**
under v0.2, with the failure attributable to the structural axis.

**Rationale.** v0.1's audit identified GPT trial 3 Stage 2 as the
canonical structural-fail case (17 redundant rules, fabricated
mechanism "road and air rob motion" not anchored to any observation).
GPT trial 3 already fails the v0.1 content axis, so V2 cannot be
"discovered" via that trial — it requires the structural axis to find
cases the content axis missed, i.e., cases that were content-PASS in
v0.1. The 5 content-PASS trials are the only candidates; predicting at
least 2 of them flip is a non-trivial claim that the new axis carries
real detection signal.

**Scoring.**

- **Confirmed:** ≥ 2 of the 5 v0.1 all-content-PASS trials are
  reclassified to composite FAIL, with both structural judges agreeing
  on the FAIL OR with Agent 2 resolving the disagree case to FAIL.
- **Partially confirmed:** exactly 1 of the 5 flips to composite FAIL.
- **Refuted:** none of the 5 v0.1 all-content-PASS trials flips; the
  structural axis adds no new failure detection beyond the content
  axis.

## Scoring procedure (V1 and V2)

1. Agent 1 is dispatched on the 17 content disagree cases using the
   prompt frozen at the locked commit
   (`prompts/agent1_content_resolver.md`). Each run is a fresh API
   client with a new session UUID, no cross-call state.
2. Structural judges (Anthropic + OpenAI) are dispatched on each of
   the 60 v0.1 trials. Each judge receives the trial's Stage 1
   response concatenated with the Stage 2 response, plus the criteria
   from `frameworks/01_aristotelian/structural_criteria.md` and the
   prompt frozen at the locked commit (`prompts/judge_structural.md`).
   Per-trial classification = both structural judges agree.
3. Agent 2 is dispatched on each structural-axis disagree case using
   the prompt frozen at the locked commit
   (`prompts/agent2_structural_resolver.md`). Same fresh-client,
   no-state contract as Agent 1.
4. Composite verdict per trial is computed deterministically per the
   AND rule above.
5. V1 verdict computed from Agent 1 vs human-audit comparison.
6. V2 verdict computed from the composite verdict shift over the 5
   v0.1 content-PASS trials.
7. The v0.2 findings document (`analysis/v0_2_findings.md`) records:
   - per-axis verdicts for all 60 trials
   - composite verdicts for all 60 trials
   - the v0.1 → v0.2 verdict diff
   - Agent 1 agreement rate with human audit, with the
     same-vendor subset broken out
   - structural-axis IRR (dual-judge disagreement rate)
   - V1 and V2 verdicts
   - any deviation from this prereg, with timestamps and rationale.

## Frozen artifacts (referenced by the `prereg-v0.2-locked` tag)

The following files contribute substantive content to the v0.2
protocol and the scoring criteria. At the locked commit, their
contents are part of the v0.2 prereg envelope:

- `frameworks/01_aristotelian/structural_criteria.md` — N9-N12 spec,
  judge-facing
- `prompts/judge_structural.md` — system prompt shared by both
  structural judges (Anthropic + OpenAI)
- `prompts/agent1_content_resolver.md` — system prompt for Agent 1
- `prompts/agent2_structural_resolver.md` — system prompt for Agent 2

The v0.1 prereg envelope (observations, ideal_induction,
pass_fail_criteria, prediction_tests, the four `prompts/stage*.md`
templates, and the four `prompts/judge_*.md` templates) is **not**
modified by v0.2 and remains pinned at `prereg-v0.1-locked`. v0.2
reads it; v0.2 does not write it.

If any of the v0.2-new files needs revision after lock, the project
must issue a new prereg version (e.g. `prereg-v0.2.1-locked`) with the
revised files and an explicit *deviation from prereg* notice
accompanying any v0.2 results that have already been published under
the original lock.

## Publication policy

PhysLit commits to publishing the **complete v0.2 output set** — the
structural-judge verdicts for all 60 trials, Agent 1 verdicts for all
17 content disagree cases, Agent 2 verdicts for every
structural-axis disagree case — under the same commit that publishes
the v0.2 findings. Selective publication is forbidden by `CLAUDE.md`.
The structural-axis IRR is published as a methodology-quality
indicator alongside the v0.1 content-axis IRR (36.67 %).

The author commits to publishing the V1 and V2 verdicts **regardless
of direction**. A refutation of V1 (Agent 1 disagrees with the human
audit on most of the 17 cases) is as publishable a result as
confirmation — it is direct evidence that LLM-as-resolver does not
straightforwardly replace human audit. A refutation of V2 (the
structural axis adds no new failure detection) is similarly publishable
— it would be evidence that the content-axis criteria alone capture
most physics-literacy failures on this framework.

The v0.1 verdicts (P1 confirmed, P3 confirmed) are **not modified** by
v0.2 publication. v0.2 is reported as a methodology extension and as a
new finding layer on the same Aristotelian dataset, not as a revision
of v0.1.
