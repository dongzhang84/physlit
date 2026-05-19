# PhysLit 02_fmv.1 — Structural-Axis Report

> **Date:** 2026-05-18.
> **Scope:** the structural axis (N9–N12) applied to the 60 frozen `02_fmv` trials — 3 models × 5 trials, Stage 1 rule sets judged.
> **Prereg lock:** [`prereg-02_fmv.1-locked`](https://github.com/dongzhang84/physlit/releases/tag/prereg-02_fmv.1-locked).
> **Companion files:**
> - [`02_fmv_1_findings.md`](./02_fmv_1_findings.md) — judging report + post-audit numerical block.
> - [`02_fmv_1_structural_audit_human_review.md`](./02_fmv_1_structural_audit_human_review.md) — verbatim human verdicts on all 7 disagreement cases.
> - [`02_fmv_1_structural_audit_worksheet.md`](./02_fmv_1_structural_audit_worksheet.md) — the input the auditor worked from.
> - [`02_fmv_1_agent2_review.md`](./02_fmv_1_agent2_review.md) — case-by-case review of the non-canonical Agent 2 resolver.

This file is the human-readable narrative report. Code, prompts, raw
trial outputs, and judge verdicts are in the repo and cross-linked
below.

---

## Abstract

`02_fmv.1` is an **additive analysis layer** over the frozen `02_fmv`
content-axis experiment — exactly as v0.2 was a structural layer over
v0.1. It runs **no new tested-model trials**: it re-judges the same 60
F=mv trials under the **structural axis** (necessary conditions
N9–N12 — parsimony, independence, traceability, hierarchy), with the
verdict on each trial's **Stage 1 induction rule set**.

It carries one deliberate fix. The v0.2 Aristotelian structural
criteria counted rules across the **Stage 1 + Stage 2 combined**
output; because the Stage 2 prompt asks the model to restate its rules
mirroring the Stage 1 numbering, that doubled every count and produced
spurious N10 duplicates — which the v0.2 structural human audit
identified as the dominant cause of its 40 % structural IRR.
`02_fmv.1` scopes the rule set, the N9 count, and the N10 redundancy
check to **Stage 1 only**.

Two predictions were locked before judging:

- **P1** — the Stage-1-only fix lowers the structural-axis dual-judge
  IRR below v0.2 Aristotelian's 40 %.
- **P2** — the structural axis flips at least 1 of the 9
  all-content-PASS `02_fmv` trials to composite FAIL.

Post-audit results: **P1 REFUTED, P2 CONFIRMED.**

The headline is **P1 REFUTED**. The structural-axis IRR is **46.67 %
(7 of 15 trials)** — *higher* than the v0.2 Aristotelian 40 %, not
lower. The double-count fix did not reduce structural disagreement,
because the disagreements were never about counting. The human audit
shows all 7 splits were judgment calls on N10 redundancy, N11
fabrication, and the N12 hierarchy threshold — not arithmetic. This is
a publishable negative result: it refutes the double-count diagnosis
as the dominant cause of structural disagreement.

**P2 CONFIRMED, decisively.** 8 of the 9 all-content-PASS trials are
reclassified to composite FAIL by the structural axis. Only 1 of 15
trials survives as composite PASS. The structural axis is not a
marginal add-on here — it detects a failure mode the content axis is
entirely blind to.

Two methodology findings are as consequential as the predictions:

1. **Judge reliability reverses completely between the content and
   structural axes.** On the `02_fmv` content axis the Claude judge
   agreed with the human audit on 86 % of disagreements and the OpenAI
   judge on 21 %. On the `02_fmv.1` structural axis the order flips:
   the Claude judge 14 %, the OpenAI judge 86 %. Same two models, same
   framework, same trials — only the judgment task changed. Judge
   reliability is **task-dependent, not model-dependent.**
2. **Content quality and structural quality are anti-correlated.** GPT
   passed all 5 content axes but failed all 5 structural; Gemini
   failed all 5 content axes but passed 3 of 5 structural. A model
   that gets the physics right can still write a bloated, redundant
   rule set, and vice versa — the two axes measure genuinely
   different things.

Total compute: 30 structural-judge calls + 7 Agent-2 resolver calls ≈
$4.0 USD. No tested-model calls. Reproducible from the
`prereg-02_fmv.1-locked` tag.

---

## 1. Design — what we built and how we ran it

### 1.1 Relationship to `02_fmv`

`02_fmv.1` reuses the 60 `02_fmv` production trials, frozen at
`prereg-02_fmv-locked`. It runs no new tested-model trials and does
not modify any `02_fmv` content verdict — it reads them. It is
**post-hoc with respect to the trial data**: the same trials,
analysed under a new axis. New criteria, same data — a legitimate
methodological move, reported as such.

### 1.2 The structural criteria and the double-count fix

`frameworks/02_fmv/structural_criteria.md` defines N9–N12 as
necessary conditions on a Stage 1 rule set:

- **N9 parsimony** — rule count. >20 hard FAIL; >15 moderate FAIL;
  12–15 a soft signal (FAIL only combined with an N10/N11 violation).
- **N10 independence** — no two rules paraphrase the same operational
  claim about the same situation.
- **N11 traceability** — every rule traces to the observations; no
  fabricated mechanism. A generalisation that reconciles observations
  is permitted (induction working as intended).
- **N12 hierarchy** — a rule set of ≥ 5 rules must contain at least
  one explicit cross-rule reference (`Rule N`, `derived from`,
  `special case of`, …). Sets of < 5 rules are exempt.

The v0.2 double-count fix is §0 of the criteria: the rule set under
judgment, the N9 count, and the N10 check are all scoped to **Stage 1
induction**. Stage 2 is shown to the judge as context only and is
never counted; a Stage 1 rule matching its Stage 2 restatement is not
an N10 duplicate.

### 1.3 Protocol

Two structural judges — Claude Opus 4.7 and GPT-5.5, the same two
vendors as the `02_fmv` content judges — independently scored each of
the 15 trials, one PASS/FAIL verdict per trial, on a fresh API client
with a new session UUID, `temperature = 0` requested. Where the two
agree, that is the structural verdict; where they disagree, the case
is resolved by **human audit**. No LLM disagree-resolver feeds the
canonical verdict (`prereg-02_fmv.1-locked` §1).

The composite verdict per trial is `content_PASS AND structural_PASS`,
combining the inherited `02_fmv` post-audit content verdict with the
structural verdict.

### 1.4 Agent 2 — a non-canonical side analysis

In parallel, and explicitly **outside the prereg envelope**, an LLM
disagree-resolver ("Agent 2", `gemini-3.1-pro-preview`) was run over
the 7 structural disagreements — to be compared against the human
audit, exactly as Agent 1 was for the `02_fmv` content axis. Agent 2
verdicts do not feed P1 or P2.

---

## 2. Results — what we found

### 2.1 Judging and IRR

The two structural judges agreed on 8 of 15 trials and split on 7 — a
structural-axis **IRR of 46.67 %**, above the 25 % audit threshold and
above v0.2 Aristotelian's 40 %. All 7 disagreements were resolved by
human audit (`02_fmv_1_structural_audit_human_review.md`).

### 2.2 The audit

The audit pattern is stark. In 6 of the 7 splits the Claude structural
judge said PASS and the OpenAI judge said FAIL; in Cases 6 and 7
(Gemini) the order was reversed. The human auditor sided with the
OpenAI judge on 6 of 7 cases. The Claude judge's systematic error was
**over-leniency on N10 and N11** — it passed rule sets with genuine
paraphrase duplicates (Cases 2–5) and with a fabricated ground-push
mechanism (Case 1), reading the criteria's "lean PASS" guidance too
far. In Case 6 the Claude judge produced a verdict-field defect:
`verdict = FAIL` while its own reasoning text concluded PASS — the
same defect class the `02_fmv` content audit found in the OpenAI
judge.

### 2.3 Post-audit numbers — the two predictions

| Prediction | Verdict | Result |
|---|---|---|
| **P1** mechanical criteria lower the structural IRR | **REFUTED** | structural IRR 46.67 % — above v0.2's 40 %, not below |
| **P2** structural axis flips a content-PASS trial | **CONFIRMED** | 8 of 9 all-content-PASS trials flip to composite FAIL (threshold ≥ 1) |

### 2.4 Resolved per-trial matrix

| Model | Trial | Content | Structural | Composite |
|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | PASS | **PASS** |
| `claude-opus-4-7` | 1 | FAIL | PASS | FAIL |
| `claude-opus-4-7` | 2 | PASS | FAIL *(audit)* | FAIL |
| `claude-opus-4-7` | 3 | PASS | FAIL *(audit)* | FAIL |
| `claude-opus-4-7` | 4 | PASS | FAIL *(audit)* | FAIL |
| `gpt-5.5-2026-04-23` | 0 | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 1 | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 2 | PASS | FAIL *(audit)* | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | FAIL | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | FAIL *(audit)* | FAIL |
| `gemini-3.1-pro-preview` | 0 | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | FAIL |
| `gemini-3.1-pro-preview` | 2 | FAIL | PASS *(audit)* | FAIL |
| `gemini-3.1-pro-preview` | 3 | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | FAIL *(audit)* | FAIL |

Structural axis PASS: 5/15. Composite PASS: **1/15** — only
`claude-opus-4-7` trial 0.

### 2.5 What the numbers mean — substantive findings

**Finding 1 — the double-count fix did not lower the structural IRR
(P1 REFUTED).** The Stage-1-only scoping was predicted to reduce
dual-judge disagreement below v0.2's 40 %. It rose to 46.67 %. The
human audit explains why: not one of the 7 disagreements was an
arithmetic split. Both judges counted Stage 1 rules identically in
every case (10, 11, 10, 15, 14, 4, 5). They split on **judgment** —
whether two rules paraphrase one operational claim (N10), whether a
rule fabricates a mechanism (N11), whether a 5-rule set needs an
explicit cross-reference (N12). The v0.2 double-count was a real
defect and worth fixing, but it was not the dominant cause of
structural disagreement. The dominant cause is that N10 and N11 still
require a substantive judgment call, and the two judges calibrate that
call differently — the Claude judge systematically lenient. A
mechanical *count* does not make a *redundancy* or *fabrication*
judgment mechanical.

**Finding 2 — the structural axis catches what the content axis
misses (P2 CONFIRMED).** 8 of the 9 trials that passed all three
content stages fail the structural axis. GPT passed every content
axis with rule sets of 14–15 rules carrying paraphrase duplicates;
the content axis has no parsimony or independence criterion, so it saw
nothing wrong. Three Claude trials (2, 3, 4) likewise passed content
but carry an N10 duplicate or an N11 fabrication. The structural axis
is not redundant with the content axis on this framework — it earns
its place.

**Finding 3 — content and structural quality are anti-correlated.**

| Model | Content-PASS | Structural-PASS |
|---|---|---|
| `claude-opus-4-7` | 4/5 | 2/5 |
| `gpt-5.5-2026-04-23` | 5/5 | 0/5 |
| `gemini-3.1-pro-preview` | 0/5 | 3/5 |

GPT got the physics right every time and wrote the worst-structured
rule sets; Gemini got the physics wrong every time and wrote the
cleanest. The two axes are measuring different competences — physical
correctness vs. the discipline of a parsimonious, traceable rule set —
and a model can be strong on one and weak on the other. Reporting only
a content pass rate would have hidden GPT's structural failure
entirely.

### 2.6 Methodological findings

**Judge reliability reverses completely across axes.** Combining the
`02_fmv` content audit with this one:

| Axis | Claude judge vs human | OpenAI judge vs human |
|---|---|---|
| Content (`02_fmv`, 14 cases) | 86 % (12/14) | 21 % (3/14) |
| Structural (`02_fmv.1`, 7 cases) | 14 % (1/7) | 86 % (6/7) |

Same two model versions, same framework, same trials, same audit
standard — only the judgment *task* changed, and the reliability
ordering inverted. A judge validated on one task cannot be assumed
reliable on another. This strengthens the `02_fmv` content finding
("judge reliability does not transfer across frameworks") into a
sharper claim: it does not transfer across *tasks* either. Judge
selection must be re-validated per axis, not once per project.

**Agent 2 — a mechanical criterion makes the LLM resolver reliable
again.** Agent 2 (`gemini-3.1-pro-preview`, non-canonical) agreed with
the human audit on **6 of 7** structural disagreements (86 %). Its one
miss is Case 3, where it passed a rule set the human failed on a
self-acknowledged N10 restatement. This echoes the `02_fmv` content
result (Agent 1 at 100 %) and stands against v0.2 Aristotelian (Agent
1 at 29.4 %): on mechanically-specified criteria an LLM resolver
reproduces the human verdict at a high rate; on interpretation-laden
criteria it does not. Agent 2 did not feed P1/P2 — but as a side
analysis it is consistent evidence that criteria specificity, not
resolver capability, governs LLM-resolver reliability.

### 2.7 A design limitation, disclosed

The N12 hierarchy criterion treats a rule set of exactly 5 rules as
requiring an explicit cross-reference (Case 7, Gemini t4, failed on
this). A set of 5 clean, independent, observation-traceable rules is
arguably good induction without forced cross-references. The < 5
exemption threshold could be raised (e.g. to < 7) in a future
revision. This does not affect the `02_fmv.1` verdicts — the criteria
are frozen at the locked commit — but is recorded here as a known
limitation.

### 2.8 Cost and reproducibility

| Component | Calls | Cost (est., USD) |
|---|---|---|
| Structural dual-judge (2 × 15) | 30 | ~3.6 |
| Agent 2 side analysis | 7 | ~0.4 |
| **Total** | **37** | **~4.0** |

Well within the prereg's ≤ $15 estimate; no tested-model calls. Every
structural verdict and every Agent-2 record is committed under
`results/<model>/02_fmv/structural{,_resolved}/`. The round reproduces
from the `prereg-02_fmv.1-locked` tag.

---

## 3. Next steps

### 3.1 Make the structural judgment more mechanical

P1 refuted the double-count diagnosis: the residual disagreement is
N10/N11 judgment, not counting. A future structural criteria revision
should attack the judgment itself — e.g. an explicit, enumerated test
for "paraphrase duplicate" (as §3's banned-token test is for content),
rather than relying on the judge's sense of redundancy. Whether that
lowers the IRR would be the natural P1 of a `02_fmv.2`.

### 3.2 Raise the N12 small-set exemption

Per §2.7, lift the hierarchy exemption from < 5 to < 7 rules in the
next criteria version, with the change pre-registered and the affected
case (Gemini t4) re-scored under the new and old rule for comparison.

### 3.3 Per-axis judge validation

The content/structural reliability reversal means a judge must be
validated separately for each axis. A future round should run a small
labelled calibration set per axis before the production judging, and
pick the judge — or weight the two judges — per axis.

### 3.4 Publication

The `02_fmv.1` output set — 30 structural-judge verdicts, 7 audited
disagreements, the Agent 2 side analysis, the full composite table —
is committed in full. P1 (a negative result against the double-count
diagnosis) and the cross-axis judge-reliability reversal are
publishable independent of the physics-literacy result, and extend the
`02_fmv` LLM-as-judge methodology thread.

---

## Appendix — files and links

- Pre-registration: [`predictions/02_fmv_1_prereg.md`](../predictions/02_fmv_1_prereg.md) — tag `prereg-02_fmv.1-locked`
- Structural criteria: [`frameworks/02_fmv/structural_criteria.md`](../frameworks/02_fmv/structural_criteria.md)
- Structural judge prompt: [`frameworks/02_fmv/prompts/judge_structural.md`](../frameworks/02_fmv/prompts/judge_structural.md)
- Structural judge verdicts: `results/<model>/02_fmv/structural/`
- Agent 2 (non-canonical) verdicts: `results/<model>/02_fmv/structural_resolved/`
- Numerical findings: [`02_fmv_1_findings.md`](./02_fmv_1_findings.md)
- Human audit: [`02_fmv_1_structural_audit_human_review.md`](./02_fmv_1_structural_audit_human_review.md), worksheet [`02_fmv_1_structural_audit_worksheet.md`](./02_fmv_1_structural_audit_worksheet.md)
- Agent 2 case review: [`02_fmv_1_agent2_review.md`](./02_fmv_1_agent2_review.md)
- Runners / tools: `scripts/judge_structural_02_fmv.py`, `build_02_fmv_1_structural_worksheet.py`, `apply_02_fmv_1_audit.py`, `run_agent2_02_fmv.py`, `build_02_fmv_1_agent2_review.py`
