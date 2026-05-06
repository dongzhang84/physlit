"""Schema for a phenomenon framework spec.

Every framework (Aristotelian / F=mv / reverse gravity / ...) is declared by
one ``frameworks/<id>/spec.yaml`` file that validates against
:class:`FrameworkSpec`. The ``tier`` field decides which generator produces
the framework's observations:

* ``tier1_simulator`` — Python simulator module path
* ``tier2_ai``        — AI-generated (architectural slot only, disabled in v0.1)
* ``tier3_manual``    — manually authored markdown

Cross-field rules are enforced by a model-level validator so that invalid
spec/tier combinations fail at load time rather than at runtime.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Tier = Literal["tier1_simulator", "tier2_ai", "tier3_manual"]
Category = Literal["A_historical", "B_counterfactual", "C_arbitrary"]


class FrameworkSpec(BaseModel):
    """The minimal description of a phenomenon framework."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(pattern=r"^\d{2}_[a-z0-9_]+$", min_length=4)
    name: str = Field(min_length=1)
    category: Category
    tier: Tier
    description: str = Field(min_length=1)
    rationale: str = Field(min_length=1)

    # Tier 1 only
    simulator_module: str | None = None

    # Tier 2 only (architectural slot; v0.5+, not used in v0.1)
    generation_prompt: str | None = None
    generator_model: str | None = None

    # Tier 3 only
    manual_authoring_note: str | None = None

    @model_validator(mode="after")
    def _check_tier_fields(self) -> FrameworkSpec:
        tier1_set = self.simulator_module is not None
        tier2_set = self.generation_prompt is not None or self.generator_model is not None
        tier3_set = self.manual_authoring_note is not None

        if self.tier == "tier1_simulator":
            if not tier1_set:
                raise ValueError("tier1_simulator requires simulator_module")
            if tier2_set or tier3_set:
                raise ValueError(
                    "tier1_simulator must not set tier2 / tier3 fields "
                    "(generation_prompt, generator_model, manual_authoring_note)"
                )
        elif self.tier == "tier2_ai":
            if self.generation_prompt is None or self.generator_model is None:
                raise ValueError("tier2_ai requires both generation_prompt and generator_model")
            if tier1_set or tier3_set:
                raise ValueError(
                    "tier2_ai must not set tier1 / tier3 fields "
                    "(simulator_module, manual_authoring_note)"
                )
        else:  # tier3_manual
            if not tier3_set:
                raise ValueError("tier3_manual requires manual_authoring_note")
            if tier1_set or tier2_set:
                raise ValueError(
                    "tier3_manual must not set tier1 / tier2 fields "
                    "(simulator_module, generation_prompt, generator_model)"
                )
        return self
