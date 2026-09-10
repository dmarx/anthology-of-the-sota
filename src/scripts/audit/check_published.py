# src/scripts/audit/check_published.py
"""Check that every `published:` agrees with the paper it is copied from.

`published:` is ground truth in one place only — a `LIT` note, where it is the
paper's publication date and feeds the scheme's alias template. Everywhere else
it is **derived and stored by hand**:

- a `SOTA` practice copies its **primary** source's date, meaning the first
  entry in `source:` (`ADR-010` makes the list ordered, `ADR-017` makes the
  first entry the one the claim rests on);
- a `NOTE` copies the date of the paper named in `paper:`.

Stored derived data goes stale when its input changes, and this record has the
receipts. The `#119` backfill found **eight practices whose `published:` was
the date of a source that had since been replaced** — `SOTA-048`'s named a
paper that was no longer in its `source:` list at all. Nothing could see it:
`luria concretize` rewrites references, not values, and the lint has no rule
relating two documents' fields.

luria has no cross-reference derivation (`derive` reads a document's own
fields), so the choice is to store it and check it. This is the check.

    python -m src.scripts.audit.check_published            # report, exit 1 on drift
    python -m src.scripts.audit.check_published --fix      # rewrite to match

Exits non-zero when anything disagrees, so CI can run it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fire
import yaml
from loguru import logger

RECORD = Path("record")


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        return {}
    return yaml.safe_load(text[3 : text.index("\n---", 3)]) or {}


def _date(value) -> str | None:
    """Normalise a YAML date or string to `YYYY-MM-DD`."""
    return str(value)[:10] if value else None


def _rewrite(path: Path, want: str) -> None:
    """Set `published:` to `want`, inserting it after `date:` if absent."""
    text = path.read_text()
    line = f"published: '{want}'"
    existing = re.search(r"^published:.*$", text, re.M)
    if existing:
        text = text[: existing.start()] + line + text[existing.end() :]
    else:
        anchor = re.search(r"^date:.*$", text, re.M)
        if not anchor:
            raise ValueError(f"{path.name}: no `date:` field to anchor after")
        text = text[: anchor.end()] + "\n" + line + text[anchor.end() :]
    path.write_text(text)


def _expected() -> tuple[dict[Path, tuple[str, str]], list[str]]:
    """Map each derived document to `(expected date, what it was copied from)`."""
    published: dict[str, str | None] = {}
    for note in (RECORD / "literature.d").glob("LIT-*.md"):
        published[note.stem] = _date(_frontmatter(note).get("published"))

    wanted: dict[Path, tuple[str, str]] = {}
    undecidable: list[str] = []

    for path in sorted((RECORD / "practices.d").glob("SOTA-*.md")):
        sources = [s for s in (_frontmatter(path).get("source") or []) if s in published]
        if not sources:
            undecidable.append(f"{path.stem}: no source in the literature record")
        elif not published[sources[0]]:
            undecidable.append(f"{path.stem}: primary source {sources[0]} is undated")
        else:
            wanted[path] = (published[sources[0]], f"primary source {sources[0]}")

    for path in sorted((RECORD / "notes.d").glob("NOTE-*.md")):
        paper = _frontmatter(path).get("paper")
        if paper not in published:
            undecidable.append(f"{path.stem}: paper {paper!r} is not in the record")
        elif not published[paper]:
            undecidable.append(f"{path.stem}: paper {paper} is undated")
        else:
            wanted[path] = (published[paper], f"paper {paper}")

    return wanted, undecidable


def main(fix: bool = False) -> None:
    """Report — or with `--fix`, repair — every `published:` that has drifted."""
    wanted, undecidable = _expected()

    missing: list[str] = []
    drifted: list[str] = []
    for path, (want, whence) in sorted(wanted.items()):
        have = _date(_frontmatter(path).get("published"))
        if have == want:
            continue
        note = f"{path.stem}: {have or 'absent'} -> {want} (from its {whence})"
        (missing if have is None else drifted).append(note)
        if fix:
            _rewrite(path, want)

    for problem in undecidable:
        logger.warning(problem)
    for note in missing:
        logger.info(f"missing  {note}")
    for note in drifted:
        logger.error(f"STALE    {note}")

    total = len(missing) + len(drifted)
    if fix:
        logger.info(f"checked {len(wanted)}, rewrote {total}")
        return
    if total:
        logger.error(
            f"checked {len(wanted)}: {len(missing)} missing, {len(drifted)} stale. "
            "Rerun with --fix, or correct the source list if that is what moved."
        )
        # Exit here rather than returning a code: `fire` echoes a return value
        # to stdout, which would print a bare "0" into every green CI log.
        sys.exit(1)
    logger.info(f"checked {len(wanted)} derived `published:` field(s), all agree")


if __name__ == "__main__":
    fire.Fire(main)
