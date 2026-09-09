# src/scripts/audit/bump_version.py
"""Bump a record document's `version:` and append a `history:` entry.

Every version bump in this record is the same two edits, and doing them by
hand went wrong three times in one session — each time the same way. The
naive edit replaces the `version:` line with a version line plus a fresh
`history:` block, which lands *before* any history the document already has,
producing either a duplicate `history:` key or entries in descending order.
`luria lint` catches both ("history: ends at version N but the document says
N+1"), and a guard that keeps catching you is a bug report about the
workflow (luria's CLAUDE.md).

    python -m src.scripts.audit.bump_version record/practices.d/SOTA-042.md \
        --note "What changed and why. The recommendation is unchanged."

Prints the new version. Refuses rather than guesses when the frontmatter is
shaped in a way it does not recognise.
"""

from __future__ import annotations

import re
import textwrap
from datetime import date
from pathlib import Path

import fire
from loguru import logger

WIDTH = 72
INDENT = "    "


def _history_span(front: str) -> tuple[int, int] | None:
    """Byte span of the `history:` block within the frontmatter, if present."""
    m = re.search(r"^history:\n(?:(?:[ #-].*)?\n)*", front, re.M)
    return (m.start(), m.end()) if m else None


def main(path: str, note: str, when: str | None = None) -> int:
    """Bump `path`'s version and append `note` as the new history entry."""
    p = Path(path)
    text = p.read_text()

    parts = text.split("---\n")
    if len(parts) < 3:
        raise SystemExit(f"{path}: no frontmatter to edit")
    front, body = parts[1], "---\n".join(parts[2:])

    vm = re.search(r"^version: (\d+)$", front, re.M)
    if not vm:
        raise SystemExit(f"{path}: no `version:` line")
    old = int(vm.group(1))
    new = old + 1

    if len(re.findall(r"^history:$", front, re.M)) > 1:
        raise SystemExit(f"{path}: more than one `history:` key — fix by hand")

    entry = (
        f"- version: {new}\n"
        f"  date: '{when or date.today().isoformat()}'\n"
        f"  note: >-\n"
        + textwrap.fill(note, WIDTH, initial_indent=INDENT, subsequent_indent=INDENT)
        + "\n"
    )

    front = front[: vm.start()] + f"version: {new}" + front[vm.end() :]
    vm = re.search(r"^version: (\d+)$", front, re.M)  # offsets moved

    span = _history_span(front)
    if span:
        # Append, so entries stay ascending and the block stays single.
        front = front[: span[1]] + entry + front[span[1] :]
    else:
        # First history the document has ever had: start it under `version:`.
        cut = front.index("\n", vm.start()) + 1
        front = front[:cut] + "history:\n" + entry + front[cut:]

    p.write_text(f"---\n{front}---\n{body}")
    logger.info(f"{p.name}: v{old} -> v{new}")
    return new


if __name__ == "__main__":
    fire.Fire(main)
