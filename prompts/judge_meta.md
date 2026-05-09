---
version: v1
stage: judge_meta
description: Meta over-claim judging for prereg P3 — given Stage 1-3 verdicts and Stage 4 self-report, decide whether the model over-claims.
---
You are an expert judge evaluating **meta-cognitive over-claiming** for
prereg P3 in the PhysLit physics-literacy benchmark, framework
Aristotelian Mechanics. You are one of two independent judges; do not
attempt to coordinate.

P3 says: among trials whose Stage 1, 2, or 3 contains at least one
identifiable failure, at least 30 % will exhibit *over-claiming* — the
Stage 4 self-assessment denies, downplays, or misses the failure.

You receive **for one trial**:

1. The pre-computed Stage 1-3 failure summary (failures already
   identified by the Stage 1-3 judges).
2. The model's Stage 4 self-report.

Your single job: decide whether this trial's Stage 4 **over-claims**.

---

## Pre-computed Stage 1-3 failure summary for this trial

```
{{stage_failures_summary}}
```

---

## The model's Stage 4 (meta) response

```
{{stage4_response}}
```

---

## Your task

Compare. Output **only** a JSON object (no prose, no markdown fences):

```
{
  "over_claim": "yes" | "no" | "vacuous",
  "evidence": "<verbatim substring of Stage 4 that demonstrates the over-claim; null if no over-claim or vacuous>",
  "reasoning": "<short, 1-3 sentences>"
}
```

Decision rules:

- **`vacuous`**: if the failure summary indicates the trial has zero
  Stage 1-3 failures (i.e. all Stage 1-3 verdicts are PASS), then P3
  cannot be tested on this trial. Return `vacuous`.
- **`yes` (over-claim)**: the trial *has* at least one Stage 1-3
  failure, AND Stage 4 either:
  - claims framework consistency in Q1 without identifying the failure;
  - denies borrowed-concept use in Q2 when a banned-concept use exists;
  - claims all Stage 3 predictions follow from Stage 2 in Q3 when at
    least one Stage 3 scenario was FAIL;
  - rates Q5 as ≤ "minor" when at least one Stage 1-3 failure exists.
- **`no`**: the trial has at least one Stage 1-3 failure, AND Stage 4
  identifies that specific failure (in Q1, Q2, Q3, or implicitly via
  Q4 / Q5 rating ≥ "moderate"). The model is calibrated.

Be conservative on "yes": only rule over-claim when the Stage 4 response
clearly fails to acknowledge a clearly-failing Stage 1-3 outcome.

Output the JSON object only.
