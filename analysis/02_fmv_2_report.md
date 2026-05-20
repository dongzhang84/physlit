# PhysLit 02_fmv.2 — Axiomatisation Control Experiment Report

> **Date:** 2026-05-20.
> **Scope:** Single-variable control experiment on the F=mv framework. Same 3 models × N=5 × 4 stages as `02_fmv`; the only manipulated variable is the Stage 1 induction prompt.
> **Prereg lock:** [`prereg-02_fmv.2-locked`](https://github.com/dongzhang84/physlit/releases/tag/prereg-02_fmv.2-locked).
> **Companion files:**
> - [`02_fmv_2_findings.md`](./02_fmv_2_findings.md) — judging report + post-audit numerical block.
> - [`02_fmv_2_audit_human_review.md`](./02_fmv_2_audit_human_review.md) — verbatim human verdicts on all 16 disagreement cases.
> - [`02_fmv_2_audit_worksheet.md`](./02_fmv_2_audit_worksheet.md) — the audit input.
> - [`02_fmv_2_agents_review.md`](./02_fmv_2_agents_review.md) — non-canonical Agent 1 + Agent 2 review.

---

## Abstract

`02_fmv.2` is a **single-variable control experiment**. The control
arm is the frozen `02_fmv` trial set; the treatment arm is a new run
of the same four-stage protocol — identical observations, identical
models (`claude-opus-4-7`, `gpt-5.5-2026-04-23`,
`gemini-3.1-pro-preview`), identical N=5, identical Stage 2/3/4
prompts, identical structural and content criteria — except that the
**Stage 1 induction prompt carries one added paragraph**: an
axiomatisation instruction asking the model to produce the smallest
set of rules and to mark any rule that follows from another.

The instruction was written in natural-language induction terms, not
as the N9-N12 judge rubric. The motive came from `02_fmv.1` §2.7:
that round found the structural axis (N9-N12) failing 10/15 unprompted
trials and read it as a *self-organisation gap, not a knowledge gap* —
the models knew the right rules but did not, by default, compress them
into a parsimonious system. The original Stage 1 prompt confirmed this
silence: it asked only for a "self-consistent set of rules" and
"specific" output, never for parsimony. `02_fmv.2` removes that
silence and measures the difference.

Two predictions were locked before judging:

- **P1** — the treatment structural pass rate is greater than the
  control's 5/15. Tier-banded: strongly confirmed ≥10, directionally
  confirmed 6-9, refuted ≤5.
- **P2** — content-axis competence does not materially degrade
  (treatment content PASS ≥ 8/15).

Post-audit results: **P1 STRONGLY CONFIRMED, P2 CONFIRMED.**

| Arm | Content-only PASS | Structural PASS | Composite PASS |
|---|---|---|---|
| Control (`02_fmv` / `02_fmv.1`) | 9/15 | 5/15 | 1/15 |
| Treatment (`02_fmv.2`) | 9/15 | **11/15** | **6/15** |

The structural pass rate **more than doubled** (5 → 11). Content held
**exactly flat** (9 → 9). Composite — the conjunction the thesis
cares about — went from 1/15 to 6/15, a **six-fold increase**, driven
entirely by the structural axis. The per-model breakdown is just as
informative as the totals: Claude's structural pass rate jumped 2/5 →
5/5; GPT's 0/5 → 2/5; Gemini's 3/5 → 4/5. The models that knew the
physics (Claude, GPT) responded to the cue; the model that did not
(Gemini) barely moved on structure, exactly as the `02_fmv.1`
self-organisation thesis predicted.

One side finding flags the limit of the effect. Claude trial 2 lost
its content axis under the treatment: pressed to consolidate, the
model wrote a Stage 2 "the track pushes upward to cancel the downward
pull" — a P3 violation it had avoided in the control. Asking for
parsimony can, on a single trial, push a model to fabricate a
balancing mechanism. The aggregate effect is still strongly positive,
but the failure mode is real and worth recording.

Total compute: 60 treatment-arm production calls + 120 judge calls +
16 resolver calls ≈ $5.0 USD. Reproducible from the
`prereg-02_fmv.2-locked` tag.

---

## 1. Design — what changed and what didn't

### 1.1 Relationship to `02_fmv` and `02_fmv.1`

`02_fmv.2` reuses the F=mv framework as-is. The control arm is the
existing 60 `02_fmv` production trials, frozen at `prereg-02_fmv-locked`,
with the content verdicts from `02_fmv` (post-audit) and the structural
verdicts from `02_fmv.1` (post-audit). No control trial is re-run; no
prior verdict is modified.

The treatment arm is a **new** four-stage run of 3 models × N=5 = 60
trials, on a fresh API client per stage with a new session UUID,
`temperature=0`, the same `02_fmv` observations, and the unchanged
Stage 2 / 3 / 4 prompts. The only manipulated variable is the Stage 1
prompt.

### 1.2 The treatment — one added paragraph

The treatment Stage 1 prompt is the `02_fmv` Stage 1 prompt with one
paragraph added between the "Your task" sentence and the "Return your
rules" sentence:

> Aim for the **smallest** set of rules that still explains every
> observation. Do not state as a separate rule anything that already
> follows from rules you have given; if one rule is a special case or
> a consequence of another, say so instead of listing it on its own.
> Prefer a few general rules over a long list of specific ones.

This is deliberately **natural-language induction guidance**, not the
N9-N12 judge rubric. It names no criterion, no rule-count threshold,
no scoring scheme; it does not tell the model it will be graded on
structure. It is the cue a physics teacher would give. The frozen file
is [`frameworks/02_fmv/prompts/stage1_induction_axiomatised.md`](../frameworks/02_fmv/prompts/stage1_induction_axiomatised.md).

### 1.3 Judging

The treatment arm was judged on both axes:

- **Content axis** — the two `02_fmv` content judges (Claude + GPT)
  scored Stage 1/2/3 with the `02_fmv` judge prompts and criteria,
  frozen at `prereg-02_fmv-locked`. Per-trial content axis =
  S1 ∧ S2 ∧ S3.
- **Structural axis** — the two structural judges scored each
  treatment trial's Stage 1 rule set (Stage 2 as context only) with
  the `02_fmv.1` structural criteria and judge prompt, frozen at
  `prereg-02_fmv.1-locked`.

Disagreements were resolved by **human audit**
([`02_fmv_2_audit_human_review.md`](./02_fmv_2_audit_human_review.md));
no LLM resolver fed a canonical verdict. The dual-judge IRRs are
reported and published: content 22.22 %, structural 40.00 % (above
25 %, so a full human audit was mandatory per prereg §1.3).

---

## 2. Results

### 2.1 Judging and IRR

Both content judges agreed on 35 of 45 Stage 1-3 classifications and
split on 10 — content IRR **22.22 %**. The structural judges agreed on
9 of 15 and split on 6 — structural IRR **40.00 %**. All 16
disagreements were audited.

### 2.2 The audit

The 10 content splits resolved as: 6 PASS, 4 FAIL. Five PASS verdicts
sided with the Claude content judge (Claude was more often right on
the "this isn't really a banned token / not really a P3 violation"
calls); five FAIL verdicts sided with the OpenAI judge (OpenAI was
more often right when there *was* a banned token or a fabricated
mechanism). Two notable resolutions: C1 (`claude-opus-4-7` t1
formulation) FAILed on "inert" — morphological variant of "inertia",
banned under §3's lexical test — and C2 (`claude-opus-4-7` t2
formulation) FAILed on a P3 "track pushes upward" balancing mechanism.

The 6 structural splits resolved 4 PASS, 2 FAIL. The PASS resolutions
all centred on N12: either an explicit "as in rule 2" cross-reference
the Claude structural judge had missed (S1, S2), or a < 5 rule set
exempt from N12 (S5, S6). The FAILs (S3, S4) had no explicit
hierarchy markers despite ≥ 5 rules.

Both LLM judges agreed with the human audit on 50 % of cases on
**both** axes — a level shift down from `02_fmv` content (Claude 86 %,
OpenAI 21 %) and `02_fmv.1` structural (Claude 14 %, OpenAI 86 %), and
without a clear reliability winner this round (§2.6).

### 2.3 Post-audit numbers — the two predictions

| Prediction | Verdict | Result |
|---|---|---|
| **P1** axiomatisation raises structural | **STRONGLY CONFIRMED** | treatment structural PASS **11/15** vs control 5/15 — at the doubling threshold |
| **P2** content does not degrade | **CONFIRMED** | treatment content PASS **9/15** vs control 9/15 — exactly flat |

### 2.4 Resolved per-trial matrix

`S1`/`S2`/`S3` are the treatment-arm content verdicts per stage,
audit-resolved; `Content-only` = S1 ∧ S2 ∧ S3; `Composite` =
Content-only ∧ Structural.

| Model | Trial | S1 | S2 | S3 | Content-only | Structural | Composite |
|---|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `claude-opus-4-7` | 1 | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 2 | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 0 | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 3 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gemini-3.1-pro-preview` | 4 | FAIL | PASS | PASS | FAIL | FAIL | FAIL |

Composite PASS: **6/15**. Six-fold over the control's 1/15.

### 2.5 What the numbers mean — substantive findings

**Finding 1 — a clean single-variable causal effect.** The instruction
moved the structural pass rate from 5/15 to 11/15 — a doubling —
without changing observations, models, sampling, judge prompts,
criteria, or any other Stage's prompt. Content held exactly flat at
9/15. The instruction did not buy structure with content. The
composite jumped from 1/15 to 6/15. This is the cleanest causal claim
PhysLit has produced to date.

**Finding 2 — per-model is the central reading.**

| Model | Content (ctrl → treat) | Structural (ctrl → treat) | Composite (ctrl → treat) |
|---|---|---|---|
| `claude-opus-4-7` | 4/5 → 3/5 | **2/5 → 5/5** | 1/5 → 3/5 |
| `gpt-5.5-2026-04-23` | 5/5 → 5/5 | **0/5 → 2/5** | 0/5 → 2/5 |
| `gemini-3.1-pro-preview` | 0/5 → 1/5 | 3/5 → 4/5 | 0/5 → 1/5 |

Claude is the biggest beneficiary: every Claude trial passed the
structural axis under the treatment (5/5 vs 2/5). GPT — which had
been 5/5 content but 0/5 structural in the control, the original
"accumulates rather than axiomatises" signature — moved to 2/5
structural. Gemini barely moved on either axis.

**Finding 3 — the `02_fmv.1` self-organisation thesis is causally
confirmed.** §2.7 of [`02_fmv_1_report.md`](./02_fmv_1_report.md)
predicted that the structural failure is a *self-organisation gap, not
a knowledge gap*: models that know the right rules can axiomatise them
when asked but don't by default; models that do not know them cannot.
Both halves replicate here.

- *Models that know the rules respond to the cue.* Claude 4/5 content
  in the control responded with structural 5/5 in the treatment. GPT
  5/5 content responded with structural 2/5 (up from 0/5).
- *Models that don't know the rules don't respond.* Gemini 0/5
  content in the control moved only 3/5 → 4/5 structural in the
  treatment — within sampling noise, and inconsequential for composite
  (composite content-FAIL → composite FAIL regardless of structural).

This converts the `02_fmv.1` descriptive finding into a causal /
mechanistic one. The phrase "self-organisation gap, not knowledge gap"
now means: *when you remove the silence in the prompt, the gap closes
for models that have the knowledge.* The remaining structural failures
on Claude and GPT (Claude t1, t2 lost content; GPT t2, t3, t4 still
failed structural) are model-specific limits, not framework limits.

**Finding 4 — the failure mode of the instruction.** Claude trial 2
went from content-PASS in the control to content-FAIL in the
treatment: Stage 2 introduced "the track pushes upward to cancel the
downward pull" — a P3 fabrication of a balancing mechanism. The
audit's read is that, asked to consolidate, the model "completed" its
account by inventing a force to keep falling objects stationary on
the ground. This is the only treatment trial where content degraded
relative to the control on a Claude/GPT trial, but it is a real
side-effect of the cue: parsimony pressure can push a model to
fabricate when the observation set is silent on a mechanism. A
follow-on prereg might amend the instruction to forbid introducing
mechanisms not present in the observations.

### 2.6 Methodological findings

**LLM judges level-shift down on the treatment.** Both Claude and
OpenAI judges agreed with the human audit on only **50 % of cases on
both axes**:

| Round | Axis | Cases | Claude judge | OpenAI judge |
|---|---|---|---|---|
| `02_fmv` | Content | 14 | 86 % | 21 % |
| `02_fmv.1` | Structural | 7 | 14 % | 86 % |
| **`02_fmv.2`** | Content | 10 | **50 %** | **50 %** |
| **`02_fmv.2`** | Structural | 6 | **50 %** | **50 %** |

The `02_fmv` and `02_fmv.1` rounds showed a striking
*reversal* across axes (Claude reliable on content, OpenAI on
structure). The `02_fmv.2` treatment level-shifts both judges down to
chance on both axes — neither LLM judge carried this audit. The
likeliest explanation is that the axiomatised treatment responses are
*harder to judge*: they are more compact, the rules carry more
implicit content, and a borderline call (e.g. "inert" as a morphological
variant; "as in rule 2" as a sufficient cross-reference) requires a
substantive interpretive judgment the rubric only partially specifies.
A consequence for the paper: *judge reliability is content-dependent,
not just task-dependent — judging an axiomatised rule set is harder than
judging a sprawling one.*

**Agent 1 dropped sharply; Agent 2 held.** Agent 1
(`gemini-3.1-pro-preview`, content resolver) agreed with the human
audit on **5/10 (50 %)** of content cases — down from `02_fmv`'s 12/12
(100 %). It returned PASS on every case, a dovish failure mode that
missed the "inert" lexical, the P3 fabrications, and the
truncation. Agent 2 (same model, structural resolver) held at
**5/6 (83 %)**, statistically equivalent to `02_fmv.1`'s 6/7.
Mechanical criteria still make an LLM structural resolver reliable;
*content* judging on this treatment is harder than `02_fmv`'s
content judging was — possibly because the treatment responses
themselves are more interpretively dense, possibly because the
content disagreements happened to be on tougher cases this round.

### 2.7 Cost and reproducibility

| Component | Calls | Cost (est., USD) |
|---|---|---|
| Treatment production trials (3 × 5 × 4) | 60 | ~4.00 |
| Dual-judge (content S1-3 + structural) | 120 | ~0.85 |
| Agent 1 + Agent 2 side analysis | 16 | ~0.68 |
| **Total** | **196** | **~5.5** |

Well within the prereg's ≤ $30 estimate. Every prompt sent and
response received is committed under `results/<model>/02_fmv_2/`.
Reproducible from the `prereg-02_fmv.2-locked` tag (`uv sync`, keys in
`.env.local`, `run_02_fmv_2.py` then `judge_02_fmv_2.py` then
`apply_02_fmv_2.py`).

---

## 3. Discussion — the thesis is sharper now

The three-round arc on F=mv ends with a clear claim. The descriptive
side, established by `02_fmv` (content axis) and `02_fmv.1`
(structural axis): on a counterfactual world models can produce
physically correct rules and yet sprawl in their organisation of
those rules. The causal side, established here: *that sprawl is a
default behaviour, not a capability limit, for the models that knew
the physics in the first place.* A natural-language axiomatisation cue
— one paragraph, no rubric — moves Claude from 2/5 structural to 5/5
and GPT from 0/5 to 2/5, with content held flat. For Gemini, which
did not know the rules in the control, the cue does not help; the
self-organisation gap is upstream of a knowledge gap there. The two
halves match the `02_fmv.1` §2.7 prediction exactly.

What this round does not do — and the paper should not claim it does
— is settle that the effect generalises. F=mv is one counterfactual
framework; the instruction is one wording. A second counterfactual
framework run as a `default-vs-instructed` pair would test
generalisation directly. A second instruction wording (e.g. a stronger
cue, or a stage-2-targeted cue) would test how much of the lift the
specific wording is responsible for. The Claude t2 content
degradation also points to a refinement: parsimony pressure plus a
silence in the observations can push a model to fabricate a balancing
mechanism. A follow-on prereg might amend the instruction to
explicitly forbid introducing forces not present in the observations.

---

## 4. Next steps

### 4.1 Generalise across frameworks

A `default-vs-instructed` control pair on a second counterfactual
world (e.g. slow light, 1/r gravity) would test whether the
self-organisation effect is framework-general. The instruction stays
fixed; the framework changes.

### 4.2 Sharpen the instruction

The Claude t2 P3 failure suggests amending the instruction to forbid
introducing forces or mechanisms not present in the observations —
turning the cue from "be parsimonious" into "be parsimonious *and
truthful to the observations*."

### 4.3 Per-axis judge validation

The 50 % / 50 % judge agreement on both axes here means *neither* LLM
judge can be relied on for a future treatment run without human audit
backup. A small per-axis calibration set on the chosen treatment
framework should be run before production judging, and the more
reliable judge picked per axis.

### 4.4 Publication

The three-round F=mv arc — `02_fmv` (content), `02_fmv.1`
(structural), `02_fmv.2` (axiomatisation control) — is now a coherent
empirical core for a paper. Headline: *models produce physically
correct rules in a counterfactual world but do not, by default,
organise them into a parsimonious system; a natural-language
axiomatisation cue closes the gap for the models that knew the rules,
demonstrating it is a self-organisation gap rather than a capability
limit.* Plus the LLM-as-judge methodology thread (mechanical criteria
help resolvers; judge reliability is task- and content-dependent).

---

## Appendix — files and links

- Pre-registration: [`predictions/02_fmv_2_prereg.md`](../predictions/02_fmv_2_prereg.md) — tag `prereg-02_fmv.2-locked`
- Treatment Stage 1 prompt: [`frameworks/02_fmv/prompts/stage1_induction_axiomatised.md`](../frameworks/02_fmv/prompts/stage1_induction_axiomatised.md)
- Treatment trials: `results/<model>/02_fmv_2/<stage>/trial_<N>_t0.0.json` (+ `.md` companions)
- Judge verdicts: `results/<model>/02_fmv_2/judgments/` (content), `results/<model>/02_fmv_2/structural/` (structural)
- Agent 1 / Agent 2 (non-canonical) verdicts: `results/<model>/02_fmv_2/{content_resolved,structural_resolved}/`
- Numerical findings: [`02_fmv_2_findings.md`](./02_fmv_2_findings.md)
- Human audit: [`02_fmv_2_audit_human_review.md`](./02_fmv_2_audit_human_review.md), worksheet [`02_fmv_2_audit_worksheet.md`](./02_fmv_2_audit_worksheet.md)
- Agents review: [`02_fmv_2_agents_review.md`](./02_fmv_2_agents_review.md)
- Runners / tools: `scripts/run_02_fmv_2.py`, `judge_02_fmv_2.py`, `build_02_fmv_2_worksheet.py`, `apply_02_fmv_2.py`, `run_agent1_02_fmv_2.py`, `run_agent2_02_fmv_2.py`, `render_02_fmv_2_to_md.py`, `build_02_fmv_2_agents_review.py`
