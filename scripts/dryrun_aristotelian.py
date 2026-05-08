"""Phase 1.5 — Aristotelian dry run.

Single-trial, single-model (Claude Opus 4.7 only), single-temperature
(0.0) end-to-end smoke test of the four-stage protocol on the
Aristotelian phenomenon set.

Output goes to ``results/_dryrun/<UTC-timestamp>/01_aristotelian/<stage>/``.
This is exploratory data and is **not** counted as v0.1 evaluation
results — the underscore prefix on ``_dryrun/`` is the marker.

Findings should be hand-recorded to ``analysis/dryrun_findings.md``
after running.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

from physlit.prompts import PromptTemplate
from physlit.runners.claude import ClaudeRunner

REPO_ROOT = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "01_aristotelian"
FRAMEWORK_DIR = REPO_ROOT / "frameworks" / FRAMEWORK_ID
PROMPTS_DIR = REPO_ROOT / "prompts"
RESULTS_DRYRUN_ROOT = REPO_ROOT / "results" / "_dryrun"

# Stage 3 scenario prompts. Hand-extracted from prediction_tests.md;
# only the model-facing portion (no PASS/FAIL columns or commentary).
# TODO post-dry-run: parse this directly from prediction_tests.md so
# the two files cannot drift.
STAGE3_SCENARIOS = """\
Scenario 1. A solid iron ball and a hollow wooden ball of the same outer dimensions are released from rest at the same instant from the top of a 30-metre stone tower into still air. Which ball strikes the ground first, and roughly by how much?

Scenario 2. A small cart sits on a sheet of perfectly smooth ice, far from any wall. A person gives the cart one quick push and immediately steps back, no longer touching the cart. Describe the cart's subsequent motion.

Scenario 3. Two stones, identical in shape and size, are released at the same instant from just below the surface of a still pond. Stone A weighs twice what stone B weighs. Which reaches the bottom first, and roughly in what ratio of times?

Scenario 4. A glass chamber is sealed and all air has been removed from it so that nothing remains inside. A small feather is released from rest near the top of the chamber. What happens?

Scenario 5. An archer fires an arrow horizontally over an open field with still air. Once the arrow has left the bowstring, what sustains its forward motion through the air, and why does it eventually fall to the ground?\
"""


def _load_dotenv() -> None:
    """Minimal ``.env.local`` loader; avoids a python-dotenv dep."""
    env_path = REPO_ROOT / ".env.local"
    if not env_path.exists():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def _extract_observations_list(observations_md: str) -> str:
    """Extract just the numbered observation list from observations.md.

    The file also contains Status, Authoring constraints, and Author note
    sections. The Author note in particular *describes which observations
    are boundary tests*, which would leak the framework's intent to the
    tested model. So we hand the model only the ``## Observations``
    section.
    """
    pattern = re.compile(
        r"^## Observations\s*\n(.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(observations_md)
    if match is None:
        raise ValueError("observations.md does not contain a '## Observations' section")
    return match.group(1).strip()


def main() -> int:
    _load_dotenv()
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 1

    observations_md = (FRAMEWORK_DIR / "observations.md").read_text()
    observations_list = _extract_observations_list(observations_md)

    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    output_root = RESULTS_DRYRUN_ROOT / timestamp
    output_root.mkdir(parents=True, exist_ok=True)

    runner = ClaudeRunner()
    print("PhysLit Phase 1.5 — Aristotelian dry run")
    print(f"Model:   {runner.model_id}")
    print(f"Output:  {output_root}/{FRAMEWORK_ID}/")
    print()

    # Stage 1 — Induction
    print("[Stage 1 — induction] Calling Claude...")
    s1_tmpl = PromptTemplate(PROMPTS_DIR / "stage1_induction.md")
    s1_prompt = s1_tmpl.render(observations=observations_list)
    s1_record = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="induction",
        prompt_text=s1_prompt,
        prompt_version=s1_tmpl.version,
        trial_index=0,
        temperature=0.0,
        max_tokens=2048,
    )
    runner.save_trial(s1_record, output_root)
    print(f"  → {len(s1_record.response_text)} chars, ~${s1_record.cost_usd_estimate:.4f}")

    # Stage 2 — Formulation
    print("[Stage 2 — formulation] Calling Claude...")
    s2_tmpl = PromptTemplate(PROMPTS_DIR / "stage2_formulation.md")
    s2_prompt = s2_tmpl.render(induced_rules=s1_record.response_text)
    s2_record = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="formulation",
        prompt_text=s2_prompt,
        prompt_version=s2_tmpl.version,
        trial_index=0,
        temperature=0.0,
        max_tokens=2048,
    )
    runner.save_trial(s2_record, output_root)
    print(f"  → {len(s2_record.response_text)} chars, ~${s2_record.cost_usd_estimate:.4f}")

    # Stage 3 — Prediction
    print("[Stage 3 — prediction] Calling Claude...")
    s3_tmpl = PromptTemplate(PROMPTS_DIR / "stage3_prediction.md")
    s3_prompt = s3_tmpl.render(
        operational_rules=s2_record.response_text,
        scenarios=STAGE3_SCENARIOS,
    )
    s3_record = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="prediction",
        prompt_text=s3_prompt,
        prompt_version=s3_tmpl.version,
        trial_index=0,
        temperature=0.0,
        max_tokens=2560,
    )
    runner.save_trial(s3_record, output_root)
    print(f"  → {len(s3_record.response_text)} chars, ~${s3_record.cost_usd_estimate:.4f}")

    # Stage 4 — Meta
    print("[Stage 4 — meta] Calling Claude...")
    s4_tmpl = PromptTemplate(PROMPTS_DIR / "stage4_meta.md")
    s4_prompt = s4_tmpl.render(
        stage1_response=s1_record.response_text,
        stage2_response=s2_record.response_text,
        stage3_response=s3_record.response_text,
    )
    s4_record = runner.run_trial(
        framework_id=FRAMEWORK_ID,
        stage="meta",
        prompt_text=s4_prompt,
        prompt_version=s4_tmpl.version,
        trial_index=0,
        temperature=0.0,
        max_tokens=2048,
    )
    runner.save_trial(s4_record, output_root)
    print(f"  → {len(s4_record.response_text)} chars, ~${s4_record.cost_usd_estimate:.4f}")

    total = sum(r.cost_usd_estimate for r in (s1_record, s2_record, s3_record, s4_record))
    print()
    print(f"Total estimated cost: ~${total:.4f}")
    print(f"Trials saved under:   {output_root}/{FRAMEWORK_ID}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
