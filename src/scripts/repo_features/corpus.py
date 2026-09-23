# src/scripts/repo_features/corpus.py
"""What the record already holds, indexed for comparison (#291).

Two indexes, because the two extractors produce two kinds of thing. An arXiv
identifier is compared against the notes; a feature name is compared against
the practices, and that comparison is the one the `#287` pilot found is
easy to get wrong.

**Two matches, not one, because neither is sufficient alone.** The `#287`
pilot measured bodies: matching them made µP look like an FP8 practice
because it mentions FP8 once, and a masked-diffusion practice look like a
speculative-decoding one because it discusses draft models. Poor precision.

Restricting to titles and summaries has the opposite failure and it is just
as bad. `speculative decoding` finds nothing, though `SOTA-227` is *"Decode
with a draft model and an accept-reject rule"* — the practice is exactly
that and never uses the phrase. Poor recall.

So a body hit is a **candidate** and a subject hit is a **confirmation**, and
the run reports which is which. Collapsing them into one number would hide
whichever error the choice made, and the point of generating this rather than
grepping by hand is that the discarding becomes an artifact somebody can
look at twice.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml


def _frontmatter(path: Path) -> dict:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def held_arxiv_ids(root: Path) -> dict[str, str]:
    """Every arXiv identifier the reading list holds, to the note that holds
    it. The version suffix is dropped — `2306.00978v2` and `2306.00978` are
    one paper, and the repositories cite both spellings."""
    out: dict[str, str] = {}
    for p in sorted((root / "record" / "literature.d").glob("LIT-*.md")):
        raw = _frontmatter(p).get("arxiv")
        if raw:
            out[str(raw).split("v")[0].strip()] = p.stem
    return out


def practices(root: Path) -> dict[str, tuple[str, str]]:
    """Practice code to (subject, body), both lower-cased.

    The subject is title plus summary — what the practice is *about*. The
    body is everything else. They are returned apart because they answer
    different questions; see the module docstring."""
    out: dict[str, tuple[str, str]] = {}
    for p in sorted((root / "record" / "practices.d").glob("SOTA-*.md")):
        parts = p.read_text(encoding="utf-8").split("---", 2)
        if len(parts) < 3:
            continue
        try:
            m = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            continue
        subject = f"{m.get('title', '')} {m.get('summary', '')}".lower()
        out[p.stem] = (subject, parts[2].lower())
    return out


def matching(corpus: dict[str, tuple[str, str]],
             feature: str) -> tuple[list[str], list[str]]:
    """(confirmed, candidates) for one feature name.

    **confirmed** — the feature is in the practice's subject, so the practice
    is about it. **candidates** — it appears only in the body, which is a
    lead and is wrong most of the time.

    Word-boundary matching on the whole name. Short names are the known
    weakness (vLLM calls chunked prefill `CP`) and are left to the reader
    rather than filtered by a guessed length threshold: the run prints what
    matched, so a name too short to mean anything is visible as one."""
    rx = re.compile(rf"\b{re.escape(feature.lower())}\b")
    confirmed = sorted(c for c, (s, _) in corpus.items() if rx.search(s))
    candidates = sorted(c for c, (s, b) in corpus.items()
                        if not rx.search(s) and rx.search(b))
    return confirmed, candidates
