"""Mock-based runner and prompt-loader tests. Safe in CI (no real API)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from physlit.judges import scan_for_banned
from physlit.prompts import PromptTemplate
from physlit.runners import CallResult, TestedModelRunner, TrialRecord


class _MockRunner(TestedModelRunner):
    """Runner with deterministic fake responses for testing."""

    @property
    def model_family(self) -> str:
        return "mock"

    @property
    def model_id(self) -> str:
        return "mock-model-20260101"

    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> CallResult:
        return CallResult(
            response_text=f"<mock response, prompt[:30]={prompt[:30]!r}>",
            primary_id=self.model_id,
            identity_fields={"response_model": self.model_id},
            input_tokens=len(prompt) // 4,
            output_tokens=8,
        )

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        return 0.0


class _DriftingRunner(_MockRunner):
    """Runner whose API returns a different model version than configured.
    Used to verify the version-mismatch guard fires (R1(a) halt-on-drift)."""

    def call_model(
        self,
        prompt: str,
        temperature: float,
        session_id: str,
        max_tokens: int,
    ) -> CallResult:
        return CallResult(
            response_text="ok",
            primary_id="mock-model-WRONG-DATE",
            identity_fields={
                "response_model": "mock-model-WRONG-DATE",
                "deployment_id": "drifted-deployment-123",
            },
            input_tokens=1,
            output_tokens=1,
        )


def test_run_trial_creates_record() -> None:
    runner = _MockRunner()
    record = runner.run_trial(
        framework_id="01_test",
        stage="induction",
        prompt_text="Hello world",
        prompt_version="v1",
        trial_index=0,
        temperature=0.0,
    )
    assert record.framework_id == "01_test"
    assert record.stage == "induction"
    assert record.model_full_version == "mock-model-20260101"
    assert record.trial_index == 0
    assert record.temperature == 0.0
    assert "mock response" in record.response_text
    # UUID4 strings are 36 chars including hyphens
    assert len(record.api_session_id) == 36


def test_run_trial_session_ids_are_unique() -> None:
    runner = _MockRunner()
    ids = {
        runner.run_trial(
            framework_id="x",
            stage="induction",
            prompt_text="p",
            prompt_version="v1",
            trial_index=i,
            temperature=0.0,
        ).api_session_id
        for i in range(20)
    }
    assert len(ids) == 20  # No collisions across trials


def test_run_trial_raises_on_version_mismatch() -> None:
    """R1(a) halt-on-drift: any identity-field mismatch must raise.

    The base class includes the auxiliary identity fields in the error
    message so the operator has the full audit context at halt time.
    """
    with pytest.raises(RuntimeError, match="Model identity mismatch"):
        _DriftingRunner().run_trial(
            framework_id="01_test",
            stage="induction",
            prompt_text="hi",
            prompt_version="v1",
            trial_index=0,
            temperature=0.0,
        )


def test_save_trial_writes_json(tmp_path: Path) -> None:
    runner = _MockRunner()
    record = runner.run_trial(
        framework_id="01_test",
        stage="induction",
        prompt_text="Hello",
        prompt_version="v1",
        trial_index=0,
        temperature=0.0,
    )
    out_path = runner.save_trial(record, tmp_path)
    assert out_path.exists()
    assert out_path.parent.name == "induction"
    assert out_path.parent.parent.name == "01_test"
    data = json.loads(out_path.read_text())
    assert data["framework_id"] == "01_test"
    assert data["stage"] == "induction"
    assert data["model_full_version"] == "mock-model-20260101"


def test_trial_record_is_frozen() -> None:
    record = TrialRecord(
        framework_id="x",
        model_full_version="v",
        stage="induction",
        trial_index=0,
        temperature=0.0,
        prompt_version="v1",
        prompt_text="p",
        response_text="r",
        response_timestamp_utc="2026-01-01T00:00:00Z",
        api_session_id="00000000-0000-0000-0000-000000000000",
        cost_usd_estimate=0.0,
    )
    with pytest.raises(Exception):  # noqa: B017 — FrozenInstanceError lives in dataclasses
        record.stage = "formulation"  # type: ignore[misc]


def test_trial_record_default_extras() -> None:
    """Post-prereg-lock fields default safely so old code paths still build."""
    record = TrialRecord(
        framework_id="x",
        model_full_version="v",
        stage="induction",
        trial_index=0,
        temperature=0.0,
        prompt_version="v1",
        prompt_text="p",
        response_text="r",
        response_timestamp_utc="2026-01-01T00:00:00Z",
        api_session_id="00000000-0000-0000-0000-000000000000",
        cost_usd_estimate=0.0,
    )
    assert record.input_tokens == 0
    assert record.output_tokens == 0
    assert record.vendor_identity_fields == {}


def test_run_trial_records_vendor_identity_fields() -> None:
    """The base ``run_trial`` must persist the call's identity_fields
    onto the TrialRecord (R1(a) audit)."""
    record = _MockRunner().run_trial(
        framework_id="01_test",
        stage="induction",
        prompt_text="hello world this is a longer prompt for token counting",
        prompt_version="v1",
        trial_index=0,
        temperature=0.0,
    )
    assert record.vendor_identity_fields == {"response_model": "mock-model-20260101"}
    assert record.input_tokens > 0
    assert record.output_tokens > 0


def test_banned_check_finds_banned_terms() -> None:
    """The calibration-time banned-concept scan flags real uses."""
    text = "The arrow continues by inertia and conserves its momentum."
    hits = scan_for_banned(text)
    found_terms = {h.term for h in hits}
    assert "inertia" in found_terms
    assert "momentum" in found_terms


def test_banned_check_skips_unrelated_text() -> None:
    """A clean Aristotelian-style passage should produce no hits.

    Note: the banned-concept scanner is intentionally over-eager
    (substring whole-word match) — this clean test passage avoids
    every banned-list term, which is itself the diagnostic property.
    """
    clean = (
        "Heavy bodies move toward the earth; light bodies rise. "
        "Motion under a pusher continues only while the pusher acts."
    )
    assert scan_for_banned(clean) == []


def test_prompt_template_render(tmp_path: Path) -> None:
    p = tmp_path / "tmpl.md"
    p.write_text("---\nversion: v1\nstage: test\n---\nHello {{name}}, you are {{role}}.\n")
    tmpl = PromptTemplate(p)
    assert tmpl.version == "v1"
    assert tmpl.stage == "test"
    rendered = tmpl.render(name="Dong", role="reviewer")
    assert rendered.strip() == "Hello Dong, you are reviewer."


def test_prompt_template_unfilled_raises(tmp_path: Path) -> None:
    p = tmp_path / "tmpl.md"
    p.write_text("---\nversion: v1\nstage: test\n---\nHello {{name}}, you are {{role}}.\n")
    tmpl = PromptTemplate(p)
    with pytest.raises(KeyError, match="Unfilled"):
        tmpl.render(name="Dong")


def test_prompt_template_unknown_key_raises(tmp_path: Path) -> None:
    p = tmp_path / "tmpl.md"
    p.write_text("---\nversion: v1\nstage: test\n---\nHello {{name}}.\n")
    tmpl = PromptTemplate(p)
    with pytest.raises(KeyError, match="Unknown"):
        tmpl.render(name="Dong", role="extra")


def test_prompt_template_missing_front_matter_raises(tmp_path: Path) -> None:
    p = tmp_path / "tmpl.md"
    p.write_text("Hello {{name}}.\n")
    with pytest.raises(ValueError, match="No YAML front-matter"):
        PromptTemplate(p)


def test_prompt_template_real_files_load() -> None:
    """Sanity check: every committed prompts/*.md parses cleanly."""
    repo = Path(__file__).resolve().parent.parent
    prompts = repo / "prompts"
    for path in sorted(prompts.glob("*.md")):
        tmpl = PromptTemplate(path)
        assert tmpl.version
        assert tmpl.stage
