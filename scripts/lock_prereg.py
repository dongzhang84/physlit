"""Lock ``predictions/v0_1_prereg.md``.

Computes SHA-256 of the **canonical content** (everything below the
``<!-- LOCK BOUNDARY -->`` line), reads HEAD commit + UTC timestamp,
edits the prereg-file header in place to embed those values, and
prints the exact ``git`` commands the operator should run to commit
and tag.

The script does **not** automatically commit, tag, or push. The
prereg-lock commit is the most consequential commit in the entire
project and explicit operator confirmation of the diff is worth the
extra step. The deviation from `CLAUDE.md`'s "push after each step"
rule is intentional and applies only to this lock operation.

Usage:
    uv run python scripts/lock_prereg.py [version]   # default v0.1
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

PREREG_PATH = Path("predictions/v0_1_prereg.md")
BOUNDARY = "<!-- LOCK BOUNDARY"


def _canonical_bytes(text: str) -> bytes:
    """Return everything below the LOCK BOUNDARY line as UTF-8 bytes."""
    idx = text.find(BOUNDARY)
    if idx < 0:
        raise SystemExit(f"{PREREG_PATH}: missing LOCK BOUNDARY marker")
    after_boundary_line = text[idx:].split("\n", 1)
    if len(after_boundary_line) < 2:
        return b""
    return after_boundary_line[1].encode("utf-8")


def _replace_unique_line(text: str, prefix: str, replacement: str) -> str:
    """Replace the single line whose start matches ``prefix`` with
    ``replacement``. Raises if 0 or > 1 matches found.
    """
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", re.MULTILINE)
    matches = pattern.findall(text)
    if len(matches) != 1:
        raise SystemExit(
            f"Header sanity check failed: expected exactly one line "
            f"starting with {prefix!r}, found {len(matches)}."
        )
    return pattern.sub(replacement, text, count=1)


def main() -> int:
    version = sys.argv[1] if len(sys.argv) > 1 else "v0.1"
    tag = f"prereg-{version}-locked"

    if not PREREG_PATH.exists():
        raise SystemExit(f"{PREREG_PATH} does not exist")

    rc = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if rc.returncode == 0:
        raise SystemExit(f"Tag {tag} already exists. Use a new version (e.g. v0.1.1).")

    text = PREREG_PATH.read_text()
    canonical_hash = hashlib.sha256(_canonical_bytes(text)).hexdigest()
    head_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    text = _replace_unique_line(
        text,
        "- Locked at git commit:",
        f"- Locked at git commit: `{head_commit}`",
    )
    text = _replace_unique_line(
        text,
        "- Locked at git tag:",
        f"- Locked at git tag: `{tag}`",
    )
    text = _replace_unique_line(
        text,
        "- Lock timestamp (UTC):",
        f"- Lock timestamp (UTC): `{timestamp}`",
    )
    text = _replace_unique_line(
        text,
        "- SHA-256 of canonical content",
        f"- SHA-256 of canonical content (everything below the LOCK "
        f"BOUNDARY line): `{canonical_hash}`",
    )

    PREREG_PATH.write_text(text)

    print(f"Updated {PREREG_PATH} with lock metadata:")
    print(f"  commit:    {head_commit}")
    print(f"  tag:       {tag}")
    print(f"  timestamp: {timestamp}")
    print(f"  sha-256:   {canonical_hash}")
    print()
    print("Now review `git diff predictions/v0_1_prereg.md` and run:")
    print(f"  git add {PREREG_PATH}")
    print(f"  git commit -m 'lock: pre-register PhysLit {version} predictions'")
    print(f"  git tag -a {tag} -m 'Pre-registered predictions locked at {timestamp}'")
    print("  git push origin main")
    print(f"  git push origin {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
