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
