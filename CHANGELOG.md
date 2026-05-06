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

### Pending external setup

- Add `PLAYBOOK_TOKEN` repository secret so `notify-playbook` workflow
  can dispatch sprint-summary updates back to indie-product-playbook.

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
