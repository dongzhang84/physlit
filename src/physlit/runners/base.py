"""Base runner: ``TrialRecord`` + ``TestedModelRunner`` ABC.

Each trial creates a fresh API client and a new session UUID
(``CLAUDE.md`` hard rule). Multi-turn or context reuse across stages
is forbidden at this layer. Subclasses *must* construct a new SDK
client inside ``call_model`` per call; do not cache one on the
instance.

Records are written verbatim under
``<output_root>/<framework_id>/<stage>/trial_<i>_t<temp>.json``.
For dry-run output, the caller passes ``output_root =
results/_dryrun/<utc-timestamp>``; for canonical v0.1 evaluation
output, ``output_root = results/<full-model-version>``.
"""

from __future__ import annotations

import json
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path


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
        """Pinned full model version string (e.g. ``claude-opus-4-7-20260101``).

        Never an alias; never a family name.
        """

    @abstractmethod
    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> tuple[str, str]:
        """Single API call. Returns ``(response_text, returned_model_version)``.

        Implementations MUST:

        - Construct a fresh SDK client inside this method (do not cache).
        - Include ``temperature`` and ``max_tokens`` in the request.
        - Return the ``response.model`` field verbatim so ``run_trial``
          can verify it matches ``self.model_id``.

        ``session_id`` is the per-trial UUID; runners that have no
        per-call session concept may simply log it.
        """

    @abstractmethod
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Approximate USD cost of the call. Per-token pricing constants
        live in the subclass. Used for the ``cost_usd_estimate`` field
        and for budget gating; not authoritative."""

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
        ``response.model`` against ``self.model_id``, returns a
        ``TrialRecord``.

        Raises ``RuntimeError`` on model version mismatch.
        """
        session_id = str(uuid.uuid4())
        response_text, returned_model = self.call_model(
            prompt_text, temperature, session_id, max_tokens
        )
        if returned_model != self.model_id:
            raise RuntimeError(
                f"Model version mismatch in {self.model_family} runner: "
                f"configured {self.model_id!r}, API returned "
                f"{returned_model!r}"
            )
        return TrialRecord(
            framework_id=framework_id,
            model_full_version=self.model_id,
            stage=stage,
            trial_index=trial_index,
            temperature=temperature,
            prompt_version=prompt_version,
            prompt_text=prompt_text,
            response_text=response_text,
            response_timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            api_session_id=session_id,
            cost_usd_estimate=self.estimate_cost(prompt_text, response_text),
        )

    @staticmethod
    def save_trial(record: TrialRecord, output_root: Path) -> Path:
        """Write the record to
        ``<output_root>/<framework_id>/<stage>/trial_<i>_t<temp>.json``.

        Returns the path written. Caller picks ``output_root``:
        ``results/<model>/`` for canonical evaluations,
        ``results/_dryrun/<timestamp>/`` for exploratory runs.
        """
        out_dir = output_root / record.framework_id / record.stage
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = f"trial_{record.trial_index}_t{record.temperature}.json"
        out_file = out_dir / filename
        out_file.write_text(json.dumps(asdict(record), indent=2, sort_keys=True))
        return out_file
