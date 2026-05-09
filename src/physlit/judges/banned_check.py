"""Lightweight banned-concept scan for calibration smoke tests.

This is **not** the v0.1 dual-judge pipeline. It is a quick syntactic
check that flags occurrences of the §3 banned-concepts list from
``frameworks/01_aristotelian/ideal_induction.md`` so the operator can
eyeball whether a model's Stage 1 induction is pristine, borderline,
or obviously contaminated.

It is intentionally over-eager (case-insensitive substring match) and
will produce false positives in contexts like "do not invoke
inertia". Real judging in v0.1 still goes through the dual-LLM
pipeline (Phase 8).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Banned terms from ``ideal_induction.md`` §3, in lower case. Each entry
# is matched case-insensitively as a whole-word substring.
BANNED_TERMS: tuple[str, ...] = (
    "inertia",
    "acceleration",
    "momentum",
    "energy",
    "gravity",
    "gravitational",
    "vacuum",
    "friction",
    "frictional",
    # "force" is matched only when it appears as a defined / quantified
    # noun; the simple substring match catches more than it should, but
    # the human reviewer can dismiss false positives.
    "force",
    # "mass" — same caveat as "force".
    "mass",
    "density",
    # Post-Aristotelian physicist names.
    "newton",
    "galileo",
    "archimedes",
)


@dataclass(frozen=True)
class BannedHit:
    """One match of a banned term in some response text."""

    term: str
    position: int
    context: str  # ~30 chars around the match


def scan_for_banned(text: str, terms: tuple[str, ...] = BANNED_TERMS) -> list[BannedHit]:
    """Return every whole-word match of any banned term in ``text``.

    Match is case-insensitive. ``context`` is a short window around
    the hit so the operator can quickly judge whether it is a real
    use of the concept or a denial.
    """
    hits: list[BannedHit] = []
    lower = text.lower()
    for term in terms:
        pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
        for match in pattern.finditer(lower):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            window = text[start:end].replace("\n", " ")
            hits.append(BannedHit(term=term, position=match.start(), context=window))
    return hits
