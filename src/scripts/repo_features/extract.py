# src/scripts/repo_features/extract.py
"""Turn a fetched index file into a list of named things (#291).

Two extractors, because the repositories answer two different questions and
`#183` turns on not confusing them.

`arxiv_ids` reads a **catalogue** — x-transformers, k-diffusion — where the
README cites the paper behind each implemented feature. What comes out is
evidence that a technique *exists*, which is a reading list.

`feature_names` reads an **adoption** index — vLLM's compatibility matrix,
diffusers' scheduler exports — where presence means people use the thing.
What comes out is evidence about `consensus`.

Neither is a parser for a format; both are deliberately loose readers of a
shape that will drift. A missed row costs a candidate, and the run says how
many it found so a drop is visible.
"""

from __future__ import annotations

import re

# `arxiv.org/abs/2306.00978`, `arxiv.org/pdf/2306.00978v2` and the bare
# `eprint = {2306.00978}` a bibtex block carries. Old-style IDs
# (`cs/0501001`) are out: nothing in these repositories cites one, and
# admitting the shape would match version numbers in prose.
_ARXIV = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|eprint\s*=\s*[{\"]?)"
                    r"(\d{4}\.\d{4,5})")

# A markdown table's first cell, which is where every adoption index this
# reads puts the feature's name: `| [LoRA](lora.md) | ... |`. The link is
# unwrapped because the name is the useful part — it is what a practitioner
# would search for.
_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_ABBR = re.compile(r"<abbr[^>]*title=\"([^\"]+)\"[^>]*>.*?</abbr>", re.S)
# A quoted CamelCase name anywhere in an export table. Not anchored to its
# own line, because the real shape is not one name per line — `diffusers`
# writes `_import_structure["scheduling_ddim"] = ["DDIMScheduler"]`, and an
# anchored pattern read that file as exporting nothing at all. Loose on
# purpose, and narrowed by the caller's suffix rather than by the pattern.
_EXPORT = re.compile(r"\"([A-Z][A-Za-z0-9_]+)\"")

# Stands in for a table's `|---|` rule while rows are collected,
# so the header can be dropped by position rather than by name.
_SEPARATOR = "\x00"


def arxiv_ids(text: str) -> list[str]:
    """Every arXiv identifier cited, de-duplicated, in sorted order.

    Sorted rather than in document order on purpose: the output is compared
    against the previous run, and a README that reorders its sections would
    otherwise read as a wholesale change."""
    return sorted(set(_ARXIV.findall(text)))


def feature_names(text: str, index: int | None = None) -> list[str]:
    """Every feature named in a markdown table's first column.

    A table's header is the row above its `|---|` separator, whatever it is
    called — `Feature` on one page and `Implementation` on the next — so it
    is dropped by position rather than by matching a word. Everything else is
    kept, including names this record will not recognise, because deciding
    what counts is the judgement pass's job and not this function's.

    `index` picks one table, 0-based. One file routinely holds several with
    different meanings — vLLM's quantization page has a hardware-support
    matrix *and* an API reference, and reading both put `get_name()` and
    `from_config(config)` in a list of techniques. Selecting by position is
    the manifest's job, because only a person can say which table means
    something."""
    tables: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        m = _ROW.match(line)
        if not m:
            current = None                      # prose or a blank ends a table
            continue
        if current is None:
            current = []
            tables.append(current)
        cell = _ABBR.sub(r"\1", m.group(1))
        cell = _LINK.sub(r"\1", cell).strip()
        if set(cell) <= set("- :"):             # the separator row
            current.append(_SEPARATOR)
            continue
        current.append(cell)

    out: list[str] = []
    for n, rows in enumerate(tables):
        if index is not None and n != index:
            continue
        if _SEPARATOR in rows:                  # drop the header and the rule
            rows = rows[rows.index(_SEPARATOR) + 1:]
        for cell in rows:
            if cell != _SEPARATOR and re.search(r"[A-Za-z]", cell) \
                    and cell not in out:
                out.append(cell)
    return out


def exported_names(text: str, suffix: str = "") -> list[str]:
    """Names a Python module exports, optionally only those ending `suffix`.

    `diffusers/schedulers/__init__.py` lists every scheduler it ships as a
    quoted string in a lazy-import table; `suffix="Scheduler"` is what turns
    that into the sampler list.

    Supply the suffix. Without one this returns every quoted CamelCase token
    in the file, which for a real module is mostly submodule plumbing — the
    pattern is deliberately loose because the file shapes differ, and the
    suffix is where the narrowing belongs."""
    found = {n for n in _EXPORT.findall(text) if n.endswith(suffix)}
    # `DDIMScheduler` is a class; `DDIM` is the technique, and the technique
    # is what the record and a practitioner both call it. Stripping the
    # suffix is what makes the comparison against the record mean anything.
    width = len(suffix)
    return sorted({n[:-width] if width and n != suffix else n for n in found})
