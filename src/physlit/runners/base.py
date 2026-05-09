"""Base runner: ``CallResult``, ``TrialRecord``, and ``TestedModelRunner`` ABC.

Each trial creates a fresh API client and a new session UUID
(``CLAUDE.md`` hard rule). Multi-turn or context reuse across stages
is forbidden at this layer. Subclasses *must* construct a new SDK
client inside ``call_model`` per call; do not cache one on the
instance.

R1(a) per-call identity capture (per
``docs/v0_1_runner_requirements.md``) is implemented by having
``call_model`` return a ``CallResult`` whose ``identity_fields``
dict carries every model-identity field the SDK exposes. The base
``run_trial`` records this dict on the ``TrialRecord`` and enforces
strict equality between the response's primary identifier and the
runner's pinned ``model_id``. A mismatch raises and halts the run.

Records are written verbatim under
``<output_root>/<framework_id>/<stage>/trial_<i>_t<temp>.json``.
For dry-run output, ``output_root = results/_dryrun/<utc-timestamp>``;
for calibration, ``results/_calibration/<utc-timestamp>``; for
canonical v0.1 production output, ``results/<full-model-version>``.
"""

from __future__ import annotations

import json
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class CallResult:
    """Outcome of one ``call_model`` invocation.

    The ``primary_id`` is the single identifier the runner compares
    against ``self.model_id`` for the strict version check. The
    ``identity_fields`` dict is the *full* set of model-identity
    fields the SDK surfaces — used for R1(a) audit and recorded
    verbatim on the ``TrialRecord``.
    """

    response_text: str
    primary_id: str
    identity_fields: dict[str, str]
    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class TrialRecord:
    """One trial of one stage. Persisted verbatim to JSON.

    Field naming is intentional and stable; downstream judges and the
    static-site renderer key off these names.
    """

    framework_id: str
    model_full_version: str
    stage: str
    trial_index: int
    temperature: float
    prompt_version: str
    prompt_text: str
    response_text: str
    response_timestamp_utc: str
    api_session_id: str
    cost_usd_estimate: float
    input_tokens: int = 0
    output_tokens: int = 0
    vendor_identity_fields: dict[str, str] = field(default_factory=dict)


class TestedModelRunner(ABC):
    """Abstract base for one tested-model family (Anthropic / OpenAI / Google).

    Subclasses implement ``model_family``, ``model_id``, ``call_model``,
    and ``estimate_cost``. All trial orchestration (fresh UUID,
    timestamp, version verification, save path) is handled here.
    """

    @property
    @abstractmethod
    def model_family(self) -> str:
        """Vendor family — ``"anthropic"`` / ``"openai"`` / ``"google"``."""

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Pinned full model version string (e.g. ``gpt-5.5-2026-04-23``).

        Never an alias; never a family name (with the exception of
        Anthropic Opus 4.7, where the alias ``claude-opus-4-7`` *is*
        the most-specific identifier the API exposes at v0.1 lock time).
        """

    @abstractmethod
    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> CallResult:
        """Single API call. Returns a :class:`CallResult`.

        Implementations MUST:

        - Construct a fresh SDK client inside this method (do not cache).
        - Include ``max_tokens`` in the request. ``temperature`` may be
          ignored by some vendors (e.g. Anthropic Opus 4.7 deprecated
          ``temperature``); record the request value but do not fail
          if the vendor rejects it.
        - Populate ``identity_fields`` with every model-identity field
          the SDK exposes — the primary one (``primary_id``) plus any
          auxiliary identifiers (system fingerprint, deployment id,
          etc.) for R1(a) audit.

        ``session_id`` is the per-trial UUID; runners that have no
        per-call session concept may simply log it.
        """

    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Approximate USD cost given the actual token counts the API
        reported. Per-token pricing constants live in the subclass.
        Used for the ``cost_usd_estimate`` field; not authoritative —
        the vendor's invoice is."""

    def run_trial(
        self,
        framework_id: str,
        stage: str,
        prompt_text: str,
        prompt_version: str,
        trial_index: int,
        temperature: float,
        max_tokens: int = 2048,
    ) -> TrialRecord:
        """Run one trial. Generates session UUID, calls model, verifies
        the response's primary identifier against ``self.model_id``,
        returns a :class:`TrialRecord`.

        Raises ``RuntimeError`` on model-identity mismatch (R1(a)
        halt-on-drift for Gemini; equivalent strict-version check for
        Anthropic and OpenAI).
        """
        session_id = str(uuid.uuid4())
        result = self.call_model(prompt_text, temperature, session_id, max_tokens)
        if result.primary_id != self.model_id:
            raise RuntimeError(
                f"Model identity mismatch in {self.model_family} runner: "
                f"configured {self.model_id!r}, API returned "
                f"{result.primary_id!r}. Auxiliary identity fields: "
                f"{result.identity_fields!r}"
            )
        return TrialRecord(
            framework_id=framework_id,
            model_full_version=self.model_id,
            stage=stage,
            trial_index=trial_index,
            temperature=temperature,
            prompt_version=prompt_version,
            prompt_text=prompt_text,
            response_text=result.response_text,
            response_timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            api_session_id=session_id,
            cost_usd_estimate=self.estimate_cost(result.input_tokens, result.output_tokens),
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            vendor_identity_fields=dict(result.identity_fields),
        )

    @staticmethod
    def save_trial(record: TrialRecord, output_root: Path) -> Path:
        """Write the record to
        ``<output_root>/<framework_id>/<stage>/trial_<i>_t<temp>.json``.

        Returns the path written. Caller picks ``output_root``:
        ``results/<model>/`` for production, ``results/_calibration/<ts>/``
        for calibration, ``results/_dryrun/<ts>/`` for exploratory runs.
        """
        out_dir = output_root / record.framework_id / record.stage
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = f"trial_{record.trial_index}_t{record.temperature}.json"
        out_file = out_dir / filename
        out_file.write_text(json.dumps(asdict(record), indent=2, sort_keys=True))
        return out_file
