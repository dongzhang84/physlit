# 03_decay Dry-Run Findings — Pre-Lock

> **Status:** v1 — written 2026-05-22 immediately after the run.
> **Scope:** exploratory, single-trial, single-model. **Not 03_decay production data.**
> **Run identifier:** `results/_dryrun/20260522T073027Z/claude-opus-4-7/03_decay/`

## 1. What we did

Ran `claude-opus-4-7` once through the four-stage protocol on the Decay
World, with a fresh API client and new session UUID per stage. Total
spend ≈ **$0.7273** (estimated; Anthropic invoice authoritative).
Output is four `trial_0_t0.0.json` files under the run-identifier
directory above (induction / formulation / prediction / meta).

The Stage 1 prompt carries the axiomatisation cue baked in by default
(prereg `predictions/03_decay_prereg.md` §1.2). The four
framework-facing prompts are the locked candidate templates at HEAD
(`frameworks/03_decay/prompts/stage{1,2,3,4}_*.md`); judging was not
run.

## 2. Stage-by-stage assessment

### Stage 1 — Induction

**§3 banned-token sweep** (against the actual 03_decay list, not the
v0.1 fallback `scan_for_banned` uses): **clean** — no banned tokens in
the response.

**Rule structure.** Two rules:
- Rule 1: "Universal multiplicative fading of motion" — names the
  correct multiplicative-per-time shape across pendulum, spring,
  falling, bell, sphere, shot, marble, top. Cites every observation.
- Rule 2: "The fading rate depends on how slow the motion is, not on
  weight or material." Claims the per-second fractional loss is set
  by the system's characteristic slowness; states the rate is
  **not** weight- or material-dependent.

**N4 violation candidate (load-bearing for judging).** Rule 2 makes
the per-second rate *system-dependent* — slower motions fade faster
per second. The Decay World's N4 requires the per-second rate be
**universal across systems** (≈ 0.99/s for the spring, the cup of
tea, and the spinning top alike). Claude's Rule 2 is, on the page,
incompatible with N4.

However, **Stage 3 then uses a single universal k ≈ 0.0101 /s across
the pendulum, the spinning flywheel, and the idealised pendulum**. The
model's *operational* belief tracks N4 even though its *stated rule*
does not. This is an internal Stage 1 ↔ Stage 3 tension that the
content judge should catch as an N4 FAIL at Stage 1 (per
`ideal_induction.md` §2 N4 and §7's "judged by meaning"; Rule 2's
slowness-dependent rate is not equivalent to a universal rate).

**No §5 disqualifying pattern was triggered.** Most notably, **no
hidden-substrate framing (§5 P2)** appears in Stage 1 — the framing is
direct: the *motion-quantity itself* fades multiplicatively, not "some
underlying X fades and the measured quantity follows". This is a
positive signal that the rule statement landed on the right shape
even though N4 is mis-stated.

### Stage 2 — Formulation

**§3 banned-token sweep:** clean.

**Operationalisation.** Restates Rule 1 as `Q(t) = Q(0) · exp(−k·t)`
and frames `k > 0` as a per-second fractional loss rate. Good.

**Concept-import issue (Stage 2 P5 territory).** Stage 4's own Q2
self-identifies four concept imports that crept in:

- `g`, defined as "the pull's strength in speed-per-second" — a
  steady gravity-like acceleration constant. Not a §3 banned token
  ("acceleration" was avoided by paraphrase), but Stage 2's "Do not
  import additional concepts" forbids it.
- `v* = g/k` as a terminal-velocity balance — a derivation, not an
  observation.
- `T = 2π / spin-rate` as the spin period (introduced in Stage 3 but
  derived from Stage 2 Rule 2's slowness scaling).
- `absolute hotness Θ(t) (in K)` with an explicit zero point — the
  observations gave Kelvin numerically, but Stage 2 framed it as an
  *absolute scale with a meaningful zero*.

These are concept imports that the Stage 2 prompt's "Do not import
additional concepts" paragraph explicitly forbids. **Whether
`judge_stage2.md` actually flags these — given that they evade §3
lexically — is the load-bearing question** for whether the prereg's
concept-import discipline is mechanically enforceable. This is the
key issue to verify before lock.

### Stage 3 — Prediction

**§3 banned-token sweep:** clean.

**Quantitative scenarios (S1–S4) with ratio binding:**

| Scen | Claude's headline | Decay PASS target | Decay PASS range | Verdict |
|------|-------------------|-------------------|------------------|---------|
| 1 | **7.4°** | ≈ 7.4° | 6.5°–8.5° | **DECAY PASS** |
| 2 | **218 K** | ≈ 219 K | 200–240 K | **DECAY PASS** |
| 3 | **73 rad/s** | ≈ 73 rad/s | 60–90 rad/s | **DECAY PASS** |
| 4 | **declines** | ≈ 0.55 m | 0.45–0.65 m | **does not fit any P3 bucket cleanly** |

**Scenario 5 (qualitative + timescale):** Says "does not swing
forever" + gives `t ≈ 456 s` — both halves PASS (timescale 300–700 s
range; not-forever wording). **DECAY PASS.**

**Scenario 4 problem (Gap 1 below).** The model says "the radius
decreases monotonically and would eventually reach the center" but
explicitly **declines to commit to a specific number**, citing its
own Stage 2 Rule 3 boundary note. The prereg's three-bucket P3
classification (`decay-correct` / `direction-correct, ratio-leaked` /
`direction-wrong`) does not have a slot for "direction correct + no
number given".

### Stage 4 — Meta

(Stage 4 is exempt from §3; banned tokens here are expected and not
counted toward FAILs.)

**Q1 — Single coherent framework?** Yes (defensible).

**Q2 — Concepts imported?** Correctly identifies all four imports
listed under Stage 2 above (`g`, `v* = g/k`, `T = 2π/spin-rate`,
absolute hotness with K). **Strong self-identification.**

**Q3 — Stage 3 predictions follow from Stage 2 rules?** Correctly
identifies that Scenarios 1, 3, and 5 reuse `k ≈ 0.0101 /s` for
unspecified-length pendulums and the top, which Stage 2 Rule 2 had
said was not pinned down. **Strong self-identification of internal
inconsistency.**

**Q4 — Differences from default physics.** Mentions "no conservation
of energy or momentum", "no friction, drag, or radiation", "absolute
temperature decays intrinsically", "v* = g/k arises from balancing
gravity against motion-decay, not against air resistance". Uses
several §3 banned tokens here — **expected, Stage 4 is exempt**.

**Q5 — Standard-physics influence:** "moderate". Self-rates honestly.

**Provisional over-claim verdict:** **no** (correct
self-identification). If this trial had at least one Stage 1–3 FAIL
under the judges, P4's denominator would include it but the
numerator would not.

## 3. Provisional verdicts at this single data point (informational only)

This is N=1 from one model and **does not pre-empt the prereg
evaluation.** Recorded for transparency.

- **P1 (composite content PASS):** likely **FAIL** for this trial.
  Probable Stage 1 N4 FAIL (Rule 2 slowness-dependent rate
  contradicts N4 universality); probable Stage 2 concept-import FAIL
  (`g`, `v* = g/k`, `T = 2π/spin-rate`); definite Stage 3 FAIL
  (Scenario 4 declines, S1 ∧ S2 ∧ S3 cannot be all-PASS even before
  considering the concept-import question).
- **P2 (modal §5 pattern):** no §5 pattern triggered on this trial,
  so it contributes nothing to the P2 distribution. In particular
  **no hidden-substrate framing** appeared — direct counter-evidence
  to the design hypothesis on N=1.
- **P3 (direction-correct, ratio-leaked vs direction-wrong):** S1,
  S2, S3 are decay-correct (not in either failure bucket). S4 does
  not fit cleanly — **Gap 1 below**.
- **P4 (over-claim):** this trial's Stage 4 correctly
  self-identifies → "no" over-claim → contributes against
  confirmation of P4 if the trial counts as failure-containing.

## 4. Gaps surfaced; decisions to make before prereg lock

### Gap 1 — P3 fourth bucket for "declined to commit"

The prereg's P3 three-bucket classification does not have a slot for
"direction correct, no number given". Claude declined Scenario 4
explicitly, citing its own rules' lack of a geometric-rate
derivation. Two ways to resolve:

- **(a)** Widen `direction-correct, ratio-leaked` to mean "named the
  direction but did not land in the Decay PASS range — including
  failures-to-commit". Strict reading of the current prereg text
  arguably already permits this ("any ratio outside Decay PASS range"
  → "no ratio" trivially outside).
- **(b)** Add an explicit fourth bucket `declined` and report it
  separately. Cleaner but locks a new classification before the
  production run.

Recommendation: **(a)** with one explicit sentence added to the
prereg's P3 scoring paragraph clarifying that
no-quantitative-commit counts as `direction-correct, ratio-leaked`
when the direction was named. This avoids adding a bucket and
matches the spirit of "ratio binding" (a non-committal answer is at
least as far from `decay-correct` as a wrong ratio).

### Gap 2 — Stage 2 concept-import enforcement

Claude's Stage 2 introduced `g`, `v* = g/k`, and "absolute hotness
Θ(t) with K" without using any §3 banned token. The Stage 2 prompt
forbids importing concepts; whether `judge_stage2.md` actually
flags these requires inspection of the Stage 2 judge prompt before
lock.

Recommendation: dry-run the Stage 2 judge against this dry-run
trial before locking the prereg, and reinforce `judge_stage2.md` if
it would have missed the imports.

### Gap 3 — N4 mis-statement vs universal application

Claude's Rule 2 says the per-second rate is slowness-dependent
(violating N4 as written), but Stage 3 uses a universal `k`. The
judges should catch this as N4 FAIL by "judged by meaning" (§7).
But this case wasn't in the §6 6-step checklist's worked
examples — worth confirming the judge prompt is alert to it.

Recommendation: spot-check the Stage 1 judge by running it against
this dry-run trial before lock, to confirm it flags Rule 2 as N4
FAIL. If it doesn't, tighten the judge prompt or the criteria
wording.

## 5. Cost and pipeline

- Pipeline ran end-to-end without error.
- Per-stage costs (approx): induction $0.1455, formulation $0.2258,
  prediction $0.1576, meta $0.1985. Total $0.7273.
- The 02_fmv-style runner pattern transferred cleanly. Scenario
  parsing on `frameworks/03_decay/prediction_tests.md` returned 5
  scenarios as expected.

No deviation from the drafted methodology was observed. Pre-lock
revisions (if any) should fall under §4 above.

## 6. Stage 1 + Stage 2 judge dry-run (added 2026-05-22)

Ran the two content judges (`claude-opus-4-7` Anthropic judge,
`gpt-5.5-2026-04-23` OpenAI judge) over the Phase-1.5 trial's
Stage 1 and Stage 2 responses, using the locked candidate judge
prompts at HEAD. Total spend ≈ **$0.5016**. Verdict JSON under
`results/_dryrun/20260522T073027Z/claude-opus-4-7/03_decay/judgments_dryrun/`.

### Stage 1 — induction judge verdicts

**Claude judge — FAIL at Step 2, clause N4.**

> Evidence: "I have given hotness its own fading rate (≈ 0.01/s)
> separate from the mechanical fading rate... the water's
> per-second fractional loss is about ten times smaller."
>
> Reasoning: "The response explicitly states different per-second
> fading rates for hotness vs. mechanical motion, violating N4
> (universality of a single rate across all closed systems). Rule
> 2 also ties the per-second rate to the period/characteristic
> slowness of motion, further violating N4."

This is a **clean catch on Gap 3.** Claude judge identified
exactly the N4 violation the design hypothesis predicted, citing
both load-bearing components: (a) Rule 2's slowness-dependent
per-second rate, and (b) a separately-quantified mechanical-vs-thermal
rate split that appears in the trial's "Tensions" section. (The
trial author had also miscomputed the thermal rate as ~10× slower
than the mechanical rate, when both are ≈ 0.99/s — Claude judge
caught the symptom; the model's arithmetic mistake is upstream of
the N4 statement.)

**OpenAI judge — FAIL at Step 1, claimed clause "banned: resistance".**

> Evidence: `air resistance`
>
> Reasoning: "The response contains the banned phrase/token
> 'air resistance' in the Tensions section. Under §3, banned
> tokens are a purely lexical test applied to the whole response,
> so this triggers FAIL at Step 1."

**This is a hallucination.** A full-text grep of the Stage 1
response for `air resistance` / `resistance` / `friction` / `drag`
/ `damping` / any §3 banned token returns no matches. The only
occurrence of the substring "air" in the response is "no surrounding
air" (and "air" is not on the 03_decay §3 list). The OpenAI judge
fabricated evidence and cited a non-existent banned token to justify
a FAIL.

The verdict is FAIL either way (Claude says FAIL on N4, OpenAI says
FAIL on §3), so the dual-judge verdict-level IRR is **agreement** on
this trial — but the **reason** disagrees substantively.

### Stage 2 — formulation judge verdicts

**Claude judge — FAIL on the numerical-operational-rate criterion.**

> Evidence: `k = k(T), with k(T₂) > k(T₁) when T₂ > T₁.`
>
> Reasoning: "The model treats the per-second rate k as a function
> of the system's characteristic time T rather than a single universal
> rate (~0.99/s). This violates universality (N4) and means a third
> party cannot compute later values for arbitrary systems without
> an unspecified k(T) function; the rate is not operational as a
> single universal multiplicative rule. Additionally, hotness is
> given a separate constant κ rather than the same universal rate."

Another clean N4 catch in operational form. Claude judge does the
same work at Stage 2 it did at Stage 1.

**OpenAI judge — FAIL with self-doubting reasoning citing
non-existent banned-token substrings.**

> Failed criterion: "No banned token appears anywhere in the
> response (`ideal_induction.md` §3)."
>
> Evidence: `speed components`
>
> Reasoning: "The banned-token list includes `momentum`, and its
> morphological variants are banned; `components` contains the
> token `momentum` as a substring? More directly, the response
> also uses `bodies`, `body`, and `orbiting bodies`, but these
> are not banned. The automatic lexical failure is triggered by
> the banned token `spin-rate`?"

**Multiple hallucinations:** `components` does not contain the
substring `momentum`; `spin-rate` is not on the §3 banned list; the
reasoning is literally written as questions to itself (`?` punctuation,
"More directly..."), indicating the judge model is uncertain and
fabricating. OpenAI judge says FAIL but the stated grounds are not
true.

### Reading on the three pre-judge-dry-run gaps

**Gap 3 (Stage 1 N4 mis-statement) — RESOLVED for Claude judge,
problematic for OpenAI judge.**

- Claude judge catches N4 cleanly with the right evidence — no
  prompt change needed for Claude.
- OpenAI judge also returns FAIL, so the dual-judge composite is
  still FAIL, but the OpenAI judge fabricates §3 evidence. In
  production this would (a) inflate the apparent §3 hit rate
  spuriously, distorting any P2-style §3-pattern distribution we
  might compute, and (b) cause dual-judge **reason** divergence
  even when the verdict agrees, which the judge_02_fmv aggregator
  flagged as IRR-clean but the §5-pattern distribution (P2 of the
  03_decay prereg) would record under the wrong pattern.

**Gap 2 (Stage 2 concept imports `g`, `v* = g/k`, `absolute hotness`) —
NOT TESTABLE from this trial.**

The §6 / Stage 2 judging halts at the first FAIL. Both judges halted
on N4 (Claude correctly, OpenAI on a fabricated §3) before reaching
the "do not import additional concepts" check. To test whether the
concept-import discipline is mechanically enforceable, we would need
a trial that passes N4 *and* has imports — not feasible from this
single Phase-1.5 trial. Gap 2 remains **unresolved** going into
production, but the production run itself will surface evidence.

**Gap 4 (NEW) — OpenAI judge fabricates §3 banned-token evidence.**

The OpenAI judge is hallucinating banned-token substrings on this
trial. Both Stage 1 and Stage 2 OpenAI verdicts cite evidence that
either (a) does not appear in the response, or (b) is a false
substring claim (`components` containing `momentum`). The mechanical
§3 lexical test is the load-bearing methodological innovation of the
02_fmv arc; if the OpenAI judge is systematically fabricating
matches, the §3 IRR may agree at verdict-level for the wrong reasons.

Options for pre-lock mitigation:

- **(i)** Tighten `judge_stage1.md` / `judge_stage2.md`: add a rule
  that any §3 FAIL must quote a verbatim substring that the judge
  itself can locate in the response — and that uncertain reasoning
  ("?" punctuation, "More directly...") is itself disqualifying.
- **(ii)** Switch the OpenAI judge to a different OpenAI model
  variant (e.g. higher reasoning tier) — but per the prereg the
  judges are pinned, so this would be a methodology change.
- **(iii)** Accept the hallucination as a known judge limitation,
  publish per-judge §3 hit rates separately, and rely on the human
  audit on the (verdict-level) disagree cases to clean up.
- **(iv)** Add a post-judge mechanical re-check: a Python script
  that programmatically scans the trial response for the cited
  evidence substring; if the cited evidence is not actually in the
  response, flag the verdict as judge-fabrication for audit.

Recommendation: **(i) + (iv)** — tighten the prompt to require
verbatim substring evidence (prompt-level discipline), AND add a
mechanical post-check that verifies cited evidence actually appears
in the response (programmatic backstop). This combination addresses
the hallucination at both the natural-language and structural
levels without changing the judge model pin.

### Decisions to make before prereg lock (updated)

| Gap | Resolution |
|-----|-----------|
| 1 — P3 fourth bucket | Decided: option (a) — "declines to commit" goes into `direction-correct, ratio-leaked`; add one clarifying sentence in prereg §2 P3 scoring paragraph. |
| 2 — Stage 2 concept imports | Not testable from this trial; accept that production data will reveal it. No prompt change pre-lock; revisit if production trials reveal the judges miss imports. |
| 3 — N4 mis-statement | Claude judge catches it cleanly. No Claude-side prompt change needed. |
| 4 — OpenAI judge §3 fabrication (NEW) | Pre-lock: tighten judge prompts to require verbatim-substring evidence + add mechanical post-check that the cited evidence appears in the response. |
