# Changelog

All notable changes to PhysLit are documented here. Dates are UTC.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
adapted for a research project: each entry is one phase of the implementation guide.

---

## [0.0.1] — 2026-05-04

### Phase 0 — Repo Scaffold

- Initial commit via `indie-product-playbook/stack/new-project.sh`:
  product spec + implementation guide copied to `docs/`,
  `sprint-report.yml` + `notify-playbook.yml` workflows wired with
  `project_id=physlit`, `extract-sprint-summary.py` copied,
  `.gitignore` / `README.md` / `.env.local` rendered from templates,
  public GitHub repo created and initial push.
- Python environment initialized with uv targeting Python 3.13:
  `pyproject.toml` configured with strict mypy, ruff (E/F/I/B/UP/SIM/RUF
  rules, line length 100), pytest. Hatchling build backend, `src/physlit`
  package layout.
- Dependencies pinned via `uv.lock`:
  `anthropic`, `openai`, `google-genai`, `pydantic`, `pyyaml`, `jinja2`,
  `click`; dev: `pytest`, `ruff`, `mypy`, `pre-commit`.
- Repository skeleton: `src/physlit/{schema,generators/{tier1,tier2,tier3},runners,judges,analysis,site}`,
  plus empty `frameworks/`, `predictions/`, `prompts/`, `results/`,
  `analysis/`, `tests/` (`.gitkeep` placeholders).
- Licensing: MIT for source code (`LICENSE`); CC BY 4.0 for phenomenon
  data, predictions, prompts, and analysis (`LICENSE-DATA`).
- `.pre-commit-config.yaml`: ruff + ruff-format + standard hygiene hooks
  (trailing-whitespace, end-of-file-fixer, check-yaml, large-file
  guard) + a local `verify-prereg` hook (no-op until Phase 5 lands the
  prereg file).
- `CLAUDE.md` documenting the architectural rules: phenomenon-generation
  tiers, pre-registration immutability, fresh-session enforcement, model
  version pinning, open-data commitment, inter-rater reliability.
- `scripts/extract-sprint-summary.py` refactored to use `pathlib.Path`
  (ruff SIM115).

All checks green:
`uv run ruff check .` · `uv run ruff format --check .` · `uv run mypy src/`.

### External setup

- `PLAYBOOK_TOKEN` repository secret configured for the
  `notify-playbook` workflow that dispatches sprint summaries back to
  indie-product-playbook. (Confirmed 2026-05-05.)

---

## [0.0.2] — 2026-05-05

### Phase 1 — Framework Spec Schema

- `src/physlit/schema/framework_spec.py` — pydantic v2 `FrameworkSpec`
  with `extra="forbid"`, `frozen=True`, id pattern `^\d{2}_[a-z0-9_]+$`,
  and a `model_validator` enforcing the tier decision tree:
  Tier 1 requires `simulator_module` (and only that), Tier 2 requires
  both `generation_prompt` and `generator_model`, Tier 3 requires
  `manual_authoring_note`. Architectural slot for Tier 2 is preserved
  for v0.5 even though no Tier 2 spec is permitted in v0.1.
- `src/physlit/schema/__init__.py` — re-exports `FrameworkSpec`,
  `Tier`, `Category` so other modules import from `physlit.schema`.
- `frameworks/01_aristotelian/spec.yaml` — first Tier 3 manual
  framework (Category A_historical). `frameworks/.gitkeep` removed
  now that the directory is populated.
- `scripts/validate_specs.py` — walks `frameworks/*/spec.yaml`,
  validates each against the schema, and additionally enforces that
  the declared `id` matches the parent directory name. Exits non-zero
  on any failure.
- `tests/test_schemas.py` — 9 tests: happy paths for Tier 1 and
  Tier 3, all three tier-mismatch errors, id pattern, `extra="forbid"`,
  frozen mutation rejection, and a parametrized sweep that loads every
  committed `spec.yaml` so any future spec drift fails CI.
- `.pre-commit-config.yaml` — added local `validate-specs` hook
  scoped to `frameworks/**.y(a)ml`, runs `validate_specs.py`.
- `pyproject.toml` — added `types-pyyaml` to dev deps so mypy strict
  passes on `yaml.safe_load` calls.

All checks green:
`uv run ruff format --check . && uv run ruff check . && uv run mypy
&& uv run pytest`.

### Next: Phase 2

- `src/physlit/generators/tier1/base.py` — `Tier1Simulator` base class
- `src/physlit/generators/tier1/f_equals_mv.py` — first Tier 1
  simulator (F=mv counterfactual world)
- `tests/test_simulators.py` — byte-identity determinism contract

---

## [0.0.3] — 2026-05-07

### Scope reduction (planning, no code change)

The original v0.1 / v0.5 / v1.0 ladder (1 → 5–7 → 15–20 frameworks; arXiv;
five academic citations) has been retired in favour of a smaller,
budget-bounded plan:

- **v0.1**: Aristotelian only × 3 models, **≤ $50 USD**.
- **v0.2**: up to 5 frameworks across A/B/C, **≤ $250 USD** —
  *optional and gated on v0.1 outcome*.
- Beyond v0.2: no commitment.

This better matches the project's nature as a research artifact
("evening project") rather than a funded benchmark.

#### Affected sections

- `docs/product-spec.md` §1.3 (status), §3.3 (prereg scope), §5.2
  (long-term roster), §6.1 (models), §8 (milestones rewritten),
  §9 (success criteria), §12 (week-by-week plan replaced by phase
  cadence).
- `docs/product-spec.zh.md` mirrored.
- `docs/implementation-guide.md` — new **Phase 1.5 — Aristotelian
  Dry Run** inserted between Phase 1 and Phase 2.
- `CLAUDE.md` Cost Awareness rewritten ($50 / $250 caps; replicate.sh
  confirmation threshold lowered to $5).
- `README.md` status line updated.

#### v0.1 protocol changes from this scope reduction

- **Temperature=0.7 secondary pass deferred** (budget). v0.1 headline
  result uses temperature=0 only. To be added back in v0.2 or when
  budget allows.
- **Pre-registration scope split**: P1 + P3 in v0.1 prereg lock;
  P2 + P4 + P5 deferred to v0.2 prereg lock (they require multi-framework
  testing).
- Three-model coverage (Claude Opus 4.7, GPT-5, Gemini 3) **retained**.
- N=5 trials per (model, stage) **retained**.
- Dual-judge IRR (Claude + GPT) **retained**.

#### v0.2 tentative selection (revisable before v0.2 prereg lock)

01_aristotelian (A) + 02_phlogiston (A) + F=mv world (B, Tier 1) +
reverse-gravity world (B, Tier 1) + color-force world (C, Tier 1).

### Next: Phase 1.5 (Aristotelian Dry Run)

Smoke-test the v0.1 pipeline at < $1 cost before prereg lock:

- `prompts/stage{1..4}_*.md` — global prompt templates
- `src/physlit/prompts/loader.py` — front-matter parser
- `src/physlit/runners/base.py` — `TrialRecord` + `run_trial` abstract base
- `src/physlit/runners/claude.py` — minimal Claude runner
- `scripts/dryrun_aristotelian.py` — orchestrate 4 stages, single trial,
  Claude only, output to `results/_dryrun/<ts>/01_aristotelian/`
- `tests/test_runners_with_mock.py` — mock-based, CI-safe
- `analysis/dryrun_findings.md` — exploratory write-up after the run
