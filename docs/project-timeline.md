# PhysLit — Project Timeline

A development timeline of the PhysLit project, reconstructed from the git
commit history. It documents the order in which the work was done: all
experimental rounds were pre-registered and sealed *before* the manuscript
was written, which is the discipline the paper relies on.

- **Span:** 2026-05-04 → 2026-06-30 (about 8 weeks)
- **Main repository:** 538 commits
- **Shape:** the first ~3 weeks (May) were experiments; the last ~5 weeks
  (late May to late June) were writing and polishing.

---

## Phase 1 — Setup and infrastructure
**May 04 – May 08 (~5 days)**

Repository created, Phase 0 configuration, Tier 1 simulators and the trial
runners brought up. Light activity (2–10 commits per day).

## Phase 2 — Experiments: three worlds, seven sub-rounds
**May 09 – May 22 (~2 weeks, the intensive core)**

Each round is anchored by a locked, SHA-256-sealed pre-registration tag:

| Date | Locked tag | Framework / round |
|---|---|---|
| May 09 | `prereg-v0.1-locked` | Aristotelian, initial round |
| May 13 | `prereg-v0.2` / `v0.2.1` | Aristotelian, additive re-analysis |
| May 18 | `prereg-02_fmv` / `02_fmv.1` | $F=mv$, initial round + structural axis |
| May 19 | `prereg-02_fmv.2` | $F=mv$, structure-prompt round |
| May 20 | `prereg-v0.3` | Aristotelian, structure-prompt round |
| May 22 | `prereg-03_decay` | Decay World |

Peak activity on May 18 (60 commits in one day); May 17–22 ran 27–60 commits
per day. **By May 22 every experimental round was locked and sealed.**

## Phase 3 — Analysis and paper writing
**May 26 – June 12**

Per-round results were first consolidated into the `analysis/` findings
write-ups, after which the manuscript advanced through four versions, each
starting on a different date:

| Start | Version | Notes |
|---|---|---|
| May 28 | `docs/paper_draft.zh.md` | earliest Chinese Markdown draft |
| Jun 01 | `latex_cn` (Chinese LaTeX) | Chinese typeset version |
| Jun 10 | `docs/paper_en.md` | readable English Markdown |
| Jun 12 | `latex_tmlr` (TMLR draft) | the submission draft, main focus |

## Phase 4 — TMLR polish and finalization
**Jun 12 – Jun 29 (the long tail)**

Sentence-by-sentence polishing of the TMLR draft: Section 6 reorder, an
appendix on prompt architecture, Figure 1 expanded into the full
dual-judge / human-audit evaluation pipeline, and the Decay World Stage 3
scenarios reconciled against the locked pre-registration. Heaviest day
Jun 22 (main repo 34 commits, TMLR draft 17 commits).

## Phase 5 — arXiv submission
**Jun 30**

Manuscript finalized and prepared for arXiv submission.

---

## One-line summary

First three weeks (May) were experiments, all sealed by May 22. The last five
weeks (late May to late June) were writing and polish, advancing through
Chinese Markdown → Chinese LaTeX → English Markdown → TMLR draft, with the
final stretch concentrated on the TMLR submission.
