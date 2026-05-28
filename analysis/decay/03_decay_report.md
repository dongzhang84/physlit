# PhysLit 03_decay — Full Report

> **Date:** 2026-05-28.
> **Scope:** 3 frontier models × 5 trials × 4 stages on the **Decay World** — a Tier 1 counterfactual world in which every isolated system's directly measured state shrinks at a universal fixed fractional rate per second.
> **Prereg lock:** [`prereg-03_decay-locked`](https://github.com/dongzhang84/physlit/releases/tag/prereg-03_decay-locked).
> **Companion files:**
> - [`03_decay_findings.md`](./03_decay_findings.md) — judging report + post-audit numerical block.
> - [`03_decay_audit_human_review.md`](./03_decay_audit_human_review.md) — verbatim human verdicts on all 54 disagreement cases.
> - [`03_decay_audit_worksheet.md`](./03_decay_audit_worksheet.md) — the audit input.
> - [`03_decay_agents_review.md`](./03_decay_agents_review.md) — non-canonical Agent 1 + Agent 2 review.

This file is the human-readable narrative report. Code, prompts, raw trial outputs, and judge verdicts are in the repo and cross-linked below. Trial JSONs have `.md` companions under `results/`.

---

## Abstract

PhysLit `03_decay` is the project's **third framework experiment** and its second counterfactual world after `02_fmv`. It tests "physics literacy" — the ability of an LLM to induce, formulate, apply, and reflect on self-consistent physical rules inside an unfamiliar framework — on the **Decay World**: a counterfactual world in which every isolated system's *directly measured* state (oscillation amplitude, absolute temperature, rotation rate, orbital radius) shrinks at a fixed fractional rate per second (≈ 0.99/s), universally across mechanical, thermal, rotational, and orbital domains, with no underlying "energy" or any other hidden substrate, and with every standard dissipative mechanism (friction, drag, damping, viscosity, radiative loss) explicitly closed off. The three tested models are Claude Opus 4.7, GPT-5.5, and Gemini 3.1 Pro.

Four predictions were locked before any production trial:

- **P1** — composite content-axis PASS count is **strictly less than 5/15**, below both prior baselines (F=mv 9/15, Aristotelian 5/15) — the Decay World is harder than either prior.
- **P2** — among Stage 1 trials that FAIL on a §5 disqualifying pattern, **hidden-substrate framing (P2)** is the modal pattern.
- **P3** — across the 60 quantitative Stage 3 predictions, the **direction-correct / ratio-leaked** bucket outnumbers the **direction-wrong** bucket.
- **P4** — among failure-containing trials, **Stage 4 over-claiming outnumbers correct self-identification**.

**Post-audit results: P1 CONFIRMED, P2 CONFIRMED, P3 CONFIRMED, P4 CONFIRMED — all four predictions confirmed.**

| Headline | Number | Comparison |
|---|---|---|
| Composite content PASS | **0/15** | F=mv 9/15 · Aristotelian 5/15 (decay world is the hardest) |
| Stage 1 §5 P2 hits | 1/1 (sole §5 pattern fired) | also 3/4 Stage 2 §5 hits are P2 |
| P3 quantitative bucket | 37 decay-correct / **23 ratio-leaked** / **0 direction-wrong** | strictly leaked > wrong |
| P4 over-claim rate | **10/15 = 67%** | v0.1 70% · 02_fmv 66.7% · 03_decay 67% |

Three rounds, three frameworks, three CONFIRMED meta-cognitive over-claim rates in the 65–70% band. The headline finding of `03_decay` is, however, **none of the four prereg verdicts** — it is a **methodology stress** that emerged in the dual-judge data. Dual-judge IRR was **40.00%**, triggering the `CLAUDE.md` 25% mandatory-audit threshold. After audit, **16 of 18 OpenAI judge FAIL clauses on the content axis were fabricated or misclassified §3 banned-token citations**, against a Decay-World §3 list of 20+ tokens with substantial semantic overlap to the response vocabulary (decay ↔ damping, slow ↔ deceleration, no-contact ↔ resistance). The OpenAI judge ran at **22% / 33% / 50%** agreement with the human audit across the three parts; the Claude judge at **67% / 81% / 50%**. This is the third framework on which the relatively reliable judge changes, and the failure mode here is mechanistic and identifiable, not random model variance.

Two non-canonical LLM resolvers were also run against the locked criteria as a side analysis: Agent 1 (content) at **82 %** agreement with the human audit, Agent 2 (per-scenario) at **97 %** agreement — the highest agent-vs-human number across the entire PhysLit programme to date.

Total compute: 60 production calls + 120 judge calls + 49 resolver calls ≈ $25 USD. Reproducible from the `prereg-03_decay-locked` tag.

---

## 1. Design — the Decay World

### 1.1 Why a third framework, and why this one

`v0.1` (Aristotelian Mechanics) and `02_fmv` (F=mv counterfactual) each tested whether frontier models can induce rules they cannot retrieve from training data. v0.1 found P1 (Stage 1 induction failure) CONFIRMED on the historical framework; `02_fmv` found P1 REFUTED on the counterfactual one — Claude and GPT both induced F=mv cleanly. The natural follow-up question is whether F=mv's REFUTED was a property of *counterfactual worlds in general*, or of *that particular counterfactual* (mechanical, single-domain, single-equation).

The Decay World is designed to push back against the "frontier models can do counterfactuals" reading by changing three load-bearing properties simultaneously:

1. **The rule binds to the directly measured quantity, not to a derived "energy".** Amplitude itself shrinks; orbital radius itself shrinks; temperature itself shrinks. There is no underlying conserved quantity to which the measured ones reduce. Standard physics, by contrast, almost always uses an underlying substrate (energy, momentum, action) to explain a derived measurement.
2. **The rule is universal across multiple domains.** Mechanical, thermal, rotational, and orbital domains all decay at the same per-second rate. A model that latches onto mechanical friction (one domain) cannot recover the universal rate; a model that latches onto Newton's law of cooling (thermal) misses the orbital decay.
3. **Every standard dissipative mechanism is explicitly closed off.** The observations are set in evacuated chambers, on smooth / polished tracks, with no contact, no air, no rubbing, no force along the direction of motion. A model that reaches for friction or drag is not just descriptively wrong — it is also evidentially wrong about the observations themselves.

The §3 banned-token list reflects this design. It contains friction, drag, damping, dissipation, viscous, air resistance, resistance, attenuation (mechanism), plus force, mass, acceleration, momentum, inertia (mechanics), plus physicist names and equation forms — about 25 distinct tokens. The model is told this list at Stage 1; reaching for any token is a §3 FAIL regardless of intent.

### 1.2 Framework artifacts (frozen at prereg lock)

- [`frameworks/03_decay/observations.md`](../../frameworks/03_decay/observations.md) — 10 hand-authored observations across six domains, with the universal per-second rate baked in via three quantitative anchors.
- [`frameworks/03_decay/ideal_induction.md`](../../frameworks/03_decay/ideal_induction.md) — Stage 1 judge criteria: §3 lexical banned-token test, §4 necessary conditions N1–N6, §5 disqualifying patterns P1–P7, §6 6-step halt-at-first-FAIL checklist. **§5 P2 was widened in this round** to catch *any* hidden-substrate framing (`X decays, all measured quantities derive from X`) regardless of substrate name — this is the design trap.
- [`frameworks/03_decay/pass_fail_criteria.md`](../../frameworks/03_decay/pass_fail_criteria.md) — Stage 2 / Stage 3 / Stage 4 criteria; Stage 3 binds each quantitative scenario to a numeric PASS range.
- [`frameworks/03_decay/prediction_tests.md`](../../frameworks/03_decay/prediction_tests.md) — five Stage 3 scenarios: 1 pendulum (10° → ~ 7.4°), 2 hot object cooling (290 K → ~ 219 K, *not* room temperature), 3 spinning top (100 → ~ 73 rad/s), 4 falling-body asymptote (~ 0.55 m terminal? — orbital target), 5 long-timescale qualitative (will it stop, and at what timescale).
- [`frameworks/03_decay/prompts/`](../../frameworks/03_decay/prompts/) — four model prompts (induction, formulation, prediction, meta) and four judge prompts (one per stage).

### 1.3 Pre-registration

The prereg ([`predictions/03_decay_prereg.md`](../../predictions/03_decay_prereg.md)) locks four predictions:

- **P1** — composite content-axis PASS count strictly less than 5/15. Anchored against two prior-round baselines: F=mv 9/15 (post-audit), Aristotelian 5/15 (post-audit, v0.1). Confirmed iff 03_decay's composite PASS is below both. The composite content axis is PASS iff Stage 1, Stage 2, and Stage 3 (all four scenarios) are PASS.
- **P2** — among Stage 1 trials that FAIL on a §5 disqualifying pattern, P2 (hidden-substrate framing) is cited strictly more times than any other §5 pattern individually. The Decay World was designed as a hidden-substrate trap; if any other §5 pattern dominates, the design hypothesis is mis-targeted.
- **P3** — across the 60 quantitative Stage 3 predictions, count(direction-correct, ratio-leaked) > count(direction-wrong). The leaked-ratio bucket also captures decline-to-commit responses (per prereg). This is a within-round ordering, not a percentage threshold.
- **P4** — count(over-claim = yes) > count(over-claim = no) across failure-containing trials. Tests whether the Decay World's unfamiliarity raises or lowers Stage 4 meta-cognitive calibration relative to the prior rounds' 66.7–70% rates.

Two existing prior baselines are referenced for P1 (F=mv 9/15, Aristotelian 5/15). No new baseline is locked; P1 is "strictly less than 5" rather than a numeric threshold.

---

## 2. Judging and the human audit

### 2.1 Dual-judge IRR

The two content judges (Anthropic-side, OpenAI-side; same prompts as 02_fmv but adapted to the Decay World framework) scored every Stage 1, Stage 2, and Stage 3 verdict. Stage 1-3 dual-judge IRR = **40.00% (18/45 units)**, triggering the `CLAUDE.md` 25% mandatory-audit threshold. The Stage 3 per-scenario layer added 32 further disagreements (verdict splits + direction splits + fabrication flags). Stage 4 over-claim added 4 more. Total: **54 cases** sent to human audit.

### 2.2 Pre-audit verdicts (lower bounds)

The unresolved-disagreements-as-PENDING pre-audit reading already pointed at four CONFIRMEDs (P1 was 0/13 composite-PASS lower-bounded; P2 was VACUOUS; P3 ≥ 15 vs 0; P4 ≥ 6 vs 5). The audit reverses none of those headlines but firms the counts and resolves the §5-pattern question for P2.

### 2.3 The audit

The full audit is in [`03_decay_audit_human_review.md`](./03_decay_audit_human_review.md). Headline:

| Part | Cases | Audit-resolved verdict distribution |
|------|-------|---------------------------------|
| A — content axis | 18 | 11 PASS / 7 FAIL |
| B — Stage 3 per-scenario | 32 | 24 decay-correct / 8 ratio-leaked / 0 direction-wrong |
| C — meta over-claim | 4 | 4 yes / 0 no |

All 18 Part A cases were the same split direction: Claude judge PASS, OpenAI judge FAIL. The audit found **16 of the 18** OpenAI judge FAIL clauses to be defective — either fabricated (the cited banned token does not appear as a substring in the response) or misclassified (a real word in the response that is not actually banned was labelled as a banned token). The two genuine FAILs the OpenAI judge identified were both Gemini Stage 2 P2 hits (C13, C14), where the rule scope did not include orbital radius and sideways speed served as the underlying decaying quantity — true §5 P2 hidden-substrate framing. The other two Stage 2 P2 FAILs (C8 GPT T0, C16 Gemini T1) were resolved by the audit against both judges' immediate citations: Claude said PASS, OpenAI cited a fabricated banned token, but the response in fact carried the §5 P2 pattern that neither judge flagged.

The 32 Part B cases largely follow the same split direction (Claude PASS / OpenAI FAIL) with the same diagnosis: OpenAI fabricated `damping` (B7–B9), `frictionless` (B19–B21), misclassified `weight` → `mass` (B4–B6), `insulation` → `inertia` (B10, B11), `factor` → `force` (B22–B24), `continuous` → `conservation` (B29–B32), `smooth` → §3 (B13, B14). The single direction-disagree case (B25, Gemini T3 s1) was a genuine model decline-to-commit — neither judge had a defensible specific quantitative prediction to grade against.

The 4 Part C cases all resolved over-claim = yes, against the OpenAI judge's call. Each of the four trials had at least one audit-confirmed Stage 1–3 FAIL that the model's Stage 4 self-assessment did not acknowledge.

---

## 3. Results

### 3.1 Per-trial matrix (post-audit)

The 15 trials × 3 stages + 4 scenarios + over-claim, after audit:

| Model | Trial | S1 | S2 | S3 overall | s1 | s2 | s3 | s4 | Over-claim | Composite |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-opus-4-7 | 0 | PASS | PASS | FAIL | FAIL (a) | FAIL (a) | FAIL (a) | FAIL (c) | yes | FAIL |
| claude-opus-4-7 | 1 | PASS | FAIL | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | no | FAIL |
| claude-opus-4-7 | 2 | PASS | PASS | FAIL | PASS (c) | PASS (c) | PASS (c) | FAIL (c) | yes | FAIL |
| claude-opus-4-7 | 3 | FAIL | PASS | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | yes | FAIL |
| claude-opus-4-7 | 4 | PASS | FAIL | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | no | FAIL |
| gpt-5.5-2026-04-23 | 0 | PASS | FAIL | FAIL | PASS (c) | PASS (c) | PASS (c) | FAIL (c) | yes | FAIL |
| gpt-5.5-2026-04-23 | 1 | FAIL | FAIL | FAIL | FAIL (c) | PASS (c) | PASS (c) | FAIL (c) | no | FAIL |
| gpt-5.5-2026-04-23 | 2 | PASS | PASS | FAIL | PASS (a) | PASS (c) | PASS (a) | FAIL (c) | yes | FAIL |
| gpt-5.5-2026-04-23 | 3 | FAIL | FAIL | FAIL | FAIL (a) | PASS (c) | PASS (c) | FAIL (c) | no | FAIL |
| gpt-5.5-2026-04-23 | 4 | FAIL | FAIL | FAIL | FAIL (a) | FAIL (c) | FAIL (c) | FAIL (c) | yes | FAIL |
| gemini-3.1-pro-preview | 0 | PASS | FAIL | FAIL | PASS (a) | PASS (c) | PASS (c) | FAIL (a) | no | FAIL |
| gemini-3.1-pro-preview | 1 | FAIL | FAIL | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | yes | FAIL |
| gemini-3.1-pro-preview | 2 | FAIL | FAIL | FAIL | PASS (a) | PASS (a) | PASS (a) | FAIL (c) | yes | FAIL |
| gemini-3.1-pro-preview | 3 | FAIL | FAIL | FAIL | FAIL (a) | PASS (a) | PASS (a) | FAIL (a) | yes | FAIL |
| gemini-3.1-pro-preview | 4 | FAIL | FAIL | PASS | PASS (a) | PASS (a) | PASS (a) | PASS (a) | yes | FAIL |

Source tags: `(c)` = pre-audit judge consensus; `(a)` = audit-resolved.

The two failure paths identified in [`03_decay_findings.md`](./03_decay_findings.md) — Stage 1 / Stage 2 outright FAIL, and the falling-body-asymptote Scenario 4 — kill every trial. Scenario 4 (orbital radius / falling-body asymptote, PASS range 0.45 m – 0.65 m, target ≈ 0.55 m) FAILs in **14 of 15 trials** by judge consensus; the lone exception (gemini t4) has S1 and S2 both consensus FAIL. No DISAGREE-resolution path through Part A flips any trial to composite PASS.

### 3.2 P1 — Decay World is harder than both priors  ·  **CONFIRMED**

Composite content PASS = **0/15**. Refuted bound was ≥ 5; confirmed bound was < 5. The Decay World is the hardest of the three frameworks tested in PhysLit so far:

| Framework | Composite content PASS (post-audit) |
|---|---|
| Aristotelian (v0.1) | 5/15 |
| F=mv (02_fmv) | 9/15 |
| Decay World (03_decay) | **0/15** |

Per-model composite (post-audit): Claude 0/5 · GPT 0/5 · Gemini 0/5. The hardness is uniform across vendors — no model carried the framework. By contrast, on F=mv, Claude and GPT both went 5/5 on Stage 1 induction; the Decay World denied every model a composite PASS regardless of vendor.

### 3.3 P2 — Hidden-substrate framing is the modal §5 pattern  ·  **CONFIRMED**

Across the 8 Stage 1 post-audit FAIL trials, the first-FAIL clause distribution is:

| First-FAIL clause | Count |
|---|---|
| §4 N4 (per-system τ, no universal constant) | 4 |
| §6.3 coverage (truncation, obs 8 incomplete) | 2 |
| §5 P2 (hidden-substrate framing) | **1** |
| §4 N6 (rate does not match the ≈ 0.99/s anchor) | 1 |

Of the 8 Stage 1 FAILs, **§5-pattern hits = 1**, and that hit is P2 (Gemini T1, where the rule scope was speed and orbital radius was derived from sideways speed). P2 is therefore strictly more than any other §5 pattern individually (1 > 0), satisfying the prereg's strictly-greater bar. P2 is CONFIRMED.

Two qualifications are honest to record:

1. **Sample size is one.** The strictly-greater bar is met at 1 P2 vs 0 P1/P3–P7, but the §5 denominator is 1/8 FAILs — most Stage 1 FAILs were §4 (N4 / N6) or §6.3 (coverage). §5 patterns are not the modal Stage 1 first-FAIL category; N4 is.
2. **The Stage 2 pattern is much stronger and supports the design hypothesis.** Three of the four Stage 2 §5 FAILs (C8 GPT T0, C13 Gemini T0, C14 Gemini T1) are P2 hidden-substrate — the model imports standard orbital mechanics and derives radius from sideways speed, treating speed as the underlying decaying quantity. C16 (Stage 1) is the same pattern. The hidden-substrate trap fired four times in this experiment; it fired *late* (Stage 2 formulation under pressure to write operational rules), not at Stage 1. This is a substantive finding that the prereg's Stage-1-only scoring window did not anticipate. A future round should consider widening P2 to Stage 1 + Stage 2 combined.

### 3.4 P3 — Ratio-leaked > direction-wrong  ·  **CONFIRMED**

Across the 60 quantitative Stage 3 predictions:

| Bucket | Pre-audit consensus | Audit-resolved | **Total** |
|---|---|---|---|
| decay-correct | 13 | 24 | **37** |
| direction-correct, ratio-leaked | 15 | 8 | **23** |
| direction-wrong | 0 | 0 | **0** |

Ratio-leaked (23) strictly greater than direction-wrong (0). P3 CONFIRMED.

The direction-wrong bucket is *empty*. Not a single model gave a wrong-direction answer in 60 quantitative predictions — no claim of "stays constant", no claim of growth, no claim of approach-to-ambient. Every Stage 3 response in the experiment correctly named that *something* decays. What models *cannot* do is supply the right ratio when the framework rule (`A(t) = A(0) · 0.99^t`) differs from the standard-physics expectation. Two failure sub-modes within ratio-leaked dominate:

- **Decline to commit** — the model identifies a scope issue (orbital outside its declared rule scope, no `r_pendulum` value supplied) and declines to give a number. Per prereg, decline-to-commit lands in ratio-leaked, since the prediction-stage prompt forbids merely-directional answers. Six of the 8 audit-resolved Part B FAILs are decline-to-commit (B15, B16, B18, B25, B28, plus the orbital scope refusals).
- **§3 pollution** — Claude T0's Stage 3 response uses "forced" in Scenario 4, which fails §3 (whole-response scope). The same one banned token in Scenario 4's body fails Scenarios 1–3 too (B1, B2, B3) even though those three scenarios' own predictions were within PASS range. This is the §3 whole-response scope rule (carried in from 02_fmv) operating as designed but with sharp consequences.

### 3.5 P4 — Over-claim > correct self-identify  ·  **CONFIRMED**

Among 15 failure-containing trials (every trial in this experiment contains at least one Stage 1–3 FAIL — the universe is the full 15):

- over-claim **yes** = **10**
- over-claim **no** = **5**

P4 CONFIRMED (10 > 5). The over-claim rate is **67 %**, sitting in the same band as the two prior rounds:

| Framework | Over-claim rate (post-audit) |
|---|---|
| Aristotelian (v0.1 P3) | 70 % |
| F=mv (02_fmv P2) | 66.7 % |
| Decay World (03_decay P4) | 67 % |

Three frameworks, three CONFIRMED meta-cognitive over-claim rates in the 65–70 % band. The Decay World's increased conceptual unfamiliarity did **not** lower the over-claim rate — neither up nor down by more than 3 percentage points. This is a candidate paper-level behavioural regularity in its own right and is independent of P1 / P2 / P3.

---

## 4. Methodology findings

### 4.1 OpenAI judge §3 stress-test failure

On the Decay World, the OpenAI content judge fabricated or misclassified §3 banned-token citations in **16 of 18 Part A FAIL clauses (89 %)**. Specifically:

- **Fabricated** (cited token does not appear in the response): `resistance` (C4, C6), `deceleration` (C5), `frictionless` (B19–B21), `damping` (B7–B9), `force` from "Reinforcing" (C16 — the spurious morphological substring match).
- **Misclassified** (real word from the response wrongly labelled as banned): `fired` → `force` (C7), `influences` → `force` (C11), `preserved` → `conservation` (C2, C3), `radiation` → §3 (C12; `radiation` is not on the §3 list), `factor` → `force` (B22–B24), `continuous` → `conservation` (B29–B32), `weight` → `mass` (B4–B6), `insulation` → `inertia` (B10, B11), `heating` → `heat` (C12), `pulled` → `force` (C1), `imported` → `momentum` (C14), `smooth` → §3 (B13, B14), `adding` → `acceleration` (C15).

The pattern is consistent with a single failure mechanism: **the OpenAI judge performs semantic association rather than substring matching, even though §3 is explicitly defined as a purely lexical test** (`ideal_induction.md` §3, second paragraph: "literal token match"). The trigger appears to be the combination of (a) a long ban list (20+ tokens) and (b) heavy semantic overlap between the framework's vocabulary and the banned concepts (the Decay World is *about* the absence of damping / dissipation / friction; responses naturally describe these absences). The Claude judge made essentially the same call as a human auditor: literal substring scan, no semantic association.

`evidence_check.py` (`prereg-03_decay-locked` Gap 4 fix) caught most fabricated citations (the `FAB` flags in the worksheet). It cannot catch misclassification, where the judge found a real word and labelled it wrongly. Roughly half the OpenAI defects are of each kind.

The OpenAI judge's defect rate on this round is the highest in the project so far: 22 % agreement on per-scenario judgments, 33 % on content stage verdicts. By contrast, on v0.1 Aristotelian the OpenAI judge was the **more** reliable of the two (68 % agreement). The two failure modes (v0.1's verdict-field self-contradiction, 03_decay's §3 fabrication) are different; the cross-framework reversal is now systematic across three rounds.

### 4.2 Judge reliability does not transfer (three data points)

| Framework | Claude judge agreement | OpenAI judge agreement | More reliable |
|---|---|---|---|
| v0.1 Aristotelian | 32 % | 68 % | OpenAI |
| 02_fmv F=mv | 79 % | 21 % | Claude |
| 03_decay (Part A content) | 67 % | 33 % | Claude |
| 03_decay (Part B per-scenario) | 81 % | 22 % | Claude |
| 03_decay (Part C meta) | 50 % | 50 % | tied |

The pattern is now systematic: **the relatively more reliable judge depends on the framework**. PhysLit's dual-judge IRR + human audit safeguard is doing real work — selective use of either judge alone would have produced unsafe results on at least one of these three rounds.

### 4.3 Agent 2 is the strongest LLM resolver tested

Two non-canonical LLM resolvers ran against the locked criteria as a side analysis:

| Agent | Cases | Agreement with human audit |
|---|---|---|
| Agent 1 (content axis) | 17 (one unparseable) | **14 / 17 = 82 %** |
| Agent 2 (per-scenario) | 32 | **31 / 32 = 97 %** |

Agent 2's 97 % is the highest agent-vs-human number in PhysLit so far. The per-scenario classification task — numeric range check + direction call — appears to be well-matched to a frontier LLM resolver. The lone disagreement (B25 Gemini T3 s1) was a direction-grading edge case where Agent 2 graded direction-wrong and the audit graded n/a (decline-to-commit); both are reasonable readings.

Agent 1's 82 % is dragged down by the same §3 OpenAI fabrications the human audit had to unwind. Agent 1 was asked to resolve content-stage disagreements; on cases where the OpenAI judge cited a fabricated token, Agent 1 sometimes followed the OpenAI line. The methodology implication is that an LLM resolver inherits the judge defects of the dual-judge layer beneath it; the audit threshold is not removable.

### 4.4 The §3 whole-response scope rule has sharp consequences

§3's whole-response scope was carried in from 02_fmv as a closed methodological question. On 03_decay it shows up sharply in B1–B3: Claude T0's Scenario 4 contains "forced", and that single token disqualifies Scenarios 1–3 in the same response even though Scenarios 1–3's own predictions are within PASS range. The rule is operating as written, but it cost Claude T0 three otherwise-correct ratio answers. Future framework designers should weigh whether per-scenario scoping or whole-response scoping is more faithful to the construct being measured.

---

## 5. Cross-framework comparison

### 5.1 P1 across three frameworks

| Framework | Composite content PASS | What it tells us |
|---|---|---|
| Aristotelian (v0.1) | 5/15 | Historical framework — models can partially induce |
| F=mv (02_fmv) | 9/15 | Single-equation counterfactual — frontier models recover it |
| Decay World (03_decay) | **0/15** | Universal-rate counterfactual — every model fails |

The Decay World validates the design intuition behind the third counterfactual: the difficulty step from F=mv to Decay is larger than F=mv → Aristotelian. The two design features that drove the harder result are (a) the rule binds to the directly measured quantity (no underlying substrate) and (b) the rule is universal across multiple domains. Together they require a model to override its strongest standard-physics prior (energy conservation) *and* induce a single rate across disparate domains.

### 5.2 P4 over-claim rate across three frameworks

| Framework | Over-claim rate | Sample (failure-containing trials) |
|---|---|---|
| v0.1 P3 | 70 % | 10/15? (v0.1 had multiple FAIL types) |
| 02_fmv P2 | 66.7 % | 8/12 |
| 03_decay P4 | 67 % | 10/15 |

Three rounds, three frameworks, the same band. This is not a within-framework finding; it is a candidate behavioural regularity about frontier models. PhysLit's main hypothesis here is not that this rate is invariant (the sample sizes are small) but that it does not improve when the framework gets harder. The Decay World is conceptually harder than F=mv, but the over-claim rate is essentially the same. Stage 4 self-assessment is approximately framework-independent for these three models in this paradigm.

### 5.3 Dual-judge IRR across three rounds

| Round | Stage 1-3 IRR | Audit triggered? | Defect mechanism on the failing side |
|---|---|---|---|
| v0.1 Aristotelian | 36.67 % | yes | Claude judge mis-reading §3 (density ambiguity) |
| 02_fmv F=mv | 26.67 % | yes (just over) | OpenAI verdict-field self-contradiction (5/14 cases) |
| 03_decay | 40.00 % | yes | OpenAI §3 fabrication / misclassification (16/18 Part A) |

Across three rounds, IRR has risen, not fallen. The IRR is not a quality signal of the judge model; it is a quality signal of the *framework × judge × criteria* combination. The Decay World's long §3 list with strong topic overlap is a stress test the OpenAI judge fails; on F=mv (much shorter ban list, less semantic overlap) the same model performed adequately on §3 but failed elsewhere. PhysLit's design — mandatory human audit when IRR > 25 % — has caught this on every round.

---

## 6. Discussion

### 6.1 What the four CONFIRMEDs mean together

The four CONFIRMEDs are not independent. P1 (composite content PASS = 0/15) is partly downstream of the §3 "whole-response scope" rule firing on B1–B3 and the universal Scenario 4 failure; P3 (ratio-leaked > direction-wrong) is partly downstream of the decline-to-commit behaviour models adopt when the scope of their inferred rule does not include the scenario's target quantity (e.g. orbital radius); P4 is roughly framework-independent at this rate. P2 is the cleanest test of the *design hypothesis* — the hidden-substrate trap was real, and it did fire — but the small Stage 1 §5 sample (1 hit) means the strongest evidence comes from Stage 2 outside the prereg scoring window.

The package supports the strongest reading of the round: **the Decay World denies every frontier model a composite content PASS**, the failure modes are *consistent with the trap the framework was designed to spring* (hidden substrate, decline-to-commit on out-of-scope quantities, training-data ratio import), and the meta-cognitive over-claim rate stays in the 65–70 % band that two prior frameworks already established.

### 6.2 The §3 stress test reframes the methodology contribution

The most generalisable finding of this round is **not** a prereg verdict — it is the OpenAI judge §3 stress-test failure. PhysLit's dual-judge + audit pipeline caught the failure cleanly (IRR 40 % > 25 % threshold → human audit → 16/18 OpenAI clauses overturned), but a less safe methodology — selective use of one judge, or omission of the audit — would have produced systematically wrong content verdicts on this framework. This is a contribution to the literature on LLM-as-judge: long, semantically-overlapping ban lists are a failure trigger; literal substring matching is not robustly performed by all frontier models even when the prompt explicitly asks for it.

### 6.3 Cost-effectiveness

The audit cost about $25 in judge + agent compute, plus the human audit time. The audit overturned 18 + 14 = 32 of 54 LLM-judge verdicts, including 23 of the OpenAI judge's calls in Part A + Part B. PhysLit's "publish every trial verbatim + run human audit on > 25 % IRR" policy is doing work that no single-judge benchmark could reproduce.

### 6.4 Limitations

- **N = 5 trials per (model, stage).** PhysLit reports counts descriptively and does not claim statistical significance. P1's 0/15 is sharp at this N, but the 1 vs 0 P2 Stage 1 §5 distinction is a single data point.
- **P2 Stage-1-only scoring window.** The prereg fixes the §5 aggregation to Stage 1 first-FAILs. The strongest §5 P2 evidence (Stage 2 formulation) sits outside the scoring window. A v0.4 prereg should consider expanding to Stage 1 + Stage 2 jointly.
- **OpenAI judge §3 defect is framework-specific.** The 16/18 fabrication rate may not transfer to other frameworks with shorter or less-overlapping ban lists; the rate is a property of the Decay World, not necessarily of the OpenAI model in general.
- **Claude judge is not validated independently.** The audit treated the Claude judge as the more reliable of the two on this round, but its 67 % / 81 % Part A / Part B agreement with the audit still has room for unflagged systematic error. A future round could test whether a third, independent judge agrees with the human audit at a higher rate.

---

## 7. Pointers

- Production runner: [`scripts/run_03_decay.py`](../../scripts/run_03_decay.py)
- Dual-judge pipeline: [`scripts/judge_03_decay.py`](../../scripts/judge_03_decay.py)
- Audit application: [`scripts/apply_03_decay.py`](../../scripts/apply_03_decay.py)
- Worksheet generator: [`scripts/build_03_decay_worksheet.py`](../../scripts/build_03_decay_worksheet.py)
- Resolver agents: [`scripts/run_agent1_03_decay.py`](../../scripts/run_agent1_03_decay.py), [`scripts/run_agent2_03_decay.py`](../../scripts/run_agent2_03_decay.py)
- Per-trial output JSONs + `.md` companions: `results/<model>/03_decay/{induction,formulation,prediction,meta}/`
- Per-trial judge verdicts: `results/<model>/03_decay/judgments/`
- Per-scenario resolved verdicts: `results/<model>/03_decay/scenario_resolved/`
