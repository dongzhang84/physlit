"""Stage-3 scenario extraction from a framework's ``prediction_tests.md``.

``prediction_tests.md`` is the **single source of truth** for the five
Stage-3 scenarios. The file mixes:

- the *prompt* sent to the tested model (this module extracts that),
- the Aristotelian PASS column and the standard-physics FAIL column
  (judges read these; the tested model must not see them),
- a *Why this scenario* commentary (human reviewers; never sent).

The runner consumes the prompts via :func:`extract_scenarios` and the
formatted block from :func:`render_scenarios_block`. Tests verify that
the extracted text contains the expected substrings, so any future
edit to ``prediction_tests.md`` that breaks the parser fails CI rather
than silently shipping a different prompt.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class Scenario(BaseModel):
    """One Stage-3 scenario extracted from a ``prediction_tests.md``."""

    model_config = ConfigDict(frozen=True)

    index: int
    title: str
    prompt: str


_HEADER_RE = re.compile(r"^## Scenario (\d+) — (.+?)$", re.MULTILINE)
_PROMPT_MARKER = "**Prompt to the model.**"


def extract_scenarios(prediction_tests_md: str) -> list[Scenario]:
    """Parse a ``prediction_tests.md`` body into a list of ``Scenario``.

    Each scenario must have a header matching ``## Scenario N — Title``
    and a body containing a single ``**Prompt to the model.**`` marker;
    the prompt text runs from that marker to the start of the first
    table line (a line beginning with ``|``). Anything after the table
    is judge-only commentary and not returned.

    Raises ``ValueError`` if the file's structure does not match.
    """
    headers = list(_HEADER_RE.finditer(prediction_tests_md))
    if not headers:
        raise ValueError("No '## Scenario N — Title' headers found in prediction_tests.md")

    scenarios: list[Scenario] = []
    for i, hdr in enumerate(headers):
        idx = int(hdr.group(1))
        title = hdr.group(2).strip()
        body_start = hdr.end()
        body_end = headers[i + 1].start() if i + 1 < len(headers) else len(prediction_tests_md)
        body = prediction_tests_md[body_start:body_end]
        marker_pos = body.find(_PROMPT_MARKER)
        if marker_pos < 0:
            raise ValueError(f"Scenario {idx} ({title!r}): missing '{_PROMPT_MARKER}' marker")
        after_marker = body[marker_pos + len(_PROMPT_MARKER) :]
        # Prompt text runs until the first markdown table or horizontal rule.
        table_match = re.search(r"\n\n(?:\||---)", after_marker)
        if table_match is None:
            raise ValueError(
                f"Scenario {idx} ({title!r}): no terminator after prompt "
                f"(expected '|' table or '---' rule)"
            )
        prompt_text = after_marker[: table_match.start()].strip()
        if not prompt_text:
            raise ValueError(f"Scenario {idx} ({title!r}): empty prompt body")
        scenarios.append(Scenario(index=idx, title=title, prompt=prompt_text))

    # Indices must be 1-based contiguous (1, 2, 3, ...). Drift here is a bug.
    expected = list(range(1, len(scenarios) + 1))
    actual = [s.index for s in scenarios]
    if actual != expected:
        raise ValueError(f"Scenario indices must be 1-based contiguous; got {actual}")
    return scenarios


def render_scenarios_block(scenarios: list[Scenario]) -> str:
    """Format scenarios as the ``{{scenarios}}`` block injected into the
    Stage 3 prompt template.

    Layout: each scenario on its own paragraph, prefixed with
    ``Scenario N. `` so the tested model sees a numbered list.
    """
    return "\n\n".join(f"Scenario {s.index}. {s.prompt}" for s in scenarios)


def load_scenarios(prediction_tests_path: Path) -> list[Scenario]:
    """Convenience: read the file at ``prediction_tests_path`` and parse."""
    return extract_scenarios(prediction_tests_path.read_text())
