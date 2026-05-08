"""Front-matter parser and renderer for ``prompts/*.md``.

Each prompt template is a markdown file with YAML front-matter
delimited by ``---`` lines. The body is plain markdown with
``{{placeholder}}`` substitutions filled at render time.

Both the unfilled-placeholder check (raises if any ``{{var}}`` is left
in the rendered text) and the unknown-placeholder check (raises if a
caller-supplied key has no slot in the body) are deliberate: silent
prompt drift is a methodology bug, not a convenience feature.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

_FRONT_MATTER_RE = re.compile(r"^---\n(.+?)\n---\n(.*)", re.DOTALL)
_PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}")


class PromptTemplate:
    """One ``prompts/*.md`` file, parsed and ready to render."""

    def __init__(self, path: Path) -> None:
        text = path.read_text()
        match = _FRONT_MATTER_RE.match(text)
        if match is None:
            raise ValueError(f"No YAML front-matter in {path}")
        meta_raw: Any = yaml.safe_load(match.group(1))
        if not isinstance(meta_raw, dict):
            raise ValueError(
                f"Front-matter in {path} must be a YAML mapping, got {type(meta_raw).__name__}"
            )
        if "version" not in meta_raw or "stage" not in meta_raw:
            raise ValueError(f"Front-matter in {path} must include 'version' and 'stage'")
        self.path: Path = path
        self.version: str = str(meta_raw["version"])
        self.stage: str = str(meta_raw["stage"])
        self.description: str = str(meta_raw.get("description", ""))
        self.body: str = match.group(2)

    def render(self, **kwargs: Any) -> str:
        """Substitute ``{{name}}`` placeholders. Raises if any placeholder
        is unfilled or if a caller-supplied key has no slot in the body."""
        body = self.body
        body_keys = set(_PLACEHOLDER_RE.findall(body))
        unknown = set(kwargs) - body_keys
        if unknown:
            raise KeyError(
                f"Unknown placeholders supplied to {self.path.name}: "
                f"{sorted(unknown)} (body has {sorted(body_keys)})"
            )
        for key, value in kwargs.items():
            body = body.replace("{{" + key + "}}", str(value))
        leftover = _PLACEHOLDER_RE.findall(body)
        if leftover:
            raise KeyError(f"Unfilled placeholders in {self.path.name}: {sorted(set(leftover))}")
        return body
