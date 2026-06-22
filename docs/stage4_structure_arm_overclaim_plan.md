# PhysLit — Stage 4 Over-Claim on the Structure Arm — Plan

> **Status: PLANNING. Not a prereg. Not locked.**
> This document is the design under discussion. Nothing here is run
> until the design is approved.
>
> **Date:** 2026-06-22
> **Author note:** the sealed rounds (`prereg-02_fmv-locked`,
> `prereg-v0.1-locked`, the structure-arm treatment tags, and
> `prereg-03_decay-locked`) are not affected by anything in this
> document. Their verdicts stay as published. This is an additive
> re-analysis layer in the same spirit as v0.2.

---

## 1. Why this round exists

The Stage 4 over-claim rate is one of the paper's headline methodology
findings (the cross-framework stability band). Today the three
frameworks do not report it on the same condition:

- **Decay World** reports over-claim on its single structure-prompt arm
  (the `meta/` Stage 4 responses were scored, audited, and the table
  carries an Over-claim column).
- **F=mv** and **Aristotelian** report over-claim only from the earlier
  arm that did not carry the structure prompt. The structure-prompt
  re-runs (`02_fmv_2`, `01_aristotelian_3`) generated Stage 4 responses
  but those responses were never scored for over-claim.

Result: the cross-framework over-claim comparison currently puts two
frameworks measured on one condition next to a third measured on
another, and the F=mv / Aristotelian results tables cannot carry an
Over-claim column the way the Decay table does.

This round closes that gap by scoring Stage 4 over-claim on the
**structure-prompt arm** for F=mv and Aristotelian, so all three
frameworks report over-claim on the same condition, and the paper can
be told as a single structure-arm story.

---

## 2. Scope

This is an **additive re-analysis layer**. No new production trials are
run. No new framework is introduced.

What is reused (no new generation calls):

- Structure-arm Stage 4 responses, already on disk:
  - `results/*/02_fmv_2/meta/trial_{0..4}_t0.0.json` (3 models × 5)
  - `results/*/01_aristotelian_3/meta/trial_{0..4}_t0.0.json` (3 models × 5)
- Structure-arm content-axis verdicts and human audit, already on disk:
  - `analysis/fmv/02_fmv_2_findings.md`, `02_fmv_2_audit_human_review.md`
  - the Aristotelian structure-arm equivalents

What is added (new judge calls only, no new model trials):

- Dual-judge over-claim classification (Claude + GPT) on the
  failure-containing trials of each structure arm
- Human audit on the dual-judge DISAGREE cases only, to match the
  post-audit standard the Decay over-claim number already meets

---

## 3. What "over-claim" means here (unchanged definition)

For a failure-containing trial (at least one of Stage 1-3 is a FAIL),
the Stage 4 self-assessment is classified as **over-claim** when it
claims that no earlier error occurred. The over-claim rate is the
fraction of failure-containing trials in that state. This is the same
definition already locked in each framework's pre-registration and
already applied to Decay.

---

## 4. Procedure

1. **Confirm the scoring tooling.** Locate the existing dual-judge
   over-claim procedure used for the Decay round (the `15 × 2` over-claim
   verdict pass) in `scripts/`, plus the over-claim judge prompt
   template. Confirm it still runs.
2. **Determine the denominators.** From the existing structure-arm
   `content_resolved` verdicts, list the failure-containing trials per
   framework (composite is 6/15 on each structure arm, so expect about 9
   failure-containing trials per framework).
3. **Score over-claim.** Run the two judges independently on the Stage 4
   `response_text` of each failure-containing trial. Write every verdict
   verbatim into `results/` (open-data rule: failures and disagreements
   are committed too).
4. **Audit disagreements only.** Compute the dual-judge disagreement
   rate. Audit just the DISAGREE cases and record a canonical verdict for
   each. Over-claim is close to a binary judgment, so the disagreement
   set is expected to be small (plausibly zero). This matches the
   post-audit basis of the Decay number; it does not re-audit agreements.
5. **Compute and record.** Produce the per-framework structure-arm
   over-claim rate. Write a re-analysis findings file documenting the
   numbers, the disagreement rate, and the audited cases. Do not edit any
   sealed round file.

### Effort and cost

- Trials to score: about 9 per framework × 2 ≈ 18.
- Judge calls: dual-judge × 18 ≈ 36.
- API cost: roughly $1-4, the same order as v0.2.
- Human audit: only the DISAGREE cases, expected 0-3 trials.
- This is deliberately kept to the same workload class as the prior
  re-analysis round.

---

## 5. Paper changes once the numbers are in

Order is **numbers first, prose second**: score the structure arm, look
at whether the stability band still holds, then edit.

Content that depends on the new numbers:

- **§6.4 over-claim.** Replace the F=mv and Aristotelian numbers with the
  structure-arm values (denominators move from 6 and 10 to about 9 and
  9; Decay stays 15). Update the summary table, the prose, and the
  Abstract band figure if it shifts. Whatever the band turns out to be is
  what gets reported.
- **Tables for F=mv and Aristotelian.** Add an Over-claim column from the
  structure-arm data, so both match the Decay table.

Content that is editing only (the "make the paper clearer" pass):

- Stop using the word **baseline** in the paper narrative. Present all
  three frameworks as the structure-prompt condition. The earlier-arm
  data stays in the open-data repo (not deleted, no selective
  publishing); it is simply no longer foregrounded as a separate arm.
- Rewrite or remove the §6 opening two-arm bookkeeping paragraph.
- Rewrite the §7 Discussion sentence about treatment versus baseline
  arms.
- Pre-registration tags appendix: the git tags are sealed and keep their
  names, but the prose labels can drop the baseline framing.
- Sync all four versions (`latex_tmlr`, `latex_en`, `docs/paper_en.md`,
  `latex_cn`), then compile.

---

## 6. Open decisions (to settle before block B editing)

1. **The "structure prompt lifted composite" comparison.** It currently
   leans on the earlier arm as the "before". Without the baseline
   framing, drop the comparison or keep one sentence?
2. **Judge-reliability finding (§6.2).** It currently sits on the earlier
   arm. First check whether the structure-arm audit files already contain
   the judge-versus-human disagreement data needed to re-tabulate it on
   the structure arm. If they do, move it; if not, decide separately.
3. **Earlier-arm data.** Confirmed intent is "not foregrounded in the
   paper", not "deleted from the repo".

---

## 7. Execution order

1. Block A: score the structure-arm Stage 4 over-claim (this document,
   §4).
2. Review the numbers and whether the band holds.
3. Block B: the paper rewrite (§5), once the numbers are locked.
