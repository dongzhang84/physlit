"""Structural Auditor (Agent 2) — v0.2 audit layer.

This package implements N9-N12 structural-criteria flagging on
Stage-1 induction and Stage-2 formulation responses, as documented in
``frameworks/01_aristotelian/ideal_induction.md`` §8.

The module emits **flags**, not verdicts. Each flag has a tier
(Tier-1 = high-confidence, regex + LLM both fired; Tier-2 = single
layer fired; Tier-3 = weak signal, archive-only). Human review on
flags is the prereg-mandated tie-breaker in v0.2.

Designed to be cheap and fast: regex layers are pure-Python (zero
API cost); LLM layer uses Anthropic Haiku at temperature 0. Run
against the locked v0.1 trial set for calibration before v0.2 prereg
lock.
"""

from __future__ import annotations

from .models import FlagTier, StructuralAuditReport, StructuralFlag
from .parse_rules import ParsedRule, extract_rules
from .structural import audit_trial_response

__all__ = [
    "FlagTier",
    "ParsedRule",
    "StructuralAuditReport",
    "StructuralFlag",
    "audit_trial_response",
    "extract_rules",
]
