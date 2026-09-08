---
status: Active
title: 'Generated views are committed on main only, and a pull request writes none'
version: 1
tags:
- record
- mechanism
date: '2026-09-08'
summary: >-
  Regenerating views on every pull request made two branches conflict on
  files neither had edited, and made a stacked branch re-conflict after each
  merge. Adopts luria's split shape ([LU-ADR-068](https://github.com/dmarx/luria/blob/main/record/decisions.d/ADR-068.md)): views on the default branch
  only, source repairs on the branch that authored them.
---

# ADR-tmphu321: Generated views are committed on main only, and a pull request writes none

## Context

`docs/` is generated. `luria index` rebuilds the practice and literature
indexes, the tag and status pages, the lineage page, the curation book, the
reports and the README badge region — 59 files — from the sources in
`record/`. Until now CI regenerated and committed them on **every** event,
pull requests included.

That is the wrong place for them, and the cost is not theoretical. In one
afternoon it produced:

- **Two branches conflicting on files neither had edited.** Batch A and batch
  B of [#56](https://github.com/dmarx/anthology-of-the-sota/issues/56) touched disjoint sources — four literature notes each, in
  different clusters — and conflicted on nineteen generated pages, because
  each had regenerated the same shared index.
- **The same conflict again after every merge.** A view is rewritten by the
  merge to `main`, so a branch that already resolved it resolves it again on
  the next rebase. The batch B branch hit it twice, and the second time also
  had to absorb `luria concretize` renaming the files the first merge had
  numbered.
- **A resolution procedure that is a ritual.** `git checkout --theirs docs/`,
  rerun `luria index`, re-stage, commit — mechanical, unreviewable, and
  performed on files whose correct content is a pure function of the sources
  anyway.

Nothing was ever *learned* from resolving one. The conflicts carried no
information, which is the tell that the file is in the wrong place rather
than that the process needs more care.

## Decision

Adopt the split luria uses on its own record ([LU-ADR-068](https://github.com/dmarx/luria/blob/main/record/decisions.d/ADR-068.md)), through the same
composite actions:

- **On a push to `main`** — `docs-generate` runs `luria concretize` and
  `luria index` with `views: "true"`, commits the regenerated views and the
  rendered README as the bot, and hands `docs-lint` the SHA it produced.
- **On a pull request** — `docs-check` runs the generate action with
  `views: "false"` and the lint action *in the same job*. Source repairs — a
  bare code linked, a journal entry's `created:` filled from its path — are
  committed onto the branch, where the review reads them. No view is written.

The asymmetry is the point, and it follows from what each kind of file is. A
**view is shared**: every branch would rewrite it, so two branches always
collide. A **repair is local**: it touches only what the branch itself
authored, so it belongs on the branch.

Contributors therefore run `luria index` locally — the reports are how you
read what the lint is about to say — and discard the result before
committing. `CLAUDE.md` says so.

## Alternatives considered

**Keep generating on PRs and merge more carefully.** This is what we were
doing. It scales with the square of the number of concurrent branches and
teaches nothing; the fourth time through the ritual is when it became clear
the file placement was the bug.

**Stop committing `docs/` at all and build it at publish time.** Cleaner in
principle, and rejected because the record is meant to be readable *in the
repository* —
<!-- inactive-ok-block: ADR-006 — Superseded, and named for the argument it
     made rather than for the pipeline that replaced it -->
[ADR-006](ADR-006.md) is about generating the registry from the record rather
than checking in a separate artefact, and the browsable view being present at
a commit is what makes a link into `docs/` stable. Views on `main` keeps
that; views nowhere does not.

**`.gitattributes` with a merge driver for `docs/`.** Would silence the
conflicts without moving anything, at the cost of a piece of custom
merge machinery every contributor has to have configured locally. It treats
the symptom, and it fails open — an unconfigured checkout silently gets the
old behaviour.

## Consequences

- A pull request's diff is now only the sources. That is a readability win
  nobody asked for: the batch A PR was 39 changed files, of which 29 were
  regenerated pages.
- `main` is the only branch whose `docs/` is current. A link into `docs/`
  from a branch may point at a stale page until the merge lands.
- The lint on a pull request reads sources rather than checking a view it
  declined to build, so the staleness check is meaningful in exactly one
  place — the push — which is where a generator that failed to run is the
  thing you want to hear about.
