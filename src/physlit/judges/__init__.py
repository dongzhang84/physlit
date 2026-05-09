"""Judge utilities for v0.1.

Two layers:
- ``banned_check.py`` — calibration-time syntactic scan for banned
  concepts. Not the v0.1 judge.
- ``judge_base.py`` + ``claude_judge.py`` + ``openai_judge.py`` — the
  v0.1 dual-judge pipeline (Phase 8 per implementation guide). Each
  Stage 1-3 trial is scored by both judges; agreement = per-trial
  verdict; disagreement is the IRR rate.
"""

from physlit.judges.banned_check import BannedHit, scan_for_banned
from physlit.judges.claude_judge import ClaudeJudge
from physlit.judges.judge_base import JudgeBase, JudgeVerdict, parse_verdict_json
from physlit.judges.openai_judge import OpenAIJudge

__all__ = [
    "BannedHit",
    "ClaudeJudge",
    "JudgeBase",
    "JudgeVerdict",
    "OpenAIJudge",
    "parse_verdict_json",
    "scan_for_banned",
]
