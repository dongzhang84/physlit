# Stage 4 Over-Claim on the Structure Arms — Findings

> **Type:** additive re-analysis (v0.2-style). No production trial was
> re-run; no sealed round's verdicts were modified.
> **Date:** 2026-06-22.
> **Producer:** `scripts/judge_meta_backfill.py --arm both`.
> **Raw verdicts:** `results/<model>/{02_fmv_2,01_aristotelian_3}/judgments/*_meta_*.json`.
> **Pending human audit:** [`stage4_structure_overclaim_audit_human_review.md`](./stage4_structure_overclaim_audit_human_review.md) (4 cases).

## Why

Decay World already reports Stage 4 over-claim on its structure-prompt arm
(its results table carries an Over-claim column). F=mv and Aristotelian
reported over-claim only on their earlier non-structure arm, because the
structure-prompt re-runs `02_fmv_2` and `01_aristotelian_3` generated
Stage 4 responses but never scored them. This round scores those existing
Stage 4 responses so all three frameworks report over-claim on the same
(structure-prompt) condition.

Each arm mirrors its own framework's original meta recipe, so the new
structure-arm number is same-recipe comparable to the published number on
the older arm:

- F=mv -> `frameworks/02_fmv/prompts/judge_meta.md` (injects pass/fail
  criteria, terse failure summary), as in the original `judge_02_fmv.py`.
- Aristotelian -> top-level `prompts/judge_meta.md` (no criteria, verbose
  failure summary), as in the original `judge_v0_1.py`.

## Denominator

Over-claim rate = (trials whose Stage 4 self-review claims no earlier error)
/ (failure-containing trials), where a failure-containing trial has at
least one of Stage 1-3 FAIL **post-audit**. The post-audit content-FAIL
set is taken from the paper's per-trial tables (Table for F=mv, Table for
Aristotelian), so the denominator matches the published composite tables.
Content-PASS trials receive a `vacuous` meta verdict and are excluded.

## F=mv structure arm (`02_fmv_2`) — 6 content-FAIL trials

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| Claude Opus 4.7 | 1 | PASS | FAIL | PASS | no |
| Claude Opus 4.7 | 2 | PASS | FAIL | PASS | **DISAGREE (M1)** |
| Gemini 3.1 Pro | 0 | FAIL | FAIL | PASS | yes |
| Gemini 3.1 Pro | 1 | FAIL | FAIL | FAIL | yes |
| Gemini 3.1 Pro | 2 | FAIL | FAIL | PASS | yes |
| Gemini 3.1 Pro | 4 | FAIL | PASS | PASS | **DISAGREE (M2)** |

Over-claim = **3/6 (50%) to 5/6 (83%)**, with 2 cases pending audit.
Reference: non-structure arm was 4/6 (67%).

## Aristotelian structure arm (`01_aristotelian_3`) — 9 content-FAIL trials

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| Claude Opus 4.7 | 0 | FAIL | FAIL | FAIL | yes |
| Claude Opus 4.7 | 1 | PASS | PASS | FAIL | yes |
| Claude Opus 4.7 | 2 | PASS | FAIL | PASS | no |
| GPT-5.5 | 3 | PASS | PASS | FAIL | yes |
| Gemini 3.1 Pro | 0 | FAIL | PASS | FAIL | yes |
| Gemini 3.1 Pro | 1 | FAIL | FAIL | FAIL | **DISAGREE (M3)** |
| Gemini 3.1 Pro | 2 | FAIL | FAIL | FAIL | **DISAGREE (M4)** |
| Gemini 3.1 Pro | 3 | PASS | FAIL | PASS | no |
| Gemini 3.1 Pro | 4 | FAIL | FAIL | PASS | yes |

Over-claim = **5/9 (56%) to 7/9 (78%)**, with 2 cases pending audit.
Reference: non-structure arm was 7/10 (70%).

## Cross-framework comparison (structure-prompt condition)

| Framework | Over-claim (structure arm) | Denominator | Older-arm reference |
|---|---|---|---|
| F=mv | 3-5 / 6 = 50-83% | 6 | 4/6 (67%) |
| Aristotelian | 5-7 / 9 = 56-78% | 9 | 7/10 (70%) |
| Decay World | 10 / 15 = 67% | 15 | (single arm) |

## Dual-judge disagreement

4 over-claim DISAGREE cases out of the 15 failure-containing trials across
the two arms (2 in F=mv, 2 in Aristotelian). All four hinge on one
interpretive question: the model partially acknowledges an imported
concept in a sub-answer (Q2) but rates overall standard-physics influence
as `None`/`Minor` at the headline (Q1/Q5). The Claude and OpenAI judges
split on whether the headline rating constitutes over-claim. The cases are
laid out for canonical human resolution in the audit worksheet linked
above. 0 fabrication flags. Total judge cost ~$3.06.

## Implication for the over-claim band

On the older arms the three frameworks sat in a narrow 67-70% band. On the
structure-prompt condition, with the smaller post-audit denominators (6, 9,
15), each framework still clusters around two-thirds, but the tight
"67-70% band" phrasing is no longer supportable at this granularity (one
trial is 11-17%). The midpoints of the two pending ranges are both 67%
(F=mv 4/6, Aristotelian 6/9), so the exact landing depends on the four
audit verdicts. The paper text should be revised from "narrow 67-70% band"
to a looser "all three cluster around two-thirds" claim, with the final
numbers set after audit.

## Provenance (sealed rounds, not modified)

The older-arm over-claim numbers remain canonical at their sealed tags and
are unchanged by this round:

- F=mv non-structure arm 4/6: `analysis/fmv/02_fmv_findings.md`.
- Aristotelian non-structure arm 7/10: `analysis/aristotelian/v0_1_findings.md`.
- Decay 10/15: `analysis/decay/03_decay_findings.md`.

This round adds the structure-arm over-claim that those rounds did not
score. It does not edit them.
