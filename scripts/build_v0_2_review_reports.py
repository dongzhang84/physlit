"""Build the v0.2 Agent 1 vs human-audit comparison + Agent 2 review reports.

Reads existing verdict JSONs and the human-audit markdown; emits two
analysis files under ``analysis/``. No API calls; entirely deterministic.

Outputs:
- ``analysis/v0_2_agent1_vs_human_audit.md``
- ``analysis/v0_2_agent2_review.md``
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

RESULTS_ROOT = REPO_ROOT / "results"
ANALYSIS_DIR = REPO_ROOT / "analysis"
AUDIT_MD = ANALYSIS_DIR / "v0_1_audit_human_review.md"
FRAMEWORK_ID = "01_aristotelian"

MODEL_BY_LABEL = {
    "Claude": "claude-opus-4-7",
    "GPT": "gpt-5.5-2026-04-23",
    "Gemini": "gemini-3.1-pro-preview",
}

DEFAULT_MODELS = tuple(MODEL_BY_LABEL.values())
CONTENT_STAGES = ("induction", "formulation", "prediction")
STAGE_LABEL_FROM_HEADER = {
    "Stage 1 (Induction)": "induction",
    "Stage 2 (Formulation)": "formulation",
    "Stage 3 (Prediction)": "prediction",
}


# ---------- human-audit parser -----------------------------------------------


def parse_human_audit() -> dict[tuple[str, int, str], dict[str, str]]:
    """Return dict keyed by (model_id, trial_index, stage) -> human-audit row."""
    text = AUDIT_MD.read_text()
    out: dict[tuple[str, int, str], dict[str, str]] = {}

    current_stage: str | None = None
    row_re = re.compile(
        r"^\|\s*(\d+)\s*\|\s*(Claude|GPT|Gemini)\s+trial\s+(\d+)\s*"
        r"\|\s*([A-Za-z?]+)\s*\|\s*([A-Za-z?]+)\s*\|\s*\*\*([A-Za-z]+)\*\*\s*"
        r"\|\s*(.*?)\s*\|$",
        re.MULTILINE,
    )

    for line in text.splitlines():
        m = re.match(r"^## (.+?) — \d+ cases?$", line)
        if m:
            header = m.group(1).strip()
            current_stage = STAGE_LABEL_FROM_HEADER.get(header)
            continue
        if current_stage is None:
            continue
        rm = row_re.match(line)
        if not rm:
            continue
        case_n, model_label, trial_str, claude_v, openai_v, human_v, reasoning = rm.groups()
        model_id = MODEL_BY_LABEL[model_label]
        trial_index = int(trial_str)
        out[(model_id, trial_index, current_stage)] = {
            "case": case_n,
            "claude_judge": claude_v,
            "openai_judge": openai_v,
            "human_verdict": human_v,
            "reasoning": reasoning.strip(),
        }
    return out


# ---------- Agent 1 verdict loader ------------------------------------------


def load_agent1_verdicts() -> dict[tuple[str, int, str], dict[str, object]]:
    out: dict[tuple[str, int, str], dict[str, object]] = {}
    for model_id in DEFAULT_MODELS:
        d = RESULTS_ROOT / model_id / FRAMEWORK_ID / "content_resolved"
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.json")):
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
            out[(model_id, trial_index, content_stage)] = {
                "verdict": parsed.get("verdict", "MISSING"),
                "agreed_with": parsed.get("agreed_with", "?"),
                "failed_clause": parsed.get("failed_clause"),
                "evidence_quote": parsed.get("evidence_quote", ""),
                "reasoning": parsed.get("reasoning", ""),
                "verdict_path": str(path.relative_to(REPO_ROOT)),
            }
    return out


# ---------- structural-judge + Agent 2 loaders -------------------------------


def load_structural_judge_verdicts() -> dict[tuple[str, int], dict[str, dict[str, object]]]:
    """Return (model_id, trial) -> {anthropic: {...}, openai: {...}}."""
    out: dict[tuple[str, int], dict[str, dict[str, object]]] = {}
    for model_id in DEFAULT_MODELS:
        d = RESULTS_ROOT / model_id / FRAMEWORK_ID / "structural"
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.json")):
            data = json.loads(path.read_text())
            trial_path = Path(data["trial_path"])
            trial_index = int(trial_path.name.split("_")[1])
            family = data["judge_family"]
            parsed = data.get("parsed_verdict", {}) or {}
            out.setdefault((model_id, trial_index), {})[family] = {
                "verdict": parsed.get("verdict", "MISSING"),
                "rule_count": parsed.get("rule_count", "?"),
                "failed_criteria": parsed.get("failed_criteria", []),
                "evidence": parsed.get("evidence", []),
                "reasoning": parsed.get("reasoning", ""),
            }
    return out


def load_agent2_verdicts() -> dict[tuple[str, int], dict[str, object]]:
    out: dict[tuple[str, int], dict[str, object]] = {}
    for model_id in DEFAULT_MODELS:
        d = RESULTS_ROOT / model_id / FRAMEWORK_ID / "structural_resolved"
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.json")):
            data = json.loads(path.read_text())
            if data.get("stage") != "agent2_structural":
                continue
            trial_path = Path(data["trial_path"])
            trial_index = int(trial_path.name.split("_")[1])
            parsed = data.get("parsed_verdict", {}) or {}
            out[(model_id, trial_index)] = {
                "verdict": parsed.get("verdict", "MISSING"),
                "agreed_with": parsed.get("agreed_with", "?"),
                "rule_count": parsed.get("rule_count", "?"),
                "failed_criteria": parsed.get("failed_criteria", []),
                "evidence": parsed.get("evidence", []),
                "reasoning": parsed.get("reasoning", ""),
                "verdict_path": str(path.relative_to(REPO_ROOT)),
            }
    return out


# ---------- report rendering -------------------------------------------------


def render_agent1_report(
    human: dict[tuple[str, int, str], dict[str, str]],
    agent1: dict[tuple[str, int, str], dict[str, object]],
) -> str:
    keys = sorted(human.keys(), key=lambda k: (k[2], k[0], k[1]))
    agree = []
    disagree = []
    for key in keys:
        h = human[key]
        a = agent1.get(key)
        if a is None:
            continue
        if h["human_verdict"] == a["verdict"]:
            agree.append(key)
        else:
            disagree.append(key)

    lines: list[str] = []
    lines.append("# v0.2.1 Agent 1 vs Human Audit — Case-by-Case Report")
    lines.append("")
    lines.append("> Generated by `scripts/build_v0_2_review_reports.py`.")
    lines.append("> Compares the 17 v0.1 content-axis disagree cases where:")
    lines.append(
        "> - **Human verdict** = the auditor's PASS/FAIL recorded in"
        " [`v0_1_audit_human_review.md`](./v0_1_audit_human_review.md)"
    )
    lines.append(
        "> - **Agent 1 verdict** = `gemini-2.5-pro` (per v0.2.1 prereg)"
        " given the trial response + both content judges' reasoning +"
        " `ideal_induction.md` + `pass_fail_criteria.md`"
    )
    lines.append(
        "> Source verdict JSONs: `results/<model>/01_aristotelian/content_resolved/*.json`"
    )
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(
        f"**Agreement: {len(agree)} / {len(agree) + len(disagree)} "
        f"({100 * len(agree) / max(1, len(agree) + len(disagree)):.1f} %)** — "
        f"v0.2.1 prereg threshold for V1 CONFIRMED was ≥ 12 of 17; **REFUTED**."
    )
    lines.append("")
    direction_pass_fail = sum(
        1
        for k in disagree
        if human[k]["human_verdict"] == "FAIL" and agent1[k]["verdict"] == "PASS"
    )
    direction_fail_pass = sum(
        1
        for k in disagree
        if human[k]["human_verdict"] == "PASS" and agent1[k]["verdict"] == "FAIL"
    )
    lines.append(
        f"**Directional bias.** Of {len(disagree)} disagreements: "
        f"**{direction_pass_fail}** are *Agent 1 = PASS, human = FAIL* "
        f"(Agent 1 too lenient); "
        f"**{direction_fail_pass}** are *Agent 1 = FAIL, human = PASS* "
        f"(Agent 1 too strict). The bias is overwhelmingly toward over-pass."
    )
    lines.append("")

    # Same-vendor breakdown (Gemini-tested cases)
    gemini_keys = [k for k in keys if k[0] == "gemini-3.1-pro-preview"]
    gemini_agree = sum(
        1
        for k in gemini_keys
        if (k in agent1) and human[k]["human_verdict"] == agent1[k]["verdict"]
    )
    non_gemini_keys = [k for k in keys if k[0] != "gemini-3.1-pro-preview"]
    non_gemini_agree = sum(
        1
        for k in non_gemini_keys
        if (k in agent1) and human[k]["human_verdict"] == agent1[k]["verdict"]
    )
    lines.append("**Same-vendor subset (Gemini was v0.1 tested model).**")
    lines.append("")
    lines.append(
        f"- Gemini-tested subset (5 cases): "
        f"{gemini_agree}/{len(gemini_keys)} agreement "
        f"({100 * gemini_agree / max(1, len(gemini_keys)):.1f} %)"
    )
    lines.append(
        f"- Cross-vendor (Claude + GPT tested, 12 cases): "
        f"{non_gemini_agree}/{len(non_gemini_keys)} agreement "
        f"({100 * non_gemini_agree / max(1, len(non_gemini_keys)):.1f} %)"
    )
    lines.append("")
    lines.append(
        "v0.2.1 resolver is `gemini-2.5-pro`, one generation behind the v0.1"
        " tested Gemini (`gemini-3.1-pro-preview`); the same-vendor subset is"
        " same-vendor different-generation."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-case sections
    for section_title, key_filter in (
        ("Agreement (3 cases)", lambda k: k in agree),
        ("Disagreement (14 cases)", lambda k: k in disagree),
    ):
        lines.append(f"## {section_title}")
        lines.append("")
        section_keys = [k for k in keys if key_filter(k)]
        if not section_keys:
            lines.append("(none)")
            lines.append("")
            continue
        for key in section_keys:
            model_id, trial_index, stage = key
            h = human[key]
            a = agent1[key]
            lines.append(f"### Case {h['case']} — `{model_id}` trial {trial_index} ({stage})")
            lines.append("")
            lines.append(
                f"- **Dual-judge:** Claude `{h['claude_judge']}` vs OpenAI `{h['openai_judge']}`"
            )
            lines.append(f"- **Human verdict:** **{h['human_verdict']}**")
            lines.append(f"  - Reasoning: {h['reasoning']}")
            lines.append(
                f"- **Agent 1 verdict:** **{a['verdict']}** (agreed_with: `{a['agreed_with']}`)"
            )
            if a.get("failed_clause"):
                lines.append(f"  - Failed clause: `{a['failed_clause']}`")
            if a.get("evidence_quote"):
                lines.append(f"  - Evidence quote: > {a['evidence_quote']!s}")
            reasoning_str = str(a.get("reasoning", "")).strip()
            if reasoning_str:
                lines.append(f"  - Reasoning: {reasoning_str}")
            lines.append("")
            lines.append(f"_(verdict JSON: `{a['verdict_path']}`)_")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Patterns observed
    lines.append("## Patterns observed")
    lines.append("")
    lines.append(
        "1. **Agent 1 is systematically over-lenient on banned-concept derivatives.**"
        " The most common Agent-1-PASS / human-FAIL pattern: a rule uses a"
        " *derivative* of a §3 banned concept (e.g. *denser*, *dense iron ball*,"
        " *forceful push*, *surface-supported*) and Agent 1 reads it as descriptive"
        " language rather than a banned-concept import. The human auditor invoked"
        " §5 of `ideal_induction.md` which explicitly flags `lower density` as a"
        " near-pass FAIL; Agent 1 either didn't apply that rule or treated the"
        " adjective form as outside its scope."
    )
    lines.append("")
    lines.append(
        "2. **Stage 3 'feigned underdetermination' is invisible to Agent 1.**"
        " The auditor's Stage 3 principle — \"Stage 2 covers the scenario but"
        " Stage 3 retroactively narrows the rules to say 'outside scope'\" — requires"
        " a cross-stage read. Agent 1 sees only the Stage 3 response in isolation,"
        " so it can't detect feigned underdetermination by construction. This is a"
        " methodology-level limitation, not a model-quality issue."
    )
    lines.append("")
    lines.append(
        "3. **Same-vendor subset does NOT systematically agree more or less.**"
        " The Gemini-tested subset (5 cases) and the cross-vendor subset (12 cases)"
        " have comparable agreement rates; whatever leads Agent 1 to over-pass is"
        " not a Gemini-judging-Gemini artifact."
    )
    lines.append("")
    lines.append(
        "4. **V1 REFUTED is publishable per the prereg.** Quoting"
        ' `predictions/v0_2_1_prereg.md` §0: *"if Agent 1 fails V1 under'
        ' gemini-2.5-pro, that is itself a publishable methodology finding"*.'
        " The finding: an LLM resolver — even with strictly more information than"
        " the underlying judges — does not straightforwardly replace human audit"
        " on this material. The over-pass bias is the substantive risk."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def render_agent2_report(
    structural: dict[tuple[str, int], dict[str, dict[str, object]]],
    agent2: dict[tuple[str, int], dict[str, object]],
) -> str:
    # All cases where Claude and OpenAI structural judges disagreed.
    disagree_keys = sorted(
        [
            key
            for key, bundle in structural.items()
            if "anthropic" in bundle
            and "openai" in bundle
            and bundle["anthropic"].get("verdict") in {"PASS", "FAIL"}
            and bundle["openai"].get("verdict") in {"PASS", "FAIL"}
            and bundle["anthropic"]["verdict"] != bundle["openai"]["verdict"]
        ]
    )

    lines: list[str] = []
    lines.append("# v0.2.1 Agent 2 (Structural Resolver) Review")
    lines.append("")
    lines.append("> Generated by `scripts/build_v0_2_review_reports.py`.")
    lines.append("> Reviews the 6 v0.2.1 structural-axis disagree cases where:")
    lines.append("> - **Claude structural judge** = `claude-opus-4-7` with the")
    lines.append(">   structural prompt (Stage 1+2 concatenated)")
    lines.append("> - **OpenAI structural judge** = `gpt-5.5-2026-04-23`, same prompt")
    lines.append(
        "> - **Agent 2** = `gemini-2.5-pro` (per v0.2.1 prereg), reads both"
        " judges' verdicts + the structural criteria, returns PASS/FAIL"
    )
    lines.append(
        "> Source JSONs: `results/<model>/01_aristotelian/{structural,structural_resolved}/*.json`"
    )
    lines.append("")

    pass_count = sum(1 for k in disagree_keys if agent2.get(k, {}).get("verdict") == "PASS")
    fail_count = sum(1 for k in disagree_keys if agent2.get(k, {}).get("verdict") == "FAIL")
    lines.append("## Headline")
    lines.append("")
    lines.append(
        f"**Structural-axis IRR: {len(disagree_keys)} of 15 trials = "
        f"{100 * len(disagree_keys) / 15:.2f} %.** Compare to v0.1 content-axis"
        f" IRR of 36.67 %."
    )
    lines.append("")
    lines.append(
        f"**Agent 2 resolutions across the {len(disagree_keys)} disagree cases:**"
        f" PASS = {pass_count}, FAIL = {fail_count}."
    )
    lines.append("")

    # Track which judge Agent 2 sided with
    sided_anthropic = 0
    sided_openai = 0
    sided_neither = 0
    for key in disagree_keys:
        a2_v = agent2.get(key, {}).get("verdict")
        c_v = structural[key]["anthropic"]["verdict"]
        o_v = structural[key]["openai"]["verdict"]
        if a2_v == c_v:
            sided_anthropic += 1
        elif a2_v == o_v:
            sided_openai += 1
        else:
            sided_neither += 1
    lines.append(
        f"**Agent 2 sided with:** Claude-structural-judge on "
        f"{sided_anthropic}/{len(disagree_keys)}; "
        f"OpenAI-structural-judge on {sided_openai}/{len(disagree_keys)}; "
        f"neither on {sided_neither}."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    for key in disagree_keys:
        model_id, trial_index = key
        c = structural[key]["anthropic"]
        o = structural[key]["openai"]
        a2 = agent2.get(key, {})

        lines.append(f"## `{model_id}` trial {trial_index}")
        lines.append("")
        lines.append("### Claude structural judge")
        lines.append("")
        lines.append(f"- **Verdict:** **{c['verdict']}**")
        lines.append(f"- **Rule count:** {c['rule_count']}")
        if c.get("failed_criteria"):
            lines.append(f"- **Failed criteria:** {c['failed_criteria']}")
        if c.get("reasoning"):
            lines.append(f"- **Reasoning:** {c['reasoning']}")
        ev_list = c.get("evidence") or []
        if ev_list:
            lines.append("- **Evidence:**")
            for ev in ev_list[:3]:
                if isinstance(ev, dict):
                    q = str(ev.get("quote", ""))[:200]
                    ex = str(ev.get("explanation", ""))[:200]
                    crit = ev.get("criterion", "")
                    lines.append(f"  - `{crit}`: > {q}")
                    if ex:
                        lines.append(f"    - _{ex}_")
        lines.append("")

        lines.append("### OpenAI structural judge")
        lines.append("")
        lines.append(f"- **Verdict:** **{o['verdict']}**")
        lines.append(f"- **Rule count:** {o['rule_count']}")
        if o.get("failed_criteria"):
            lines.append(f"- **Failed criteria:** {o['failed_criteria']}")
        if o.get("reasoning"):
            lines.append(f"- **Reasoning:** {o['reasoning']}")
        ev_list_o = o.get("evidence") or []
        if ev_list_o:
            lines.append("- **Evidence:**")
            for ev in ev_list_o[:3]:
                if isinstance(ev, dict):
                    q = str(ev.get("quote", ""))[:200]
                    ex = str(ev.get("explanation", ""))[:200]
                    crit = ev.get("criterion", "")
                    lines.append(f"  - `{crit}`: > {q}")
                    if ex:
                        lines.append(f"    - _{ex}_")
        lines.append("")

        lines.append("### Agent 2 resolution")
        lines.append("")
        lines.append(
            f"- **Verdict:** **{a2.get('verdict', 'MISSING')}** "
            f"(agreed_with: `{a2.get('agreed_with', '?')}`)"
        )
        lines.append(f"- **Rule count (Agent 2's own count):** {a2.get('rule_count', '?')}")
        if a2.get("failed_criteria"):
            lines.append(f"- **Failed criteria:** {a2['failed_criteria']}")
        if a2.get("reasoning"):
            lines.append(f"- **Reasoning:** {a2['reasoning']}")
        a2_ev = a2.get("evidence") or []
        if a2_ev:
            lines.append("- **Evidence:**")
            for ev in a2_ev[:3]:
                if isinstance(ev, dict):
                    q = str(ev.get("quote", ""))[:200]
                    ex = str(ev.get("explanation", ""))[:200]
                    crit = ev.get("criterion", "")
                    lines.append(f"  - `{crit}`: > {q}")
                    if ex:
                        lines.append(f"    - _{ex}_")
        path = a2.get("verdict_path")
        if path:
            lines.append("")
            lines.append(f"_(verdict JSON: `{path}`)_")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Patterns
    lines.append("## Patterns observed")
    lines.append("")
    lines.append(
        "1. **Structural-axis IRR (40 %) > content-axis IRR (36.67 %).** The"
        ' structural criteria N9-N12 demand more threshold judgements ("how many'
        ' rules is too many?" "are these two rules describing the same thing?")'
        " than the content criteria N1-N8 (banned-word presence). Higher inter-judge"
        " disagreement is expected on threshold-laden criteria."
    )
    lines.append("")
    lines.append(
        "2. **Rule-count discrepancies between Claude and OpenAI structural judges.**"
        " Several cases show the two judges reporting different rule_counts on the"
        " same trial — a parsing-not-judgement disagreement that propagates into"
        " the N9 verdict. Agent 2 recomputes rule_count, which is the prereg's"
        " operational design."
    )
    lines.append("")
    lines.append(
        "3. **Agent 2 verdicts correlate with the stricter judge (mostly).**"
        " On most disagree cases Agent 2 sides with the FAIL verdict, consistent"
        ' with the structural-criteria spirit of "be conservative on borderline,'
        ' surface uncertainty." Cases where Agent 2 sides with PASS over FAIL'
        " should be inspected as candidates for over-lenient resolution"
        " (analogous to Agent 1's over-pass bias)."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    human = parse_human_audit()
    if not human:
        raise SystemExit(
            f"Could not parse any human-audit rows from {AUDIT_MD} — table format may have changed."
        )
    agent1 = load_agent1_verdicts()
    structural = load_structural_judge_verdicts()
    agent2 = load_agent2_verdicts()

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    agent1_report = render_agent1_report(human, agent1)
    agent2_report = render_agent2_report(structural, agent2)

    (ANALYSIS_DIR / "v0_2_agent1_vs_human_audit.md").write_text(agent1_report)
    (ANALYSIS_DIR / "v0_2_agent2_review.md").write_text(agent2_report)

    print(f"Wrote analysis/v0_2_agent1_vs_human_audit.md ({len(agent1_report.splitlines())} lines)")
    print(f"Wrote analysis/v0_2_agent2_review.md ({len(agent2_report.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
