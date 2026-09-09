# src/scripts/audit/verify_arxiv.py
"""Check every LIT note's declared metadata against the arXiv API.

Reads `first_author:`, `title:` and `arxiv:` from each note's frontmatter and
compares them to what arXiv returns for that identifier.

What this catches: a name that belongs to nobody on the paper, an id that
resolves to nothing, a title that names a different paper. What it does NOT
catch, and the reason a clean run is not a clean bill of health: a note whose
identifier, title, author and year are all correct and mutually consistent
while its *body* describes some other paper. LIT-052 was exactly that, and
only reading the paper found it. See the curation entry of 2026-09-09.

    python -m src.scripts.audit.verify_arxiv
    python -m src.scripts.audit.verify_arxiv --record=record --json=out.json
"""

from __future__ import annotations

import difflib
import json
import re
import time
import urllib.request
from pathlib import Path

import fire
from loguru import logger

API = "https://export.arxiv.org/api/query"
BATCH = 40          # arXiv rejects much larger id_lists
PAUSE = 3.0         # the API's own guidance is one request every three seconds
TITLE_FLOOR = 0.72  # below this, two titles are different papers

# Corporate authors: arXiv renders these with the words in the other order
# ("Kimi Team" -> "Team Kimi"), so a surname check flags every one of them.
# They are not findings.
_TEAM = re.compile(r"\bteam\b", re.I)


def _frontmatter(text: str) -> str:
    parts = text.split("---\n")
    return parts[1] if len(parts) > 2 else ""


def _field(fm: str, name: str) -> str:
    m = re.search(rf"^{name}:\s*'?(.+?)'?\s*$", fm, re.M)
    return m.group(1).strip() if m else ""


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _fetch(ids: list[str]) -> dict[str, dict]:
    """Return {bare_arxiv_id: {title, authors}} for the ids given.

    Keyed by the id in the RESPONSE, never by position: arXiv does not return
    entries in id_list order, and pairing them positionally silently compares
    every note against a different paper.
    """
    url = f"{API}?id_list={','.join(ids)}&max_results={len(ids)}"
    with urllib.request.urlopen(url, timeout=60) as r:
        xml = r.read().decode("utf-8", "replace")
    out = {}
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        eid = re.search(r"<id>https?://arxiv\.org/abs/([^<]+)</id>", entry)
        if not eid:
            continue
        title = re.search(r"<title>(.*?)</title>", entry, re.S)
        out[eid.group(1).split("v")[0]] = {
            "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else "",
            "authors": re.findall(r"<author>\s*<name>([^<]+)</name>", entry),
        }
    return out


def main(record: str = "record", json_out: str | None = None) -> int:
    """Verify every note carrying an `arxiv:` id. Returns the finding count."""
    notes = []
    for path in sorted(Path(record, "literature.d").glob("LIT-*.md")):
        fm = _frontmatter(path.read_text())
        if arxiv := _field(fm, "arxiv"):
            notes.append(
                {
                    "code": path.stem,
                    "arxiv": arxiv,
                    "bare": arxiv.split("v")[0],
                    "first_author": _field(fm, "first_author"),
                    "title": _field(fm, "title"),
                }
            )
    logger.info(f"{len(notes)} notes carry an arxiv id")

    got: dict[str, dict] = {}
    for i in range(0, len(notes), BATCH):
        chunk = notes[i : i + BATCH]
        got |= _fetch([n["arxiv"] for n in chunk])
        logger.debug(f"{min(i + BATCH, len(notes))}/{len(notes)}")
        time.sleep(PAUSE)

    findings = []
    for n in notes:
        paper = got.get(n["bare"])
        if not paper:
            findings.append({**n, "kind": "unresolved"})
            continue

        declared = n["first_author"]
        surnames = [a.split()[-1].lower() for a in paper["authors"]]
        if declared and not _TEAM.search(declared) and declared.lower() not in surnames:
            findings.append(
                {**n, "kind": "author", "actual": paper["authors"][:3],
                 "paper": paper["title"]}
            )

        ratio = difflib.SequenceMatcher(
            None, _norm(n["title"]), _norm(paper["title"])
        ).ratio()
        if ratio < TITLE_FLOOR:
            findings.append(
                {**n, "kind": "title", "ratio": round(ratio, 2),
                 "paper": paper["title"]}
            )

    # Two notes on one identifier: usually already triaged by status, but
    # worth a periodic look.
    seen: dict[str, list[str]] = {}
    for n in notes:
        seen.setdefault(n["bare"], []).append(n["code"])
    duplicates = {k: v for k, v in seen.items() if len(v) > 1}

    for f in findings:
        if f["kind"] == "author":
            logger.warning(
                f"{f['code']}  first_author={f['first_author']!r} is not an author "
                f"of {f['arxiv']} ({', '.join(f['actual'])}) — {f['paper'][:60]}"
            )
        elif f["kind"] == "title":
            logger.warning(
                f"{f['code']}  title does not match {f['arxiv']} "
                f"(ratio {f['ratio']}) — arXiv says {f['paper'][:60]!r}"
            )
        else:
            logger.warning(f"{f['code']}  {f['arxiv']} resolves to nothing")
    for bare, codes in duplicates.items():
        logger.info(f"{bare} is held by {', '.join(codes)} — check their statuses")

    if json_out:
        Path(json_out).write_text(
            json.dumps({"findings": findings, "duplicates": duplicates}, indent=1)
        )

    logger.info(f"{len(findings)} finding(s), {len(duplicates)} duplicate id(s)")
    return len(findings)


if __name__ == "__main__":
    fire.Fire(main)
