# src/scripts/repo_features/run.py
"""One pass: resolve, fetch, extract, diff against the last run (#291).

The lockfile is what makes this more than a grep. Without it a run says what
each repository implements today; with it a run says what **changed**, and the
`gone` column is the signal nothing else in this project can produce. Per
`ADR-058` a disappearance means read this again, never lower the consensus —
a library can narrow its scope without the field changing its mind.
"""
# inactive-ok-file: ADR-058 — Proposed, and it is the decision this module
# implements rather than one it relies on.


from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from loguru import logger
from omegaconf import OmegaConf

from . import corpus, extract, refs

LOCK = "repo-features.lock.json"
CONFIG = Path(__file__).with_name("repos.yaml")


def _extract(kind: str, text: str) -> list[str]:
    if kind == "arxiv":
        return extract.arxiv_ids(text)
    if kind == "table" or kind.startswith("table:"):
        _, _, which = kind.partition(":")
        return extract.feature_names(text, int(which) if which else None)
    if kind.startswith("exports"):
        _, _, suffix = kind.partition(":")
        return extract.exported_names(text, suffix)
    raise ValueError(f"unknown extractor {kind!r}")


def observe(config: Path | None = None) -> dict:
    """Read every repository at a resolved commit. Network, no record."""
    cfg = OmegaConf.load(config or CONFIG)
    out: dict[str, dict] = {}
    for name, spec in OmegaConf.to_container(cfg)["repos"].items():
        sha = refs.resolve(spec["repo"], spec.get("ref", "HEAD"))
        found: list[str] = []
        for path, kind in spec["files"].items():
            found += _extract(kind, refs.read(spec["repo"], sha, path))
        logger.info(f"{name}@{sha[:8]}: {len(set(found))} item(s)")
        out[name] = {"repo": spec["repo"], "kind": spec["kind"],
                     "sha": sha, "items": sorted(set(found))}
    return out


def changes(now: dict, before: dict) -> dict[str, dict[str, list[str]]]:
    """Per repository, what appeared and what disappeared since the lockfile.

    A repository absent from `before` reports everything as new, which is
    right — a first run has seen nothing before — and is distinguished from a
    quiet run by the counts rather than by a flag."""
    out = {}
    for name, obs in now.items():
        was = set((before.get(name) or {}).get("items", []))
        has = set(obs["items"])
        out[name] = {"new": sorted(has - was), "gone": sorted(was - has)}
    return out


def load_lock(root: Path) -> dict:
    path = root / LOCK
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("repos", {})


def write_lock(root: Path, observed: dict) -> Path:
    path = root / LOCK
    path.write_text(json.dumps(
        {"generated": dt.datetime.now(dt.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
         "repos": observed}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return path
