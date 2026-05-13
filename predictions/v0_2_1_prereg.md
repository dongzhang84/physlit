# Pre-Registered Predictions for PhysLit v0.2.1

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `8806fc5eae01ae2c3f2acf1d9dccdfcfbc62a2ca`
- Locked at git tag: `prereg-v0.2.1-locked`
- Lock timestamp (UTC): `2026-05-13T18:47:27Z`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `6aa14ba4ae6ff84f8a0d8e7c65141b2401516af6f593cb8c07b5c4a329a132ed`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST NOT
> be modified.** Any revision requires a new version (`v0.2.2`,
> `v0.2.3`, …) with its own tag and an explicit "deviation from prereg"
> notice published alongside any results.
>
> The v0.2 prereg envelope (`predictions/v0_2_prereg.md`,
> `prereg-v0.2-locked`) is **not modified** by this version. v0.2.1
> reuses the v0.2 frozen artifacts (criteria + prompts) byte-for-byte
> and overrides only the resolver-agent model identifier, per the
> deviation notice in §0 below.
>
> Retrieve v0.2.1-frozen content post-lock with:
> `git show prereg-v0.2.1-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## 0. Deviation from prereg v0.2

**Why this version exists.** v0.2 was locked at 2026-05-13 08:13 UTC.
Between then and the first attempt to dispatch resolver-agent calls
(2026-05-13 08:27 UTC), Google's `gemini-3.1-pro-preview` endpoint
entered a sustained high-demand throttle. Three consecutive retry
attempts spaced ~1 hour apart (09:19, 10:38, ~11:32 PDT) all returned
`503 UNAVAILABLE: This model is currently experiencing high demand`.
A 4-model probe on 2026-05-13 18:32 UTC confirmed
`gemini-3.1-pro-preview` specifically times out
(`504 DEADLINE_EXCEEDED` at the SDK layer), while
`gemini-2.5-pro` and `gemini-2.5-flash` — both generally-available
in the same vendor family — return normally.

**Single change relative to v0.2.** The resolver-agent model
identifier is revised from `gemini-3.1-pro-preview` (preview-tier)
to **`gemini-2.5-pro` (generally-available, one generation behind)**.
All other v0.2 decisions are preserved unchanged: structural-judge
models (Claude Opus 4.7 + GPT-5.5), single combined structural
verdict per trial, Stage 1+2 concatenated input, composite verdict
by AND of the two axes, V1 and V2 prediction thresholds.

**Why GA over preview.** The v0.1 prereg already disclosed
"preview-weight drift" as a methodology risk; v0.2 inherited that
risk. The persistent `503 UNAVAILABLE` upgraded the risk from
*hypothetical weight drift* to *concrete capacity unavailability*.
Pinning a GA model removes both: GA models do not silently swap
weights, and Google's capacity guarantees for GA endpoints are
materially stronger than for preview endpoints.

**Capability impact.** Gemini 2.5 Pro is one generation behind 3.1
Pro. For the resolver task — read two judges' verdicts plus the
relevant criteria file, return PASS/FAIL with a written rationale —
capability headroom is ample at the 2.5 tier; this is not a
frontier-reasoning task. The substantive risk is judgement
calibration, which the V1 prediction (Agent 1 vs human-audit
agreement ≥ 12 of 17) directly measures. V1 remains the published
validation; if Agent 1 fails V1 under `gemini-2.5-pro`, that is
itself a publishable methodology finding (not a license to retry
with a different model).

**Same-vendor disclosure refinement.** v0.2 disclosed that
`gemini-3.1-pro-preview` was the v0.1 *tested* model on 5 of 17
content disagree cases (same model judging same model on a known
subset). Under v0.2.1 the resolver model is `gemini-2.5-pro` — the
same *vendor* (Google) but a different *model generation* from the
v0.1 tested Gemini. The same-vendor concern is therefore weaker
(vendor-wide bias must span generations to leak in); the v0.2 V1
same-vendor cross-check is retained as a precaution and will be
reported.

**Frozen artifacts unchanged.** The criteria and prompt files listed
in §6 below are inherited byte-for-byte from `prereg-v0.2-locked`.
No structural-criteria revision, no prompt revision. Only the
resolver-agent model identifier changes, plus its associated price
estimator constants in `src/physlit/v0_2/gemini_agent.py`.

## Scope (PhysLit v0.2.1)

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
  Agent 2 (structural axis) are Google **Gemini 2.5 Pro**, pinned to
  **`gemini-2.5-pro`** — generally-available, verified responsive on
  2026-05-13 18:32 UTC during the v0.2.1 model-availability probe.
  Each agent receives the disagree case's response text, both judges'
  verdicts and reasoning verbatim, and the relevant criteria file.
  The agent emits PASS/FAIL plus a written rationale.

  **Why not GPT-5.5 as resolver.** Using GPT-5.5 in the resolver role
  would put OpenAI in three of the six LLM seats in the v0.2.1
  pipeline (content judge + structural judge + resolver), against two
  each for Anthropic and Google. Same-vendor judge+resolver compounds
  any OpenAI-specific systematic bias: the vendor whose model produced
  one of the conflicting judgments would also be the vendor
  adjudicating the conflict, and that bias is not observable from the
  pipeline output (the resolver effectively agrees with itself across
  roles, so cross-vendor cross-checks fail silently). Gemini-as-resolver
  carries a different risk — same-vendor-with-tested-model on the 5 of
  17 content disagree cases where a Gemini model was the v0.1 tested
  model — but that risk is bounded (small known subset), visible
  (subset identity known before running), and analyzable (the V1
  scoring step below requires a separately-tabulated same-vendor vs
  cross-vendor cross-check). The same-vendor judge+resolver risk has
  no equivalent mitigation.

  **Same-vendor judging disclosure (refined).** The v0.1 tested Gemini
  was `gemini-3.1-pro-preview`; under v0.2.1 the resolver is
  `gemini-2.5-pro` — same *vendor* (Google) but a different *model
  generation*. Five of the 17 content disagree cases have a Gemini
  model on both sides (tested model and resolver). The same-vendor
  concern under v0.2.1 is therefore weaker than under v0.2 (vendor-
  wide bias must span model generations to leak in); v0.2.1 will
  nonetheless publish a same-vendor vs cross-vendor cross-check of
  Agent 1 verdicts in the V1 findings.

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
| Agent 1 (content resolver) | Google | `gemini-2.5-pro` |
| Agent 2 (structural resolver) | Google | `gemini-2.5-pro` |

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
