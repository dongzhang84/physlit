# PhysLit Analysis

A chronological log of every pre-registered sub-round PhysLit ran, what it
measured, and what the post-audit numbers came out at. The paper presents a
curated subset of these results; this directory holds the complete record.

All trials run at temperature 0 with N=5 per model on the same three frontier
models: Claude Opus 4.7, GPT-5.5 (`gpt-5.5-2026-04-23`), and Gemini 3.1 Pro
(`gemini-3.1-pro-preview`). Every sub-round is locked by a SHA-256-sealed
prereg and a git tag; numbers below are post-audit, canonical.

## Framework summary

| Subdirectory | Framework | Difficulty | Latest composite PASS | Sub-rounds |
|---|---|---|---|---|
| [`fmv/`](./fmv/) | F=mv counterfactual world | Easy | 6/15 (treatment arm, content ∧ structural) | `02_fmv` · `02_fmv.1` · `02_fmv.2` |
| [`aristotelian/`](./aristotelian/) | Aristotelian Mechanics | Medium | 6/15 (treatment arm, content ∧ structural) | `v0.1` · `v0.2` · `v0.2.1` · `v0.3` |
| [`decay/`](./decay/) | Decay World | Hard | 0/15 (content axis only) | `03_decay` |

"Composite" here means the conjunction of the content axis (Stage 1 + Stage 2 +
every Stage 3 scenario, judged on the framework's N1–N* necessary conditions
and banned-word list) and the structural axis (N9–N12: parsimony, independence,
traceability, hierarchy of the Stage 1 rule set). Decay World currently has the
content axis only; the structural axis has not been applied there.

## Sub-round log

Each row below is one locked prereg. **"Same trials"** means the round
re-judges an earlier round's trial JSONs and does not call any production API.
**"New trials"** means the round ran the full four-stage protocol from scratch
(15 trials = 3 models × 5 trials each).

### F=mv (`fmv/`)

| Tag | Locked | Purpose | Trials | Headline |
|---|---|---|---|---|
| `prereg-02_fmv-locked` | 2026-05-18 | **Content-axis baseline.** First end-to-end test of the F=mv framework. Judges Stage 1–3 on the framework's eight necessary conditions and the banned-word list. Tests P1 (induction failure), P2 (meta-cognitive over-claim), P3 (mechanical criteria reduce inter-rater disagreement), P4 (Stage 3 ratio leak). | new | 9/15 content-only PASS · over-claim 4/6 · Stage 3 ratio leak 0/45 |
| `prereg-02_fmv.1-locked` | 2026-05-18 | **Structural-axis layer.** Adds N9–N12 to the frozen `02_fmv` trials, no new production. Fixes the v0.2 Aristotelian double-count bug by scoping the rule count to Stage 1 only. Tests whether the structural axis catches failures the content axis missed. | same trials | 1/15 composite (content ∧ structural) · structural PASS 5/15 |
| `prereg-02_fmv.2-locked` | 2026-05-19 | **Axiomatization treatment.** Single-variable control experiment. The only change vs `02_fmv` is one paragraph added to the Stage 1 prompt asking the model to axiomatize its rule set (smallest set + mark rule-to-rule dependencies). Tests whether axiomatization raises the structural pass rate without degrading content. **This is the result the paper publishes for §3 ($F=mv$).** | new | 6/15 composite · content 9/15 · structural 11/15 |

### Aristotelian (`aristotelian/`)

| Tag | Locked | Purpose | Trials | Headline |
|---|---|---|---|---|
| `prereg-v0.1-locked` | 2026-05-09 | **Content-axis baseline + PhysLit v0.1 foundation.** The first PhysLit round. Established the four-stage protocol, the dual-judge architecture, the prereg-with-SHA-256 lock mechanism, and the human-audit pathway. Judges Stage 1–3 on eight Aristotelian necessary conditions and the banned-word list. Tests P1 (induction failure under training-data conflict), P3 (meta-cognitive over-claim). | new | 5/15 content-only PASS · over-claim 70% · content-axis IRR 36.67% (triggered human audit) |
| `prereg-v0.2-locked` | 2026-05-13 | **Structural-axis introduction.** First introduction of the N9–N12 structural axis to PhysLit. Re-judges the frozen `v0.1` trials with the new axis applied. Defines the rule-count, independence, traceability, and hierarchy checks. | same trials | 2/15 composite · structural PASS 8/15 · structural-axis IRR 40% |
| `prereg-v0.2.1-locked` | 2026-05-13 | **Throttling-fix patch, not a substantive new round.** Identical to `v0.2` in criteria, judges, and trial data; the only change is the non-canonical resolver-agent model, which swaps from `gemini-3.1-pro-preview` (sustained 503 throttle that afternoon) to `gemini-2.5-pro` (generally available, one generation behind). Documented because PhysLit's open-data rule forbids silent model changes. | same trials | unchanged from `v0.2` |
| `prereg-v0.3-locked` | 2026-05-20 | **Axiomatization treatment.** Direct parallel of `02_fmv.2` on the Aristotelian framework. Same axiomatization paragraph added to the Stage 1 prompt. Tests whether the axiomatization effect observed on `02_fmv` transfers to a multi-principle, training-data-saturated framework. **This is the result the paper publishes for §4 (Aristotelian).** | new | 6/15 composite · content 6/15 · structural 15/15 |

### Decay World (`decay/`)

| Tag | Locked | Purpose | Trials | Headline |
|---|---|---|---|---|
| `prereg-03_decay-locked` | 2026-05-22 | **Content-axis baseline on the hardest framework.** Tests a four-domain (mechanical, thermal, rotational, orbital) exponential-decay rule with no underlying substrate. Twelve observations span all four domains; banned-word list bans every standard dissipation mechanism. Judges Stage 1–3 on the Decay World necessary conditions. The structural axis has not been applied to this framework. | new | 0/15 content-only PASS |

## Naming conventions inside each subdirectory

| Pattern | Purpose |
|---|---|
| `<round>_report.md` | Human-readable narrative report — start here |
| `<round>_findings.md` | Auto-generated numerical block: pre- and post-audit verdicts, IRR, per-trial matrix |
| `<round>_audit_worksheet.md` | Human-audit input: dual-judge disagreement cases with side-by-side trial responses |
| `<round>_audit_human_review.md` | Verbatim human verdicts on every audit case (canonical disagree resolution) |
| `<round>_agents_review.md` | Non-canonical LLM resolver (Agent 1 / Agent 2) results vs the human audit |
| `<round>_blog_post.zh.md` · `<round>_twitter_post.zh.txt` | Chinese popular-audience drafts (local-only unless published) |
| `dryrun_findings.md` | Phase 1.5 dry-run output for that framework (lower-bound smoke test pre-lock) |

## Reading order

1. **Headline numbers across all frameworks**: the framework summary table above.
2. **What changed between sub-rounds**: the sub-round log above, plus [`../CHANGELOG.md`](../CHANGELOG.md).
3. **Per-framework deep dive**: each subdirectory's `<round>_report.md`.
4. **Raw post-audit verdicts and per-trial matrices**: each subdirectory's `<round>_findings.md`.
5. **Disagree-case audit trail**: each subdirectory's `<round>_audit_human_review.md`.
6. **Project-wide methodology and design rules**: [`../docs/product-spec.md`](../docs/product-spec.md), [`../CLAUDE.md`](../CLAUDE.md).
