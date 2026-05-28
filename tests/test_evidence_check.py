"""Tests for ``physlit.judges.evidence_check``.

The evidence-check module is part of the ``prereg-03_decay-locked``
envelope; its substring-matching semantics must not drift after
lock. These tests pin the behaviour on the four canonical cases
from the dry-run (``analysis/decay/03_decay_dryrun_findings.md`` §6, the
Gap 4 audit trail) plus a handful of synthetic edge cases.
"""

from __future__ import annotations

from physlit.judges import check_evidence
from physlit.judges.evidence_check import normalise_for_match

# --- Substring presence -------------------------------------------------


def test_pass_verdict_no_evidence_required() -> None:
    """A PASS verdict with evidence=null must not be flagged."""
    r = check_evidence(
        verdict={"verdict": "PASS", "evidence": None},
        response_text="anything",
    )
    assert r.fabricated is False
    assert r.evidence_required is False


def test_fail_verdict_with_real_substring_passes() -> None:
    """A FAIL whose evidence is a real substring must not be flagged."""
    r = check_evidence(
        verdict={"verdict": "FAIL", "evidence": "the pendulum loses"},
        response_text="In one second the pendulum loses some amplitude.",
    )
    assert r.fabricated is False
    assert r.found is True


def test_fail_verdict_with_fabricated_substring_is_flagged() -> None:
    """The canonical Gap-4 case — the cited string isn't in the response."""
    r = check_evidence(
        verdict={"verdict": "FAIL", "evidence": "air resistance"},
        response_text="The motion fades even with no surrounding air.",
    )
    assert r.fabricated is True
    assert r.found is False


def test_fail_verdict_empty_evidence_is_flagged() -> None:
    """A FAIL with an empty / missing evidence string is a schema violation
    and must be treated as fabrication."""
    r = check_evidence(
        verdict={"verdict": "FAIL", "evidence": ""},
        response_text="anything",
    )
    assert r.fabricated is True


def test_fail_verdict_null_evidence_is_flagged() -> None:
    r = check_evidence(
        verdict={"verdict": "FAIL", "evidence": None},
        response_text="anything",
    )
    assert r.fabricated is True


# --- Normalisation ------------------------------------------------------


def test_case_insensitive() -> None:
    r = check_evidence(
        verdict={"verdict": "FAIL", "evidence": "Air RESISTANCE"},
        response_text="reduced by air resistance in the experiment",
    )
    assert r.found is True


def test_collapsed_whitespace_matches_line_break() -> None:
    """A judge-quoted 'air resistance' should still match if the response
    happens to wrap the phrase across a newline + indentation."""
    r = check_evidence(
        verdict={"verdict": "FAIL", "evidence": "air resistance"},
        response_text="reduced by air\n   resistance in the experiment",
    )
    assert r.found is True


def test_normalise_for_match_does_not_strip_markdown() -> None:
    """``**smallest**`` is not normalised to ``smallest``."""
    assert normalise_for_match("**Smallest**") == "**smallest**"


# --- Ellipsis handling --------------------------------------------------


def test_ellipsis_three_dots_splits_and_both_fragments_required() -> None:
    """A scholarly 'A ... B' quote: both fragments must be substrings."""
    r = check_evidence(
        verdict={
            "verdict": "FAIL",
            "evidence": "the pendulum fades ... at a fixed fractional rate",
        },
        response_text=(
            "We observe that the pendulum fades from a high amplitude "
            "to a low one, at a fixed fractional rate per second."
        ),
    )
    assert r.found is True
    assert "ellipsis-split" in r.reason


def test_ellipsis_unicode_horizontal_ellipsis() -> None:
    """The U+2026 single-char ellipsis is also a split marker."""
    r = check_evidence(
        verdict={
            "verdict": "FAIL",
            "evidence": "the pendulum fades … fixed fractional rate",
        },
        response_text=(
            "We observe that the pendulum fades from high to low, at a "
            "fixed fractional rate per second."
        ),
    )
    assert r.found is True


def test_ellipsis_with_one_missing_fragment_is_flagged() -> None:
    """If 'A ... B' is quoted but only A is in the response, flag it."""
    r = check_evidence(
        verdict={
            "verdict": "FAIL",
            "evidence": "the pendulum fades ... a wholly invented phrase",
        },
        response_text="We observe that the pendulum fades over time.",
    )
    assert r.fabricated is True


# --- Over-claim verdicts ------------------------------------------------


def test_over_claim_no_does_not_require_evidence() -> None:
    """A meta verdict with over_claim='no' or 'vacuous' has evidence=null
    and must not be flagged."""
    r = check_evidence(
        verdict={"over_claim": "no", "evidence": None},
        response_text="anything",
    )
    assert r.fabricated is False
    assert r.evidence_required is False


def test_over_claim_yes_requires_evidence() -> None:
    """A meta verdict with over_claim='yes' must cite a real substring."""
    r = check_evidence(
        verdict={"over_claim": "yes", "evidence": "I made no errors"},
        response_text="My Stage 3 answers were perfect; I made no errors anywhere.",
    )
    assert r.fabricated is False
    assert r.found is True


def test_over_claim_yes_with_fabricated_evidence_is_flagged() -> None:
    r = check_evidence(
        verdict={"over_claim": "yes", "evidence": "I am uncertain"},
        response_text="My Stage 3 answers were perfect; I made no errors.",
    )
    assert r.fabricated is True
