# v0.1 production runner requirements

This file lists requirements that the v0.1 production runner
(Phase 6 in [`implementation-guide.md`](./implementation-guide.md))
must satisfy. The requirements are referenced from the prereg
methodology footnotes but are **not part of the prereg-locked
envelope themselves** — the prereg locks *what* must be measured
and disclosed, this file describes *how* the runner implements
that measurement.

The runner cannot make its first production call until every R*
requirement listed here is implemented and tested.

---

## R1 — Gemini preview-weight drift monitoring

**Background.** v0.1 pins Google as `gemini-3.1-pro-preview` per the
Tested-models block + Preview-status caveat in
[`predictions/v0_1_prereg.md`](../predictions/v0_1_prereg.md).
Preview models do not carry stability guarantees from Google; the
underlying weights behind a given preview identifier may change
without notice from one call to the next.

The prereg commits to disclosing any such drift as a methodology
deviation. To make drift observable rather than silent, the
production runner MUST implement both parts below.

### R1(a) — Per-call identity capture with mid-run halt

Every Gemini API call MUST record all model-identity fields the
SDK exposes on the response, including but not limited to:

- `response.model_version`
- `response.model` (if present on the SDK version in use)
- any per-candidate identity field surfaced by the SDK (e.g.
  `response.candidates[i].deployment_id` or equivalent)

The exact set is determined at production-runner build time by
inspecting the installed `google-genai` SDK version, and is recorded
in the relevant `TrialRecord` field (e.g.
`extra_metadata.gemini_identity_fields` or a structured nested
field — implementation detail).

If any captured identity field on any call mid-run differs from the
lock-time identifier `"gemini-3.1-pro-preview"`, the runner MUST
halt before issuing the next call. Resumption requires an explicit
operator decision recorded in
[`analysis/aristotelian/v0_1_findings.md`](../analysis/aristotelian/v0_1_findings.md) along
with the drift evidence (timestamp, trial index, captured identity
field values).

### R1(b) — Post-trial-set re-ping with disclosure

After the full v0.1 trial set has completed (3 models × 5 trials ×
4 stages = 60 trials, all judged and aggregated), the runner MUST
send one follow-up ping to Gemini using the same minimal parameters
as the lock-time discovery ping:

- model: `gemini-3.1-pro-preview`
- contents: `"hi"`
- config: `max_output_tokens=16`

The returned `response.model_version` MUST be compared against the
lock-time value (also `"gemini-3.1-pro-preview"`). The result of
this comparison — match or mismatch, with the exact post-run value
— MUST be disclosed in
[`analysis/aristotelian/v0_1_findings.md`](../analysis/aristotelian/v0_1_findings.md), with:

- the lock-time identifier
- the post-run identifier
- the timestamps of the trial set's first and last call
- the methodology-deviation classification (none / minor / major)

A mismatch does not invalidate v0.1 results automatically; it does
require explicit acknowledgement and may prompt a v0.1.1 prereg
revision, depending on the magnitude of drift.

### Why both halves are needed

R1(a) catches drift the moment it happens, preventing silent
contamination of subsequent trials. R1(b) catches drift that may
have happened between trials (network-level routing changes that
the per-call check could miss) and provides a single
auditable disclosure point in the findings document.

Together they convert preview-weight drift from an invisible risk
into an observable, disclosable one — which is the prereg's
required handling per the Preview-status caveat.

---

## (Future R2, R3, ...)

Additional production-runner requirements may be added here as they
surface during Phase 6 build. Each must include:

- Background (what risk it addresses)
- Specific implementation requirements
- The prereg / methodology document it serves
