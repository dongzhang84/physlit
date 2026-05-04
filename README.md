# PhysLit

> An open-source diagnostic for physics literacy in large language models — replacing percentage benchmarks with binary cognitive judgments across induction, formulation, and prediction.

PhysLit asks whether a language model can do physics — not solve physics problems, but reason from observation to law to prediction inside an unfamiliar framework. We test 15 framework worlds (some historically real, some counterfactual, some arbitrary) and produce binary cognitive judgments, not a leaderboard score.

## Status

**v0.0.1 — Phase 0 (scaffolding)**, 2026-05-04. Docs complete, Python environment initialized, repo skeleton ready. Phenomenon sets, runners, and analysis pipeline still to build.

## Docs

- [docs/product-spec.md](./docs/product-spec.md) — what PhysLit is, the methodology, the four design rules, pre-registered predictions
- [docs/implementation-guide.md](./docs/implementation-guide.md) — phase-by-phase build plan

## Stack

- Python 3.13
- [uv](https://docs.astral.sh/uv/) for dependency management
- pydantic for schema validation
- anthropic / openai / google-genai SDKs
- Jinja2 for static-site rendering
- GitHub Pages + GitHub Actions for hosting and CI

**No backend, no database, no auth, no payments.** All results are JSON files committed to the repo. The capability matrix is a static site.

## Quick start (after Phase 0 is checked in)

```bash
git clone https://github.com/dongzhang84/physlit.git
cd physlit
uv sync                    # install deps in .venv
uv run pytest              # run tests
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
