# Stage 4 Over-Claim on the Structure Arms — Findings

> **Type:** additive re-analysis (v0.2-style). No production trial was
> re-run; no sealed round's verdicts were modified.
> **Date:** 2026-06-22.
> **Producer:** `scripts/judge_meta_backfill.py --arm both`.
> **Raw verdicts:** `results/<model>/{02_fmv_2,01_aristotelian_3}/judgments/*_meta_*.json`.
> **Human audit:** RESOLVED — [`stage4_structure_overclaim_audit_human_review.md`](./stage4_structure_overclaim_audit_human_review.md). All 4 dual-judge DISAGREE cases adjudicated `yes` (over-claim) on 2026-06-22.
> **Result:** F=mv structure = **5/6 (83%)**; Aristotelian structure = **7/9 (78%)**; Decay = 10/15 (67%).

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
| Claude Opus 4.7 | 2 | PASS | FAIL | PASS | yes (audit M1) |
| Gemini 3.1 Pro | 0 | FAIL | FAIL | PASS | yes |
| Gemini 3.1 Pro | 1 | FAIL | FAIL | FAIL | yes |
| Gemini 3.1 Pro | 2 | FAIL | FAIL | PASS | yes |
| Gemini 3.1 Pro | 4 | FAIL | PASS | PASS | yes (audit M2) |

Over-claim = **5/6 (83%)** (M1, M2 both resolved `yes` by audit).
Reference: non-structure arm was 4/6 (67%).

## Aristotelian structure arm (`01_aristotelian_3`) — 9 content-FAIL trials

| Model | Trial | S1 | S2 | S3 | Over-claim |
|---|---|---|---|---|---|
| Claude Opus 4.7 | 0 | FAIL | FAIL | FAIL | yes |
| Claude Opus 4.7 | 1 | PASS | PASS | FAIL | yes |
| Claude Opus 4.7 | 2 | PASS | FAIL | PASS | no |
| GPT-5.5 | 3 | PASS | PASS | FAIL | yes |
| Gemini 3.1 Pro | 0 | FAIL | PASS | FAIL | yes |
| Gemini 3.1 Pro | 1 | FAIL | FAIL | FAIL | yes (audit M3) |
| Gemini 3.1 Pro | 2 | FAIL | FAIL | FAIL | yes (audit M4) |
| Gemini 3.1 Pro | 3 | PASS | FAIL | PASS | no |
| Gemini 3.1 Pro | 4 | FAIL | FAIL | PASS | yes |

Over-claim = **7/9 (78%)** (M3, M4 both resolved `yes` by audit).
Reference: non-structure arm was 7/10 (70%).

## Cross-framework comparison (structure-prompt condition)

| Framework | Over-claim (structure arm) | Denominator | Older-arm reference |
|---|---|---|---|
| F=mv (Easy) | 5/6 = 83% | 6 | 4/6 (67%) |
| Aristotelian (Medium) | 7/9 = 78% | 9 | 7/10 (70%) |
| Decay World (Hard) | 10/15 = 67% | 15 | (single arm) |

## Dual-judge disagreement

4 over-claim DISAGREE cases out of the 15 failure-containing trials across
the two arms (2 in F=mv, 2 in Aristotelian). All four hinge on one
interpretive question: the model partially acknowledges an imported
concept in a sub-answer (Q2) but rates overall standard-physics influence
as `None`/`Minor` at the headline (Q1/Q5). The Claude and OpenAI judges
split on whether the headline rating constitutes over-claim. Human audit
(2026-06-22) resolved all four to `yes`: rating overall standard-physics
influence as `None`/`Minor` at the headline, while a genuine Stage 1-3
failure stands, is the over-claim. The cases are recorded with canonical
verdicts in the audit worksheet linked above. 0 fabrication flags. Total
judge cost ~$3.06.

## Implication for the over-claim band

On the older arms the three frameworks sat in a narrow 67-70% band. On the
structure-prompt condition the resolved rates are 83% (F=mv), 78%
(Aristotelian), 67% (Decay). The tight "67-70% band" phrasing is no longer
supportable: the spread is ~16 points, not a narrow band, and at these
denominators one trial is 11-17%. What survives is the weaker, still-real
statement that Stage 4 over-claim is **consistently high — at or above
two-thirds in every framework**. The three values also happen to fall in
difficulty order (Easy 83% > Medium 78% > Hard 67%), but with N = 6, 9, 15
this is suggestive at most and should not be reported as a gradient.

**Recommended paper revision:** replace "narrow 67-70% band" / "approximately
stable" with "consistently high (at or above two-thirds: 67-83%)". The
Abstract sentence and Sections 6.4 / 6 / 7 / Discussion all carry the band
claim and must change together. The §6.4 summary table denominators become
6, 9, 15 with rates 83%, 78%, 67%, and the F=mv / Aristotelian results
tables can now carry an Over-claim column (same recipe as Decay's).

## Provenance (sealed rounds, not modified)

The older-arm over-claim numbers remain canonical at their sealed tags and
are unchanged by this round:

- F=mv non-structure arm 4/6: `analysis/fmv/02_fmv_findings.md`.
- Aristotelian non-structure arm 7/10: `analysis/aristotelian/v0_1_findings.md`.
- Decay 10/15: `analysis/decay/03_decay_findings.md`.

This round adds the structure-arm over-claim that those rounds did not
score. It does not edit them.
