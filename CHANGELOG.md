# Changelog

All notable changes to PhysLit are documented here. Dates are UTC.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/),
adapted for a research project: each entry is one phase of the implementation guide.

---

## Rounds at a glance

| Framework | Difficulty | Sub-rounds | Composite content PASS (post-audit) | Headline finding |
|---|---|---|---|---|
| **F=mv counterfactual world** | Easy | `02_fmv`, `02_fmv.1`, `02_fmv.2` | **9/15** | Claude and GPT induce the counterfactual rules cleanly; only Gemini slides back to F=ma. Axiomatisation cue raises structural pass rate 5/15 → 11/15. |
| **Aristotelian Mechanics** | Medium | `v0.1`, `v0.2`, `v0.2.1`, `v0.3` | **5/15** | Historical framework — partial induction. Same axiomatisation cue lifts structural pass rate 8/15 → 15/15 (saturated); cross-framework replication holds. |
| **Decay World** | Hard | `03_decay` | **0/15** | Universal-rate counterfactual with no underlying substrate denies every model a composite PASS. Hidden-substrate trap fires; OpenAI judge §3 stress-test fails (16/18 fabricated/misclassified). |

Three rounds, three frameworks, the same Stage 4 over-claim rate band: v0.1 70 %, 02_fmv 66.7 %, 03_decay 67 %. Frontier models do not improve at self-identifying their own slips as the framework gets harder.

Detailed per-round entries are below in reverse-chronological order; physical files are organized by framework under [`analysis/`](./analysis/README.md).

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
- `analysis/aristotelian/dryrun_findings.md` — exploratory write-up after the run

---

## [0.1.0] — 2026-05-11

### v0.1 — Aristotelian production experiment

The changelog lapsed during the v0.1 and v0.2 production phases; this
and the next entry are condensed catch-up. Full detail is in the
per-round reports under `analysis/`.

- v0.1 prereg drafted and locked (`prereg-v0.1-locked`); production
  runner + dual-judge pipeline built.
- Production: 3 models (Claude Opus 4.7, GPT-5.5, Gemini 3.1 Pro) ×
  N=5 × 4 stages on Aristotelian Mechanics — 60 trials, 120 judge
  verdicts.
- Dual-judge content IRR 36.67 % → prereg-mandated human audit of 22
  disagreement cases.
- Result: P1 (induction failure) and P3 (meta miscalibration) both
  CONFIRMED post-audit. Report: `analysis/aristotelian/v0_1_report.md`.

---

## [0.2.0] — 2026-05-13

### v0.2 — Structural axis + disagree-resolver agents

- Additive analysis layer over the frozen v0.1 dataset: a structural
  judging axis (N9-N12 — parsimony, independence, traceability,
  hierarchy) and two LLM disagree-resolver agents replacing the v0.1
  human-audit pathway. Locked as `prereg-v0.2-locked`; `v0.2.1` is a
  deviation switching the resolver model.
- Result: V1 (Agent 1 reproduces the human audit) REFUTED — 29.4 %
  agreement; V2 (structural axis adds failure detection) CONFIRMED.
- A follow-up human audit of the structural-axis disagreements found
  the structural criteria carried a Stage 1+2 double-count defect and
  that the v0.2 LLM resolvers did not reliably reproduce human
  structural judgment.

---

## [02_fmv] — 2026-05-18

### 02_fmv — F=mv counterfactual-world experiment

First from-scratch experiment since v0.1, and the first
framework-scoped pre-registration (`prereg-02_fmv-locked`).

- New framework `frameworks/02_fmv/` — the F=mv World, a counterfactual
  world where pace tracks the present push (force ∝ velocity). 12
  hand-authored observations; criteria written mechanical-first (§3 is
  a purely lexical banned-token test, fixing the v0.1 ambiguity);
  framework-specific Stage 1-4 model prompts and judge prompts.
- New, independent tooling: `run_02_fmv.py`, `judge_02_fmv.py`,
  `build_02_fmv_audit_worksheet.py`, `apply_02_fmv_audit.py`,
  `render_02_fmv_to_md.py`, `run_agent1_02_fmv.py`. A SIGALRM per-call
  timeout was added to the runners after a vendor SDK call hung
  indefinitely.
- Production: 3 models × N=5 × 4 stages = 60 trials; 120 judge
  verdicts. Content axis only — the N9-N12 structural axis is out of
  scope by explicit prereg decision.
- Dual-judge IRR 26.67 % → human audit of 14 disagreement cases.
- Result, post-audit: **P1 REFUTED** (4/15 Stage 1 FAIL, all Gemini —
  Claude and GPT induced the F=mv rules cleanly), **P2 CONFIRMED**
  (66.7 % over-claim), **P3 PARTIALLY CONFIRMED** (IRR 26.67 %),
  **P4 REFUTED** (0/45 quantitative leak).
- Methodology: a non-canonical Agent 1 resolver run against the
  mechanical criteria agreed with the human audit on 12/12 content
  cases (vs 29.4 % in v0.2) — evidence the v0.2 resolver-unreliability
  finding was substantially a criteria-ambiguity artifact. Judge
  reliability reversed across frameworks (OpenAI reliable on v0.1,
  Claude on F=mv).
- Cost ≈ $17.3 USD. Report: `analysis/fmv/02_fmv_report.md`.

## [02_fmv.1] — 2026-05-18

### 02_fmv.1 — structural axis on the F=mv trials

Additive analysis layer over the frozen `02_fmv` content trials —
the structural axis (N9-N12), exactly as v0.2 added structure to v0.1.
Pre-registered at `prereg-02_fmv.1-locked`; no new tested-model trials.

- Corrected structural criteria (`frameworks/02_fmv/structural_criteria.md`):
  the rule count, N9 parsimony, and N10 redundancy check are scoped to
  **Stage 1 only**, fixing the v0.2 Stage 1+2 double-count defect.
  New structural judge prompt; two predictions (P1, P2).
- New tooling: `judge_structural_02_fmv.py`,
  `build_02_fmv_1_structural_worksheet.py`, `apply_02_fmv_1_audit.py`,
  `run_agent2_02_fmv.py`, `build_02_fmv_1_agent2_review.py`.
- 30 structural dual-judge verdicts over the 15 trials; structural-axis
  IRR 46.67 % → human audit of all 7 disagreement cases.
- Result, post-audit: **P1 REFUTED** — the Stage-1-only fix did *not*
  lower the structural IRR (46.67 % > v0.2's 40 %); the 7 splits were
  N10/N11/N12 judgment calls, not counting artifacts, refuting the
  double-count diagnosis as the dominant cause. **P2 CONFIRMED** — 8 of
  9 all-content-PASS trials flip to composite FAIL; only 1/15 trials is
  composite PASS.
- Methodology: judge reliability reverses completely between axes —
  Claude judge 86 % content / 14 % structural, OpenAI 21 % / 86 % (same
  models, same trials). Content and structural quality are
  anti-correlated (GPT 5/5 content, 0/5 structural; Gemini 0/5, 3/5).
  Non-canonical Agent 2 resolver agreed with the human audit 6/7.
- Cost ≈ $4.0 USD. Report: `analysis/fmv/02_fmv_1_report.md`.

## [02_fmv.2] — 2026-05-20

### 02_fmv.2 — axiomatisation control experiment on F=mv

Single-variable control experiment over the F=mv framework: same
observations, same models, same N=5, same Stage 2-4 prompts, same
judges, same criteria as `02_fmv` — only the Stage 1 prompt changes.
Pre-registered at `prereg-02_fmv.2-locked` before any treatment trial.

- New frozen artifact: `frameworks/02_fmv/prompts/stage1_induction_axiomatised.md`
  — the `02_fmv` Stage 1 prompt with one added paragraph asking for
  the smallest set of rules and explicit cross-rule references.
  Natural-language guidance, not the N9-N12 rubric.
- New tooling: `run_02_fmv_2.py`, `judge_02_fmv_2.py`,
  `apply_02_fmv_2.py`, `build_02_fmv_2_worksheet.py`,
  `render_02_fmv_2_to_md.py`, `run_agent1_02_fmv_2.py`,
  `run_agent2_02_fmv_2.py`, `build_02_fmv_2_agents_review.py`.
- Production: 60 new treatment-arm trials (3 models × N=5 × 4 stages);
  120 judge verdicts (content + structural); 16 non-canonical resolver
  verdicts. Content IRR 22.22 %, structural IRR 40.00 % → 16-case
  human audit.
- Result, post-audit: **P1 STRONGLY CONFIRMED** — treatment structural
  PASS **11/15** vs control 5/15, doubled (per-model: Claude 2/5 →
  5/5, GPT 0/5 → 2/5, Gemini 3/5 → 4/5). **P2 CONFIRMED** — treatment
  content PASS **9/15** vs control 9/15, exactly flat. Composite
  jumped **1/15 → 6/15**.
- Substantive finding: `02_fmv.1` §2.7 self-organisation thesis
  *causally* confirmed. Models that know the rules (Claude, GPT)
  respond to the natural-language cue; Gemini (content-weak) barely
  moves. The structural failure is a default-behaviour gap, not a
  capability limit, for the models that have the underlying knowledge.
- Side-effect of the cue: Claude trial 2 lost its content axis —
  Stage 2 fabricated a "track pushes upward" balancing mechanism. A
  follow-on instruction should forbid introducing forces not in the
  observations.
- Methodology: both LLM judges level-shift to 50 % vs the human audit
  on both axes (down from the strong asymmetries of `02_fmv` and
  `02_fmv.1`). Likely the axiomatised treatment responses are harder
  to judge. Agent 1 dropped to 5/10 (uniform-PASS failure mode);
  Agent 2 held at 5/6 (83 %).
- Cost ≈ $5.5 USD. Report: `analysis/fmv/02_fmv_2_report.md`.

## [v0.3] — 2026-05-20

### v0.3 — Aristotelian axiomatisation control (cross-framework replication of `02_fmv.2`)

Single-variable control experiment on the Aristotelian framework,
parallel to `02_fmv.2`. The added Stage 1 instruction is
**byte-for-byte identical** to `02_fmv.2`'s — verified by diff at
commit time — so the cross-framework comparison is valid.
Pre-registered at `prereg-v0.3-locked`.

- New frozen artifact: `frameworks/01_aristotelian/prompts/stage1_induction_axiomatised.md`
  (v0.1 global Stage 1 prompt + the `02_fmv.2` axiomatisation paragraph
  inserted at the matching anchor).
- New tooling: `run_v0_3.py`, `judge_v0_3.py`, `apply_v0_3.py`,
  `build_v0_3_worksheet.py`, `render_v0_3_to_md.py`,
  `run_agent1_v0_3.py`, `run_agent2_v0_3.py`,
  `build_v0_3_agents_review.py`.
- Results subtree renamed `v0_3` → `01_aristotelian_3` (under user
  feedback that the v0_3 path didn't say which framework). 191 JSON
  files rewritten (`framework_id` + `trial_path` fields). Prereg
  tag / analysis filenames keep `v0_3` (prereg is locked).
- Production: 60 new treatment-arm trials; 120 judge verdicts;
  13 non-canonical resolver verdicts. Content IRR 17.78 %, structural
  IRR 20.00 % → 11-case human audit.
- Result, post-audit: **P1 STRONGLY CONFIRMED** — structural PASS
  **15/15** vs control 8/15, absolute lift **+7** (saturated; per-
  model GPT **0/5 → 5/5**, Gemini 3/5 → 5/5, Claude already at 5/5).
  **P2 CONFIRMED** — content PASS 6/15 vs control 5/15 (+1).
  Composite jumped **2/15 → 6/15** — same ceiling as `02_fmv.2`.
- **Cross-framework comparison** (central deliverable): the same
  one-paragraph cue lifts structural pass rate on both frameworks
  (F=mv +6, Aristotelian +7), holds content roughly flat on both
  (F=mv 0, Aristotelian +1), and brings composite to 6/15 on both.
  The `02_fmv.1` self-organisation thesis is causally confirmed on a
  second framework. GPT is the dominant mover on both.
- Side finding: every one of the 8 content disagreements audited FAIL.
  Parsimony pressure can pull the model toward training-data
  vocabulary — broader on Aristotelian (Newton-leak vocab) than on
  F=mv (single P3 fabrication). A future round should add a
  "don't introduce vocabulary beyond the observations" clause.
- Methodological: two known judge defects re-emerged — OpenAI
  Stage 1+2 double-count (S2, third occurrence; v0.3 reuses v0.2
  criteria per prereg's identical-baseline commitment, so the
  `02_fmv.1`-fix didn't apply) and Claude verdict-field
  self-contradiction (S1, S3; same defect class as `02_fmv.1` Case 6).
  Both documented in `v0_3_audit_human_review.md`.
- Cost ≈ $6.8 USD. Report: `analysis/aristotelian/v0_3_report.md`.

## [03_decay] — 2026-05-28

### 03_decay — Decay World experiment

Third framework and the project's second counterfactual world after
`02_fmv`. The Decay World is a Tier 1 setting in which every isolated
system's directly measured state (oscillation amplitude, absolute
temperature, rotation rate, orbital radius) shrinks at a fixed
fractional rate per second (~ 0.99/s), universally across mechanical,
thermal, rotational, and orbital domains, with no underlying "energy"
substrate and with every standard dissipative mechanism (friction,
drag, damping, viscosity, radiative loss) explicitly closed off.
Pre-registered at `prereg-03_decay-locked`; four predictions locked
before any production trial.

- New framework `frameworks/03_decay/`: 10 hand-authored observations
  across six domains, `ideal_induction.md` with widened §5 P2
  (hidden-substrate framing), `pass_fail_criteria.md` with numeric
  PASS ranges for the 4 quantitative scenarios, four model prompts
  and four judge prompts.
- New tooling: `run_03_decay.py`, `judge_03_decay.py`,
  `apply_03_decay.py`, `build_03_decay_worksheet.py`,
  `build_03_decay_agents_review.py`, `render_03_decay_to_md.py`,
  `reparse_03_decay.py`, `run_agent1_03_decay.py`,
  `run_agent2_03_decay.py`. The judge runner integrates the new
  `evidence_check.py` module (Gap 4 fix) that flags fabricated
  banned-token citations.
- Production: 60 trials (3 models × N=5 × 4 stages); 120 content
  judge verdicts; 49 non-canonical resolver runs. Stage 1-3 IRR
  **40.00 %** → 54 cases sent to human audit (18 content + 32 Stage 3
  per-scenario + 4 meta over-claim).
- **Audit worksheet C/B numbering aligned 1:1 with agents review
  A1/A2** (`build_03_decay_worksheet.py` Part A sort key updated;
  Part B already matched).
- Result, post-audit: **P1 CONFIRMED · P2 CONFIRMED · P3 CONFIRMED ·
  P4 CONFIRMED** — all four prereg predictions confirmed.
  - **P1**: composite content PASS **0/15** vs F=mv 9/15 and
    Aristotelian 5/15. The Decay World is the hardest of the three
    frameworks tested in PhysLit so far; no model, no vendor scores a
    composite PASS.
  - **P2**: of 8 post-audit Stage 1 FAILs, the §5-pattern count is 1
    (P2, Gemini T1) vs 0 of every other §5 pattern. Strictly greater
    bar met but with a sample size of 1; the strongest §5 P2 evidence
    is actually at Stage 2 (3 of 4 §5 hits), outside the prereg
    scoring window.
  - **P3**: across 60 quantitative predictions, **37 decay-correct /
    23 ratio-leaked / 0 direction-wrong**. The direction-wrong bucket
    is empty — every model named the right direction (something
    decays) but the framework rule's ratio differs from the standard
    physics expectation in 23 of 60 cases. The 23 includes 6
    decline-to-commit responses (orbital outside model's declared
    scope, no `r_pendulum` value supplied, etc.).
  - **P4**: 10 over-claim = yes vs 5 no across 15 failure-containing
    trials = 67 %. Same band as Aristotelian (70 %, v0.1) and F=mv
    (66.7 %, 02_fmv) — three rounds, three frameworks, 65–70 %
    over-claim rate is now a candidate behavioural regularity.
- Methodology: the **OpenAI judge §3 stress-test failure** is the
  most generalisable finding. 16 of 18 Part A OpenAI FAIL clauses are
  defective (fabricated tokens, or real words misclassified as
  banned) on a §3 list of 20+ tokens with heavy semantic overlap with
  the framework vocabulary. `evidence_check.py` caught fabricated
  citations; misclassifications required human audit. OpenAI judge
  agreement with the audit: 22 % (B) / 33 % (A) / 50 % (C). Claude
  judge: 67 % / 81 % / 50 %. Third consecutive round in which the
  relatively reliable judge changes — the dual-judge + audit
  safeguard is doing real work.
- **Agent 2 (per-scenario resolver) agreed with the human audit on
  31/32 = 97 %** — the highest agent-vs-human number in PhysLit so
  far. Agent 1 (content) at 14/17 = 82 %, dragged down by the same
  OpenAI §3 fabrications the audit had to unwind.
- Cost ≈ $25 USD. Report: `analysis/decay/03_decay_report.md`. Human-audit
  detail: `analysis/decay/03_decay_audit_human_review.md`.

## [paper] — 2026-06-12

### Write-up and TMLR submission preparation

Experimental phase closed after `03_decay`. This entry covers the
write-up phase only: **no new framework, no new production trials, no
new API calls, nothing written to `results/`.** All three frameworks'
data is sealed; the paper reports it.

- Three parallel manuscripts built from the same results: `latex_en/`
  (English), `latex_cn/` (Chinese), and `latex_tmlr/` (the TMLR
  submission draft). `latex_tmlr/` is its own git repository and is
  gitignored from the main repo. `docs/paper_en.md` is the readable
  Markdown port kept in sync with `latex_en/` / `latex_tmlr/`.
- Structure: 8 main sections (Intro, Methodology, the three framework
  rounds, Cross-Framework Findings, Discussion, Conclusion) plus
  Appendices A–D (pre-registration tags + SHA-256, and per-framework
  observation sets, banned-word lists, N-condition checklists, and
  Stage 3 scenarios). Heavy appendices, light main text.
- **Headline metric is the composite = content ∧ structural axis**,
  reported from the axiomatization-prompt arm: F=mv **6/15**
  (`02_fmv.2`), Aristotelian **6/15** (`v0.3`), Decay World **0/15**
  (content axis only — its prereg scopes the structural axis out). Note
  this differs from the content-only **9/15** in the "Rounds at a
  glance" table above and in the per-round `02_fmv`/`03_decay` entries:
  both are correct, they count different axes. The paper standardizes
  on the composite axis throughout; the sealed per-round entries keep
  their original content-only baselines untouched.
- External review: `latex_tmlr/tmlr_feedback_gpt_v1.txt` holds a
  GPT-authored TMLR-style review (13 numbered items) plus a per-item
  response log. Items 2/5/11 applied (abstract rewritten to lead with
  the evaluation gap, Keywords line dropped, openness repetition
  trimmed); items 3/4 rejected by the author (§1 stays uncompressed,
  the Easy/Medium/Hard section titles stay); items 6/7/12/13 deferred
  to a single pre-submission polish pass.
- Next step: the deferred polish pass (tighten framework intro
  paragraphs, foreground the contribution bullets, trim the conclusion
  recap, fix LaTeX overfull boxes / warnings / build-mode consistency),
  then submit to TMLR.
