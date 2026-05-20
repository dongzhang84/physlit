"""v0.3 Agent 1 — NON-CANONICAL content-axis disagree resolver.

Resolves content disagreements in the v0.3 treatment arm using the
global v0.1/v0.2 agent prompt (``prompts/agent1_content_resolver.md``)
with its fielded placeholders. Mirrors ``scripts/run_agent1_02_fmv_2.py``
but adapted to v0.1's prompt shape.

**Not part of the prereg envelope** — the human audit is canonical.
Verdicts to ``results/<model>/v0_3/content_resolved/``.

Resolver model: ``gemini-3.1-pro-preview``. Run with the sandbox
disabled (Bash sandbox blocks the google-genai endpoint).

Usage: ``uv run python scripts/run_agent1_v0_3.py``
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
TREATMENT_ID = "v0_3"
SOURCE_FRAMEWORK_DIR = REPO / "frameworks" / "01_aristotelian"
GLOBAL_PROMPTS_DIR = REPO / "prompts"
RESULTS = REPO / "results"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
CONTENT_STAGES = ("induction", "formulation", "prediction")
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
    for fp in sorted(glob.glob(str(RESULTS / model / TREATMENT_ID / "judgments" / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if not name.startswith("trial_"):
            continue
        out[(int(name.split("_")[1]), d["stage"], d["judge_family"])] = (
            d.get("parsed_verdict") or {}
        )
    return out


def _response(model: str, trial: int, stage: str) -> str:
    p = RESULTS / model / TREATMENT_ID / stage / f"trial_{trial}_t0.0.json"
    return json.loads(p.read_text())["response_text"] if p.exists() else "(missing)"


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict") or parsed.get("overall_verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def main() -> int:
    _load_dotenv()
    tmpl = PromptTemplate(GLOBAL_PROMPTS_DIR / "agent1_content_resolver.md")
    ideal_md = (SOURCE_FRAMEWORK_DIR / "ideal_induction.md").read_text()
    pf_md = (SOURCE_FRAMEWORK_DIR / "pass_fail_criteria.md").read_text()

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

    print("=== v0.3 Agent 1 — non-canonical content-axis resolver ===")
    print(f"  resolver: gemini-3.1-pro-preview | content disagree cases: {len(cases)}")
    print("  NOT canonical — human audit remains the disagree resolution.\n")

    runner = GeminiRunner()
    signal.signal(signal.SIGALRM, _on_alarm)
    total_cost = 0.0

    for model, trial, stage in cases:
        a = judgments[model][(trial, stage, "anthropic")]
        b = judgments[model][(trial, stage, "openai")]
        prompt = tmpl.render(
            framework_id="01_aristotelian",
            ideal_induction_md=ideal_md,
            pass_fail_criteria_md=pf_md,
            tested_model=model,
            trial_index=trial,
            stage=stage,
            tested_response=_response(model, trial, stage),
            judge_a_verdict=_verdict(a) or "?",
            judge_a_reasoning=str(a.get("reasoning", "")),
            judge_b_verdict=_verdict(b) or "?",
            judge_b_reasoning=str(b.get("reasoning", "")),
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
        out_dir = RESULTS / model / TREATMENT_ID / "content_resolved"
        out_dir.mkdir(parents=True, exist_ok=True)
        rec = {
            "framework_id": TREATMENT_ID,
            "round": "v0.3",
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

    print(f"\n=== done — {len(cases)} cases, resolver cost ~${total_cost:.4f} ===")
    print("Agent 1 verdicts saved under results/<model>/v0_3/content_resolved/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
