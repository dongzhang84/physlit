"""Verify integrity of every locked ``predictions/v0_*_prereg.md``.

Pre-commit hook + CI guard. For each prereg file under ``predictions/``
matching ``v*_prereg.md``, computes SHA-256 of its canonical content
(everything below the ``<!-- LOCK BOUNDARY -->`` line) and compares to
the declared hash in that file's header. Fails on any mismatch.

Per-file behaviour:

- prereg file missing: not checked (the file simply does not exist).
- header has not yet been populated by the lock script: not checked
  (drafted but not locked is allowed).
- header declares a hash: must match the computed hash exactly.

Once a prereg is locked, any silent edit to its canonical content
fails this script and therefore the pre-commit hook and CI.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

PREREG_DIR = Path("predictions")
PREREG_GLOB = "v*_prereg.md"
BOUNDARY = "<!-- LOCK BOUNDARY"

_DECLARED_HASH_RE = re.compile(
    r"^- SHA-256 of canonical content[^:]*:\s*`([0-9a-fA-F]{64})`",
    re.MULTILINE,
)


def _canonical_bytes(text: str, path: Path) -> bytes:
    idx = text.find(BOUNDARY)
    if idx < 0:
        print(
            f"PREREG INTEGRITY FAILURE: {path}: missing LOCK BOUNDARY marker.",
            file=sys.stderr,
        )
        sys.exit(1)
    after_boundary_line = text[idx:].split("\n", 1)
    if len(after_boundary_line) < 2:
        return b""
    return after_boundary_line[1].encode("utf-8")


def _check_one(path: Path) -> tuple[str, str] | None:
    """Return ``(declared, actual)`` on mismatch, else ``None``."""
    text = path.read_text()
    header = text.split(BOUNDARY, 1)[0]
    match = _DECLARED_HASH_RE.search(header)
    if match is None:
        # Drafted but not yet locked — skip.
        return None
    declared = match.group(1).lower()
    actual = hashlib.sha256(_canonical_bytes(text, path)).hexdigest()
    if declared == actual:
        return None
    return declared, actual


def main() -> int:
    if not PREREG_DIR.is_dir():
        return 0
    prereg_paths = sorted(PREREG_DIR.glob(PREREG_GLOB))
    if not prereg_paths:
        return 0

    failed: list[tuple[Path, str, str]] = []
    for path in prereg_paths:
        result = _check_one(path)
        if result is not None:
            declared, actual = result
            failed.append((path, declared, actual))

    if not failed:
        return 0

    for path, declared, actual in failed:
        print(
            f"PREREG INTEGRITY FAILURE: {path}\n"
            f"  declared SHA-256: {declared}\n"
            f"  actual SHA-256:   {actual}\n"
            f"\n"
            f"  The canonical content (everything below the LOCK BOUNDARY\n"
            f"  line) has been edited since the lock. To revise the prereg,\n"
            f"  create a new version (e.g. v0.1.1, v0.2.1) with its own tag,\n"
            f"  NOT by editing this file in place. See `CLAUDE.md`\n"
            f"  'Pre-registration is irreversible' for the methodology rationale.",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
