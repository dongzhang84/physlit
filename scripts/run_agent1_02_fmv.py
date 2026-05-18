"""02_fmv Agent 1 — NON-CANONICAL content-axis disagree resolver.

Runs an LLM resolver over the 12 content-axis dual-judge disagreement
cases (Stage 1 / 2 / 3). For each case the resolver reads the tested
response, both judges' verdicts + reasoning, and the frozen 02_fmv
criteria, and returns PASS / FAIL.

**This is NOT part of the prereg-02_fmv-locked envelope.** The §1
"Out of scope" clause commits 02_fmv to human-audit-only resolution of
disagreements. Agent 1 here is a side analysis only: a V1-style
calibration probe — afterwards, Agent 1's verdicts are compared
against the human audit. Agent 1 verdicts do **not** feed P1 / P2 / P4;
the human audit does. Output is written to a separate directory and
clearly labelled.

Resolver model: ``gemini-3.1-pro-preview`` — cross-vendor against the
two content judges (Claude + GPT). It runs from this script via the
google-genai SDK; the Bash sandbox blocks that endpoint, so run with
the sandbox disabled.

The 2 meta over-claim disagreements are not covered — Agent 1 is a
content-axis resolver.

Usage:
    uv run python scripts/run_agent1_02_fmv.py
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
FRAMEWORK_ID = "02_fmv"
FRAMEWORK_DIR = REPO / "frameworks" / FRAMEWORK_ID
RESULTS = REPO / "results"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
PRIOR_STAGE = {"formulation": "induction", "prediction": "formulation"}
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


def _judgments(model: str) -> dict[tuple[int, str, str], dict[str, Any]]:
    out: dict[tuple[int, str, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(RESULTS / model / FRAMEWORK_ID / "judgments" / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if not name.startswith("trial_"):
            continue
        out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
            d.get("parsed_verdict") or {}
        )
    return out


def _response(model: str, trial: int, stage: str) -> str:
    p = RESULTS / model / FRAMEWORK_ID / stage / f"trial_{trial}_t0.0.json"
    return json.loads(p.read_text())["response_text"] if p.exists() else "(missing)"


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _judge_block(parsed: dict[str, Any], stage: str) -> str:
    """Render one judge's verdict as text for the resolver prompt."""
    if stage == "prediction":
        lines = [f"overall_verdict: {_verdict(parsed)}"]
        for sc in parsed.get("scenarios") or []:
            if not isinstance(sc, dict):
                continue
            lines.append(
                f"  Scenario {sc.get('index', '?')}: {sc.get('verdict', '?')} "
                f"(direction: {sc.get('direction', '?')}) "
                f"fails: {sc.get('failed_criterion') or '-'} | {(sc.get('reasoning') or '').strip()}"
            )
        return "\n".join(lines)
    clause = parsed.get("first_fail_clause") or parsed.get("failed_criterion") or "(n/a)"
    return (
        f"verdict: {_verdict(parsed)}\n"
        f"failed clause / criterion: {clause}\n"
        f"evidence: {(parsed.get('evidence') or '(none)').strip()}\n"
        f"reasoning: {(parsed.get('reasoning') or '').strip()}"
    )


def main() -> int:
    _load_dotenv()
    tmpl = PromptTemplate(FRAMEWORK_DIR / "prompts" / "agent1_content_resolver.md")
    crit = {
        "ideal_induction_md": (FRAMEWORK_DIR / "ideal_induction.md").read_text(),
        "pass_fail_criteria_md": (FRAMEWORK_DIR / "pass_fail_criteria.md").read_text(),
        "prediction_tests_md": (FRAMEWORK_DIR / "prediction_tests.md").read_text(),
    }

    # Collect the 12 content-axis disagree cases.
    cases: list[tuple[str, int, str]] = []
    judgments: dict[str, dict[tuple[int, str, str], dict[str, Any]]] = {}
    for model in MODELS:
        j = _judgments(model)
        judgments[model] = j
        for trial in range(5):
            for stage in CONTENT_STAGES:
                a = j.get((trial, stage, "anthropic"))
                b = j.get((trial, stage, "openai"))
                if a is None or b is None:
                    continue
                va, vb = _verdict(a), _verdict(b)
                if va and vb and va != vb:
                    cases.append((model, trial, stage))

    print("=== 02_fmv Agent 1 — non-canonical content-axis resolver ===")
    print(f"  resolver: gemini-3.1-pro-preview | content disagree cases: {len(cases)}")
    print("  NOT canonical — human audit remains the disagree resolution.\n")

    runner = GeminiRunner()
    signal.signal(signal.SIGALRM, _on_alarm)
    total_cost = 0.0
    summary: list[tuple[str, int, str, str, str, str]] = []

    for model, trial, stage in cases:
        a = judgments[model][(trial, stage, "anthropic")]
        b = judgments[model][(trial, stage, "openai")]
        prior = PRIOR_STAGE.get(stage)
        prompt = tmpl.render(
            **crit,
            tested_model=model,
            trial_index=trial,
            stage=stage,
            prior_context=(
                _response(model, trial, prior)
                if prior
                else "(not applicable — Stage 1 is the first stage)"
            ),
            tested_response=_response(model, trial, stage),
            judge_a_block=_judge_block(a, stage),
            judge_b_block=_judge_block(b, stage),
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
                    print(f"  {model} t{trial} {stage}: FAILED — {type(exc).__name__}: {exc}")
                    break
                print(
                    f"    [retry {attempt}/5] {type(exc).__name__}; waiting {delay:.0f}s",
                    flush=True,
                )
                time.sleep(delay)
                delay = min(delay * 2, 60.0)

        total_cost += cost
        verdict = (parsed or {}).get("verdict", "PARSE_ERROR")
        agreed = (parsed or {}).get("agreed_with", "-")
        ja, jb = _verdict(a), _verdict(b)
        out_dir = RESULTS / model / FRAMEWORK_ID / "content_resolved"
        out_dir.mkdir(parents=True, exist_ok=True)
        rec = {
            "framework_id": FRAMEWORK_ID,
            "non_canonical": True,
            "note": "Agent 1 side analysis — NOT the prereg disagree resolution; human audit is canonical.",
            "resolver_model": "gemini-3.1-pro-preview",
            "tested_model": model,
            "trial_index": trial,
            "stage": stage,
            "judge_a_verdict": ja,
            "judge_b_verdict": jb,
            "parsed_verdict": parsed or {},
            "raw_response": raw,
            "cost_usd_estimate": round(cost, 6),
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        (out_dir / f"agent1_{stage}_t{trial}_{uuid.uuid4().hex[:8]}.json").write_text(
            json.dumps(rec, indent=2, sort_keys=True)
        )
        print(
            f"  {model} t{trial} {stage}: claude={ja} openai={jb} -> Agent1={verdict} (with {agreed})"
        )
        summary.append((model, trial, stage, str(ja), str(jb), str(verdict)))

    print(f"\n=== done — {len(cases)} cases, resolver cost ~${total_cost:.4f} ===")
    print("Agent 1 verdicts saved under results/<model>/02_fmv/content_resolved/.")
    print("Compare against the human audit once analysis/02_fmv_audit_worksheet.md is filled in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
