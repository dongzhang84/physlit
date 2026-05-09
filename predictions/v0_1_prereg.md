# Pre-Registered Predictions for PhysLit v0.1

**Lock metadata** (auto-populated by `scripts/lock_prereg.py` — values
below show `<PENDING>` until the lock script runs):

- Locked at git commit: `<PENDING — set by lock script>`
- Locked at git tag: `<PENDING — set by lock script>`
- Lock timestamp (UTC): `<PENDING — set by lock script>`
- SHA-256 of canonical content (everything below the LOCK BOUNDARY line): `<PENDING — set by lock script>`

> Once locked, **the canonical content below the LOCK BOUNDARY MUST NOT
> be modified.** Any revision requires a new version (`v0.1.1`,
> `v0.1.2`, …) with its own tag and an explicit "deviation from prereg"
> notice published alongside any results.
>
> The artifact files referenced below (observations, ideal_induction,
> pass_fail_criteria, prediction_tests, meta_questions, and the four
> `prompts/stage*.md` templates) are likewise frozen at the locked
> commit. Retrieve any of them post-lock with:
> `git show prereg-v0.1-locked:<path>`.

<!-- LOCK BOUNDARY — do not edit anything below this line -->

## Scope (PhysLit v0.1)

PhysLit v0.1 is a budget-bounded probe of physics literacy on a
**single framework**: Aristotelian Mechanics (Category A, Tier 3
manual). This prereg locks the predictions, the experimental protocol,
and the scoring criteria **before any production model run**.

**Tested models.** Three frontier models, each pinned to a specific
version string. Version strings were verified against the live APIs
on 2026-05-09 ahead of this lock; the runner enforces a strict equality
check between the request's `model` field and the response's identity
field on every call.

- **Anthropic Claude Opus 4.7** — `claude-opus-4-7`. Anthropic has not
  yet published a date-stamped 4.7 variant, so the bare alias *is* the
  most-specific identifier the API exposes at lock time. Runner
  verifies `response.model == "claude-opus-4-7"` per call.

- **OpenAI GPT-5.5** — `gpt-5.5-2026-04-23`. This is the date-stamped
  GPT-5.5 main variant at standard-flagship tier. The pro tier
  (`gpt-5.5-pro-2026-04-23`) was rejected because the v0.1 budget cap
  of $50 USD does not accommodate the ~3–5× higher token price; v0.1
  therefore compares standard-flagship reasoning models across vendors
  and defers pro-tier comparison to v0.2. Runner verifies
  `response.model == "gpt-5.5-2026-04-23"` per call.

- **Google Gemini 3.1 Pro** — `gemini-3.1-pro-preview`. **Specific ID,
  not the family alias** `gemini-3-pro-preview`. See the preview-status
  caveat immediately below for both the alias-drift rationale and the
  preview-weight-drift handling. Runner verifies
  `response.model_version == "gemini-3.1-pro-preview"` per call.

**Preview-status caveat (Gemini 3.1 Pro Preview).** Google has not
promoted any Gemini 3 Pro model out of preview status as of lock
time; `gemini-3.1-pro-preview` is the most-stable identifier
available. The family alias `gemini-3-pro-preview` was rejected after
the 2026-05-09 discovery ping found it auto-resolving at request
time to `gemini-3.1-pro-preview`. Pinning the specific ID eliminates
alias-resolution drift as a source of methodology noise (see
`analysis/dryrun_findings.md` §8 for the discovery's paper trail).
Preview-weight drift, however, remains possible — Google does not
guarantee weight stability for preview models, and the underlying
model behind `gemini-3.1-pro-preview` could change without notice.
The v0.1 production runner is required to monitor and disclose any
such drift per the requirements documented in
`docs/v0_1_runner_requirements.md` (R1, two parts: per-call identity
capture with mid-run halt-on-drift, and post-trial-set re-ping with
disclosure in `analysis/v0_1_findings.md`). Should any drift be
detected during the v0.1 trial period, results will be reported as a
methodology deviation per the publication policy.

**Protocol per `(model × stage)`:**

- N = 5 trials per stage; each trial creates a fresh API client and a
  new session UUID (no multi-turn or context reuse across stages)
- Default sampling — the originally-drafted `temperature=0` headline
  plus `temperature=0.7` secondary pass was retired on 2026-05-08
  after Anthropic Opus 4.7 was found to reject the `temperature`
  parameter; see `docs/product-spec.md` §4.5 for the methodology
  footnote
- Four sequential stages: induction → formulation → prediction → meta,
  each in its own fresh session
- Dual-judge inter-rater reliability: Claude Opus 4.7 + GPT-5 score
  every Stage 1–3 response independently using the criteria committed
  in `frameworks/01_aristotelian/pass_fail_criteria.md` and
  `frameworks/01_aristotelian/ideal_induction.md` at the locked commit;
  judge disagreement rate is published per framework as a
  methodology-quality indicator. Disagreement > 25 % triggers human
  audit before result publication.

**Predictions in scope of this lock:** P1 and P3 only. P2, P4, and P5
require multi-framework testing and remain in `docs/product-spec.md`
§3.3 for a future v0.2 prereg lock if v0.2 is undertaken.

**Out of scope of v0.1, by explicit decision:**

- Frameworks beyond Aristotelian Mechanics
- The originally-drafted `temperature=0.7` secondary pass
- Open-weight models (DeepSeek, Llama)
- Reasoning-optimised model variants

## P1 — Induction failure under training-data conflict

**Prediction.** At least one of the three frontier models tested in
v0.1 will, in **3 or more of its 5 trials** on the Aristotelian
Mechanics framework, introduce real-physics concepts not derivable
from the given observations alone. Specifically, the Stage 1
(Induction) response will use one or more terms from the banned list
in `frameworks/01_aristotelian/ideal_induction.md` §3 — including but
not limited to *force* (as a defined quantity), *mass* (as distinct
from weight), *acceleration*, *momentum*, *inertia*, *energy*,
*gravity*, *friction*, or *vacuum* — judged under the lean checklist
in §6 of that file. Naming a banned concept *only to deny it* still
counts under §3.

**Scoring.**

- **Confirmed:** at least one of `{Claude, GPT-5, Gemini}` produces a
  Stage 1 response that fails the §3 banned-concepts check in 3 or
  more of its 5 trials, with both LLM judges agreeing on the failure
  in each of those trials.
- **Partially confirmed:** at least one model fails the
  banned-concept check in 1 or 2 of 5 trials, OR exactly 3 trials
  fail under one judge while the other judge agrees with that judge's
  failure verdict on 2 or fewer of those 3 trials (i.e., the
  dual-judge agreement requirement is met for ≤ 2 trials).
- **Refuted:** every model passes the §3 banned-concept check in 4 or
  5 of its 5 trials, with both judges in agreement.

**Phase 1.5 dry-run signal (informational, not v0.1 data).** In a
single Aristotelian induction trial against Claude Opus 4.7 on
2026-05-08 (`results/_dryrun/20260508T083204Z/`), the response used
no §3-banned concepts. This single data point does not pre-empt the
prereg evaluation; it is recorded here for transparency about what
was known at lock time. The author elected to leave P1 unchanged
rather than weaken it in light of one favourable data point —
"prereg means prereg."

## P3 — Meta-cognitive miscalibration

**Prediction.** Among v0.1 trials whose Stage 1, 2, or 3 contains at
least one identifiable failure (banned-concept use, cross-stage
drift, or Stage 3 prediction not derivable from the model's own
Stage 2 rules), **at least 30 %** will exhibit *meta-cognitive
over-claiming*: in the Stage 4 self-assessment, the model fails to
identify the failure when answering Q1, Q2, or Q3, or rates standard
physics influence as ≤ "minor" in Q5 despite the failure being
present.

**Scoring.**

- **Confirmed:** ≥ 30 % over-claiming rate (numerator: trials with a
  Stage 1–3 failure that is not flagged in Stage 4; denominator:
  trials with at least one Stage 1–3 failure), with both judges
  agreeing on the over-claim classification.
- **Partially confirmed:** 15 %–30 % over-claiming, OR ≥ 30 % under
  one judge but only ≥ 15 % under the other.
- **Refuted:** < 15 % over-claiming.
- **Vacuous (untestable at v0.1 scope):** if zero trials contain any
  Stage 1–3 failure, the denominator is empty and P3 cannot be
  evaluated. This outcome is reported as "vacuous" alongside the P1
  result rather than confirmed/refuted; it would itself be evidence
  that frontier models on Aristotelian are stronger than the prereg
  expected.

**Phase 1.5 dry-run signal (informational, not v0.1 data).** The
Aristotelian dry-run trial recorded at
`results/_dryrun/20260508T083204Z/01_aristotelian/` contained no
Stage 1–3 failures — Claude self-rated standard-physics influence as
"minor", which an independent reader of the same trial would broadly
agree with (Stage 4 explicitly identified two borrowed concepts:
*impressed motion* and the *earthy / fiery* category labels). On
this single trial, calibration was good. Again, this is one data
point, recorded for transparency, not relied on by the prereg.

## Scoring procedure (both predictions)

1. After all v0.1 trials complete, the diagnostic-report builder
   classifies each Stage 1–3 response per the criteria committed in
   the `prereg-v0.1-locked` tag (banned-concept check, coverage map,
   near-pass patterns, scenario-specific PASS modes).
2. Both judges (Claude Opus 4.7 and GPT-5, with system-prompt
   instructions also committed at the locked commit) score
   independently.
3. Per-trial classification = both judges agree.
4. Disagreements are logged separately and published as the IRR rate;
   they do not enter the P1 / P3 numerators.
5. P1 and P3 verdicts are computed from the agreed classifications.
6. The `v0_1_findings.md` document records:
   - the per-trial classifications (with judge reasoning verbatim)
   - the IRR rate
   - the P1 and P3 verdicts (`confirmed` / `partially confirmed` /
     `refuted` / `vacuous` for P3)
   - any deviation from this prereg, with timestamps and rationale.

## Frozen artifacts (referenced by the `prereg-v0.1-locked` tag)

The following files contribute substantive content to the protocol
and the scoring criteria. At the locked commit, their contents are
part of the prereg envelope:

- `frameworks/01_aristotelian/observations.md`
- `frameworks/01_aristotelian/ideal_induction.md`
- `frameworks/01_aristotelian/pass_fail_criteria.md`
- `frameworks/01_aristotelian/prediction_tests.md`
- `prompts/stage1_induction.md`
- `prompts/stage2_formulation.md`
- `prompts/stage3_prediction.md`
- `prompts/stage4_meta.md`

If any of these files needs revision after lock, the project must
issue a new prereg version (e.g. `prereg-v0.1.1-locked`) with the
revised files and an explicit *deviation from prereg* notice
accompanying any v0.1 results that have already been published under
the original lock.

## Publication policy

PhysLit commits to publishing the **complete v0.1 trial set** —
including any responses that fail to load, fail to parse, or are
ambiguous to the judges — in `results/<model-version>/` under the
same commit that publishes the diagnostic report. Selective
publication is forbidden by `CLAUDE.md`. The judge disagreement rate
is published per framework as a methodology-quality indicator.

The author commits to publishing the verdict on each prediction
above **regardless of direction**. Refutation of P1 (Claude /
GPT-5 / Gemini all stayed inside the framework on Aristotelian) is
as publishable a result as confirmation, and arguably more
interesting.
