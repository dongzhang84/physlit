"""02_fmv.1 structural-axis judging — dual structural judges + P1/P2.

The structural-axis layer over the frozen 02_fmv content trials, per
`predictions/02_fmv_1_prereg.md`. For each of the 15 trials it
dispatches two structural judges (Claude + GPT) over the trial's Stage
1 (induction) + Stage 2 (formulation) responses — the verdict is on
the Stage 1 rule set; Stage 2 is context, never counted (the v0.2
double-count fix). Verdicts are saved to
`results/<model>/02_fmv/structural/`.

Then it aggregates:

- structural-axis IRR (dual-judge disagreement over 15 trials) -> P1
- composite verdict (content AND structural) per trial; how many of
  the 9 all-content-PASS trials flip to composite FAIL -> P2

DISAGREE cases are flagged for human audit, not auto-resolved; P1's
IRR is audit-invariant, P2 is a lower bound while a disagreement on a
content-PASS trial is unresolved. Report appended to
`analysis/fmv/02_fmv_1_findings.md`.

The structural judges are Claude + OpenAI — both reachable from the
sandboxed environment; no sandbox override needed. No existing code is
modified.

Usage: uv run python scripts/judge_structural_02_fmv.py [--n-trials N]
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any

from physlit.judges import ClaudeJudge, JudgeBase, JudgeVerdict, OpenAIJudge
from physlit.prompts import PromptTemplate

REPO = Path(__file__).resolve().parent.parent
FRAMEWORK_ID = "02_fmv"
FRAMEWORK_DIR = REPO / "frameworks" / FRAMEWORK_ID
RESULTS = REPO / "results"
FINDINGS = REPO / "analysis" / "fmv" / "02_fmv_1_findings.md"
MODELS = ("claude-opus-4-7", "gpt-5.5-2026-04-23", "gemini-3.1-pro-preview")
JUDGE_MAX_TOKENS = 8192
CALL_TIMEOUT_SECONDS = 300

# Frozen — 02_fmv post-audit content-axis verdicts. A trial's content
# axis is PASS iff its Stage 1, 2, and 3 are all PASS. Source: the
# post-audit matrix in analysis/fmv/02_fmv_findings.md (9 PASS, 6 FAIL).
CONTENT_ALL_PASS: frozenset[tuple[str, int]] = frozenset(
    {
        ("claude-opus-4-7", 0),
        ("claude-opus-4-7", 2),
        ("claude-opus-4-7", 3),
        ("claude-opus-4-7", 4),
        ("gpt-5.5-2026-04-23", 0),
        ("gpt-5.5-2026-04-23", 1),
        ("gpt-5.5-2026-04-23", 2),
        ("gpt-5.5-2026-04-23", 3),
        ("gpt-5.5-2026-04-23", 4),
    }
)


def _load_dotenv() -> None:
    env = REPO / ".env.local"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        s = raw.strip()
        if s and not s.startswith("#") and "=" in s:
            k, _, v = s.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


# --- Transient-error retry + per-call timeout (same contract as run_02_fmv) ---
_TRANSIENT_MARKERS = (
    "overload",
    "rate limit",
    "rate_limit",
    "unavailable",
    "timeout",
    "503",
    "529",
)


class _CallTimeout(Exception):
    pass


def _on_alarm(signum: int, frame: object) -> None:
    raise _CallTimeout(f"judge call exceeded {CALL_TIMEOUT_SECONDS}s")


def _is_transient(exc: Exception) -> bool:
    if isinstance(exc, _CallTimeout):
        return True
    status = getattr(exc, "status_code", None)
    if status in (408, 409, 429, 500, 502, 503, 504, 529):
        return True
    text = f"{type(exc).__name__} {exc}".lower()
    return any(m in text for m in _TRANSIENT_MARKERS)


def _judge_with_retry(judge: JudgeBase, *, trial_path: Path, prompt: str) -> JudgeVerdict:
    delay = 4.0
    signal.signal(signal.SIGALRM, _on_alarm)
    for attempt in range(1, 7):
        signal.alarm(CALL_TIMEOUT_SECONDS)
        try:
            result = judge.judge_one(
                trial_path=trial_path,
                stage="structural",
                prompt=prompt,
                max_tokens=JUDGE_MAX_TOKENS,
            )
        except Exception as exc:
            signal.alarm(0)
            if not _is_transient(exc) or attempt == 6:
                raise
            print(
                f"      [retry {attempt}/5] {type(exc).__name__}; waiting {delay:.0f}s", flush=True
            )
            time.sleep(delay)
            delay = min(delay * 2, 60.0)
        else:
            signal.alarm(0)
            return result
    raise AssertionError("unreachable")  # pragma: no cover


def _response(model: str, trial: int, stage: str) -> str:
    p = RESULTS / model / FRAMEWORK_ID / stage / f"trial_{trial}_t0.0.json"
    return json.loads(p.read_text())["response_text"] if p.exists() else "(missing)"


def _verdict(parsed: dict[str, Any]) -> str | None:
    raw = parsed.get("verdict")
    if not isinstance(raw, str):
        return None
    up = raw.strip().upper()
    return up if up in {"PASS", "FAIL"} else None


def _structural_dir(model: str) -> Path:
    return RESULTS / model / FRAMEWORK_ID / "structural"


# === Dispatch ===========================================================
def dispatch(n_trials: int, judges: list[tuple[str, JudgeBase]]) -> float:
    tmpl = PromptTemplate(FRAMEWORK_DIR / "prompts" / "judge_structural.md")
    criteria = (FRAMEWORK_DIR / "structural_criteria.md").read_text()
    observations = (FRAMEWORK_DIR / "observations.md").read_text()
    total_cost = 0.0

    for model in MODELS:
        out_dir = _structural_dir(model)
        out_dir.mkdir(parents=True, exist_ok=True)
        for t in range(n_trials):
            s1_path = RESULTS / model / FRAMEWORK_ID / "induction" / f"trial_{t}_t0.0.json"
            s2_path = RESULTS / model / FRAMEWORK_ID / "formulation" / f"trial_{t}_t0.0.json"
            if not s1_path.exists() or not s2_path.exists():
                print(f"  [skip] {model} trial {t}: missing Stage 1/2 JSON")
                continue
            prompt = tmpl.render(
                structural_criteria_md=criteria,
                observations_md=observations,
                stage1_response=_response(model, t, "induction"),
                stage2_response=_response(model, t, "formulation"),
            )
            verdicts: dict[str, str | None] = {}
            for jfam, judge in judges:
                v = _judge_with_retry(judge, trial_path=s1_path, prompt=prompt)
                judge.save_verdict(v, out_dir)
                total_cost += v.cost_usd_estimate
                verdicts[jfam] = _verdict(v.parsed_verdict) if v.parse_error is None else None
            print(
                f"  {model} trial {t}: claude={verdicts.get('anthropic')} "
                f"openai={verdicts.get('openai')}"
            )
    return total_cost


# === Aggregation ========================================================
def _load_structural(model: str) -> dict[tuple[int, str], dict[str, Any]]:
    """{(trial_index, judge_family): parsed_verdict}."""
    out: dict[tuple[int, str], dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(_structural_dir(model) / "*.json"))):
        d = json.loads(Path(fp).read_text())
        name = Path(d["trial_path"]).name
        if name.startswith("trial_"):
            out[(int(name.split("_")[1]), d["judge_family"])] = d.get("parsed_verdict") or {}
    return out


def aggregate(n_trials: int, judge_cost: float) -> None:
    rows: list[dict[str, Any]] = []
    disagree = total = 0
    for model in MODELS:
        sv = _load_structural(model)
        for t in range(n_trials):
            a = _verdict(sv.get((t, "anthropic")) or {})
            b = _verdict(sv.get((t, "openai")) or {})
            if a is None or b is None:
                struct = "MISSING"
            else:
                total += 1
                struct = a if a == b else "DISAGREE"
                if struct == "DISAGREE":
                    disagree += 1
            content = "PASS" if (model, t) in CONTENT_ALL_PASS else "FAIL"
            if content == "FAIL":
                composite = "FAIL"
            elif struct == "PASS":
                composite = "PASS"
            elif struct == "FAIL":
                composite = "FAIL"
            else:
                composite = struct  # DISAGREE / MISSING
            rows.append(
                {
                    "model": model,
                    "trial": t,
                    "content": content,
                    "structural": struct,
                    "composite": composite,
                }
            )

    irr = disagree / total if total else 0.0
    p1 = "CONFIRMED" if irr < 0.40 else "REFUTED"

    # P2 — all-content-PASS trials flipped to composite FAIL by structural.
    content_pass = [r for r in rows if r["content"] == "PASS"]
    flipped = [r for r in content_pass if r["structural"] == "FAIL"]
    pending = [r for r in content_pass if r["structural"] == "DISAGREE"]
    p2 = "CONFIRMED" if flipped else "REFUTED"
    preliminary = disagree > 0

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    o: list[str] = []
    o.append("\n## 02_fmv.1 structural-axis report\n")
    o.append(f"- Generated: `{ts}`\n")
    o.append("- Prereg lock: `prereg-02_fmv.1-locked`\n")
    o.append(f"- Structural judge cost (estimated): ${judge_cost:.4f}\n")
    if preliminary:
        o.append(
            f"- **PRELIMINARY** — {disagree} structural dual-judge "
            f"disagreement(s) await human audit. P1's IRR is audit-invariant; "
            f"P2 is a lower bound while a disagreement on a content-PASS trial "
            f"is unresolved ({len(pending)} such).\n"
        )
    o.append("\n### Structural-axis IRR\n")
    o.append(f"- {disagree}/{total} trials = **{irr:.2%}**\n\n")
    o.append("### Per-trial structural + composite verdicts\n\n")
    o.append("| Model | Trial | Content | Structural | Composite |\n|---|---|---|---|---|\n")
    for r in rows:
        o.append(
            f"| `{r['model']}` | {r['trial']} | {r['content']} | "
            f"{r['structural']} | {r['composite']} |\n"
        )
    o.append("\n")
    o.append(f"### P1 — Mechanical structural criteria reduce disagreement  ·  **{p1}**\n")
    o.append(
        f"Structural IRR {irr:.2%} (Confirmed < 40%; v0.2 Aristotelian structural IRR was 40%).\n\n"
    )
    o.append(f"### P2 — Structural axis catches a content-missed failure  ·  **{p2}**\n")
    o.append(
        f"All-content-PASS trials: {len(content_pass)}. Flipped to composite "
        f"FAIL via the structural axis: **{len(flipped)}** "
        f"({', '.join(f'{r["model"]} t{r["trial"]}' for r in flipped) or 'none'}). "
        f"Threshold ≥ 1.\n"
    )
    if pending:
        o.append(
            f"- {len(pending)} content-PASS trial(s) have a structural "
            f"DISAGREE pending audit: "
            f"{', '.join(f'{r["model"]} t{r["trial"]}' for r in pending)}.\n"
        )
    o.append("\n")

    FINDINGS.parent.mkdir(parents=True, exist_ok=True)
    if not FINDINGS.exists():
        FINDINGS.write_text("# PhysLit 02_fmv.1 — Structural-Axis Findings\n\n")
    with FINDINGS.open("a") as fh:
        fh.write("".join(o))

    print()
    print(f"=== P1 {p1} (IRR {irr:.2%}) | P2 {p2} ({len(flipped)} flipped) ===")
    if preliminary:
        print(f"(PRELIMINARY — {disagree} structural disagreement(s) await human audit)")
    print(f"Report appended to {FINDINGS.relative_to(REPO)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-trials", type=int, default=5)
    args = parser.parse_args()
    _load_dotenv()

    judges: list[tuple[str, JudgeBase]] = [("anthropic", ClaudeJudge()), ("openai", OpenAIJudge())]
    print("=== PhysLit 02_fmv.1 structural-axis judging ===")
    print(f"  trials: {3 * args.n_trials} | structural judges: Claude + GPT\n")

    cost = dispatch(args.n_trials, judges)
    print()
    print("=== Aggregating ===")
    aggregate(args.n_trials, cost)
    return 0


if __name__ == "__main__":
    sys.exit(main())
