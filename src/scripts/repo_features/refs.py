# src/scripts/repo_features/refs.py
"""Resolve a repository to an exact commit, and read a file at it (#291).

Pinning is the whole reason this module exists. `ADR-058` requires the
observation to name what it read, and the `#287` pilot demonstrated the
failure by fetching from `main` and being unable afterwards to say which
`main`. A report that cannot be reproduced is a claim nobody can check.

The GitHub API is unreachable from a session (403 through the proxy), which
is what made pinning look hard. It is not: `git ls-remote` is plain git over
HTTPS and answers with the SHA directly, and `raw.githubusercontent.com`
serves any ref including a full SHA.
"""
# inactive-ok-file: ADR-058 — Proposed, and it is the decision this module
# implements rather than one it relies on.


from __future__ import annotations

import subprocess
import urllib.request

from loguru import logger

RAW = "https://raw.githubusercontent.com/{repo}/{ref}/{path}"
TIMEOUT = 60


def resolve(repo: str, ref: str = "HEAD") -> str:
    """The commit `ref` names in `repo`, as a full SHA.

    A SHA passed in comes back unchanged, so a manifest that already pins can
    be re-resolved without a network round trip and without special-casing at
    the call site."""
    if len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
        return ref
    out = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{repo}", ref],
        capture_output=True, text=True, timeout=TIMEOUT, check=True).stdout
    if not out.strip():
        raise LookupError(f"{repo}: no ref {ref!r}")
    sha = out.split()[0]
    logger.debug(f"{repo}@{ref} -> {sha}")
    return sha


def read(repo: str, sha: str, path: str) -> str:
    """One file from a repository at an exact commit.

    Raises rather than returning empty on a missing path: an index file that
    moved is a manifest that needs editing, and a run that silently extracted
    nothing from it would report the repository as having lost every feature
    it has."""
    url = RAW.format(repo=repo, ref=sha, path=path)
    with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
        if r.status != 200:
            raise LookupError(f"{url}: HTTP {r.status}")
        return r.read().decode("utf-8")
