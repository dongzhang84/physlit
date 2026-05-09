"""Tested-model runners. Each subclass enforces fresh API client per call."""

from physlit.runners.base import CallResult, TestedModelRunner, TrialRecord
from physlit.runners.claude import ClaudeRunner
from physlit.runners.gemini import GeminiRunner
from physlit.runners.openai import OpenAIRunner

__all__ = [
    "CallResult",
    "ClaudeRunner",
    "GeminiRunner",
    "OpenAIRunner",
    "TestedModelRunner",
    "TrialRecord",
]
