"""Verify ``predictions/v0_1_prereg.md`` integrity.

Pre-commit hook + CI guard. Computes SHA-256 of the canonical content
(everything below the ``<!-- LOCK BOUNDARY -->`` line), compares to the
declared hash in the header. Fails on mismatch.

No-op if:

- the prereg file does not exist (Phase 5 not yet started); or
- the header has not yet been populated by the lock script
  (drafted but not locked).

Once locked, any silent edit to the canonical content fails this
script and therefore the pre-commit hook and CI.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

PREREG_PATH = Path("predictions/v0_1_prereg.md")
BOUNDARY = "<!-- LOCK BOUNDARY"

_DECLARED_HASH_RE = re.compile(
    r"^- SHA-256 of canonical content[^:]*:\s*`([0-9a-fA-F]{64})`",
    re.MULTILINE,
)


def _canonical_bytes(text: str) -> bytes:
    idx = text.find(BOUNDARY)
    if idx < 0:
        print(
            f"PREREG INTEGRITY FAILURE: {PREREG_PATH}: missing LOCK BOUNDARY marker.",
            file=sys.stderr,
        )
        sys.exit(1)
    after_boundary_line = text[idx:].split("\n", 1)
    if len(after_boundary_line) < 2:
        return b""
    return after_boundary_line[1].encode("utf-8")


def main() -> int:
    if not PREREG_PATH.exists():
        return 0

    text = PREREG_PATH.read_text()
    header = text.split(BOUNDARY, 1)[0]
    match = _DECLARED_HASH_RE.search(header)
    if match is None:
        # Drafted but not yet locked — hook is a no-op.
        return 0

    declared = match.group(1).lower()
    actual = hashlib.sha256(_canonical_bytes(text)).hexdigest()
    if declared == actual:
        return 0

    print(
        f"PREREG INTEGRITY FAILURE: {PREREG_PATH}\n"
        f"  declared SHA-256: {declared}\n"
        f"  actual SHA-256:   {actual}\n"
        f"\n"
        f"  The canonical content (everything below the LOCK BOUNDARY\n"
        f"  line) has been edited since the lock. To revise the prereg,\n"
        f"  create a new version (e.g. v0.1.1) with its own tag, NOT by\n"
        f"  editing this file in place. See `CLAUDE.md` 'Pre-registration\n"
        f"  is irreversible' for the methodology rationale.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
