"""Tests for the Stage-3 scenario parser and round-trip parity with
``frameworks/01_aristotelian/prediction_tests.md``.

The parity tests are deliberately tied to the *committed* Aristotelian
file: any edit that breaks the parser will fail here, before it can
produce a malformed prompt at runtime.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from physlit.scenarios import (
    Scenario,
    extract_scenarios,
    load_scenarios,
    render_scenarios_block,
)

REPO = Path(__file__).resolve().parent.parent
ARISTOTELIAN_PATH = REPO / "frameworks" / "01_aristotelian" / "prediction_tests.md"


def test_extract_scenarios_returns_five_aristotelian() -> None:
    scenarios = load_scenarios(ARISTOTELIAN_PATH)
    assert len(scenarios) == 5
    assert [s.index for s in scenarios] == [1, 2, 3, 4, 5]


def test_extracted_prompts_contain_expected_substrings() -> None:
    """Each scenario's parsed prompt must contain the substring that
    keys it to its physics-content. If a future edit reshuffles the
    file, this test fails before the dry-run runner sees a wrong
    prompt at runtime. Whitespace is normalised to single spaces so
    line wrapping in the source markdown does not break the match."""
    scenarios = load_scenarios(ARISTOTELIAN_PATH)
    expectations = {
        1: ("iron ball", "wooden ball", "tower"),
        2: ("smooth ice", "push", "subsequent motion"),
        3: ("two stones", "twice what stone b weighs"),
        4: ("sealed", "all air has been removed", "feather"),
        5: ("archer", "arrow", "sustains"),
    }
    by_index = {s.index: s for s in scenarios}
    for idx, substrings in expectations.items():
        prompt_normalised = " ".join(by_index[idx].prompt.lower().split())
        for needle in substrings:
            assert needle.lower() in prompt_normalised, (
                f"Scenario {idx}: expected substring {needle!r} not in "
                f"parsed prompt; prediction_tests.md may have drifted"
            )


def test_extracted_prompts_strip_judge_columns() -> None:
    """The PASS / FAIL prediction columns and 'Why this scenario'
    commentary are for judges and must NEVER reach the tested model."""
    scenarios = load_scenarios(ARISTOTELIAN_PATH)
    for s in scenarios:
        assert "Aristotelian (PASS)" not in s.prompt, (
            f"Scenario {s.index}: judge column leaked into model prompt"
        )
        assert "Standard physics (FAIL)" not in s.prompt, (
            f"Scenario {s.index}: judge column leaked into model prompt"
        )
        assert "Why this scenario" not in s.prompt, (
            f"Scenario {s.index}: reviewer commentary leaked into model prompt"
        )


def test_render_scenarios_block_is_numbered() -> None:
    scenarios = load_scenarios(ARISTOTELIAN_PATH)
    block = render_scenarios_block(scenarios)
    assert block.startswith("Scenario 1.")
    assert "\n\nScenario 2." in block
    assert "\n\nScenario 5." in block
    # And the block does NOT contain the judge content or commentary
    assert "Aristotelian (PASS)" not in block
    assert "Why this scenario" not in block


def test_extract_scenarios_raises_on_missing_marker() -> None:
    bad = """## Scenario 1 — broken

Some text but no prompt marker.

| Column | Prediction |
"""
    with pytest.raises(ValueError, match="missing '\\*\\*Prompt to the model"):
        extract_scenarios(bad)


def test_extract_scenarios_raises_on_no_terminator() -> None:
    # Marker present but never a table or '---' afterwards
    bad = """## Scenario 1 — broken

**Prompt to the model.** A scenario but never a table or rule.
"""
    with pytest.raises(ValueError, match="no terminator after prompt"):
        extract_scenarios(bad)


def test_extract_scenarios_raises_on_non_contiguous_indices() -> None:
    bad = """## Scenario 1 — first

**Prompt to the model.** First.

| a | b |

## Scenario 3 — third (skipped 2!)

**Prompt to the model.** Third.

| a | b |
"""
    with pytest.raises(ValueError, match="1-based contiguous"):
        extract_scenarios(bad)


def test_scenario_is_frozen() -> None:
    s = Scenario(index=1, title="x", prompt="y")
    with pytest.raises(Exception):  # noqa: B017 — pydantic ValidationError
        s.index = 2
