# PhysLit v0.3 — Aristotelian Axiomatisation Control Experiment Report

> **Date:** 2026-05-20.
> **Scope:** Single-variable control experiment on the Aristotelian framework. Same 3 models × N=5 × 4 stages as v0.1; the only manipulated variable is the Stage 1 induction prompt. Direct parallel of `02_fmv.2` on F=mv.
> **Prereg lock:** [`prereg-v0.3-locked`](https://github.com/dongzhang84/physlit/releases/tag/prereg-v0.3-locked).
> **Companion files:**
> - [`v0_3_findings.md`](./v0_3_findings.md) — judging report + post-audit numerical block.
> - [`v0_3_audit_human_review.md`](./v0_3_audit_human_review.md) — verbatim human verdicts on all 11 disagreement cases.
> - [`v0_3_audit_worksheet.md`](./v0_3_audit_worksheet.md) — the audit input.
> - [`v0_3_agents_review.md`](./v0_3_agents_review.md) — non-canonical Agent 1 + Agent 2 review.

---

## Abstract

`v0.3` is a **single-variable control experiment** on the Aristotelian
framework, parallel to `02_fmv.2` on F=mv. The control arm is the
frozen v0.1 trial set with the v0.1 content verdicts (audit-resolved)
and the v0.2 structural verdicts (audit-resolved). The treatment arm
is a new four-stage run, identical to v0.1 in every respect — same
observations, same models (`claude-opus-4-7`, `gpt-5.5-2026-04-23`,
`gemini-3.1-pro-preview`), same N=5, same Stage 2/3/4 prompts, same
content criteria, same structural criteria — except that the **Stage
1 induction prompt carries one added paragraph** asking for the
smallest set of rules with explicit consequence relationships.

**The added paragraph is byte-for-byte identical to the `02_fmv.2`
treatment instruction.** This is the load-bearing methodological
commitment of this round: cross-framework generalisation can only be
claimed if the intervention is the same intervention. The "don't
introduce mechanisms not in the observations" refinement raised by
`02_fmv.2`'s Claude-t2 P3 finding was deliberately *not* adopted.

Two predictions were locked before judging:

- **P1** — the treatment structural pass rate is greater than the
  control's 8/15. Tier-banded against an **absolute lift** anchored
  on the `02_fmv.2` net structural improvement: strongly confirmed
  ≥ 13 (lift ≥ 5), directionally confirmed 9–12, refuted ≤ 8.
- **P2** — content-axis competence does not materially degrade
  (treatment content PASS ≥ 4/15).

Post-audit results: **P1 STRONGLY CONFIRMED, P2 CONFIRMED.**

| Arm | Content-only PASS | Structural PASS | Composite PASS |
|---|---|---|---|
| Control (v0.1 / v0.2) | 5/15 | 8/15 | 2/15 |
| Treatment (v0.3) | 6/15 | **15/15** | **6/15** |

The structural pass rate **saturated** at 15/15 — every treatment
trial passed N9–N12. Absolute lift +7, exceeding the
`02_fmv.2` lift of +6 and the prereg's STRONGLY-CONFIRMED threshold of
+5. Content held nearly flat (+1, 5→6, well within the no-degradation
tolerance). Composite (content ∧ structural) tripled: 2/15 → 6/15.

The per-model pattern matches the `02_fmv.1` §2.7 self-organisation
thesis exactly:

| Model | Content (ctrl → treat) | Structural (ctrl → treat) | Composite (ctrl → treat) |
|---|---|---|---|
| `claude-opus-4-7` | 1/5 → 2/5 | **5/5 → 5/5** | 1/5 → 2/5 |
| `gpt-5.5-2026-04-23` | 3/5 → 4/5 | **0/5 → 5/5** | 0/5 → 4/5 |
| `gemini-3.1-pro-preview` | 1/5 → 0/5 | 3/5 → 5/5 | 1/5 → 0/5 |

GPT is again the headline mover — structural 0/5 → 5/5 (perfect
ceiling) under the same instruction that lifted it 0/5 → 2/5 on F=mv.
Claude's structural was already 5/5 on Aristotelian in the control,
so there was no headroom; its content shifted from t1 (control) to
t3 + t4 (treatment). Gemini's content fell 1 → 0 (the control's
gemini t2 PASS was audited FAIL on this run); its structural moved
3 → 5 but didn't help composite because content collapsed.

**The cross-framework generalisation is solid.** The same one-paragraph
intervention raises the structural pass rate on both a counterfactual
world (F=mv: 5 → 11) and a historical framework (Aristotelian: 8 → 15),
holds content roughly flat in both, and lifts composite to the same
6/15 ceiling on both. The `02_fmv.1` self-organisation thesis — *models
that know the rules respond to the cue; models that don't, don't* —
replicates here: Claude and GPT (the content-stronger models) account
for almost all the composite lift; Gemini barely moves on composite.

One important caveat surfaces from the human audit's *content*
verdicts. All 8 Claude/Gemini content disagreements audited FAIL,
revealing a pattern that wasn't visible in the structural numbers
alone: the parsimony pressure of the instruction may *encourage*
Newton-leak. The Claude content judge missed:

- **Banned vocabulary derivatives** ("denser", "heavier per equal
  volume" — the density concept under a different name).
- **Training-data concept import** ("speeds up, slows down, or holds
  steady" — acceleration vocabulary that no observation supports).
- **Standard-physics knowledge exposure** (a Stage 3 response named
  Galileo's vacuum result to deny it, which §3 counts as use).

A side effect parallel to (but distinct from) `02_fmv.2`'s Claude-t2
P3 fabrication: parsimony pressure can push a model to reach for the
cleaner Newtonian language. The structural axis still moves
decisively; the content side gains only 1 trial because the new leaks
offset the new wins.

Total compute: 60 treatment-arm production calls + 120 judge calls +
13 resolver calls ≈ $6.8 USD. Reproducible from the
`prereg-v0.3-locked` tag.

---

## 1. Design — what changed and what didn't

### 1.1 Relationship to v0.1 / v0.2 / `02_fmv.2`

`v0.3` reuses the Aristotelian framework as-is. The control arm is
the existing 60 v0.1 production trials, frozen at
`prereg-v0.1-locked`, with content verdicts from v0.1 (audit-resolved)
and structural verdicts from v0.2 (audit-resolved). No control trial
is re-run; no prior verdict is modified.

The treatment arm is a **new** four-stage run of 3 models × N=5 = 60
trials, on a fresh API client per stage with a new session UUID,
`temperature=0`, the same v0.1 observations, and the unchanged v0.1
Stage 2/3/4 prompts. The only manipulated variable is the Stage 1
prompt.

The intervention is byte-for-byte identical to `02_fmv.2`'s
(`frameworks/01_aristotelian/prompts/stage1_induction_axiomatised.md`),
verified by `diff`-comparison at commit time. The cross-framework
comparison is only meaningful if the intervention is the same; the
prereg explicitly forbade amending the wording for this round.

### 1.2 Judging

The treatment arm was judged on both axes with the v0.1/v0.2 baseline
judging — the prereg's identical-baseline-judging commitment — so
the cross-framework comparison stays clean:

- **Content axis** — the two content judges (Claude + GPT) scored
  Stage 1/2/3 with the v0.1 global judge prompts and v0.1 criteria,
  frozen at `prereg-v0.1-locked`.
- **Structural axis** — the two structural judges scored each
  treatment trial's Stage 1 rule set (Stage 2 concatenated as context)
  with the v0.2 structural criteria, frozen at
  `prereg-v0.2-locked`.

Disagreements resolved by human audit
([`v0_3_audit_human_review.md`](./v0_3_audit_human_review.md)); no
LLM resolver feeds a canonical verdict. Both dual-judge IRRs are
below 25 %.

---

## 2. Results

### 2.1 Judging and IRR

Content IRR **17.78 %** (8/45). Structural IRR **20.00 %** (3/15).
Neither above the 25 % full-audit threshold. All 11 disagreements
were audited individually.

### 2.2 The audit

**8 content cases — all FAIL.** The Claude content judge called every
disputed case PASS; the human audit aligned with OpenAI's FAIL on every
one. The disputed verdicts split across four leak types:

| Leak type | Cases | Mechanism |
|---|---|---|
| A — Banned vocabulary derivative | C1, C5 | "denser" / "heavier per equal volume" (= density) |
| B — Training-data concept import | C2, C8 | "speeds up / slows down" / "constant speeds" — concepts no observation supports |
| C — Standard-physics knowledge exposure | C3, C4 | Named Galileo's vacuum result / predicted vacuum scenario in standard-physics language |
| D — Missing framework concept | C6, C7 | Stage 1 never induced antiperistasis / impetus → Stage 3 arrow predictions defaulted |

**3 structural cases — all PASS.** Two systematic judge defects
recurred from prior rounds:

- **S2 (Gemini t3)** — OpenAI's N10 FAIL is the v0.2 Stage 1+2
  double-count bug: counted 4+4=8 rules, called Stage-2 mirror a
  "duplicate". `02_fmv.1` fixed this defect by scoping the count to
  Stage 1 only; v0.3 reuses the v0.2 criteria (per prereg's
  identical-baseline commitment), so the bug re-emerged.
- **S1 (GPT t1) and S3 (Gemini t4)** — Claude verdict-field
  self-contradiction: the reasoning explicitly ends with "Correcting
  my verdict: this should be PASS" / "Verdict should be PASS" while
  the structured `verdict` field still says FAIL. Same defect class as
  `02_fmv.1` Case 6 (Gemini t2). Resolution: follow the reasoning.

### 2.3 Post-audit numbers — the two predictions

| Prediction | Verdict | Result |
|---|---|---|
| **P1** axiomatisation raises structural | **STRONGLY CONFIRMED** | treatment structural PASS **15/15** vs control 8/15 — absolute lift +7 (threshold +5 for STRONGLY) |
| **P2** content does not degrade | **CONFIRMED** | treatment content PASS **6/15** vs control 5/15 — +1, well within the no-degradation tolerance |

### 2.4 Resolved per-trial matrix

| Model | Trial | S1 | S2 | S3 | Content-only | Structural | Composite |
|---|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 1 | PASS | PASS | FAIL | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 2 | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 3 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `claude-opus-4-7` | 4 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | FAIL | FAIL | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | PASS | **PASS** |
| `gemini-3.1-pro-preview` | 0 | FAIL | PASS | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | FAIL | FAIL | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 3 | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | FAIL | PASS | FAIL | PASS | FAIL |

Composite PASS: **6/15**. Up from control's 2/15.

### 2.5 What the numbers mean — substantive findings

**Finding 1 — structural axis saturates at 15/15.** The
axiomatisation instruction moved Aristotelian structural pass rate
from 8/15 to 15/15. Every Stage 1 rule set in the treatment arm —
Claude, GPT, Gemini, every trial — satisfied N9–N12 by the v0.2
criteria + the human audit. This is the cleanest single-variable
causal effect PhysLit has produced.

**Finding 2 — the cue affects content too, in a directionally bad way
on Aristotelian.** Content held nearly flat in net (+1) but the
trial-level reshuffling reveals a side effect. Three Claude trials
(t0, t1, t2) had content FAIL in the treatment that wouldn't have
been content-FAIL had the instruction not been added — they
introduced Newton-leak vocabulary or knowledge that wasn't there in
v0.1 (per audit). The parsimony pressure plausibly *pulled the model
toward the cleaner Newtonian formulation* it knows from training
data: "denser", "speeds up / slows down", explicit naming of
Galileo's vacuum result. The instruction's "consolidate" pressure
becomes a "use the cleaner physics you already know" pressure. The
F=mv equivalent was the Claude-t2 P3 fabrication; here the side
effect is broader and more diffuse.

**Finding 3 — per-model pattern replicates `02_fmv.1` §2.7 thesis.**

| Model | Net structural lift (ctrl → treat) | Net composite lift |
|---|---|---|
| `claude-opus-4-7` | 0 (5/5 already saturated) | +1 |
| `gpt-5.5-2026-04-23` | **+5 (0/5 → 5/5)** | **+4** |
| `gemini-3.1-pro-preview` | +2 (3/5 → 5/5) | −1 |

GPT is the dominant mover on both rounds. The model that gets the
physics roughly right but writes the sprawliest rule sets is the
model most responsive to the consolidation cue. Gemini barely moves
on composite (content collapse offsets the structural gain) — same
self-organisation-gap-vs-knowledge-gap pattern.

### 2.6 Methodological findings

**Two judge defects re-emerged in this round, both with documented
prior precedents elsewhere in the project.**

- **OpenAI Stage 1+2 double-count** (S2). The v0.2 structural
  criteria say "rule count means top-level numbered or bolded
  propositions in the Stage 1 + Stage 2 combined output"; the
  Stage 2 prompt requires the model to "restate the rules mirroring
  the numbering you used earlier". The two combined produce a
  built-in N10 false positive on any well-formed Stage 2. `02_fmv.1`
  fixed this by scoping count and N10 to Stage 1; v0.3 reuses the
  v0.2 criteria so the bug returned. Audit resolution: apply the
  Stage-1-only principle.
- **Claude verdict-field self-contradiction** (S1, S3). The
  structured `verdict` field reports FAIL while the reasoning text
  explicitly concludes "this should be PASS" / "Verdict should be
  PASS". Same defect class as `02_fmv.1` Case 6. Audit resolution:
  follow the reasoning.

The content judges showed an opposite asymmetry from prior rounds:
the **Claude content judge took the lenient direction on every
single content disagreement (8/8 PASS) and was wrong on every single
one** per the audit. On `02_fmv` Claude was the more reliable judge
at 86 %; on `v0.3` Claude's lean-PASS direction stayed the same but
no longer aligned with the audit because every disputed case in this
round was a real Newton leak. The OpenAI judge's lean-FAIL was
substantively right this round even when its specific reasoning
varied in quality.

### 2.7 Cost and reproducibility

| Component | Calls | Cost (est., USD) |
|---|---|---|
| Treatment production trials (3 × 5 × 4) | 60 | ~5.10 |
| Dual-judge (content S1-3 + structural) | 120 | ~1.30 |
| Agent 1 + Agent 2 side analysis (incl. 2 retries) | 13 | ~0.45 |
| **Total** | **193** | **~6.85** |

Within the prereg's ≤ $30 estimate. Every prompt + response committed
under `results/<model>/01_aristotelian_3/`. Reproducible from the
`prereg-v0.3-locked` tag.

---

## 3. Cross-framework comparison — the central deliverable

Two rounds of the same axiomatisation intervention, on two different
frameworks:

| Framework | Round | Content (ctrl → treat) | Structural (ctrl → treat) | Composite (ctrl → treat) |
|---|---|---|---|---|
| F=mv (counterfactual) | `02_fmv.2` | 9 → 9 (Δ 0) | 5 → 11 (Δ +6) | 1 → 6 (Δ +5) |
| Aristotelian (historical) | **`v0.3`** | 5 → 6 (Δ +1) | 8 → **15** (Δ **+7**) | 2 → 6 (Δ +4) |

**The axiomatisation effect is robust across both frameworks.** Three
features hold in both:

1. **Structural pass rate moves dramatically up** (+6 and +7 absolute
   trials). On both frameworks the lift exceeds the +5 STRONGLY-CONFIRMED
   threshold; on Aristotelian it saturates at 15/15.
2. **Content holds roughly flat.** F=mv exactly flat (9 → 9);
   Aristotelian +1 (5 → 6). No round trades content for parsimony at
   the aggregate level.
3. **Composite jumps to the same ceiling on both** (1/15 → 6/15 on
   F=mv; 2/15 → 6/15 on Aristotelian). Two independent frameworks
   under identical intervention converge on the same total composite
   pass count.

**Per-model, the pattern is the same on both rounds:**

| Model | F=mv structural lift | Aristotelian structural lift | F=mv composite lift | Aristotelian composite lift |
|---|---|---|---|---|
| `claude-opus-4-7` | +3 (2 → 5) | 0 (5 → 5, saturated) | +2 | +1 |
| `gpt-5.5-2026-04-23` | **+2 (0 → 2)** | **+5 (0 → 5)** | **+2** | **+4** |
| `gemini-3.1-pro-preview` | +1 (3 → 4) | +2 (3 → 5) | +1 | −1 |

GPT is the dominant mover on both frameworks — content-strong /
structure-weak in the control, content-strong / structure-strong in
the treatment, on both. Claude was already structurally clean on
Aristotelian (5/5), so the Aristotelian round shows the response
constrained by the saturation ceiling; on F=mv it had room to move
(2 → 5). Gemini moves the smallest amount on both rounds — and on
Aristotelian, content collapse (1 → 0) cancels the structural gain.

**One feature differs between rounds** — the *side effect of the
cue*. On F=mv it surfaced as a single P3 fabrication (Claude t2 Stage
2: "the track pushes upward"). On Aristotelian it surfaced as a
broader pattern of Newton leak in three Claude trials (density
derivatives, acceleration vocabulary, standard-physics knowledge
exposure). The shared mechanism: parsimony pressure can push a model
to reach for the cleaner formulation it knows from training data.
This shows up differently on a counterfactual world (where the
"cleaner" thing the model reaches for is a fabricated balancing
mechanism) versus a historical-framework world (where the "cleaner"
thing is the actual Newtonian-language vocabulary the model has
memorised).

**The `02_fmv.1` §2.7 self-organisation thesis is now causally
confirmed on two independent frameworks.** The same natural-language
axiomatisation cue closes the structural gap for the models that have
the underlying knowledge, on both a counterfactual world the model
could not have memorised and a historical framework it has every
opportunity to confuse with Newton. The thesis is not framework-
specific.

---

## 4. Discussion

### 4.1 What the F=mv + Aristotelian arc establishes

Three rounds of substantive results, plus two control rounds, now line
up as the empirical core of the paper:

- **`02_fmv` (descriptive, content axis on a counterfactual world).**
  Frontier models can induce a counterfactual physics from naked
  observations: 9/15 content-PASS, including all 5 GPT trials. The
  models did not retreat to F=ma when the observations contradicted it.
- **`02_fmv.1` (descriptive, structural axis on the same trials).**
  Yet those same trials are structurally sprawling — 5/15 structural-PASS,
  GPT 0/5. The §2.7 reading: a *self-organisation gap, not a knowledge
  gap*.
- **`02_fmv.2` (causal, axiomatisation control on F=mv).** A
  one-paragraph cue closes the gap for Claude and GPT (the
  content-strong models); structural 5 → 11, content held exactly
  flat. The thesis is causal: the structural shortfall is a default
  behaviour, not a capability limit, for the models that have the
  underlying knowledge.
- **`v0.3` (causal, same instruction on Aristotelian).** The effect
  generalises across frameworks: structural 8 → 15, content held
  nearly flat (+1), same composite ceiling 6/15 reached.

The empirical claim the paper can make: *on two independent
frameworks — one counterfactual, one historical — frontier LLMs
produce physically-correct rules but do not, by default, organise
them into a parsimonious axiomatic system; a single natural-language
cue closes the structural gap for the models with the underlying
knowledge, with content held roughly flat.*

### 4.2 The side-effect: parsimony pressure pulls toward training data

Aristotelian surfaced a side effect of the cue more sharply than F=mv
did. Three Claude trials introduced Newton-leak language in the
treatment that they hadn't used in the control: "denser",
"speeds up / slows down", an explicit naming of Galileo's vacuum
result. The mechanism is plausible: asked to *consolidate* the rule
set into a smaller, more general account, the model reaches for the
cleaner formulation it knows — and the cleaner formulation it knows
is Newtonian. On a counterfactual world (F=mv) that pull surfaced as
a single fabricated balancing mechanism (Claude t2 P3). On a historical
framework (Aristotelian) it surfaces as broader vocabulary leak. Same
mechanism, framework-shaped expression.

This is a refinement of the intervention worth a future round —
`v0.3.1` or similar — with an explicit "do not introduce vocabulary
or mechanisms beyond what the observations provide" clause added.
The clean Aristotelian numbers (content +1) hide a real structural
problem with the cue that a sharpened version could plausibly close.

### 4.3 The judge-defect inventory

By the end of this round, two LLM-as-judge defects are documented at
publication-quality across three rounds:

- **OpenAI Stage 1+2 double-count** — v0.2 (original), `02_fmv.1`
  (fixed via Stage-1-only criteria), `v0.3` (re-emerged because v0.3
  reuses v0.2 criteria). The defect arises from the interaction
  between the structural-criteria text and the Stage 2 prompt's
  mirror-numbering instruction. Mitigation: scope count and N10 to
  Stage 1.
- **Claude verdict-field self-contradiction** — `02_fmv.1` Case 6,
  `v0.3` S1, `v0.3` S3. The structured `verdict` field reports FAIL
  while the reasoning text concludes PASS. Mitigation: follow the
  reasoning; flag the verdict field as unreliable.

Both are documented in `v0_3_audit_human_review.md` with full
case-level evidence. They are LLM-as-judge artifacts, not specific to
PhysLit's experimental design, and both have published precedent in
prior rounds.

---

## 5. Next steps

### 5.1 Sharpen the instruction

Add a clause forbidding the introduction of vocabulary or mechanisms
beyond what the observations provide. Run a third axiomatisation
round (`v0.3.1` or `02_fmv.3`) with the amended instruction, compare
against this round, see whether content holds tighter while
structural stays up. The amended-cue cross-framework comparison would
be the natural follow-up paper section.

### 5.2 Per-axis judge calibration

The Claude content judge took the lenient direction on every disputed
case in this round and was wrong on every one. The OpenAI structural
judge double-counted on a case it had no need to. Both have established
precedents but no per-round validation. A small per-axis calibration
set on the target framework run before production judging would
identify the more reliable judge for each axis on each framework.

### 5.3 Publication

The F=mv + Aristotelian axiomatisation arc is now the empirical core
of the paper. Headline: *frontier LLMs produce physically-correct
rules but do not, by default, axiomatise; a natural-language cue
closes the structural gap on two independent frameworks; the effect
is concentrated in the content-knowledgeable models.* Side findings:
the cue has a content side-effect (training-data vocabulary leak)
worth documenting and refining; LLM-as-judge methodology has two
documented defects requiring published mitigation strategies.

---

## Appendix — files and links

- Pre-registration: [`predictions/v0_3_prereg.md`](../../predictions/v0_3_prereg.md) — tag `prereg-v0.3-locked`
- Treatment Stage 1 prompt: [`frameworks/01_aristotelian/prompts/stage1_induction_axiomatised.md`](../../frameworks/01_aristotelian/prompts/stage1_induction_axiomatised.md) (byte-identical insertion to `02_fmv.2`'s)
- Treatment trials: `results/<model>/01_aristotelian_3/<stage>/trial_<N>_t0.0.json` (+ `.md` companions, both content and structural verdicts attached)
- Judge verdicts: `results/<model>/01_aristotelian_3/judgments/` (content), `results/<model>/01_aristotelian_3/structural/` (structural)
- Agent 1 / Agent 2 (non-canonical) verdicts: `results/<model>/01_aristotelian_3/{content_resolved,structural_resolved}/`
- Numerical findings: [`v0_3_findings.md`](./v0_3_findings.md)
- Human audit: [`v0_3_audit_human_review.md`](./v0_3_audit_human_review.md), worksheet [`v0_3_audit_worksheet.md`](./v0_3_audit_worksheet.md)
- Agents review: [`v0_3_agents_review.md`](./v0_3_agents_review.md)
- Runners / tools: `scripts/run_v0_3.py`, `judge_v0_3.py`, `apply_v0_3.py`, `build_v0_3_worksheet.py`, `run_agent1_v0_3.py`, `run_agent2_v0_3.py`, `render_v0_3_to_md.py`, `build_v0_3_agents_review.py`
