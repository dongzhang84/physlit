"""Unit tests for the structural-audit (Agent 2) prototype.

Covers:
- parse_rules: numbered-list extraction across bolded / plain / Rule-N shapes
- N9 parsimony tier boundaries
- N11 regex layer hit on known smuggled-mechanism patterns
- N12 hierarchy heuristic
- Orchestrator end-to-end on a synthetic trial JSON
- Orchestrator end-to-end on the real v0.1 GPT trial 3 (Stage 2 formulation),
  which the v0.1 human audit identified as the canonical structural-fail case.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from physlit.audit import FlagTier, audit_trial_response, extract_rules
from physlit.audit.structural import (
    check_n9_parsimony,
    check_n11_smuggle_regex,
    check_n12_hierarchy,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------- parse_rules ----------------------------------------------------


def test_extract_rules_bolded_markdown() -> None:
    text = """
**1. Heavy bodies fall.**

Some explanation.

**2. Light bodies rise.**

More text.

**3. Medium resists.**
"""
    rules = extract_rules(text)
    assert len(rules) == 3
    assert rules[0].number == 1
    assert "Heavy bodies fall" in rules[0].body


def test_extract_rules_rule_n_prefix() -> None:
    text = """
Rule 1: The cart needs a pusher.
Rule 2: The arrow flies onward.
Rule 3: Heavy bodies seek their natural place.
"""
    rules = extract_rules(text)
    assert len(rules) == 3
    assert rules[1].body.startswith("The arrow flies")


def test_extract_rules_plain_numbered() -> None:
    text = """
1. Heavier things fall faster.
2. Light substances move up.
3. Some things resist motion.
"""
    rules = extract_rules(text)
    assert len(rules) == 3


def test_extract_rules_returns_empty_on_no_pattern() -> None:
    text = "This response is just prose with no numbered rules at all."
    assert extract_rules(text) == []


# ---------- N9 parsimony ---------------------------------------------------


def test_n9_no_flag_when_rule_count_at_observation_count() -> None:
    assert check_n9_parsimony(rule_count=12, observation_count=12) == []


def test_n9_tier_3_when_slightly_over() -> None:
    flags = check_n9_parsimony(rule_count=13, observation_count=12)
    assert len(flags) == 1
    assert flags[0].tier == FlagTier.TIER_3


def test_n9_tier_2_when_rule_count_exceeds_1_25x_observations() -> None:
    # rule_count > obs * 1.25 -> Tier-2. For obs=12, rule_count >= 16.
    flags = check_n9_parsimony(rule_count=16, observation_count=12)
    assert len(flags) == 1
    assert flags[0].tier == FlagTier.TIER_2


def test_n9_tier_3_at_1_25x_boundary() -> None:
    # rule_count == 15 is exactly obs * 1.25 — strictly less than 1.25-floor, so Tier-3.
    flags = check_n9_parsimony(rule_count=15, observation_count=12)
    assert len(flags) == 1
    assert flags[0].tier == FlagTier.TIER_3


def test_n9_tier_1_when_rule_count_exceeds_5_thirds_of_observations() -> None:
    # rule_count > obs * 5/3 -> Tier-1. For obs=12, that means rule_count >= 21.
    flags = check_n9_parsimony(rule_count=21, observation_count=12)
    assert len(flags) == 1
    assert flags[0].tier == FlagTier.TIER_1


def test_n9_tier_2_when_rule_count_at_5_thirds_boundary() -> None:
    # rule_count == 20 is exactly obs * 5/3 — not strictly greater, so Tier-2.
    flags = check_n9_parsimony(rule_count=20, observation_count=12)
    assert len(flags) == 1
    assert flags[0].tier == FlagTier.TIER_2


def test_n9_no_flag_when_rule_count_zero() -> None:
    assert check_n9_parsimony(rule_count=0) == []


# ---------- N11 regex smuggle ----------------------------------------------


def test_n11_regex_detects_road_robs_motion() -> None:
    text = "The road and air rob motion from the cart once nothing pushes it."
    flags = check_n11_smuggle_regex(text)
    assert len(flags) >= 1
    assert all(f.criterion == "N11" for f in flags)
    assert all(f.tier == FlagTier.TIER_2 for f in flags)
    assert any("motion-removal" in f.explanation for f in flags)


def test_n11_regex_detects_surface_supported() -> None:
    text = "The oak floats because it is surface-supported by the water."
    flags = check_n11_smuggle_regex(text)
    assert len(flags) >= 1
    assert any("surface-support" in f.explanation for f in flags)


def test_n11_regex_detects_vector_components() -> None:
    text = "The horizontal and vertical components combine to give the trajectory."
    flags = check_n11_smuggle_regex(text)
    assert len(flags) >= 1
    assert any("vector-decomposition" in f.explanation for f in flags)


def test_n11_regex_passes_clean_aristotelian_text() -> None:
    text = (
        "Heavy bodies seek their natural place. The air helps to bear the "
        "arrow forward. The medium resists passage and slows the pebble."
    )
    assert check_n11_smuggle_regex(text) == []


# ---------- N12 hierarchy --------------------------------------------------


def test_n12_no_flag_under_threshold() -> None:
    from physlit.audit.parse_rules import ParsedRule

    rules = [ParsedRule(number=i + 1, body=f"rule {i}") for i in range(4)]
    assert check_n12_hierarchy(rules, "no markers here") == []


def test_n12_flags_flat_enumeration_at_threshold() -> None:
    from physlit.audit.parse_rules import ParsedRule

    rules = [ParsedRule(number=i + 1, body=f"rule {i}") for i in range(7)]
    flags = check_n12_hierarchy(rules, "Every rule stands on its own without reference.")
    assert len(flags) == 1
    assert flags[0].tier == FlagTier.TIER_2


def test_n12_passes_when_hierarchy_marker_present() -> None:
    from physlit.audit.parse_rules import ParsedRule

    rules = [ParsedRule(number=i + 1, body=f"rule {i}") for i in range(7)]
    text = "Rule 5 is a corollary of rule 1."
    assert check_n12_hierarchy(rules, text) == []


# ---------- Orchestrator end-to-end ----------------------------------------


def _make_synthetic_trial(response_text: str, **overrides: object) -> dict[str, object]:
    return {
        "framework_id": "01_aristotelian",
        "model_full_version": "test-model",
        "stage": "induction",
        "trial_index": 0,
        "response_text": response_text,
        **overrides,
    }


def test_audit_orchestrator_clean_response_emits_no_flags() -> None:
    response = """
**1. Heavy bodies tend toward their natural place.**

**2. Light bodies tend upward.**

**3. The medium resists passage.**
"""
    report = audit_trial_response(_make_synthetic_trial(response))
    assert report.rule_count == 3
    assert report.flags == []


def test_audit_orchestrator_detects_combined_n9_and_n11() -> None:
    rules_block = "\n".join(
        f"**{i}. The road and air rob motion from rule {i} body.**" for i in range(1, 21)
    )
    report = audit_trial_response(_make_synthetic_trial(rules_block))
    assert report.rule_count == 20
    criteria = {f.criterion for f in report.flags}
    assert "N9" in criteria
    assert "N11" in criteria


# ---------- Real v0.1 fixture: GPT trial 3 Stage 2 -------------------------

GPT_TRIAL_3_STAGE_2 = (
    REPO_ROOT
    / "results"
    / "gpt-5.5-2026-04-23"
    / "01_aristotelian"
    / "formulation"
    / "trial_3_t0.0.json"
)


@pytest.mark.skipif(
    not GPT_TRIAL_3_STAGE_2.is_file(),
    reason="v0.1 GPT trial 3 fixture not present (running outside the full repo)",
)
def test_audit_on_real_gpt_trial_3_stage_2_flags_n9() -> None:
    """The v0.1 human audit identified GPT trial 3 Stage 2 as 17-rule redundant.
    The structural auditor should flag N9 parsimony at Tier-1 or Tier-2."""
    trial_json = json.loads(GPT_TRIAL_3_STAGE_2.read_text())
    report = audit_trial_response(trial_json)
    n9_flags = [f for f in report.flags if f.criterion == "N9"]
    assert n9_flags, (
        f"Expected at least one N9 flag on GPT trial 3 Stage 2 "
        f"(rule_count={report.rule_count}); got none. "
        "Either the rule-parser missed the rule list, or the N9 thresholds "
        "are too lenient — both worth investigating."
    )
