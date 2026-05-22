"""03_decay Agent 2 — NON-CANONICAL Stage 3 per-scenario resolver.

03_decay's prereg P3 requires per-scenario classification across
Scenarios 1, 2, 3, 4 (the ratio-binding quantitative ones). The
production judging surfaced two kinds of pending P3 units that need
human audit:

- **Scenario-level disagreements** — Claude and OpenAI judges
  classified the same (trial, scenario) differently
  (PASS vs FAIL, or same verdict with different direction).
- **Fabrication-flagged scenarios** — at least one judge cited
  evidence that mechanical evidence_check (Gap 4) marked as not
  present in the response.

This script runs an LLM resolver (gemini-3.1-pro-preview) over both
populations using the global ``prompts/agent2_scenario_resolver.md``
with the locked 03_decay criteria. The resolver returns
PASS / FAIL plus a ``direction`` classification (correct / wrong /
n/a), matching the three-bucket P3 schema.

**Not part of the prereg envelope** — the human audit is canonical.
Verdicts to ``results/<model>/03_decay/scenario_resolved/``.

Resolver model: ``gemini-3.1-pro-preview``. Run with the sandbox
disabled (Bash sandbox blocks the google-genai endpoint).

Usage: ``uv run python scripts/run_agent2_03_decay.py``
"""

from __future__ import annotations

import glob
import json
import os
import signal
import sys
import time
import uuid
from pathlib import Path
from typing import Any

from physlit.judges import parse_verdict_json
from physlit.prompts import PromptTemplate
from physlit.runners import GeminiRunner

REPO = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "03_decay"
FRAMEWORK_DIR = REPO / "frameworks" / FRAMEWORK_ID
GLOBAL_PROMPTS_DIR = REPO / "prompts"
RESULTS = REPO / "results"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
QUANT_SCENARIOS = (1, 2, 3, 4)
RESOLVER_MAX_TOKENS = 8192
CALL_TIMEOUT_SECONDS = 300


def _load_dotenv() -> None:
    env = REPO / ".env.local"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        s = raw.strip()
        if s and not s.startswith("#") and "=" in s:
            k, _, v = s.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


class _CallTimeout(Exception):
    pass


def _on_alarm(signum: int, frame: object) -> None:
    raise _CallTimeout(f"resolver call exceeded {CALL_TIMEOUT_SECONDS}s")


def _stage3_verdicts(model: str) -> dict[tuple[int, str], dict[str, Any]]:
    """Return {(trial_index, judge_family): full_parsed_verdict} for the
    Stage 3 (prediction) judgments only."""
    out: dict[tuple[int, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / FRAMEWORK_ID / "judgments" / "*.json"))):
        d = json.loads(Path(fp).read_text())
        if d.get("stage") != "prediction":
            continue
        name = Path(d["trial_path"]).name
        if not name.startswith("trial_"):
            continue
        out[(int(name.split("_")[1]), d["judge_family"])] = d.get("parsed_verdict") or {}
    return out


def _scenario_block(parsed: dict[str, Any], idx: int) -> dict[str, Any] | None:
    for sc in parsed.get("scenarios") or []:
        if isinstance(sc, dict) and sc.get("index") == idx:
            return sc
    return None


def _scenario_fab_flag(parsed: dict[str, Any], idx: int) -> bool:
    for ev in parsed.get("_evidence_check") or []:
        if ev.get("scope") == f"scenario_{idx}" and ev.get("fabricated"):
            return True
    return False


def _response(model: str, trial: int, stage: str) -> str:
    p = RESULTS / model / FRAMEWORK_ID / stage / f"trial_{trial}_t0.0.json"
    return json.loads(p.read_text())["response_text"] if p.exists() else "(missing)"


def _scenario_verdict(sc: dict[str, Any] | None) -> str | None:
    if not isinstance(sc, dict):
        return None
    raw = sc.get("verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _scenario_direction(sc: dict[str, Any] | None) -> str | None:
    if not isinstance(sc, dict):
        return None
    raw = sc.get("direction")
    if not isinstance(raw, str):
        return None
    low = raw.strip().lower()
    return low if low in {"correct", "wrong", "n/a"} else None


def main() -> int:
    _load_dotenv()
    tmpl = PromptTemplate(GLOBAL_PROMPTS_DIR / "agent2_scenario_resolver.md")
    prediction_tests_md = (FRAMEWORK_DIR / "prediction_tests.md").read_text()
    pf_md = (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()
    ideal_md = (FRAMEWORK_DIR / "ideal_induction.md").read_text()

    cases: list[tuple[str, int, int, str]] = []  # (model, trial, scenario, reason)
    s3v: dict[str, dict[tuple[int, str], dict[str, Any]]] = {}
    for model in MODELS:
        v = _stage3_verdicts(model)
        s3v[model] = v
        for trial in range(5):
            a = v.get((trial, "anthropic"))
            b = v.get((trial, "openai"))
            if a is None or b is None:
                continue
            for sidx in QUANT_SCENARIOS:
                sca = _scenario_block(a, sidx)
                scb = _scenario_block(b, sidx)
                va, da = _scenario_verdict(sca), _scenario_direction(sca)
                vb, db = _scenario_verdict(scb), _scenario_direction(scb)
                fab_a = _scenario_fab_flag(a, sidx)
                fab_b = _scenario_fab_flag(b, sidx)
                reasons = []
                if va is None or vb is None:
                    reasons.append("missing verdict")
                elif va != vb:
                    reasons.append("verdict disagree")
                elif va == "FAIL" and da != db:
                    reasons.append("direction disagree")
                if fab_a or fab_b:
                    reasons.append(f"fab(a={fab_a},b={fab_b})")
                if reasons:
                    cases.append((model, trial, sidx, ";".join(reasons)))

    print("=== 03_decay Agent 2 — non-canonical Stage 3 per-scenario resolver ===")
    print(f"  resolver: gemini-3.1-pro-preview | scenario cases needing resolution: {len(cases)}")
    print("  NOT canonical — human audit remains the disagree resolution.\n")

    runner = GeminiRunner()
    signal.signal(signal.SIGALRM, _on_alarm)
    total_cost = 0.0

    for model, trial, sidx, reason in cases:
        a = s3v[model][(trial, "anthropic")]
        b = s3v[model][(trial, "openai")]
        sca = _scenario_block(a, sidx) or {}
        scb = _scenario_block(b, sidx) or {}

        def _fmt_evcheck(parsed_v: dict[str, Any], scenario_idx: int) -> str:
            for ev in parsed_v.get("_evidence_check") or []:
                if ev.get("scope") == f"scenario_{scenario_idx}":
                    return (
                        "FABRICATED"
                        if ev.get("fabricated")
                        else "OK"
                        if ev.get("found")
                        else "not-required"
                    )
            return "n/a"

        prompt = tmpl.render(
            prediction_tests_md=prediction_tests_md,
            pass_fail_criteria_md=pf_md,
            ideal_induction_md=ideal_md,
            framework_id=FRAMEWORK_ID,
            tested_model=model,
            trial_index=trial,
            scenario_index=sidx,
            stage2_response=_response(model, trial, "formulation"),
            stage3_response=_response(model, trial, "prediction"),
            judge_a_verdict=_scenario_verdict(sca) or "?",
            judge_a_direction=_scenario_direction(sca) or "?",
            judge_a_evidence=str(sca.get("evidence", ""))[:500],
            judge_a_evidence_check=_fmt_evcheck(a, sidx),
            judge_a_reasoning=str(sca.get("reasoning", "")),
            judge_b_verdict=_scenario_verdict(scb) or "?",
            judge_b_direction=_scenario_direction(scb) or "?",
            judge_b_evidence=str(scb.get("evidence", ""))[:500],
            judge_b_evidence_check=_fmt_evcheck(b, sidx),
            judge_b_reasoning=str(scb.get("reasoning", "")),
        )

        delay = 4.0
        parsed: dict[str, Any] | None = None
        raw = ""
        cost = 0.0
        for attempt in range(1, 7):
            signal.alarm(CALL_TIMEOUT_SECONDS)
            try:
                res = runner.call_model(prompt, 0.0, str(uuid.uuid4()), RESOLVER_MAX_TOKENS)
                signal.alarm(0)
                raw = res.response_text
                cost = runner.estimate_cost(res.input_tokens, res.output_tokens)
                parsed, _ = parse_verdict_json(raw)
                break
            except Exception as exc:
                signal.alarm(0)
                if attempt == 6:
                    print(f"  {model} t{trial} s{sidx}: FAILED — {type(exc).__name__}: {exc}")
                    break
                print(
                    f"    [retry {attempt}/5] {type(exc).__name__}; waiting {delay:.0f}s",
                    flush=True,
                )
                time.sleep(delay)
                delay = min(delay * 2, 60.0)

        total_cost += cost
        v = (parsed or {}).get("verdict", "PARSE_ERROR")
        d = (parsed or {}).get("direction", "-")
        ag = (parsed or {}).get("agreed_with", "-")
        ja_v, jb_v = _scenario_verdict(sca), _scenario_verdict(scb)
        ja_d, jb_d = _scenario_direction(sca), _scenario_direction(scb)
        out_dir = RESULTS / model / FRAMEWORK_ID / "scenario_resolved"
        out_dir.mkdir(parents=True, exist_ok=True)
        rec = {
            "framework_id": FRAMEWORK_ID,
            "round": "03_decay",
            "non_canonical": True,
            "note": "Agent 2 side analysis — NOT the prereg disagree resolution; human audit is canonical.",
            "resolver_model": "gemini-3.1-pro-preview",
            "tested_model": model,
            "trial_index": trial,
            "scenario_index": sidx,
            "case_reason": reason,
            "judge_a_verdict": ja_v,
            "judge_a_direction": ja_d,
            "judge_b_verdict": jb_v,
            "judge_b_direction": jb_d,
            "parsed_verdict": parsed or {},
            "raw_response": raw,
            "cost_usd_estimate": round(cost, 6),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        (out_dir / f"agent2_t{trial}_s{sidx}_{uuid.uuid4().hex[:8]}.json").write_text(
            json.dumps(rec, indent=2, sort_keys=True)
        )
        print(
            f"  {model} t{trial} s{sidx} [{reason}]:"
            f" claude={ja_v}/{ja_d} openai={jb_v}/{jb_d}"
            f" -> Agent2={v}/{d} (with {ag})"
        )

    print(f"\n=== done — {len(cases)} cases, resolver cost ~${total_cost:.4f} ===")
    print("Agent 2 verdicts saved under results/<model>/03_decay/scenario_resolved/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
