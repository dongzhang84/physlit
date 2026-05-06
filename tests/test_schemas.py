"""Tests for FrameworkSpec schema and the spec validator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from physlit.schema import FrameworkSpec

FRAMEWORKS_DIR = Path(__file__).resolve().parent.parent / "frameworks"


def _aristotelian() -> dict[str, Any]:
    return {
        "id": "01_aristotelian",
        "name": "Aristotelian Mechanics",
        "category": "A_historical",
        "tier": "tier3_manual",
        "description": "desc",
        "rationale": "why",
        "manual_authoring_note": "reviewed",
    }


def _f_equals_mv() -> dict[str, Any]:
    return {
        "id": "02_f_equals_mv",
        "name": "F=mv World",
        "category": "B_counterfactual",
        "tier": "tier1_simulator",
        "description": "desc",
        "rationale": "why",
        "simulator_module": "physlit.generators.tier1.f_equals_mv",
    }


def test_aristotelian_validates() -> None:
    spec = FrameworkSpec.model_validate(_aristotelian())
    assert spec.tier == "tier3_manual"
    assert spec.simulator_module is None


def test_tier1_minimal_validates() -> None:
    spec = FrameworkSpec.model_validate(_f_equals_mv())
    assert spec.simulator_module == "physlit.generators.tier1.f_equals_mv"


def test_tier1_missing_simulator_module_fails() -> None:
    data = _f_equals_mv()
    del data["simulator_module"]
    with pytest.raises(ValidationError, match="simulator_module"):
        FrameworkSpec.model_validate(data)


def test_tier3_with_simulator_module_fails() -> None:
    data = _aristotelian()
    data["simulator_module"] = "physlit.generators.tier1.bogus"
    with pytest.raises(ValidationError, match="must not set tier1"):
        FrameworkSpec.model_validate(data)


def test_tier2_requires_both_prompt_and_model() -> None:
    data: dict[str, Any] = {
        "id": "99_tier2_demo",
        "name": "Tier 2 Demo",
        "category": "C_arbitrary",
        "tier": "tier2_ai",
        "description": "desc",
        "rationale": "why",
        "generation_prompt": "prompt only",
    }
    with pytest.raises(ValidationError, match="generation_prompt and generator_model"):
        FrameworkSpec.model_validate(data)


def test_id_pattern_enforced() -> None:
    data = _aristotelian()
    data["id"] = "Aristotelian"  # missing leading digits + lowercase pattern
    with pytest.raises(ValidationError, match="id"):
        FrameworkSpec.model_validate(data)


def test_unknown_field_rejected() -> None:
    data = _aristotelian()
    data["bogus_extra"] = 1
    with pytest.raises(ValidationError, match="bogus_extra"):
        FrameworkSpec.model_validate(data)


def test_spec_is_frozen() -> None:
    spec = FrameworkSpec.model_validate(_aristotelian())
    with pytest.raises(ValidationError):
        spec.name = "mutated"


@pytest.mark.parametrize(
    "spec_path",
    sorted(FRAMEWORKS_DIR.glob("*/spec.yaml")),
    ids=lambda p: p.parent.name,
)
def test_committed_spec_validates(spec_path: Path) -> None:
    data = yaml.safe_load(spec_path.read_text())
    spec = FrameworkSpec.model_validate(data)
    assert spec.id == spec_path.parent.name, "id must match directory name"
