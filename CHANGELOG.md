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

### Next: Phase 1

- `src/physlit/schema/framework_spec.py` — pydantic `FrameworkSpec` model
- `frameworks/01_aristotelian/spec.yaml` — first manual (Tier 3) framework
- `scripts/validate_specs.py` — schema validator
- `tests/test_schemas.py` — schema validation tests
