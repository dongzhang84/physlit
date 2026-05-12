"""Extract a numbered rule list from a Stage-1 induction or Stage-2 formulation response.

Models emit rules in a few stable shapes:

  - bolded markdown: ``**1. The cart …**``
  - plain numbered list: ``1. The cart …`` / ``1) The cart …``
  - "Rule N" prefix: ``Rule 1: The cart …`` / ``Rule 1. The cart …``

The parser is heuristic — it accepts the first shape that returns ≥ 2 rules.
Failure mode is documented (returns empty list); downstream checks gracefully
degrade (N9 parsimony reports an "uncounted" flag at Tier-3 rather than
silently passing).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Patterns probed in order. Each pattern must capture (number, body) where number
# is decimal digits. Patterns are anchored to start-of-line with optional leading
# whitespace and optional markdown emphasis markers.
_RULE_PATTERNS: tuple[re.Pattern[str], ...] = (
    # **1. body**  or  **Rule 1: body**  — bolded
    re.compile(
        r"^\s*\*\*(?:Rule\s+)?(\d{1,3})[\.\):]\s*([^\n*]+?)\*\*",
        re.MULTILINE | re.IGNORECASE,
    ),
    # Rule 1: body  /  Rule 1. body  /  Rule 1) body
    re.compile(
        r"^\s*Rule\s+(\d{1,3})\s*[\.\):]\s*(.+?)(?=\n\s*Rule\s+\d|\n\s*\n|\Z)",
        re.MULTILINE | re.IGNORECASE | re.DOTALL,
    ),
    # 1. body  /  1) body  — plain numbered list
    re.compile(
        r"^\s*(\d{1,3})[\.\)]\s+(.+?)(?=\n\s*\d{1,3}[\.\)]\s|\n\s*\n|\Z)",
        re.MULTILINE | re.DOTALL,
    ),
)


@dataclass(frozen=True)
class ParsedRule:
    """One extracted rule from a Stage 1/2 response."""

    number: int  # the digit the model wrote, not always 1..N
    body: str  # rule text, stripped, single-line collapsed


def extract_rules(text: str) -> list[ParsedRule]:
    """Return parsed rules in the order they appear in the response.

    If multiple patterns match the same text, the first pattern that returns
    ≥ 2 rules wins. Empty list if no pattern produces a useful match.
    """
    best: list[ParsedRule] = []
    for pattern in _RULE_PATTERNS:
        candidates: list[ParsedRule] = []
        for match in pattern.finditer(text):
            number_str, body = match.group(1), match.group(2)
            body_clean = _normalise_body(body)
            if not body_clean:
                continue
            candidates.append(ParsedRule(number=int(number_str), body=body_clean))
        if len(candidates) >= 2 and len(candidates) > len(best):
            best = candidates
    return best


def _normalise_body(body: str) -> str:
    # Collapse internal whitespace and strip markdown emphasis remnants.
    collapsed = re.sub(r"\s+", " ", body).strip()
    collapsed = collapsed.strip("*").strip()
    # Trim trailing punctuation that the pattern may have stopped on.
    return collapsed.rstrip(".:;,")
