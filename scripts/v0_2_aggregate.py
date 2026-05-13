"""v0.2 composite-verdict aggregator.

Run LAST, after `run_agent1.py`, `run_structural_judging.py`, and
`run_agent2.py` have all completed. Reads:

  * v0.1 content-judge verdicts (read-only from
    `results/<model>/judgments/`)
  * Agent 1 verdicts (`results/<model>/01_aristotelian/content_resolved/`)
  * Structural-judge verdicts (`results/<model>/01_aristotelian/structural/`)
  * Agent 2 verdicts (`results/<model>/01_aristotelian/structural_resolved/`)
  * The v0.1 post-audit human-resolved DISAGREE table (from
    `analysis/v0_1_findings.md`, indirectly via `scripts/apply_audit.py`'s
    dict — re-imported here for the V1 cross-check)

And emits:

  * One per-trial composite verdict table
  * V1 verdict (Agent 1 vs human audit agreement on 17 content disagrees)
  * V2 verdict (#{v0.1 content-PASS trials that flip to composite FAIL})
  * Structural-axis IRR
  * `analysis/v0_2_findings.md` (appended block)

No API calls. Deterministic.

Usage:
    uv run python scripts/v0_2_aggregate.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from physlit.judges.aggregate import load_trial_verdicts  # noqa: E402
from physlit.v0_2 import (  # noqa: E402
    load_structural_verdicts,
)

FRAMEWORK_ID = "01_aristotelian"
RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"
FINDINGS_FILE = ANALYSIS_DIR / "v0_2_findings.md"
DEFAULT_MODELS = (
    "claude-opus-4-7",
    "gpt-5.5-2026-04-23",
    "gemini-3.1-pro-preview",
)
N_TRIALS = 5
CONTENT_STAGES: tuple[str, ...] = ("induction", "formulation", "prediction")


# v0.1 post-audit human verdicts on the 17 content disagree cases.
# Mirrors the dict in `scripts/apply_audit.py` so V1 can be computed
# without parsing the auto-generated findings markdown. Keyed by
# (model_id, trial_index, stage) -> "PASS" | "FAIL".
HUMAN_AUDIT_CONTENT_VERDICTS: dict[tuple[str, int, str], str] = {
    ("claude-opus-4-7", 2, "induction"): "FAIL",
    ("claude-opus-4-7", 2, "formulation"): "FAIL",
    ("claude-opus-4-7", 3, "induction"): "FAIL",
    ("claude-opus-4-7", 3, "formulation"): "FAIL",
    ("claude-opus-4-7", 3, "prediction"): "FAIL",
    ("claude-opus-4-7", 4, "formulation"): "FAIL",
    ("gpt-5.5-2026-04-23", 1, "induction"): "FAIL",
    ("gpt-5.5-2026-04-23", 1, "prediction"): "PASS",
    ("gpt-5.5-2026-04-23", 2, "prediction"): "PASS",
    ("gpt-5.5-2026-04-23", 3, "induction"): "FAIL",
    ("gpt-5.5-2026-04-23", 3, "formulation"): "FAIL",
    ("gpt-5.5-2026-04-23", 3, "prediction"): "FAIL",
    ("gemini-3.1-pro-preview", 0, "formulation"): "FAIL",
    ("gemini-3.1-pro-preview", 3, "formulation"): "FAIL",
    ("gemini-3.1-pro-preview", 3, "prediction"): "PASS",
    ("gemini-3.1-pro-preview", 4, "induction"): "FAIL",
    ("gemini-3.1-pro-preview", 4, "formulation"): "FAIL",
}


def _verdict_str(parsed: dict[str, Any]) -> str | None:
    """Normalise verdict. Stage 3 content judgments use ``overall_verdict``;
    everything else uses ``verdict``."""
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    upper = raw.strip().upper()
    if upper not in {"PASS", "FAIL"}:
        return None
    return upper


def _classify_content_axis() -> dict[tuple[str, int, str], str]:
    """For each (model, trial, stage), return PASS/FAIL/MISSING under v0.2.

    Algorithm:
    - If both v0.1 judges agree (PASS, PASS) or (FAIL, FAIL): that's the verdict.
    - If they disagree: load Agent 1's verdict for that case; that's the verdict.
    - If still missing: MISSING.
    """
    judgments_root = RESULTS_ROOT
    by_key = {}
    for model_id in DEFAULT_MODELS:
        verdict_dir = judgments_root / model_id / "judgments"
        if not verdict_dir.is_dir():
            continue
        loaded = load_trial_verdicts(verdict_dir)
        by_key.update(loaded)

    agent1_verdicts: dict[tuple[str, int, str], str] = {}
    for model_id in DEFAULT_MODELS:
        agent1_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / "content_resolved"
        if not agent1_dir.is_dir():
            continue
        for path in sorted(agent1_dir.glob("*.json")):
            data = json.loads(path.read_text())
            stage_label = data.get("stage", "")
            if not stage_label.startswith("agent1_content_"):
                continue
            content_stage = stage_label[len("agent1_content_") :]
            trial_path = Path(data["trial_path"])
            trial_filename = trial_path.name
            if not trial_filename.startswith("trial_"):
                continue
            trial_index = int(trial_filename.split("_")[1])
            parsed = data.get("parsed_verdict", {}) or {}
            v = _verdict_str(parsed)
            if v is None:
                continue
            agent1_verdicts[(model_id, trial_index, content_stage)] = v

    out: dict[tuple[str, int, str], str] = {}
    for model_id in DEFAULT_MODELS:
        for trial_index in range(N_TRIALS):
            for stage in CONTENT_STAGES:
                key_a = (model_id, trial_index, stage, "anthropic")
                key_b = (model_id, trial_index, stage, "openai")
                parsed_a = by_key.get(key_a, {})
                parsed_b = by_key.get(key_b, {})
                v_a = _verdict_str(parsed_a)
                v_b = _verdict_str(parsed_b)
                if v_a is None or v_b is None:
                    out[(model_id, trial_index, stage)] = "MISSING"
                    continue
                if v_a == v_b:
                    out[(model_id, trial_index, stage)] = v_a
                    continue
                # Disagree → Agent 1
                agent_v = agent1_verdicts.get((model_id, trial_index, stage))
                if agent_v is None:
                    out[(model_id, trial_index, stage)] = "DISAGREE"
                else:
                    out[(model_id, trial_index, stage)] = agent_v
    return out


def _classify_structural_axis() -> tuple[
    dict[tuple[str, int], str],
    int,
    int,
    int,
]:
    """For each (model, trial), return PASS/FAIL/MISSING under v0.2.

    Returns (verdicts, total, disagree_count, missing_count) — the latter
    three feed into the structural-axis IRR.
    """
    bundles = load_structural_verdicts(
        results_root=RESULTS_ROOT,
        model_ids=DEFAULT_MODELS,
        n_trials=N_TRIALS,
    )

    agent2_verdicts: dict[tuple[str, int], str] = {}
    for model_id in DEFAULT_MODELS:
        agent2_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / "structural_resolved"
        if not agent2_dir.is_dir():
            continue
        for path in sorted(agent2_dir.glob("*.json")):
            data = json.loads(path.read_text())
            if data.get("stage") != "agent2_structural":
                continue
            trial_path = Path(data["trial_path"])
            trial_filename = trial_path.name
            if not trial_filename.startswith("trial_"):
                continue
            trial_index = int(trial_filename.split("_")[1])
            # Find model from trial_path: .../<model>/01_aristotelian/...
            try:
                model_id_from_path = trial_path.parts[trial_path.parts.index(FRAMEWORK_ID) - 1]
            except ValueError:
                continue
            parsed = data.get("parsed_verdict", {}) or {}
            v = _verdict_str(parsed)
            if v is None:
                continue
            agent2_verdicts[(model_id_from_path, trial_index)] = v

    out: dict[tuple[str, int], str] = {}
    total = 0
    disagree_count = 0
    missing_count = 0
    for (model_id, trial_index), bundle in bundles.items():
        joint = bundle.joint_verdict
        if joint == "MISSING":
            out[(model_id, trial_index)] = "MISSING"
            missing_count += 1
            continue
        total += 1
        if joint in {"PASS", "FAIL"}:
            out[(model_id, trial_index)] = joint
            continue
        # DISAGREE → Agent 2
        disagree_count += 1
        agent_v = agent2_verdicts.get((model_id, trial_index))
        if agent_v is None:
            out[(model_id, trial_index)] = "DISAGREE"
        else:
            out[(model_id, trial_index)] = agent_v
    return out, total, disagree_count, missing_count


def _composite_verdict(
    content: dict[tuple[str, int, str], str], structural: dict[tuple[str, int], str]
) -> dict[tuple[str, int], str]:
    """Combine the two axes by AND. Any axis FAIL → composite FAIL."""
    out: dict[tuple[str, int], str] = {}
    for model_id in DEFAULT_MODELS:
        for trial_index in range(N_TRIALS):
            content_verdicts = [content.get((model_id, trial_index, s)) for s in CONTENT_STAGES]
            struct_v = structural.get((model_id, trial_index))

            if "MISSING" in content_verdicts or struct_v in (None, "MISSING"):
                out[(model_id, trial_index)] = "MISSING"
                continue
            if "DISAGREE" in content_verdicts or struct_v == "DISAGREE":
                out[(model_id, trial_index)] = "INCOMPLETE"
                continue
            any_content_fail = any(v == "FAIL" for v in content_verdicts)
            struct_fail = struct_v == "FAIL"
            out[(model_id, trial_index)] = "FAIL" if (any_content_fail or struct_fail) else "PASS"
    return out


def _agent1_human_agreement() -> tuple[int, int, list[tuple[tuple[str, int, str], str, str]]]:
    """Compute Agent 1 verdicts on the 17 v0.1 content disagree cases and
    compare each to the human-audit verdict from
    ``HUMAN_AUDIT_CONTENT_VERDICTS``.

    Returns (agree_count, total, disagree_rows). disagree_rows lists
    (key, agent_v, human_v) for cases where they differ.
    """
    expected = set(HUMAN_AUDIT_CONTENT_VERDICTS.keys())
    agreements = 0
    total = 0
    diffs: list[tuple[tuple[str, int, str], str, str]] = []

    for model_id in DEFAULT_MODELS:
        agent1_dir = RESULTS_ROOT / model_id / FRAMEWORK_ID / "content_resolved"
        if not agent1_dir.is_dir():
            continue
        for path in sorted(agent1_dir.glob("*.json")):
            data = json.loads(path.read_text())
            stage_label = data.get("stage", "")
            if not stage_label.startswith("agent1_content_"):
                continue
            content_stage = stage_label[len("agent1_content_") :]
            trial_path = Path(data["trial_path"])
            trial_filename = trial_path.name
            if not trial_filename.startswith("trial_"):
                continue
            trial_index = int(trial_filename.split("_")[1])
            key = (model_id, trial_index, content_stage)
            if key not in expected:
                continue
            parsed = data.get("parsed_verdict", {}) or {}
            agent_v = _verdict_str(parsed)
            human_v = HUMAN_AUDIT_CONTENT_VERDICTS[key]
            if agent_v is None:
                continue
            total += 1
            if agent_v == human_v:
                agreements += 1
            else:
                diffs.append((key, agent_v, human_v))
    return agreements, total, diffs


def _emit_findings(
    *,
    content_verdicts: dict[tuple[str, int, str], str],
    structural_verdicts: dict[tuple[str, int], str],
    composite: dict[tuple[str, int], str],
    v1_agree: int,
    v1_total: int,
    v1_diffs: list[tuple[tuple[str, int, str], str, str]],
    struct_total: int,
    struct_disagree: int,
) -> str:
    lines: list[str] = []
    lines.append("## v0.2 final report")
    lines.append(f"- Generated: `{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}`")
    lines.append("- Prereg lock: `prereg-v0.2-locked`")
    lines.append("")

    # V1
    rate = v1_agree / v1_total if v1_total else 0.0
    if v1_agree >= 12:
        v1_verdict = "CONFIRMED"
    elif v1_agree >= 9:
        v1_verdict = "PARTIALLY CONFIRMED"
    else:
        v1_verdict = "REFUTED"
    lines.append("### V1 — Agent 1 calibration against human audit")
    lines.append(f"**Verdict: {v1_verdict}**")
    lines.append("")
    lines.append(
        f"Agent 1 agreed with the v0.1 human audit on **{v1_agree} of "
        f"{v1_total} content disagree cases ({rate * 100:.1f} %)**. "
        f"Threshold for CONFIRMED was ≥ 12 of 17 per the prereg."
    )
    lines.append("")
    if v1_diffs:
        lines.append("#### Cases where Agent 1 differed from human audit")
        lines.append("")
        lines.append("| Model | Trial | Stage | Agent 1 | Human audit |")
        lines.append("|---|---|---|---|---|")
        for key, agent_v, human_v in v1_diffs:
            m, t, s = key
            lines.append(f"| `{m}` | {t} | {s} | {agent_v} | {human_v} |")
        lines.append("")

    # V2
    v0_1_pass_trials = (
        ("claude-opus-4-7", 1),
        ("gpt-5.5-2026-04-23", 0),
        ("gpt-5.5-2026-04-23", 2),
        ("gpt-5.5-2026-04-23", 4),
        ("gemini-3.1-pro-preview", 2),
    )
    flipped = []
    for model_id, trial_index in v0_1_pass_trials:
        composite_v = composite.get((model_id, trial_index), "MISSING")
        struct_v = structural_verdicts.get((model_id, trial_index), "MISSING")
        if composite_v == "FAIL" and struct_v == "FAIL":
            flipped.append((model_id, trial_index))
    if len(flipped) >= 2:
        v2_verdict = "CONFIRMED"
    elif len(flipped) == 1:
        v2_verdict = "PARTIALLY CONFIRMED"
    else:
        v2_verdict = "REFUTED"
    lines.append("### V2 — Structural axis adds detection over content-only")
    lines.append(f"**Verdict: {v2_verdict}**")
    lines.append("")
    lines.append(
        f"Of the 5 v0.1 all-content-PASS trials "
        f"(Claude trial 1, GPT trials 0/2/4, Gemini trial 2), "
        f"**{len(flipped)} flipped to composite FAIL** via the structural axis. "
        f"Threshold for CONFIRMED was ≥ 2 per the prereg."
    )
    lines.append("")
    if flipped:
        lines.append("#### Flipped trials")
        lines.append("")
        for model_id, trial_index in flipped:
            lines.append(f"- `{model_id}` trial {trial_index}")
        lines.append("")

    # Structural IRR
    struct_irr_rate = (struct_disagree / struct_total) if struct_total else 0.0
    lines.append("### Structural-axis IRR")
    lines.append(
        f"Structural judges disagreed on **{struct_disagree} of "
        f"{struct_total} trials ({struct_irr_rate * 100:.2f} %)**. "
        f"Compare to v0.1 content-axis IRR of 36.67 %."
    )
    lines.append("")

    # Composite per-trial table
    lines.append("### Composite per-trial verdicts (content AND structural)")
    lines.append("")
    lines.append("| Model | Trial | S1 | S2 | S3 | Structural | Composite |")
    lines.append("|---|---|---|---|---|---|---|")
    for model_id in DEFAULT_MODELS:
        for trial_index in range(N_TRIALS):
            s1 = content_verdicts.get((model_id, trial_index, "induction"), "?")
            s2 = content_verdicts.get((model_id, trial_index, "formulation"), "?")
            s3 = content_verdicts.get((model_id, trial_index, "prediction"), "?")
            sv = structural_verdicts.get((model_id, trial_index), "?")
            comp = composite.get((model_id, trial_index), "?")
            lines.append(f"| `{model_id}` | {trial_index} | {s1} | {s2} | {s3} | {sv} | {comp} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    content_verdicts = _classify_content_axis()
    structural_verdicts, struct_total, struct_disagree, _ = _classify_structural_axis()
    composite = _composite_verdict(content_verdicts, structural_verdicts)
    v1_agree, v1_total, v1_diffs = _agent1_human_agreement()

    block = _emit_findings(
        content_verdicts=content_verdicts,
        structural_verdicts=structural_verdicts,
        composite=composite,
        v1_agree=v1_agree,
        v1_total=v1_total,
        v1_diffs=v1_diffs,
        struct_total=struct_total,
        struct_disagree=struct_disagree,
    )

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    if FINDINGS_FILE.exists():
        existing = FINDINGS_FILE.read_text()
        FINDINGS_FILE.write_text(existing.rstrip() + "\n\n" + block)
    else:
        FINDINGS_FILE.write_text(
            "# PhysLit v0.2 — Findings\n\n"
            "This file accumulates v0.2 evaluation findings: structural-axis\n"
            "judging, Agent 1 / Agent 2 resolver outputs, and the composite\n"
            "verdict over v0.1 trials.\n\n" + block
        )

    print(f"Appended v0.2 findings block to {FINDINGS_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
