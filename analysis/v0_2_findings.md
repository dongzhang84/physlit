# PhysLit v0.2 — Findings

This file accumulates v0.2 evaluation findings: structural-axis
judging, Agent 1 / Agent 2 resolver outputs, and the composite
verdict over v0.1 trials.

## v0.2.1 final report
- Generated: `2026-05-13T19:49:09Z`
- Prereg lock: `prereg-v0.2.1-locked`
- Resolver agent (Agent 1 + Agent 2): `gemini-2.5-pro`

### V1 — Agent 1 calibration against human audit
**Verdict: REFUTED**

Agent 1 agreed with the v0.1 human audit on **5 of 17 content disagree cases (29.4 %)**. Threshold for CONFIRMED was ≥ 12 of 17 per the prereg.

#### Cases where Agent 1 differed from human audit

| Model | Trial | Stage | Agent 1 | Human audit |
|---|---|---|---|---|
| `claude-opus-4-7` | 2 | formulation | PASS | FAIL |
| `claude-opus-4-7` | 4 | formulation | PASS | FAIL |
| `claude-opus-4-7` | 3 | induction | PASS | FAIL |
| `claude-opus-4-7` | 3 | prediction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | formulation | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 1 | induction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | induction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 3 | prediction | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 2 | prediction | FAIL | PASS |
| `gemini-3.1-pro-preview` | 3 | formulation | PASS | FAIL |
| `gemini-3.1-pro-preview` | 0 | formulation | PASS | FAIL |
| `gemini-3.1-pro-preview` | 4 | formulation | PASS | FAIL |

### V2 — Structural axis adds detection over content-only
**Verdict: CONFIRMED**

Of the 5 v0.1 all-content-PASS trials (Claude trial 1, GPT trials 0/2/4, Gemini trial 2), **4 flipped to composite FAIL** via the structural axis. Threshold for CONFIRMED was ≥ 2 per the prereg.

#### Flipped trials

- `gpt-5.5-2026-04-23` trial 0
- `gpt-5.5-2026-04-23` trial 2
- `gpt-5.5-2026-04-23` trial 4
- `gemini-3.1-pro-preview` trial 2

> **Superseded in part — see "Post-audit revision" below.** The
> 2026-05-17 human audit reverses the structural verdict on Gemini
> trial 2 (it no longer flips) and adds Gemini trial 0 as a new flip.
> The CONFIRMED verdict still holds under every reading (flips remain
> ≥ 2), but the flipped-trial list above is the pre-audit version.

### Structural-axis IRR
Structural judges disagreed on **6 of 15 trials (40.00 %)**. Compare to v0.1 content-axis IRR of 36.67 %.

### Composite per-trial verdicts (content AND structural)

> **Revised 2026-05-17 — human standard.** The `Structural` column now
> uses the human audit verdict for the 6 disagree trials
> (`analysis/v0_2_structural_audit_human_review.md`) and the
> dual-judge agreed verdict for the 9 non-disagree trials (`†` = not
> human-audited; may still be affected by the Stage 1+2 double-count
> design bug — see "Post-audit revision" below). `Content-only` =
> S1 ∧ S2 ∧ S3, i.e. the verdict if there were no structural axis.
> Rows whose composite flipped against the pre-audit table are marked
> ⇄.

| Model | Trial | S1 | S2 | S3 | Content-only | Structural (human std) | Composite |
|---|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS | FAIL | PASS | FAIL | PASS † | FAIL |
| `claude-opus-4-7` | 1 | PASS | PASS | PASS | PASS | PASS † | PASS |
| `claude-opus-4-7` | 2 | FAIL | PASS | PASS | FAIL | PASS † | FAIL |
| `claude-opus-4-7` | 3 | PASS | FAIL | PASS | FAIL | **PASS** (was FAIL) | FAIL |
| `claude-opus-4-7` | 4 | FAIL | PASS | PASS | FAIL | PASS | FAIL |
| `gpt-5.5-2026-04-23` | 0 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 1 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 2 | PASS | PASS | FAIL | FAIL | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 3 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gpt-5.5-2026-04-23` | 4 | PASS | PASS | PASS | PASS | FAIL † | FAIL |
| `gemini-3.1-pro-preview` | 0 | PASS | PASS | PASS | PASS | **FAIL** (was PASS) | FAIL ⇄ |
| `gemini-3.1-pro-preview` | 1 | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| `gemini-3.1-pro-preview` | 2 | PASS | PASS | PASS | PASS | **PASS** (was FAIL) | PASS ⇄ |
| `gemini-3.1-pro-preview` | 3 | FAIL | PASS | PASS | FAIL | FAIL † | FAIL |
| `gemini-3.1-pro-preview` | 4 | FAIL | PASS | FAIL | FAIL | PASS | FAIL |

Composite PASS (human standard): **2 of 15** — `claude-opus-4-7`
trial 1 and `gemini-3.1-pro-preview` trial 2. (Same count as the
pre-audit table, but the membership changed: Gemini trial 0 dropped
out, Gemini trial 2 entered.)

---

## Structural axis (N9–N12) — full per-trial matrix

The `Structural` column above is a single collapsed PASS/FAIL. This
section unpacks it: all **36 structural verdicts** behind it — 30 raw
dual-judge verdicts (3 models × 5 trials × 2 judges) plus 6 Agent 2
resolutions for the disagree cases.

Source JSONs (verbatim API responses, committed):

- Raw judges: `results/<model>/01_aristotelian/structural/{anthropic,openai}_structural_*.json`
- Agent 2: `results/<model>/01_aristotelian/structural_resolved/google_agent2_structural_*.json`

`gpt-5.5-2026-04-23` has no `structural_resolved/` files because both
judges agreed FAIL on all 5 GPT trials — no disagreement to resolve.

Criteria: N9 parsimony, N10 independence, N11 traceability, N12
hierarchy — defined in `frameworks/01_aristotelian/structural_criteria.md`.
`rc` = the judge's reported `rule_count`.

### Master matrix

The `Pre-audit final` column is the dual-judge + Agent 2 pipeline
verdict. The `Human audit` column (added 2026-05-17) is the verdict
from the human re-audit of the 6 disagree cases —
`analysis/v0_2_structural_audit_human_review.md`. The 9 non-disagree
trials were not human-audited (`— not audited`).

| Model | Trial | Claude judge | OpenAI judge | Agent 2 | Pre-audit final | Human audit |
|---|---|---|---|---|---|---|
| `claude-opus-4-7` | 0 | PASS (rc 11) | PASS (rc 11) | — | PASS | — not audited |
| `claude-opus-4-7` | 1 | PASS (rc 9) | PASS (rc 9) | — | PASS | — not audited |
| `claude-opus-4-7` | 2 | PASS (rc 10) | PASS (rc 20) | — | PASS | — not audited |
| `claude-opus-4-7` | 3 | PASS (rc 7) | FAIL (rc 14, N10) | FAIL (rc 14, N10+N11) | FAIL | **PASS** (Agent 2 wrong) |
| `claude-opus-4-7` | 4 | PASS (rc 10) | FAIL (rc 20, N9) | PASS (rc 10) | PASS | **PASS** (Agent 2 right) |
| `gpt-5.5-2026-04-23` | 0 | FAIL (rc 15, N9) | FAIL (rc 30, N9+N10) | — | FAIL | — not audited |
| `gpt-5.5-2026-04-23` | 1 | FAIL (rc 17, N9+N12) | FAIL (rc 17, N9) | — | FAIL | — not audited |
| `gpt-5.5-2026-04-23` | 2 | FAIL (rc 17, N9) | FAIL (rc 34, N9) | — | FAIL | — not audited |
| `gpt-5.5-2026-04-23` | 3 | FAIL (rc 15, N10) | FAIL (rc 15, N10) | — | FAIL | — not audited |
| `gpt-5.5-2026-04-23` | 4 | FAIL (rc 15, N9+N12) | FAIL (rc 30, N9+N10) | — | FAIL | — not audited |
| `gemini-3.1-pro-preview` | 0 | FAIL (rc 7, N12) | PASS (rc 14) | PASS (rc 7) | PASS | **FAIL** (Agent 2 wrong) |
| `gemini-3.1-pro-preview` | 1 | FAIL (rc 7, N12) | PASS (rc 7) | PASS (rc 7) | PASS | **PASS** (Agent 2 right) |
| `gemini-3.1-pro-preview` | 2 | PASS (rc 7) | FAIL (rc 14, N10) | FAIL (rc 14, N10) | FAIL | **PASS** (Agent 2 wrong) |
| `gemini-3.1-pro-preview` | 3 | FAIL (rc 3, N11) | FAIL (rc 6, N10) | — | FAIL | — not audited |
| `gemini-3.1-pro-preview` | 4 | FAIL (rc 7, N12) | PASS (rc 14) | PASS (rc 7) | PASS | **PASS** (Agent 2 right) |

Disagree cases (6 of 15, IRR 40.00 %): Claude trials 3 & 4; Gemini
trials 0, 1, 2, 4. Gemini trial 3 is an *agree-FAIL* — both judges
FAIL but on different criteria (Claude N11, OpenAI N10).

**Agent 2 vs human audit: 3 of 6 (50 %).** Agent 2 was wrong on
Claude trial 3, Gemini trial 0, and Gemini trial 2.

### Caveat — Claude structural-judge verdict/reasoning inconsistency

In **5 trials** the Claude structural judge's `verdict` field says
`FAIL` while its own `reasoning` text explicitly self-corrects to PASS
("all four criteria pass", "revising my verdict to PASS", "verdict
should be PASS"): GPT trial 0, and Gemini trials 0, 1, 3, 4. The
parsed `verdict` field — `FAIL` — is what the IRR and the master
matrix above use, per the prereg's "parsed verdict is authoritative"
rule. But this means part of the 40 % structural IRR is an artifact
of this output bug, not genuine judge disagreement. Agent 2 caught it
on Gemini trials 0/1/4 (sided with the PASS reading). It is logged
here as a v0.2 methodology defect; a fix belongs in v0.2.2+.

### Per-trial judge reasoning (verbatim)

#### `claude-opus-4-7`

- **Trial 0 — PASS / PASS → PASS.**
  - Claude: 11 top-level rules (Stage 1 & 2 are parallel formulations of the same set), within N9. Distinct phenomena, all traceable, arrow impetus-fading is permitted elaboration; cross-refs present → N12 OK.
  - OpenAI: same 11-rule reading; overlaps function as applications not duplicates; cross-refs present.
- **Trial 1 — PASS / PASS → PASS.**
  - Claude: 9 rules treated as one set, distinct phenomena, all traceable, cross-refs ("see Rule 8", "Rules 2-4") → all pass.
  - OpenAI: 9 rules, Stage 2 a reformulation not a new set, cross-refs present.
- **Trial 2 — PASS / PASS → PASS.**
  - Claude: 10 rules (same numbering both stages), distinct, traceable, cross-refs → pass.
  - OpenAI: counted 20 (Stage 1 + Stage 2 mechanically) but 20 ≤ N9 high threshold so not an N9 fail; no independent N10 duplicate → PASS.
- **Trial 3 — PASS / FAIL → Agent 2 FAIL.** *(disagree)*
  - Claude: 7 rules, distinct, traceable, cross-refs → PASS.
  - OpenAI: 14 rules combined; Stage 2 restates Stage 1 (Rule 1 duplicated) → FAIL N10.
  - Agent 2 (`google_agent2_structural_f8e46221.json`): FAIL, agreed_with judge_b. Criteria require treating Stage 1+2 as one set → 14 rules; Stage 2 are operational reformulations of Stage 1's seven → N10 redundancy. Also flags N11: "road's roughness" introduced as a cart-stopping mechanism unsupported by Obs. 2.
- **Trial 4 — PASS / FAIL → Agent 2 PASS.** *(disagree)*
  - Claude: 10 rules matched across stages, distinct, traceable, abundant cross-refs → PASS.
  - OpenAI: counted 20 (10 proposed + 10 operational) → FAIL N9 (>15).
  - Agent 2 (`google_agent2_structural_7002c571.json`): PASS, agreed_with judge_a. Stage 2 is an explicit "Operational formulation" of Stage 1 — a mitigating structure per the N9 notes; mechanically counting 20 would wrongly punish a model for showing its work. Correct count is 10 → passes N9/N10/N11/N12.

#### `gpt-5.5-2026-04-23` — all 5 trials agree FAIL (no Agent 2)

- **Trial 0 — FAIL / FAIL → FAIL.** Claude: 15 rules, soft-signal band, leans PASS in prose but parsed verdict FAIL/N9 *(see caveat)*. OpenAI: 30 rules (15+15) → FAIL N9 (high) + N10 (heavenly-motion rule duplicated).
- **Trial 1 — FAIL / FAIL → FAIL.** Claude: 17 rules → FAIL N9 (>15) + N12 (no cross-rule references anywhere). OpenAI: 17 rules → FAIL N9, stops at first failure.
- **Trial 2 — FAIL / FAIL → FAIL.** Claude: 17 rules → FAIL N9; Rule 17 is a meta-procedure restating Rules 1–16. OpenAI: counted 34 rules → FAIL N9 (>20).
- **Trial 3 — FAIL / FAIL → FAIL.** Both: 15 rules; N9 only a soft signal, N12 passes — but Rules 9 & 13 make the same operational claim (cart/arrow motion fades once the mover stops) → FAIL N10. Rare clean cross-judge agreement on criterion *and* count.
- **Trial 4 — FAIL / FAIL → FAIL.** Claude: 15 rules + flat enumeration with no cross-refs → FAIL N9-soft + N12. OpenAI: 30 rules → FAIL N9 + N10 (Rule 3 / Rule 13 paraphrase the air-as-hindrance claim).

#### `gemini-3.1-pro-preview`

- **Trial 0 — FAIL / PASS → Agent 2 PASS.** *(disagree)*
  - Claude: 7 rules, all criteria pass per reasoning, but parsed verdict FAIL/N12 *(see caveat — internally inconsistent)*.
  - OpenAI: 14 rules (7+7), Stage 2 restates Stage 1 → not N10; cross-refs present → PASS.
  - Agent 2 (`google_agent2_structural_4351785d.json`): PASS, agreed_with judge_b. Counted 7 (Stage 2 = elaboration of Stage 1). Noted Judge A's report is internally inconsistent — FAIL verdict, PASS reasoning.
- **Trial 1 — FAIL / PASS → Agent 2 PASS.** *(disagree)*
  - Claude: 7 rules; reasoning explicitly "revising my verdict to PASS" but parsed verdict FAIL/N12 *(see caveat)*.
  - OpenAI: 7 rules, distinct, cross-refs present → PASS.
  - Agent 2 (`google_agent2_structural_983d265a.json`): PASS, agreed_with judge_b. Aligns with Judge A's *corrected* reasoning + Judge B's verdict.
- **Trial 2 — PASS / FAIL → Agent 2 FAIL.** *(disagree)*
  - Claude: 7 rules (same 7 both stages), distinct, traceable, cross-refs → PASS.
  - OpenAI: 14 rules; Stage 1 & Stage 2 "Natural Directions" rule make the same claim → FAIL N10.
  - Agent 2 (`google_agent2_structural_fb813cd1.json`): FAIL, agreed_with judge_b. Procedure requires concatenating Stage 1+2 → 14 rules; each of the 7 principles stated twice → N10. Passes N9/N11/N12.
- **Trial 3 — FAIL / FAIL → FAIL** (agree-FAIL, different criteria).
  - Claude: only 3 rules; reasoning self-corrects to "verdict should be PASS" but parsed verdict FAIL/N11 *(see caveat)*.
  - OpenAI: 6 rules (3+3); Stage 2 duplicates Stage 1 Rule 3 → FAIL N10.
- **Trial 4 — FAIL / PASS → Agent 2 PASS.** *(disagree)*
  - Claude: 7 rules; reasoning "all four criteria pass" but parsed verdict FAIL/N12 *(see caveat)*.
  - OpenAI: 14 rules, Stage 2 restates Stage 1, cross-refs present → PASS.
  - Agent 2 (`google_agent2_structural_2283a50a.json`): PASS, agreed_with judge_b. Counted 7; calls OpenAI's 14 an over-count and Judge A's FAIL verdict contradicted by its own reasoning.

### Patterns

1. **The recurring fault line is rule-counting, not judgment.** Every
   disagree case reduces to: does Stage 2's "operational formulation"
   add 7 new rules (OpenAI's mechanical count) or re-state the 7 from
   Stage 1 (Claude's reading)? This single parsing decision drives
   N9 and N10. Agent 2 recomputes `rule_count` itself — exactly the
   prereg's design intent.
2. **Agent 2 leaned PASS (4 of 6 disagree cases).** Same over-pass
   direction flagged for Agent 1 on the content axis — candidate for
   over-lenient resolution; worth a v0.2.2 audit.
3. **GPT-5.5 fails structurally regardless of count convention.** All
   5 trials fail under both judges — GPT genuinely produces 15–17+
   rules per stage, a flat redundant rule soup, which is precisely
   the v0.1 failure pattern the structural axis was built to catch.

---

## Post-audit revision — structural axis (human standard, 2026-05-17)

The structural-axis IRR of 40 % exceeded the 25 % audit threshold, so
all 6 disagree trials were human-audited via
`analysis/v0_2_structural_audit_worksheet.md`. The verdicts are
canonical in `analysis/v0_2_structural_audit_human_review.md` and are
summarised here.

### Agent 2 calibration against the human audit

| Case | Trial | Agent 2 | Human | Agent 2 correct? |
|---|---|---|---|---|
| 1 | `claude-opus-4-7` trial 3 | FAIL | **PASS** | ❌ |
| 2 | `claude-opus-4-7` trial 4 | PASS | **PASS** | ✅ |
| 3 | `gemini-3.1-pro-preview` trial 0 | PASS | **FAIL** | ❌ |
| 4 | `gemini-3.1-pro-preview` trial 1 | PASS | **PASS** | ✅ |
| 5 | `gemini-3.1-pro-preview` trial 2 | FAIL | **PASS** | ❌ |
| 6 | `gemini-3.1-pro-preview` trial 4 | PASS | **PASS** | ✅ |

**Agent 2 agreed with the human audit on 3 of 6 (50 %).** This is the
structural-axis analogue of the V1 finding for Agent 1 on the content
axis (29.4 %): an LLM resolver substituted for a human auditor does
not reliably reproduce human structural judgment.

### Criteria design bug — Stage 1 + Stage 2 double-count

The root cause of 3 of the 3 Agent 2 errors (and most of the 40 %
IRR) is a conflict between two frozen artifacts:

- `frameworks/01_aristotelian/structural_criteria.md` §2: "Rule count
  means top-level numbered or bolded propositions in the Stage 1 +
  Stage 2 **combined** output."
- `prompts/stage2_formulation.md`: "Return your operational rules as
  a numbered list, **mirroring the numbering you used earlier**."

A model that correctly obeys the Stage 2 prompt re-states its Stage 1
rules in operational form. The structural criteria then count those
re-statements again, mechanically doubling `rule_count` and tripping
N9 (parsimony) or N10 (independence). **Correct prompt compliance is
scored as a structural failure.** This is a v0.2 criteria design
limitation and must be disclosed as such in any published result.

The human audit counts **core principles only** (the Stage 1 count);
Stage 2 mirroring is not an N10 redundancy. N10 is assessed *within*
the Stage 1 core set — which is how the audit caught the one real
redundancy nobody else did (Gemini trial 0, Rules 1 and 7 both state
celestial circular motion).

**Fix for v0.3.** `structural_criteria.md` should specify: "Count
core principles (the Stage 1 count). Stage 2 operational expansions
of the same rules do not count as additional rules. N10 redundancy is
assessed within the Stage 1 core set."

### Conclusion without the structural axis vs with it (human standard)

Using the human-audited structural verdicts (6 disagree trials) plus
the dual-judge agreed verdict (9 non-disagree trials, not
human-audited, marked `†`):

- **Content-only** (S1 ∧ S2 ∧ S3, no structural axis): **7 of 15**
  trials PASS — `claude` t1; `gpt` t0, t1, t3, t4; `gemini` t0, t2.
- **With the structural axis** (composite): **2 of 15** trials PASS —
  `claude` t1 and `gemini` t2.

The structural axis flips **5 content-PASS trials to composite FAIL**:
`gpt` trials 0, 1, 3, 4 and `gemini` trial 0. The prereg V2 prediction
("structural axis adds detection over content-only", threshold ≥ 2)
therefore remains **CONFIRMED** under the human standard.

Two caveats on that count:

1. Four of the five flips (`gpt` trials 0/1/3/4) rest on dual-judge
   *agree-FAIL* verdicts that were **not human-audited**. GPT trials 0
   and 4 fail on a Stage-1 count of 15 rules — an N9 *soft signal*,
   not a hard fail by itself — so their structural FAIL may not
   survive a human audit under the corrected core-count rule. GPT
   trials 1/2/3 are firmer (17 core rules, or a within-Stage-1 N10
   duplicate). A follow-up audit of the 9 non-disagree trials is
   recommended before the V2 count is treated as final.
2. The one human-audited new flip — `gemini` trial 0 — is solid: it
   fails N10 on a genuine within-Stage-1 redundancy (Rules 1 and 7),
   independent of the double-count bug.

### Revised headline

- **Structural axis, human standard:** Claude 5/5 structural-PASS,
  GPT 0/5, Gemini 4/5 (`gemini` trial 0 FAIL on real internal
  redundancy; `gemini` trial 3 FAIL not human-audited).
- **Agent 2 (`gemini-2.5-pro`) reproduced human structural judgment
  on 3/6 disagree cases.** Combined with the V1 content-axis result
  (Agent 1, 29.4 %), the v0.2.1 evidence is that an LLM disagree-
  resolver is not a sound substitute for human audit at this task.
- The 40 % structural IRR is substantially inflated by two defects —
  the Claude verdict-field bug and the Stage 1+2 double-count — both
  fixable; neither is a property of the frameworks under test.
