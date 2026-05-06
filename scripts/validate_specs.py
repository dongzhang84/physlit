"""Validate every ``frameworks/*/spec.yaml`` against :class:`FrameworkSpec`.

Run via ``uv run python scripts/validate_specs.py``. Exits non-zero on any
schema violation. Wired into pre-commit so spec drift fails the commit.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from physlit.schema import FrameworkSpec

FRAMEWORKS_DIR = Path("frameworks")


def validate_one(spec_file: Path) -> tuple[bool, str]:
    """Return (ok, message) for a single spec file."""
    try:
        data: Any = yaml.safe_load(spec_file.read_text())
    except yaml.YAMLError as e:
        return False, f"YAML parse error: {e}"
    if not isinstance(data, dict):
        return False, f"top-level YAML must be a mapping, got {type(data).__name__}"
    try:
        FrameworkSpec.model_validate(data)
    except Exception as e:  # pydantic ValidationError or ValueError from validator
        return False, str(e)

    declared_id = data.get("id")
    expected_dir = spec_file.parent.name
    if declared_id != expected_dir:
        return False, f"id={declared_id!r} does not match directory name {expected_dir!r}"

    return True, "ok"


def main() -> int:
    spec_files = sorted(FRAMEWORKS_DIR.glob("*/spec.yaml"))
    if not spec_files:
        print(f"[WARN] no spec.yaml files under {FRAMEWORKS_DIR}/")
        return 0

    failures = 0
    for spec_file in spec_files:
        ok, message = validate_one(spec_file)
        marker = "OK " if ok else "ERR"
        print(f"[{marker}] {spec_file}: {message}")
        if not ok:
            failures += 1

    if failures:
        print(f"\n{failures} spec file(s) failed validation", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
