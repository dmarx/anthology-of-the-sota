---
status: Proposed
title: 'Turn the enforcement dial on the two checks that bind a document to its paper'
version: 1
tags:
- mechanism
date: '2026-09-16'
summary: >-
  `lint.fail_on` has been empty since the record was built, so every check is
  advice. `source-mismatch` and `source-unchecked` go into it — the only two
  that verify a document is about the paper it names, both at zero today, and
  between them the check that would have failed the import in [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) instead of
  printing a clean run. Recorded alongside a check that was proposed and
  rejected on measurement: an invariant on `source:` asserting that a practice
  shares its paper's topic, which reports 73 edges across 64 practices and is
  mostly the record doing what it decided to do.
---

# ADR-tmpme6k8: Turn the enforcement dial on the two checks that bind a document to its paper

## Context

The unbound-lineage pass found fifteen mis-filed documents and summarised
eleven of them as *a claim inherits the topic of the document it was extracted
from*. That reads like a rule a machine could enforce, and the obvious
mechanism was already in the config surface: `chains` take an `invariant`, and
`source:` is a declared reference, so a chain over it would report every
practice whose topic differs from its paper's — no upstream change needed.

Three measurements, in the order they were taken.

**The summary does not survive measurement.** Of 220 practices that name a
source, **167 — 76% — already share their source's topic.** That is the
ordinary case: an Adam practice sourced to the Adam paper is both
`training-optimization`, and correctly. Of the six practices retagged in the
lineage pass, four had inherited their source's topic and **two had not** —
`SOTA-098` and `SOTA-099` were wrong in the other direction. "Inherits its
source's topic" describes four documents, not a defect.

**The invariant was already measured and rejected upstream, on this record.**
`luria/invariants.py` says so in its own docstring:

> Measured on the record this was built for, running the check over `source:`
> — which joins a practice to its paper across two vocabularies that a
> decision had deliberately separated — makes findings of 48 of 235 edges, and
> every one of them is a cross-domain citation the record was changed to
> permit. A check that fires on a project for doing the thing it decided to do
> is worse than no check.

**Its premise has since changed, and the conclusion survives anyway.** That
measurement was taken when the practice registry had seven topics and the
reading list thirteen; [ADR-026](ADR-026.md) made them one vocabulary of thirteen, so the
mechanical cause of those 48 is gone. Re-measured today the check reports **73
unbound edges across 64 practices** — worse, not better. The largest single
crossing is eight practices in `adaptation-and-tuning` sourced to papers in
`analysis-and-evaluation`, which is the evolution-strategies line drawing
recommendations from papers that measure rather than recommend. That is the
record working correctly, and it is the same structural fact the
unbound-lineage pass in [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140) names: `analysis-and-evaluation` is a kind,
not a subject, so it unbinds any line that grows an analysis paper. (That
pass's own ADR is unmerged as this is written, which is why it is cited by
pull request rather than by code.)

So the answer to *can this be enforced in config* is **no, and it should not
be** — but the question pointed at a dial that is genuinely off.

## Decision

**`lint.fail_on` gains `source-mismatch` and `source-unchecked`.**

The dial has been `[]` since the record was built, which means every finding
the lint produces is advice. These two are the only checks that answer *is
this document about the paper it names*, which is the question the record's
first design principle rests on — a citation nothing can follow is a string.

- **`source-mismatch`** compares the recorded title against what the
  identifier actually serves, reading the committed lockfile so it costs no
  network. Verified on this branch: retitle `LIT-045` to a different paper's
  title and the lint reports *"`arxiv: 2104.09864` resolves to 'RoFormer…',
  not 'A Mean Field View…'"* and exits 1.
- **`source-unchecked`** is the other half and the one that matters for new
  work: it fires when nothing has ever verified an identifier and upstream
  could not be reached. Under `network: auto` the lint resolves an unknown
  identifier live, so the normal path for a newly filed paper is that it gets
  checked and pinned during the contribution that files it. Also verified:
  a freshly minted note carrying `arxiv: 1901.09321` under a title that is not
  Fixup Initialization's fails the run.

**Both are at zero today**, which is the precondition. A dial turned on over
existing findings fails the next contributor for somebody else's backlog, and
the seven `retired-citations` and four `legacy-spellings` currently open are
exactly that — they stay advice until someone clears them.

## Consequences

**[#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) would have failed instead of merging.** That import filed three
readings against identifiers belonging to other papers — `1805.01361` recorded
as Mei, Montanari and Nguyen when it is a hyperspectral-regression paper,
`1906.08632` under a different Goldt paper's title, `2102.11742` under a title
belonging to nothing. All three are title-versus-identifier disagreements,
which is precisely `source-mismatch`. They were caught by a script written by
hand for that contribution; the lint printed a clean run beside it.

**Filing a paper now includes resolving its identifier.** In practice the lint
does it, because `network: auto` asks about what it does not know and writes
the answer into `remotes.lock.json`. The contributor's obligation is to commit
the lockfile, which the record already does.

**A network outage can now fail a contribution that adds a new paper.** This
is the real cost and it is narrow: every identifier already in the record is
pinned, so an outage only affects a contribution introducing one, and the
remedy — resolve locally, commit the lockfile — is in the author's hands. The
alternative is a green run that means "nobody could check" and is
indistinguishable from one that means "checked".

**It does not cover the defect [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) actually shipped.** Sixty-seven duplicate
notes, each a second document for a paper the record already held, with
correct titles and correct identifiers. Nothing in luria's finding vocabulary
is about two documents claiming one identifier, and no config setting produces
it. That one is upstream, and it is filed as such rather than papered over
here.

## Alternatives considered

**A chain over `source:` with `invariant: primary_topic`.** The measurement
above: 73 edges, 64 practices, mostly correct. Rejected on the same grounds
luria rejected it, for a different reason than luria had.

**`network: require`.** Makes not being able to ask a finding on every run,
so a green CI run means every reference was verified rather than remembered.
Stronger and tempting, and it converts any arXiv outage into a red build for
contributions that touch nothing. `auto` plus the two failable classes buys
most of it and fails only where a new citation is actually unverified.

**Promote more classes while the dial is being opened.** `retired-citations`
and `legacy-spellings` have open findings; promoting them would fail the next
contribution for a pre-existing backlog. `pending-documents` counts undecided
ADRs, which is a fact about deliberation rather than a defect. The dial is
opened on the two that are clean and load-bearing, and the rest stays advice
until someone clears it deliberately.
