# src/scripts/audit/reading_time.py
"""Rank the papers-feed reading tracker by cumulative reading time.

The earlier worklist ranked the feed by revisits — the number of reading
sessions. This ranks it by the sum of `duration_seconds` over those sessions,
which is active time: the tracker reports `idle_seconds` separately and
`duration_seconds` already excludes it. The two rankings disagree most in the
two-to-four-session band, where one long read counts for little by revisits.

Only works the record does not hold are printed. "Held" means a LIT note
carries the arXiv id or the title; an id merely *mentioned* in a journal entry
is not held, because declining a paper in prose is not filing it.

What this does NOT do: say whether a paper belongs. Time measures attention,
not relevance — the single largest total in the feed is a planetary-science
paper. Every row still needs a disposition from someone who read the title.
See the curation entry of 2026-09-25.

    python -m src.scripts.audit.reading_time
    python -m src.scripts.audit.reading_time --min_seconds=300 --json=out.json
"""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

import fire
from loguru import logger

SNAPSHOT = "https://raw.githubusercontent.com/dmarx/papers-feed/refs/heads/main/data/papers/gh-store-snapshot.json"

_ARXIV_URL = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5}|[a-z-]+/\d{7})")
_ARXIV_ID = re.compile(r"^(?:arxiv\.)?(\d{4}\.\d{4,5}|[a-z-]+/\d{7})$")
# Titles the feed records when it could not read one: a Cloudflare interstitial,
# or the hash of the URL. Keying on them would merge unrelated papers.
_NO_TITLE = re.compile(r"^(just a moment|[0-9a-f]{6,8}$|\d{4}\.\d{4,5}$)", re.I)


def _norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower().removeprefix("title:"))[:60]


@dataclass
class Work:
    key: str
    title: str = ""
    url: str = ""
    arxiv: str | None = None
    seconds: int = 0
    sessions: int = 0
    feed_ids: list[str] = field(default_factory=list)


def _arxiv_of(feed_id: str, url: str) -> str | None:
    bare = re.sub(r"^arxiv[.:]", "", feed_id)
    if m := _ARXIV_ID.match(bare):
        return m.group(1)
    if m := _ARXIV_URL.search(url):
        return m.group(1)
    return None


def aggregate(objects: dict) -> list[Work]:
    """Merge every feed key for one paper into a work, ranked by active seconds."""
    meta = {k.split(":", 1)[1]: v["data"] for k, v in objects.items() if k.startswith("paper:")}
    works: dict[str, Work] = {}
    for key, obj in objects.items():
        if not key.startswith("interactions:"):
            continue
        feed_id = key.split(":", 1)[1]
        sessions = [i["data"] for i in obj["data"]["interactions"] if i["type"] == "reading_session"]
        if not sessions:
            continue
        m = meta.get(feed_id, {})
        title = " ".join((m.get("title") or "").split())
        url = m.get("url") or ""
        arxiv = _arxiv_of(feed_id, url)
        titled = bool(title) and not _NO_TITLE.match(title)
        wkey = f"arxiv:{arxiv}" if arxiv else f"title:{_norm_title(title)}" if titled else f"id:{feed_id}"
        w = works.setdefault(wkey, Work(key=wkey, arxiv=arxiv))
        if titled and len(title) > len(w.title):
            w.title = title
        w.url = w.url or url
        w.seconds += sum(s.get("duration_seconds", 0) for s in sessions)
        w.sessions += len(sessions)
        w.feed_ids.append(feed_id)
    # A title-keyed entry whose title matches an arXiv-keyed work is the same paper.
    by_title = {_norm_title(w.title): w for w in works.values() if w.arxiv and w.title}
    for wkey in [k for k in works if k.startswith("title:")]:
        if (target := by_title.get(wkey.removeprefix("title:"))) is not None:
            dup = works.pop(wkey)
            target.seconds += dup.seconds
            target.sessions += dup.sessions
            target.feed_ids += dup.feed_ids
    return sorted(works.values(), key=lambda w: -w.seconds)


def unheld(works: list[Work], ids: set[str], titles: set[str]) -> list[Work]:
    """Drop works a LIT note already carries, by arXiv id or by title."""
    held_titles = {_norm_title(t) for t in titles}
    return [
        w for w in works
        if not (w.arxiv in ids or any(i in ids for i in w.feed_ids) or _norm_title(w.title) in held_titles)
    ]


def held(record: Path) -> tuple[set[str], set[str]]:
    """Every arXiv id and title carried by a LIT note's frontmatter."""
    ids, titles = set(), set()
    for note in (record / "literature.d").glob("LIT-*.md"):
        text = note.read_text()
        if m := re.search(r"^arxiv:\s*['\"]?([^'\"\s]+)", text, re.M):
            ids.add(m.group(1))
        if m := re.search(r"^title:\s*['\"]?(.*?)['\"]?\s*$", text, re.M):
            titles.add(m.group(1))
    return ids, titles


def main(snapshot: str = SNAPSHOT, record: str = "record", min_seconds: int = 600, json_out: str | None = None):
    """Print unheld works with at least `min_seconds` of active reading time."""
    if snapshot.startswith("http"):
        logger.info(f"fetching {snapshot}")
        with urllib.request.urlopen(snapshot) as r:
            objects = json.load(r)["objects"]
    else:
        objects = json.loads(Path(snapshot).read_text())["objects"]
    works = aggregate(objects)
    ids, titles = held(Path(record))
    by_sessions = sorted(works, key=lambda w: (-w.sessions, -w.seconds))
    revisit_rank = {w.key: i + 1 for i, w in enumerate(by_sessions)}
    rows = [w for w in unheld(works, ids, titles) if w.seconds >= min_seconds]
    logger.info(f"{len(works)} works, {len(works) - len(unheld(works, ids, titles))} held, {len(rows)} unheld >= {min_seconds}s")
    for w in rows:
        print(f"{w.seconds:6d}s {w.sessions:3d}x rev#{revisit_rank[w.key]:<5d} {w.key[:30]:30s} {(w.title or w.url)[:80]}")
    if json_out:
        Path(json_out).write_text(json.dumps([asdict(w) | {"revisit_rank": revisit_rank[w.key]} for w in rows], indent=1))


if __name__ == "__main__":
    fire.Fire(main)
