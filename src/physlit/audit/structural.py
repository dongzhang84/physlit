"""Structural-criteria checks (N9 / N10 / N11 regex / N12) and the orchestrator.

The orchestrator combines regex-layer results with optional LLM-layer results
(passed in from ``llm_smuggle.py``) and emits a single ``StructuralAuditReport``
per trial.

Tiering rule:
    - regex hit + LLM hit on overlapping evidence  →  Tier-1
    - single layer hit                              →  Tier-2
    - soft-threshold heuristic only                 →  Tier-3
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .models import FlagTier, StructuralAuditReport, StructuralFlag
from .parse_rules import ParsedRule, extract_rules

# Default observation count for 01_aristotelian. Other frameworks pass their own
# count via the orchestrator's ``observation_count`` parameter.
DEFAULT_OBSERVATION_COUNT = 12

# N9 parsimony thresholds. Expressed as ratios so they scale across frameworks.
# For obs=12 these match the §8 doc exactly: Tier-3 when rule_count > 12,
# Tier-2 when rule_count > 15, Tier-1 when rule_count > 20.
N9_TIER_3_RATIO_FLOOR = 1.0  # rule_count > obs * 1.0
N9_TIER_2_RATIO_FLOOR = 1.25  # rule_count > obs * 1.25
N9_TIER_1_RATIO_FLOOR = 5.0 / 3.0  # rule_count > obs * 5/3

# N12 hierarchy markers. If a rule set has ≥ 5 rules and none of these markers
# appear anywhere in the response text, flag Tier-2 (flat enumeration).
HIERARCHY_MARKERS: tuple[str, ...] = (
    "derived from",
    "corollary",
    "follows from",
    "special case of",
    "combined with",
    "consequence of",
    "implies",
    "by application of",
)
N12_MIN_RULES_FOR_HIERARCHY = 5


# N11 regex layer — smuggled mechanism. Patterns target verbs and phrases that
# describe a mechanism (an active thing doing something to motion) not present
# in the 12 Aristotelian observations. Each match is one Tier-2 hit on its own;
# if the LLM layer also flags overlapping evidence, it becomes Tier-1.
@dataclass(frozen=True)
class _SmugglePattern:
    """Internal: one regex pattern + an explanation of why it indicates smuggling."""

    pattern: re.Pattern[str]
    label: str
    explanation: str


_SMUGGLE_PATTERNS: tuple[_SmugglePattern, ...] = (
    _SmugglePattern(
        pattern=re.compile(
            r"\b(?:road|air|surface|ground|medium|substance)s?\b[^.]{0,40}"
            r"\b(?:robs?|saps?|consumes?|drains?|steals?|removes?|absorbs?|"
            r"depletes?|extracts?)\b",
            re.IGNORECASE,
        ),
        label="motion-removal mechanism",
        explanation=(
            "Describes the road/air/medium as actively *removing* motion — a Newtonian "
            "friction analogue not present in the 12 observations."
        ),
    ),
    _SmugglePattern(
        pattern=re.compile(
            r"\bsurface[-\s]supported\b|\bbuoyant\s+support\b",
            re.IGNORECASE,
        ),
        label="surface-support mechanism",
        explanation=(
            "Surface-support / buoyant-support framings import a buoyancy mechanism "
            "(Archimedean) not derivable from observation 5."
        ),
    ),
    _SmugglePattern(
        pattern=re.compile(
            r"\bhorizontal\s+(?:and\s+vertical\s+)?components?\b|"
            r"\bvertical\s+components?\b|"
            r"\bcomponents?\s+(?:of|combine|add|decompos)|"
            r"\bresultant\b|"
            r"\bnet\s+(?:force|effect)\b|"
            r"\bvector\s+(?:sum|decomposition)\b",
            re.IGNORECASE,
        ),
        label="vector-decomposition mechanism",
        explanation=(
            "Vector / component / resultant language imports Newtonian mechanics' "
            "decomposition apparatus — not derivable from the observations."
        ),
    ),
    _SmugglePattern(
        pattern=re.compile(
            r"\bfrictional?[-\s]?(?:like|effect|drag)\b",
            re.IGNORECASE,
        ),
        label="friction-derivative",
        explanation=(
            "Hyphenated or near-friction phrasing imports the §3 banned 'friction' "
            "concept while sidestepping the literal word."
        ),
    ),
)


def check_n9_parsimony(
    rule_count: int,
    observation_count: int = DEFAULT_OBSERVATION_COUNT,
) -> list[StructuralFlag]:
    """N9: rule count should not vastly exceed observation count.

    Three tiers based on the rule:observation ratio. If rules could not be
    parsed (rule_count == 0), no flag — N9 needs a rule count.
    """
    if rule_count <= 0:
        return []
    ratio = rule_count / observation_count
    if rule_count > observation_count * N9_TIER_1_RATIO_FLOOR:
        tier = FlagTier.TIER_1
    elif rule_count > observation_count * N9_TIER_2_RATIO_FLOOR:
        tier = FlagTier.TIER_2
    elif rule_count > observation_count * N9_TIER_3_RATIO_FLOOR:
        tier = FlagTier.TIER_3
    else:
        return []
    return [
        StructuralFlag(
            criterion="N9",
            tier=tier,
            layer="heuristic",
            evidence=f"rule_count={rule_count}, observation_count={observation_count}",
            explanation=(
                f"Rule count exceeds observation count by ratio {ratio:.2f} — "
                "suggests redundancy or fabrication beyond what the observations support."
            ),
        )
    ]


def check_n10_independence(rules: list[ParsedRule]) -> list[StructuralFlag]:
    """N10: no two rules should describe the same phenomenon.

    Prototype implementation is a stub. Production N10 requires an LLM
    clustering pass (or embedding similarity); deferred until the v0.2
    Agent 2 calibration run validates the parsing layer first.
    """
    _ = rules  # acknowledged, deferred
    return []


def check_n11_smuggle_regex(response_text: str) -> list[StructuralFlag]:
    """N11 regex layer: scan response for smuggled-mechanism patterns.

    Each pattern match emits one Tier-2 flag (single layer). The orchestrator
    promotes overlapping regex+LLM evidence to Tier-1 when an LLM layer is
    provided.
    """
    flags: list[StructuralFlag] = []
    for sp in _SMUGGLE_PATTERNS:
        for match in sp.pattern.finditer(response_text):
            start = max(0, match.start() - 40)
            end = min(len(response_text), match.end() + 40)
            window = response_text[start:end].replace("\n", " ").strip()
            flags.append(
                StructuralFlag(
                    criterion="N11",
                    tier=FlagTier.TIER_2,
                    layer="regex",
                    evidence=f"…{window}…",
                    explanation=f"{sp.label}: {sp.explanation}",
                )
            )
    return flags


def check_n12_hierarchy(
    rules: list[ParsedRule],
    response_text: str,
) -> list[StructuralFlag]:
    """N12: rule sets of size ≥ 5 with no hierarchy markers are flat enumerations."""
    if len(rules) < N12_MIN_RULES_FOR_HIERARCHY:
        return []
    lower = response_text.lower()
    for marker in HIERARCHY_MARKERS:
        if marker in lower:
            return []
    return [
        StructuralFlag(
            criterion="N12",
            tier=FlagTier.TIER_2,
            layer="heuristic",
            evidence=f"rule_count={len(rules)}, no hierarchy markers found",
            explanation=(
                f"Flat enumeration of {len(rules)} rules with none of the hierarchy "
                f"markers {HIERARCHY_MARKERS} — no explicit theory structure."
            ),
        )
    ]


def audit_trial_response(
    trial_json: dict[str, Any],
    llm_smuggle_flags: list[StructuralFlag] | None = None,
    observation_count: int = DEFAULT_OBSERVATION_COUNT,
) -> StructuralAuditReport:
    """Run all structural checks on one trial JSON and emit a report.

    ``trial_json`` is a dict in the shape produced by ``runners/base.py`` —
    must include ``response_text``, ``framework_id``, ``model_full_version``,
    ``stage``, and ``trial_index``.

    ``llm_smuggle_flags`` is an optional pre-computed list of N11 LLM-layer
    flags. When provided, overlapping (criterion=N11) regex+LLM evidence is
    promoted to Tier-1.
    """
    response_text = trial_json["response_text"]
    rules = extract_rules(response_text)

    flags: list[StructuralFlag] = []
    flags.extend(check_n9_parsimony(len(rules), observation_count))
    flags.extend(check_n10_independence(rules))
    regex_n11 = check_n11_smuggle_regex(response_text)
    flags.extend(_combine_n11(regex_n11, llm_smuggle_flags or []))
    flags.extend(check_n12_hierarchy(rules, response_text))

    return StructuralAuditReport(
        trial_path=str(trial_json.get("trial_path", "")),
        framework_id=trial_json["framework_id"],
        model_full_version=trial_json["model_full_version"],
        stage=trial_json["stage"],
        trial_index=int(trial_json["trial_index"]),
        rule_count=len(rules),
        flags=flags,
    )


def _combine_n11(
    regex_flags: list[StructuralFlag],
    llm_flags: list[StructuralFlag],
) -> list[StructuralFlag]:
    """Merge N11 regex and LLM layers; promote overlapping evidence to Tier-1.

    Overlap heuristic: any 15-char window of regex evidence appearing inside any
    LLM evidence promotes both to Tier-1 (single combined flag). Non-overlapping
    items from either layer keep their original Tier-2.
    """
    if not llm_flags:
        return regex_flags

    combined: list[StructuralFlag] = []
    matched_llm: set[int] = set()
    matched_regex: set[int] = set()

    for r_idx, r in enumerate(regex_flags):
        r_text = r.evidence.lower()
        for l_idx, lflag in enumerate(llm_flags):
            l_text = lflag.evidence.lower()
            if _has_overlap(r_text, l_text):
                matched_regex.add(r_idx)
                matched_llm.add(l_idx)
                combined.append(
                    StructuralFlag(
                        criterion="N11",
                        tier=FlagTier.TIER_1,
                        layer="combined",
                        evidence=f"regex: {r.evidence}  ||  llm: {lflag.evidence}",
                        explanation=(
                            f"Both layers agree on smuggled mechanism. "
                            f"Regex: {r.explanation} LLM: {lflag.explanation}"
                        ),
                    )
                )
                break

    for r_idx, r in enumerate(regex_flags):
        if r_idx not in matched_regex:
            combined.append(r)
    for l_idx, lflag in enumerate(llm_flags):
        if l_idx not in matched_llm:
            combined.append(lflag)
    return combined


def _has_overlap(a: str, b: str, window: int = 15) -> bool:
    """Cheap overlap check: does any ``window``-char substring of ``a`` appear in ``b``?"""
    if len(a) < window or len(b) < window:
        return a in b or b in a
    return any(a[i : i + window] in b for i in range(0, len(a) - window + 1, max(1, window // 3)))
