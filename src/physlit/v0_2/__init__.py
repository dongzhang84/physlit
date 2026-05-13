"""v0.2 analysis layer — structural axis + disagree-resolver agents.

This package builds on v0.1's frozen content-judging output. It does
not modify any v0.1 artifact. v0.2 reads v0.1's trial responses,
content-judge verdicts, and human-audit verdicts, and adds:

- A second judging axis (structural, N9-N12) using the same two
  vendor judges with a different prompt.
- Two Gemini-3.1-Pro resolver agents (Agent 1 for content disagrees,
  Agent 2 for structural disagrees).
- A composite verdict aggregator (`v0.2_aggregate.py`) that combines
  the two axes by AND.

All v0.2 frozen artifacts (criteria, prompts) are pinned at the
`prereg-v0.2-locked` git tag.
"""

from __future__ import annotations

from .gemini_agent import GEMINI_AGENT_MODEL_ID, GeminiAgent
from .loaders import (
    ContentDisagreeCase,
    StructuralVerdictBundle,
    find_content_disagree_cases,
    load_structural_verdicts,
)

__all__ = [
    "GEMINI_AGENT_MODEL_ID",
    "ContentDisagreeCase",
    "GeminiAgent",
    "StructuralVerdictBundle",
    "find_content_disagree_cases",
    "load_structural_verdicts",
]
