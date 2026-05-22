"""Mechanical post-check for judge evidence fabrication.

A judge LLM is asked to quote a **verbatim substring** of the tested
model's response in its ``evidence`` field. The dry-run for the
03_decay framework surfaced a failure mode in which the OpenAI judge
fabricated banned-token evidence: it cited "air resistance" as
appearing in a Stage 1 response that did not in fact contain the
substring "air resistance", and claimed "components" contained
"momentum" as a substring (which it does not). See
``analysis/03_decay_dryrun_findings.md`` §6 (Gap 4) for the audit
trail.

This module provides a single function, :func:`check_evidence`, that
verifies the judge's cited ``evidence`` substring actually appears in
the tested model's response. The comparison is intentionally
permissive — it normalises case and whitespace runs but otherwise
requires a literal substring match. Verdicts whose evidence cannot
be located are flagged ``judge_fabrication = True`` and per the
locked 03_decay prereg (scoring step 2a) are routed to human audit.

The module is part of the 03_decay prereg envelope; do not edit its
substring-matching logic without issuing a new prereg version.

Scope:
- Only the ``evidence`` field is checked. ``reasoning`` is free
  prose and is not substring-matched.
- A PASS verdict with ``evidence: null`` (the schema for a passing
  trial) is treated as not-fabricated.
- A non-string ``evidence`` value is treated as fabricated (the
  schema requires a string for FAILs).
- The function does not infer intent — it returns a boolean. It is
  the caller's responsibility to record / route fabricated verdicts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

__all__ = ["EvidenceCheckResult", "check_evidence", "normalise_for_match"]


_WS_RUN = re.compile(r"\s+")

# Ellipsis forms a judge may use to elide the middle of a longer
# quoted passage. The check splits on these and requires each
# non-trivial fragment to be a substring; this accommodates
# legitimate scholarly quotation form ("A ... B" where both A and B
# are real substrings) without weakening the fabrication check.
_ELLIPSIS_SPLIT = re.compile(r"\.{3,}|…|\[\.\.\.\]|\[…\]")
# Minimum fragment length (after normalisation) considered
# substantive. Short connecting words like "and" or "the" left
# dangling around an ellipsis should not be the only thing that
# must be located.
_MIN_FRAGMENT_LEN = 8


def normalise_for_match(text: str) -> str:
    """Normalise text for permissive substring matching.

    Two normalisations only — anything more aggressive risks
    over-matching:

    - **case-fold** (so "Air Resistance" and "air resistance" match);
    - **collapse whitespace runs** to a single space (so a line wrap
      that splits a phrase like "air\\n resistance" still matches the
      judge's quoted ``"air resistance"``).

    Leading and trailing whitespace are also stripped. Markdown
    syntax (``**``, ``_``, etc.) is **not** stripped — the judge
    should quote the response as it is, including any markdown
    formatting that surrounds the cited phrase.
    """
    return _WS_RUN.sub(" ", text).strip().casefold()


def _split_on_ellipsis(evidence: str) -> list[str]:
    """Split an evidence string on ellipsis forms (``...``, ``…``,
    ``[...]``, ``[…]``) and return the non-trivial fragments.

    A fragment is "non-trivial" iff its normalised length is at
    least :data:`_MIN_FRAGMENT_LEN`. This allows the judge to use
    "A ... B" elision in legitimate quotation; each side must still
    be a real substring of the response.

    If the evidence contains no ellipsis, returns a single-element
    list with the original string.
    """
    parts = _ELLIPSIS_SPLIT.split(evidence)
    if len(parts) == 1:
        return [evidence]
    return [p for p in parts if len(normalise_for_match(p)) >= _MIN_FRAGMENT_LEN]


@dataclass(frozen=True)
class EvidenceCheckResult:
    """Outcome of a single (verdict, response) evidence check."""

    found: bool
    """True iff the normalised evidence appears as a substring of the
    normalised response."""

    fabricated: bool
    """True iff the verdict cites evidence that cannot be located.
    Equivalent to ``not found and evidence_required``."""

    evidence_required: bool
    """True iff the verdict's schema requires a non-null
    ``evidence`` field (i.e. a FAIL verdict). A PASS verdict with
    ``evidence: null`` is not required to be substring-matchable."""

    cited_evidence: str | None
    """The ``evidence`` string as supplied by the judge (unaltered).
    None when the verdict was PASS with ``evidence: null``."""

    reason: str
    """Human-readable explanation of the outcome."""


def _verdict_says_fail(verdict: dict[str, Any]) -> bool:
    """Stage 1 / Stage 2 verdicts use ``verdict``; Stage 3 verdicts
    nest per-scenario ``verdict`` inside a ``scenarios`` list; the
    meta verdict uses ``over_claim``. This helper handles the
    Stage 1 / Stage 2 case; Stage 3 scenarios and Stage 4 are
    handled by their own call sites passing the relevant sub-dict.
    """
    v = verdict.get("verdict")
    return isinstance(v, str) and v.strip().upper() == "FAIL"


def check_evidence(
    *,
    verdict: dict[str, Any],
    response_text: str,
) -> EvidenceCheckResult:
    """Verify a judge verdict's ``evidence`` field against the
    tested-model response.

    Parameters
    ----------
    verdict
        The parsed JSON verdict dict produced by a judge. Must
        contain (at minimum) ``evidence`` and, depending on the
        stage, ``verdict`` or ``over_claim``.
    response_text
        The tested model's response that the judge was scoring.
        For Stage 1 this is the induction response; for Stage 2 the
        formulation response; for Stage 3 the prediction response
        (and per-scenario evidence is matched against the entire
        Stage 3 prediction response, not a per-scenario slice — the
        Stage 3 prompt does not partition the response); for the
        meta judge, the Stage 4 response.

    Returns
    -------
    :class:`EvidenceCheckResult`
        ``fabricated`` is True iff a non-null evidence string was
        cited and cannot be located in ``response_text`` after the
        normalisation described in :func:`normalise_for_match`.
    """
    ev = verdict.get("evidence")
    # PASS verdicts have evidence=null per the schema; nothing to verify.
    is_over_claim = "over_claim" in verdict
    if is_over_claim:
        oc = verdict.get("over_claim")
        evidence_required = isinstance(oc, str) and oc.strip().lower() == "yes"
    else:
        evidence_required = _verdict_says_fail(verdict)

    if not evidence_required:
        # No evidence is required; whatever's in ``ev`` is informational.
        return EvidenceCheckResult(
            found=ev is None or ev == "",
            fabricated=False,
            evidence_required=False,
            cited_evidence=ev if isinstance(ev, str) else None,
            reason="evidence not required (PASS / no over-claim / vacuous)",
        )

    if not isinstance(ev, str) or not ev.strip():
        # FAIL verdict with empty / non-string evidence — schema violation.
        return EvidenceCheckResult(
            found=False,
            fabricated=True,
            evidence_required=True,
            cited_evidence=ev if isinstance(ev, str) else None,
            reason="FAIL verdict with empty or non-string evidence field",
        )

    haystack = normalise_for_match(response_text)
    fragments = _split_on_ellipsis(ev)

    if len(fragments) == 0:
        # Ellipsis-only or whitespace-only evidence — schema violation.
        return EvidenceCheckResult(
            found=False,
            fabricated=True,
            evidence_required=True,
            cited_evidence=ev,
            reason="evidence consists only of ellipsis / whitespace",
        )

    missing: list[str] = []
    for frag in fragments:
        needle = normalise_for_match(frag)
        if needle and needle not in haystack:
            missing.append(frag)

    if not missing:
        if len(fragments) == 1:
            reason = "evidence located in response (substring match)"
        else:
            reason = (
                f"evidence located in response — {len(fragments)} ellipsis-"
                f"split fragments all matched as substrings"
            )
        return EvidenceCheckResult(
            found=True,
            fabricated=False,
            evidence_required=True,
            cited_evidence=ev,
            reason=reason,
        )

    return EvidenceCheckResult(
        found=False,
        fabricated=True,
        evidence_required=True,
        cited_evidence=ev,
        reason=(
            f"cited evidence is not a substring of the response after "
            f"case / whitespace normalisation — {len(missing)} of "
            f"{len(fragments)} fragment(s) missing; likely judge "
            f"fabrication"
        ),
    )
