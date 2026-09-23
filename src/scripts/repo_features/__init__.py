# src/scripts/repo_features/__init__.py
"""What the big repositories implement, diffed against the record (#291).

A repository that ships a technique is evidence about `consensus` and nothing
else (ADR-058, #288). This package produces the *observation* half of that
decision: what each repository implemented, at a ref it can name, and what
changed since the last run. The judgement half stays in `consensus_note`,
written by a person.

Four steps, one module each:

    refs     resolve a repo to an exact commit, and fetch a file at it
    extract  pull a feature list out of what was fetched
    corpus   index what the record already holds
    diff     new / gone / unmatched, against the last run's lockfile
"""
# inactive-ok-file: ADR-058 — Proposed, and it is the decision this module
# implements rather than one it relies on.

