"""Tested-model runners. Each subclass enforces fresh API client per call."""

from physlit.runners.base import TestedModelRunner, TrialRecord

__all__ = ["TestedModelRunner", "TrialRecord"]
