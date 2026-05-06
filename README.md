# PhysLit

> An open-source diagnostic for physics literacy in large language models — replacing percentage benchmarks with binary cognitive judgments across induction, formulation, and prediction.

PhysLit asks whether a language model can do physics — not solve physics problems, but reason from observation to law to prediction inside an unfamiliar framework. We test 15 framework worlds (some historically real, some counterfactual, some arbitrary) and produce binary cognitive judgments, not a leaderboard score.

## Status

**v0.0.2 — Phase 1 (Framework Spec Schema)**, 2026-05-05. Pydantic
`FrameworkSpec` model + tier decision-tree validation, first Tier 3
framework (Aristotelian Mechanics), spec validator wired into pre-commit.
Phenomenon generators, runners, and analysis pipeline still to build.

## Docs

- [docs/product-spec.md](./docs/product-spec.md) — what PhysLit is, the methodology, the four design rules, pre-registered predictions
- [docs/implementation-guide.md](./docs/implementation-guide.md) — phase-by-phase build plan
- [CLAUDE.md](./CLAUDE.md) — architectural rules and Claude Code project guide
- [CHANGELOG.md](./CHANGELOG.md) — phase-by-phase release notes

## Repo layout

```
physlit/
├── docs/
│   ├── product-spec.md                  methodology, design rules, predictions
│   └── implementation-guide.md          phase-by-phase build plan
│
├── frameworks/                          phenomenon framework specs (committed data)
│   └── 01_aristotelian/spec.yaml        Tier 3 manual — first framework
├── predictions/                         pre-registered predictions    [Phase 5, locked]
├── prompts/                             versioned model prompts       [Phase 6+]
├── results/                             raw API responses, all trials [Phase 7+]
├── analysis/                            cost log, IRR reports, matrix [Phase 9+]
│
├── scripts/
│   ├── validate_specs.py                frameworks/*/spec.yaml schema check
│   └── extract-sprint-summary.py        sprint report helper
│
├── src/physlit/
│   ├── schema/                          pydantic models (cross-module contracts)
│   │   └── framework_spec.py            FrameworkSpec + tier validation
│   ├── generators/
│   │   ├── tier1/                       Python simulators              [Phase 2]
│   │   ├── tier2/                       AI generator (stub only in v0.1) [Phase 3]
│   │   └── tier3/                       manual-authoring loaders       [Phase 4]
│   ├── runners/                         tested-model orchestration     [Phase 6–7]
│   ├── judges/                          dual-LLM IRR pipeline          [Phase 8]
│   ├── analysis/                        cross-stage / meta analysis    [Phase 9]
│   └── site/                            Jinja2 static-site renderer    [Phase 10]
│
├── tests/
│   └── test_schemas.py                  FrameworkSpec + committed-spec sweep
│
├── CLAUDE.md                            architectural rules (load-bearing)
├── CHANGELOG.md                         phase-by-phase release notes
├── SPRINT.md                            auto-generated activity report
├── .pre-commit-config.yaml              ruff + verify-prereg + validate-specs
├── pyproject.toml                       uv-managed; mypy strict, ruff
├── uv.lock                              committed — required for reproducibility
├── LICENSE                              MIT — code
└── LICENSE-DATA                         CC BY 4.0 — frameworks, predictions, prompts, results, analysis
```

Phase tags in brackets point at `docs/implementation-guide.md`. Empty directories use `.gitkeep` until populated; do not delete the placeholder before adding real content.

## Evaluation pipeline

End-to-end shape of one framework × all tested models. This is the v0.1 target
architecture; today only the schema layer (top-left input) is wired up.

```
                                    ┌─ Claude Opus 4.7 ─┐
observations.md ──┐                 │                   │
                  │                 │  5 fresh sessions │
prompts/stage1    │   runner        │  × 2 temperatures │ ──▶ results/<model-ver>/
_induction.md  ───┼──▶ orchestrator ┼─ GPT-5 ───────────┤       01_aristotelian/
                  │   (replicate.sh)│  (same)           │       induction/
                  │                 │                   │         trial_0_t0.0.json
                  │                 └─ Gemini 3 ────────┘         trial_0_t1.0.json
                  │                                                ...
                  ▼
           save trial JSON verbatim
                  │
                  ▼
        Judges (Claude + GPT, independent)
        read response_text + pass_fail_criteria.md
        → emit PASS / FAIL + reasoning
                  │
                  ▼
        IRR check (do the two judges agree?)
                  │
                  ▼
        analysis/ → capability matrix HTML
```

Per-trial isolation is load-bearing: every trial gets a fresh API client and
a new session UUID, and stages 1/2/3 never share context. See `CLAUDE.md`
("Architectural Rules") for the methodology rationale.

## Quick start

```bash
git clone https://github.com/dongzhang84/physlit.git
cd physlit
uv sync                              # install deps + dev tools into .venv
uv run pre-commit install            # one-time: hook ruff + spec validators

uv run pytest                        # run tests
uv run python scripts/validate_specs.py   # validate every frameworks/*/spec.yaml
```

Local gates (must all pass before commit):

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

To reproduce a full evaluation run (requires API keys and budget):

```bash
ANTHROPIC_API_KEY=... OPENAI_API_KEY=... GOOGLE_API_KEY=... ./replicate.sh
```

## License

- **Code** (`src/`, `tests/`, `scripts/`, configs) — [MIT](./LICENSE)
- **Data** (`frameworks/`, `predictions/`, `prompts/`, `analysis/`, `results/`) — [CC BY 4.0](./LICENSE-DATA)

## Upstream

Born out of [`indie-product-playbook`](https://github.com/dongzhang84/indie-product-playbook). See `ideas/physlit.md` and `implementation-guides/physlit.md` upstream for the original spec.
