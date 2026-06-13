# PhysLit

> Read this first. PhysLit is a research artifact, not a product.
> Code decisions optimize for **methodological auditability**, not user experience.

---

## Current Phase (2026-06): write-up and TMLR submission

The experimental phase is **closed**. All three frameworks (F=mv,
Aristotelian, Decay World) have been run, audited, and sealed. We are
not running new trials. The active work is the paper.

- **Headline metric**: composite PASS = content ∧ structural axis,
  from the axiomatization-prompt arm. F=mv **6/15**, Aristotelian
  **6/15**, Decay World **0/15** (content axis only). The content-only
  **9/15** figures in older per-round notes are a different axis, not
  an error — see the `[paper]` entry in `CHANGELOG.md`.
- **Manuscripts**: `latex_tmlr/` is the TMLR submission draft and the
  main battleground (its own git repo, gitignored from this repo).
  `latex_en/` and `latex_cn/` are parallel English/Chinese LaTeX
  versions; `docs/paper_en.md` is the readable Markdown port.
- **Next step**: the deferred pre-submission polish pass tracked in
  `latex_tmlr/tmlr_feedback_gpt_v1.txt` (GPT review + per-item response),
  then submit to TMLR.
- `README.md` and the `CHANGELOG.md` `[paper]` entry are the source of
  truth for current status.

---

## Tech Stack

- **Language**: Python 3.13, strict typing throughout (`mypy --strict`)
- **Dep mgmt**: `uv` — never use pip / poetry / conda in this repo
- **Package layout**: `src/physlit/` (src layout, not flat)
- **Schema validation**: pydantic v2 (BaseModel for every input/output structure)
- **AI SDKs**: `anthropic`, `openai`, `google-genai`
- **Templating**: Jinja2 (static-site rendering only)
- **Testing**: pytest
- **Lint/format**: ruff (single source for both)
- **CI**: GitHub Actions
- **Hosting**: GitHub Pages (static site only — no backend)

**No backend. No database. No auth. No web app.** All data is committed JSON; all output is a static HTML capability matrix.

---

## Architectural Rules (these are load-bearing)

### Phenomenon generation

- **Tier 1** (Python simulator) where the framework is mathematically codable — F=mv, reverse gravity, 1/r gravity, slow light, energy decay, etc.
- **Tier 3** (manual authorship) for conceptual frameworks — Aristotelian, phlogiston, observer-dependent, Lamarckian.
- **Tier 2** (AI-generated) is **disabled in v0.1**. The architectural slot exists but the class raises `NotImplementedError`. Reason: contamination ambiguity between generator-AI and tested-AI. Deferred to v0.5 with concrete mitigation plan.

### Pre-registration is irreversible

- Every round has its own `predictions/<round>_prereg.md`, locked via `scripts/lock_prereg.sh` which writes the file's SHA-256 into its header and tags `prereg-<round>-locked` (e.g. `prereg-v0.1-locked`, `prereg-02_fmv-locked`, `prereg-03_decay-locked`).
- `scripts/verify_prereg_integrity.py` runs as a pre-commit hook AND in CI. Any silent edit to a locked prereg fails the commit. **Never edit any locked prereg** — links inside become stale over time (e.g. after directory reorganizations), but the file's canonical content stays sealed.
- A new prereg version requires a new tag (`prereg-<round>.1-locked`) and an explicit "deviation from prereg" notice in published results.

### N=5 trials, fresh sessions — enforced in code

- `src/physlit/runners/base.py` orchestrates trials. Each trial creates a fresh API client + new session UUID.
- **Multi-turn or context reuse across stages is forbidden at this layer.** Reject any PR that shortcuts this for cost reasons. The methodology depends on it.
- N=5 is a parameter; do not lower it without an explicit pre-registration revision.

### Model version pinning

- Every runner pins the exact model version string the Anthropic / OpenAI / Google API exposes — never a family alias like `claude-opus`. As of 2026-05-08, Opus 4.7 is published only under the bare alias `claude-opus-4-7` (no date suffix); when a date-stamped variant ships, the pin must be updated to match.
- After each API call, runners verify `response.model == config.model_id` and raise on mismatch. Silent version drift is a methodology bug.

### Open data verbatim

- Every prompt sent → committed to `prompts/` (versioned).
- Every response received → committed to `results/<model-version>/<framework>/<stage>/trial_N_t<temp>.json`.
- Selective publishing is forbidden. If a trial fails on the API side, the failure record is also committed.

### Inter-rater reliability

- Pass/fail judgments where semantic interpretation is needed run through **two LLM judges** (Claude + GPT) independently. Disagreement rate per phenomenon set is published as a methodology-quality indicator.
- Disagreement rate > 25% on any framework triggers human audit before public release.

---

## Python Patterns

- Prefer `pathlib.Path` over `open()` strings everywhere.
- Use pydantic for all data schemas — never plain dicts crossing module boundaries.
- Pure functions where possible. Side effects (API calls, file I/O) confined to runners and scripts.
- Async only where the API call itself is async; otherwise sync. Don't wrap synchronous logic in async for no reason.
- Type hints everywhere; `from __future__ import annotations` for forward refs.
- `dataclass` with `frozen=True` or pydantic `BaseModel` — pick one per module, don't mix.

---

## Determinism Contract (for Tier 1 simulators)

Every Tier 1 simulator must satisfy:

1. Same seed → byte-identical output across machines and Python versions
2. No external API calls (HTTP, file system writes, time-dependent state)
3. No `random.random()` without explicit seed
4. `tests/test_simulators.py` enforces byte-identity with two consecutive runs

If a simulator can't be deterministic, escalate it to Tier 3 (manual). Don't ship a flaky generator.

---

## Cost Awareness

- Frontier-model API calls add up. PhysLit's accumulated spend across 7 sub-rounds and 3 frameworks is ≈ $90 USD total (per-round figures recorded in each round's `analysis/<framework>/<round>_findings.md`). Each new round budgets independently — there is no single project-wide cap, but a per-round prereg must state expected cost before lock.
- **Phase 1.5 dry run** (Claude single-trial, < $1) precedes every prereg lock. Dry-run output goes to `results/_dryrun/<timestamp>/`, never to `results/<model-version>/`. See `docs/implementation-guide.md` Phase 1.5.
- `scripts/estimate_cost.py` runs before any production model batch. `replicate.sh` requires confirmation when the estimate exceeds **$5**.
- CI never runs real API calls — only mocks in `tests/test_runners_with_mock.py`.
- Every result file records the actual cost. Cross-round headline costs (production + judge): v0.1 ≈ $14 · v0.2 (additive re-analysis, no production) ≈ $4 · `02_fmv` ≈ $17 · `02_fmv.1` ≈ $4 · `02_fmv.2` ≈ $5 · v0.3 ≈ $7 · `03_decay` ≈ $25.

---

## Known Gotchas

- **uv lockfile is committed**: `uv.lock` is part of the repo. `pip install -e .` won't reproduce results — always use `uv sync`.
- **API SDK alias drift**: anthropic SDK may resolve a family alias (e.g. `claude-opus`) to whichever current 4.x build is latest. Always pin the most specific version string the API exposes — currently `claude-opus-4-7` for Opus 4.7, with a date suffix once Anthropic publishes one.
- **Pre-commit on first install**: after `uv sync`, run `uv run pre-commit install` once to hook into git.
- **Empty directories**: `frameworks/`, `predictions/`, etc. use `.gitkeep` until populated. Don't delete the placeholder before adding real content — Git will lose the directory.
- **Tests don't catch prereg drift**: only `verify_prereg_integrity.py` does. CI must run it; pytest alone is not enough.

---

## Don'ts

- ❌ **Never modify `predictions/v0_1_prereg.md` after lock.** New version → new file + new tag.
- ❌ **Never use multi-turn conversation across stages.** Stage 1, 2, 3 are independent fresh sessions.
- ❌ **Never use `claude-opus-latest` or any alias.** Always full version string.
- ❌ **Never `git push --force` to main.**
- ❌ **No async without justification.** Most of this code is offline batch — sync is fine.
- ❌ **No Tier 2 AI generator in v0.1.** Architectural stub only.
- ❌ **No selective result publishing.** All trials published, including failures.

---

## Environment Variables

```bash
# Tested-model APIs
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=

# Judge APIs (recommend separate keys for budget tracking)
ANTHROPIC_JUDGE_KEY=
OPENAI_JUDGE_KEY=

# Not used: DATABASE_URL, STRIPE_*, SUPABASE_*, RESEND_*
```

---

## Reference Documents

- `docs/product-spec.md` — methodology, the 4 design rules, pre-registered predictions
- `docs/implementation-guide.md` — phase-by-phase build plan
- `analysis/README.md` — per-framework navigation (which round produced which file)
- `CHANGELOG.md` — per-round release notes and the cross-framework headline table
- Upstream playbook: https://github.com/dongzhang84/indie-product-playbook
