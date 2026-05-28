# PhysLit 02_fmv — Full Report

> **Date:** 2026-05-18.
> **Scope:** 3 frontier models × 5 trials × 4 stages on the F=mv World.
> **Prereg lock:** [`prereg-02_fmv-locked`](https://github.com/dongzhang84/physlit/releases/tag/prereg-02_fmv-locked).
> **Companion files:**
> - [`02_fmv_findings.md`](./02_fmv_findings.md) — judging report + post-audit numerical block.
> - [`02_fmv_audit_human_review.md`](./02_fmv_audit_human_review.md) — verbatim human verdicts on all 14 disagreement cases.
> - [`02_fmv_audit_worksheet.md`](./02_fmv_audit_worksheet.md) — the input the auditor worked from.

This file is the human-readable narrative report. Code, prompts, raw
trial outputs, and judge verdicts are in the repo and cross-linked
below. Trial JSONs have `.md` companions under `results/`.

---

## Abstract

PhysLit 02_fmv is the project's **second framework experiment** and
the first from-scratch run since v0.1. It tests "physics literacy" —
the ability of an LLM to induce, formulate, apply, and reflect on
self-consistent physical rules inside an unfamiliar framework — on the
**F=mv World**: a counterfactual world where a body's pace is set by
the push acting on it (force ∝ velocity), not by its acceleration. The
three tested models are Claude Opus 4.7, GPT-5.5, and Gemini 3.1 Pro.

Four predictions were locked before any production trial:

- **P1** — a majority of the 15 Stage 1 induction trials FAIL: the
  models import F=ma machinery rather than inducing the F=mv rules.
- **P2** — among failure-containing trials, ≥ 50 % over-claim in the
  Stage 4 self-reflection.
- **P3** — the dual-judge content-axis IRR falls below v0.1's 36.67 %,
  and below the 25 % audit threshold (the *mechanical-criteria* claim).
- **P4** — ≥ 30 % of the 45 quantitative Stage 3 predictions name the
  right direction but give the F=ma ratio.

Post-audit results: **P1 REFUTED, P2 CONFIRMED, P3 PARTIALLY
CONFIRMED, P4 REFUTED.**

The headline is **P1 REFUTED**. Only 4 of 15 Stage 1 trials failed —
all four Gemini — and Claude and GPT induced the F=mv rules cleanly in
every trial. Frontier models did **not**, on this counterfactual
world, slide back to the F=ma physics in their training data. This is
the opposite of v0.1, where Aristotelian induction failed (P1
confirmed there).

Two methodology findings are as consequential as the predictions:

1. **A mechanically-specified criterion makes an LLM disagree-resolver
   reliable.** v0.2 found an LLM resolver ("Agent 1") agreed with the
   human audit only 29.4 % of the time, on v0.1's ambiguous criteria.
   Re-run here as a non-canonical side analysis against the mechanical
   02_fmv criteria, Agent 1 agreed with the human audit on **12 / 12
   content cases (100 %)**.
2. **Judge reliability does not transfer across frameworks.** On v0.1
   Aristotelian the OpenAI judge was the more reliable of the two; on
   F=mv it agreed with the human audit on 3 / 14 disagreement cases,
   the Claude judge on 11 / 14 — a near-complete reversal, same prompts
   and same models.

Total compute: 60 production calls + 120 judge calls + 12 resolver
calls ≈ $17.3 USD. Reproducible from the `prereg-02_fmv-locked` tag.

---

## 1. Motivation — why a counterfactual world

### 1.1 The benchmark gap (recap)

The case for PhysLit is made in full in
[`v0_1_report.md`](../aristotelian/v0_1_report.md) §1. In brief: standard physics
benchmarks count correct answers, which measures coverage of the
training distribution, not physical reasoning. PhysLit instead tests
the *cognitive work* of physics — induction, formulation, prediction —
inside a framework that does not match the model's training prior.

### 1.2 Why an F=mv counterfactual world

v0.1 used Aristotelian Mechanics: a *historical* framework, real and
internally coherent, present in training data primarily as a position
to be argued against. That design has one residual confound — the
framework still exists in the training data, so a model's behaviour
mixes "can it reason inside the framework" with "how is the framework
represented in its prior".

The F=mv World removes that confound. It is **counterfactual** — it
has no literature, no historical proponents, no training-data
representation at all. A model cannot retrieve it; it can only induce
it from the twelve observations. And it conflicts with the training
prior more sharply than Aristotelian Mechanics does: where Aristotle
disagrees with Newton *qualitatively*, F=mv disagrees *numerically* —
a steadily pushed body moves at a steady pace (not an accelerating
one), a released body stops at once (no inertia), all bodies fall at
one unchanging pace. Every one of those directly contradicts a
specific, heavily-drilled F=ma fact.

It is also **Tier 1** (simulator-codable): the world's law is a clean
deterministic relation, so the framework can be specified without the
conceptual fuzziness of "natural place". The first round uses a
hand-authored 12-observation set; the deterministic simulator is
deferred.

### 1.3 Scope, and one deliberate methodology change

02_fmv is a **content-axis experiment**. Each trial is judged on the
content criteria (necessary conditions, banned-token test,
disqualifying patterns). The structural axis (the v0.2 N9–N12 layer)
is **out of scope by explicit prereg decision** — its absence here is
deliberate, not an omission. Disagreements are resolved by **human
audit**, not by an LLM resolver — unlike v0.2.

One change is carried in deliberately. v0.1's criteria left their
hardest call to interpretation (`ideal_induction.md` §3 banned
"density (as a defined quantity)" while §5 failed the bare word
"denser"), and a human auditor and an LLM resolver split on that gap.
The 02_fmv criteria are written to be **mechanical**: §3 is a purely
lexical banned-token test, with no intent assessment. Whether that
reduces dual-judge disagreement is itself pre-registered (P3).

---

## 2. Design — what we built and how we ran it

### 2.1 Pre-registration

`predictions/02_fmv_prereg.md` was locked at `prereg-02_fmv-locked`
before any production trial. It commits the four predictions, the
three pinned model versions, the N=5 protocol, the content-axis-only
scope, human-audit resolution, and the frozen artifacts (observation
set, criteria, the four model prompts, the four judge prompts).

It is **framework-scoped** — tag and results carry the `02_fmv`
identifier, not a `v0.X` number. v0.1 and v0.2 are untouched; 02_fmv
reuses none of their data.

### 2.2 The F=mv World

The model is given twelve plain-language observations
(`frameworks/02_fmv/observations.md`) — e.g. "a steady pull moves the
block at one unchanging pace; it does not gather speed", "the instant
the pull is released, the block halts where it is", "a boulder and a
pebble fall side by side at one unchanging pace". The observations use
only descriptive language (push, pull, pace, heavy, fall); they never
state the law and never use a banned token.

A pre-lock dry run (Claude, N=1) surfaced one criteria defect: the
purely-lexical §3 test FAILed a response for the everyday verb "force"
("the observations force a conclusion"). Since "force" is not an F=ma
discriminator — both physics have a force — it was removed from the
banned list before lock. The final banned set is *acceleration,
velocity, inertia, momentum, mass, gravity, friction, energy*,
physicist names, and the equation `F = ma`.

### 2.3 The four-stage protocol

Each trial runs four independent stages, each in a fresh API session
with no context reuse: **Stage 1** induction (observations → rules),
**Stage 2** formulation (rules → operational form), **Stage 3**
prediction (apply the rules to five novel scenarios), **Stage 4** meta
(reflect on the three prior responses). N = 5 trials per model.

### 2.4 Sampling

Every call requests `temperature = 0`. OpenAI and Google honour it;
Anthropic Opus 4.7 rejects the parameter and runs at its default. No
temperature-variation pass.

### 2.5 Dual-judge evaluation and human audit

Each Stage 1–3 response is scored by two independent LLM judges
(Claude Opus 4.7 and GPT-5.5), each given the framework-specific judge
prompt and the frozen criteria. Where the two agree, that is the
verdict; where they disagree, the case is resolved by **human audit**.
The dual-judge disagreement rate (IRR) is published as a
methodology-quality indicator; an IRR above 25 % triggers a full human
audit before release.

### 2.6 Pipeline and infrastructure notes

`run_02_fmv.py` ran the 60 production trials; `judge_02_fmv.py`
dispatched the 120 judge calls and aggregated; `build_02_fmv_audit_
worksheet.py` produced the audit input; `apply_02_fmv_audit.py`
recomputed the predictions post-audit. Two infrastructure problems
were met and fixed without touching frozen artifacts:

- A Gemini Stage 4 call hung for ~5 hours (the vendor SDKs do blocking
  I/O with no timeout). A SIGALRM-based per-call timeout was added to
  the runners; a hung call is now interrupted at 300 s and retried.
- The Bash sandbox blocks `generativelanguage.googleapis.com`; the
  Gemini trials were run with the sandbox disabled. Anthropic and
  OpenAI endpoints were reachable throughout.

---

## 3. Results — what we found

### 3.1 Judging and IRR

The two judges agreed on 33 of 45 Stage 1–3 classifications and split
on 12 — a content-axis **IRR of 26.67 %**, above the 25 % audit
threshold. Plus 2 Stage 4 over-claim disagreements: **14 disagreement
cases** total.

### 3.2 The audit

All 14 disagreement cases were resolved by human audit
(`02_fmv_audit_human_review.md`). Two findings stood out immediately.
First, **only 2 of the 14 cases were genuine FAILs** — and both for
the substring "mass" inside a banned token ("massless", "massive") in
a parenthetical boundary note, never in an actual rule or prediction.
The other 12 disagreements were judge error, not model error. Second,
the OpenAI judge was wrong on most of them: it hallucinated banned
tokens that were not in the response (3 cases), and in 5 cases its
verdict field said FAIL while its own reasoning text concluded the
response should pass (see §3.5).

### 3.3 Post-audit numbers — the four predictions

| Prediction | Verdict | Result |
|---|---|---|
| **P1** induction failure | **REFUTED** | 4 / 15 Stage 1 trials FAIL (threshold ≥ 8) |
| **P2** meta miscalibration | **CONFIRMED** | 4 / 6 failure-containing trials over-claim = 66.7 % |
| **P3** mechanical criteria reduce IRR | **PARTIALLY CONFIRMED** | IRR 26.67 % — below v0.1's 36.67 %, above the 25 % bar |
| **P4** Stage 3 quantitative leak | **REFUTED** | 0 / 45 direction-correct / ratio-leaked predictions |

Per-stage PASS counts (post-audit, of 15 trials): Stage 1 **11/15**,
Stage 2 **11/15**, Stage 3 **14/15**. Trials passing all three content
stages: **9/15**.

All four verdicts match the pre-audit dual-judge result — the audit
firmed the underlying counts and resolved every DISAGREE row, but
flipped no prediction.

### 3.4 What the numbers mean — substantive findings

**Finding 1 — frontier models induced the counterfactual world
cleanly.** P1 predicted a majority of Stage 1 trials would fail. Only
4 of 15 did, and all four are Gemini. Claude and GPT induced the F=mv
rules — pace tracks the present push, no build-up, no carry-over, all
bodies fall alike — in every one of their trials, using the
observations' own vocabulary and importing no banned concept. On this
counterfactual world the models suspended their F=ma prior. This is
the direct opposite of v0.1, where Aristotelian induction failed.

**Finding 2 — the result is uneven across models.** All-content-PASS
trials: Claude 4/5, GPT 5/5, Gemini 0/5. Gemini accounts for every
Stage 1 failure and never passed all three content stages. The
"models are physics-literate" reading holds for two of three frontier
models, not all.

**Finding 3 — more passes than v0.1, but not a controlled
comparison.** v0.1 Aristotelian vs 02_fmv F=mv, audit-resolved: Stage
1 PASS 7/15 → 11/15; Stage 2 6/15 → 11/15; all-content-PASS 5/15 →
9/15. The improvement is real but has three sources that must not be
conflated: (a) the F=mv World is a cleaner, more learnable framework
than Aristotelian's conceptual cluster; (b) the banned list is
marginally more permissive (`force` removed); (c) genuine
model competence — the audit confirmed only 2 real banned-token
violations in 14 disagreements. Because v0.1 and 02_fmv differ in
framework, criteria, and banned list, "11/15 vs 7/15" is *suggestive,
not a controlled result*. A clean cross-framework claim needs more
frameworks judged under a common criteria standard.

**Finding 4 — meta-cognitive miscalibration persists (P2).** Of the 6
failure-containing trials, 4 over-claimed in Stage 4 — denied or
missed a slip the trial's own record shows. The clearest case: a
Gemini trial that used "massive" (a banned-token violation) and whose
Stage 4 both claimed zero standard-physics influence and stated a Q4
"difference" that contradicts the model's own Stage 1 rule. Models
remain poor at auditing themselves, consistent with v0.1's P3.

### 3.5 Methodological findings

**A mechanical criterion makes the LLM resolver reliable.** v0.2's V1
prediction — that an LLM disagree-resolver ("Agent 1") would match the
human audit — was REFUTED there at 29.4 % agreement, and that result
was read as evidence LLM resolvers cannot replace human audit. Re-run
here as a **non-canonical side analysis** (Agent 1 = `gemini-3.1-pro-
preview`, run over the 12 content disagreements, not feeding any
prediction), Agent 1 agreed with the human audit on **12 of 12
(100 %)** — cross-vendor 8/8, same-vendor 4/4. The single change
between the two runs is the criteria: v0.1's were interpretation-laden,
02_fmv's are mechanical. This is direct evidence that v0.2's "LLM
resolver is unreliable" finding was substantially a criteria-ambiguity
artifact: with a mechanical criterion, the LLM resolver reproduces the
human verdict exactly. (Caveat: 12 cases, one framework, and the
cases were dominated by a single split pattern — see Finding 5.)

**Judge reliability does not transfer across frameworks.** On v0.1
Aristotelian the OpenAI judge was the more reliable of the two
(agreeing with the human audit far more often than the Claude judge).
On F=mv the order reverses: the Claude judge agreed with the human
audit on 11 of 14 disagreement cases, the OpenAI judge on 3 of 14 —
same judge prompts, same model versions, opposite outcome. Judge
selection is not a one-time calibration; a judge validated on one
framework cannot be assumed reliable on the next.

**Finding 5 — the OpenAI judge verdict-field defect.** In 5 of the 14
cases the OpenAI judge's `reasoning` text explicitly concludes the
response should pass ("no listed banned token appears"), while its
`verdict` field says FAIL. The structured field and the reasoning
contradict each other. This is the same defect class seen in v0.2's
Aristotelian structural audit — there, in the Claude structural judge.
It appears to be a systematic LLM-as-judge failure mode: the verdict
field is committed before the reasoning chain completes. A post-hoc
consistency check (flag any verdict whose reasoning contradicts it) is
recommended for future rounds.

### 3.6 Cost and reproducibility

| Component | Calls | Cost (est., USD) |
|---|---|---|
| Production trials (3 × 5 × 4) | 60 | ~4.8 |
| Dual-judge (Stage 1–3 + meta) | 120 | ~11.9 |
| Agent 1 side analysis | 12 | ~0.6 |
| **Total** | **192** | **~17.3** |

Within the prereg's ≤ $60 estimate. Every prompt sent and response
received is committed under `results/<model>/02_fmv/`; every result
file records its own cost. The run reproduces from the
`prereg-02_fmv-locked` tag (`uv sync`, keys in `.env.local`,
`run_02_fmv.py` then `judge_02_fmv.py`).

---

## 4. Next steps

### 4.1 Structural axis on F=mv

The N9–N12 structural axis was out of scope this round. Applying it to
the F=mv trials would be a separate, additively pre-registered round
(`02_fmv.1`), exactly as v0.2 added the structural axis to v0.1. The
v0.2 structural criteria carried a Stage 1+2 double-count defect; a
structural round on F=mv should fix that first.

### 4.2 More frameworks for a controlled comparison

Finding 3 cannot be made a clean cross-framework claim from two
frameworks judged under different criteria. A worthwhile next
experiment: 2–3 further frameworks (phlogiston, reverse-gravity,
colour-force) judged under the *same* mechanical criteria standard, so
that pass rates become directly comparable.

### 4.3 The deterministic simulator

02_fmv used a hand-authored observation set. Building the Tier 1
simulator (`physlit.generators.tier1.fmv`) would make the observation
set reproducible byte-for-byte and let observation count and content
be varied systematically.

### 4.4 Publication

The 02_fmv result set — 60 trials, 120 judge verdicts, 14 audited
disagreements, Agent 1 side analysis — is committed in full. The two
methodology findings (mechanical criteria make an LLM resolver
reliable; judge reliability does not transfer across frameworks) are
publishable independent of the physics-literacy result and, with the
v0.2 V1 result, form a coherent thread on LLM-as-judge methodology.

---

## Appendix — files and links

- Pre-registration: [`predictions/02_fmv_prereg.md`](../../predictions/02_fmv_prereg.md) — tag `prereg-02_fmv-locked`
- Framework: [`frameworks/02_fmv/`](../../frameworks/02_fmv/) — `spec.yaml`, `observations.md`, `ideal_induction.md`, `pass_fail_criteria.md`, `prediction_tests.md`, `prompts/`
- Production trials: `results/<model>/02_fmv/<stage>/trial_<N>_t0.0.json` (+ `.md` companions)
- Judge verdicts: `results/<model>/02_fmv/judgments/`
- Agent 1 (non-canonical) verdicts: `results/<model>/02_fmv/content_resolved/`
- Numerical findings: [`02_fmv_findings.md`](./02_fmv_findings.md)
- Human audit: [`02_fmv_audit_human_review.md`](./02_fmv_audit_human_review.md), worksheet [`02_fmv_audit_worksheet.md`](./02_fmv_audit_worksheet.md)
- Runners / tools: `scripts/run_02_fmv.py`, `judge_02_fmv.py`, `build_02_fmv_audit_worksheet.py`, `apply_02_fmv_audit.py`, `run_agent1_02_fmv.py`, `render_02_fmv_to_md.py`
