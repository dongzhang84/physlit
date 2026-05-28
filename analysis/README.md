# PhysLit Analysis

Per-framework outputs from PhysLit's pre-registered evaluation rounds. Each framework subdirectory holds the findings, narrative reports, audit worksheets, and human-audit records produced by that framework's experiments.

| Subdirectory | Framework | Difficulty | Composite content PASS | Sub-rounds |
|---|---|---|---|---|
| [`fmv/`](./fmv/) | F=mv counterfactual world | Easy | 9/15 | `02_fmv` · `02_fmv.1` · `02_fmv.2` |
| [`aristotelian/`](./aristotelian/) | Aristotelian Mechanics | Medium | 5/15 | `v0.1` · `v0.2` · `v0.2.1` · `v0.3` |
| [`decay/`](./decay/) | Decay World | Hard | 0/15 | `03_decay` |

Composite content PASS counts are post-audit, evaluated on the **canonical** content axis at temperature 0 across Claude Opus 4.7, GPT-5.5, and Gemini 3.1 Pro at N=5 trials each. See each framework's `*_report.md` for full methodology and per-trial detail.

## Naming conventions inside each subdirectory

| Pattern | Purpose |
|---|---|
| `<round>_report.md` | Human-readable narrative report — start here |
| `<round>_findings.md` | Auto-generated numerical block — pre- and post-audit verdicts, IRR, per-trial matrix |
| `<round>_audit_worksheet.md` | Human-audit input (dual-judge disagreement cases, side-by-side trial responses) |
| `<round>_audit_human_review.md` | Verbatim human verdicts on every audit case (canonical disagree resolution) |
| `<round>_agents_review.md` | Non-canonical LLM resolver (Agent 1 / Agent 2) results vs the human audit |
| `<round>_blog_post.zh.md` · `<round>_twitter_post.zh.txt` | Local-only Chinese popular-audience drafts (gitignored unless published) |
| `dryrun_findings.md` | Phase 1.5 dry-run output for that framework (lower-bound smoke test pre-lock) |

## Cross-framework navigation

For the overall project narrative across all three frameworks, see [`../README.md`](../README.md) and [`../CHANGELOG.md`](../CHANGELOG.md). The chronological history of every sub-round (what changed between v0.1 → v0.2 → v0.3, between 02_fmv → 02_fmv.1 → 02_fmv.2, etc.) is in the changelog.
