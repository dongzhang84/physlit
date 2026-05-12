"""Dataclasses for structural-audit flags and reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class FlagTier(StrEnum):
    """Confidence tier for one structural flag.

    Tier-1: regex + LLM layers both fired on overlapping evidence — high confidence,
        human review prioritised.
    Tier-2: single layer fired — moderate confidence, human review next-priority.
    Tier-3: weak signal (e.g. soft threshold breach) — archived, not strictly required
        for human review.
    """

    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"


@dataclass(frozen=True)
class StructuralFlag:
    """One structural-criterion flag on one trial."""

    criterion: str  # "N9" / "N10" / "N11" / "N12"
    tier: FlagTier
    layer: str  # "regex" / "llm" / "combined" / "heuristic"
    evidence: str  # verbatim quote or count from the response
    explanation: str  # one-sentence human-readable justification


@dataclass(frozen=True)
class StructuralAuditReport:
    """Per-trial structural-audit output."""

    trial_path: str
    framework_id: str
    model_full_version: str
    stage: str
    trial_index: int
    rule_count: int
    flags: list[StructuralFlag] = field(default_factory=list)

    @property
    def tier1_count(self) -> int:
        return sum(1 for f in self.flags if f.tier == FlagTier.TIER_1)

    @property
    def tier2_count(self) -> int:
        return sum(1 for f in self.flags if f.tier == FlagTier.TIER_2)

    @property
    def tier3_count(self) -> int:
        return sum(1 for f in self.flags if f.tier == FlagTier.TIER_3)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Convert FlagTier enum to its string value for JSON serialisation.
        for flag in d["flags"]:
            flag["tier"] = (
                flag["tier"].value if isinstance(flag["tier"], FlagTier) else flag["tier"]
            )
        return d

    @staticmethod
    def save(report: StructuralAuditReport, output_dir: Path) -> Path:
        """Write the report to ``<output_dir>/structural_<stage>_trial<N>.json``."""
        import json

        output_dir.mkdir(parents=True, exist_ok=True)
        out_file = output_dir / f"structural_{report.stage}_trial{report.trial_index}.json"
        out_file.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True))
        return out_file
