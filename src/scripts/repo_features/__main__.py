# src/scripts/repo_features/__main__.py
"""`python -m src.scripts.repo_features` — one pass, reported (#291).

    python -m src.scripts.repo_features                # read, report, lock
    python -m src.scripts.repo_features --write_lock=False   # dry run

Writes `docs/reports/repo-features.md`, which is a view and lands on the
default branch only (ADR-018), and `repo-features.lock.json`, which is a
source and is committed on the branch that ran it — the same split the
arXiv lockfile already uses.
"""

from __future__ import annotations

from pathlib import Path

import fire
from loguru import logger

from . import corpus, report, run


def main(root: str = ".", config: str | None = None,
         write_lock: bool = True) -> None:
    here = Path(root)
    observed = run.observe(Path(config) if config else None)
    deltas = run.changes(observed, run.load_lock(here))

    practices = corpus.practices(here)
    held = corpus.held_arxiv_ids(here)
    matches: dict[str, dict] = {}
    for name, obs in observed.items():
        if obs["kind"] == "catalogue":
            matches[name] = {i: held.get(i, "") for i in obs["items"]}
        else:
            matches[name] = {i: corpus.matching(practices, i)
                             for i in obs["items"]}

    out = here / "docs" / "reports" / "repo-features.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report.render(observed, deltas, matches), encoding="utf-8")
    logger.info(f"wrote {out}")
    if write_lock:
        logger.info(f"wrote {run.write_lock(here, observed)}")


if __name__ == "__main__":
    fire.Fire(main)
