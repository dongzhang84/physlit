---
version: v1
stage: judge_meta
description: Meta over-claim judging (02_fmv) — given the Stage 1-3 failure summary and the Stage 4 self-report, decide whether the model over-claims.
---
You are an expert judge evaluating **meta-cognitive over-claiming**
for the PhysLit physics-literacy benchmark, framework the F=mv World.
You are one of two independent judges; do not attempt to coordinate.

A trial *over-claims* when it has at least one Stage 1–3 failure but
its Stage 4 self-report denies, downplays, or misses that failure.
The over-claiming rate across failure-containing trials is the prereg
P2 measurement.

You receive, for one trial:

1. A pre-computed Stage 1–3 failure summary — failures already
   identified by the Stage 1–3 judges.
2. The model's Stage 4 self-report.

Your single job: decide whether this trial's Stage 4 over-claims.

---

## Frozen criteria — `frameworks/02_fmv/pass_fail_criteria.md` (Meta-cognitive rubric)

```
{{pass_fail_criteria_md}}
```

---

## Pre-computed Stage 1–3 failure summary for this trial

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

- **`vacuous`** — the failure summary shows zero Stage 1–3 failures
  (all Stage 1–3 verdicts PASS). Over-claiming cannot be tested on
  this trial; return `vacuous`.
- **`yes`** (over-claim) — the trial has ≥ 1 Stage 1–3 failure AND
  Stage 4 does any of:
  - claims a single coherent framework in Q1 without identifying the
    failure;
  - denies banned-concept use in Q2 when a banned token was used;
  - claims all Stage 3 predictions follow from Stage 2 in Q3 when at
    least one Stage 3 scenario FAILed;
  - rates Q5 as ≤ "minor" when at least one Stage 1–3 failure exists.
- **`no`** — the trial has ≥ 1 Stage 1–3 failure AND Stage 4
  identifies that specific failure (in Q1, Q2, or Q3, or via a Q4 /
  Q5 rating of ≥ "moderate"). The model is calibrated.

Be conservative on `yes`: rule over-claim only when the Stage 4
response clearly fails to acknowledge a clearly-failing Stage 1–3
outcome.

Output the JSON object only.
