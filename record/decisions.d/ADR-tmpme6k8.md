---
status: Proposed
title: 'Turn the enforcement dial on the two checks that bind a document to its paper'
version: 1
tags:
- mechanism
date: '2026-09-16'
summary: >-
  `lint.fail_on` has been empty since the record was built, so every check is
  advice. `source-mismatch` goes into it — the one check that verifies a
  document is about the paper it names, at zero today, and the check that
  would have failed the import in [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) instead of printing a clean run.
  `source-unchecked` is deliberately left out: its only failure mode is an
  upstream outage, which a contributor cannot act on. Recorded alongside a
  check proposed and rejected on measurement: an invariant on `source:`
  asserting a practice shares its paper's topic, which reports 73 edges
  across 64 practices and is mostly the record doing what it decided to do.
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

**`lint.fail_on` gains `source-mismatch`, and only that.**

The dial has been `[]` since the record was built, which means every finding
the lint produces is advice. `source-mismatch` is the check that answers *is
this document about the paper it names* — the question the record's first
design principle rests on, because a citation nothing can follow is a string.
It compares the recorded title against what the identifier actually serves,
reading the committed lockfile so it costs no network.

Verified on this branch rather than assumed: retitle `LIT-045` to a different
paper's title and the lint reports *"`arxiv: 2104.09864` resolves to
'RoFormer…', not 'A Mean Field View…'"* and exits 1. A freshly minted note
whose identifier does not match its title fails the same way, with the
identifier resolved live and pinned in the same run.

**`source-unchecked` is deliberately not promoted.** It is the natural
companion — it fires when nothing has ever verified an identifier and
upstream could not be reached — and promoting it would convert an arXiv
outage into a red build for a contribution that did nothing wrong. A failure
a contributor cannot act on is one they learn to route around, and a dial
people route around is worse than a dial that is off. It stays a warning,
which is the right volume for "nobody could check this".

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

**No new way for CI to fail on something outside the contributor's control.**
That was the cost of the version of this decision that also promoted
`source-unchecked`, and it is why that half was cut. `source-mismatch` reads
the committed lockfile, so it fails only on a disagreement that is in the
diff — which is a thing the author can fix.

**It does not cover the defect [#138](https://github.com/dmarx/anthology-of-the-sota/issues/138) actually shipped.** Sixty-seven duplicate
notes, each a second document for a paper the record already held, with
correct titles and correct identifiers and a green lint. Nothing in luria's
finding vocabulary asks whether two documents resolve to the same place, and
no config setting produces it.

That is **[LU-#165](https://github.com/dmarx/luria/issues/165)** upstream — *"Two documents can name the same source and
nothing notices: add a `duplicate-source` finding and a `luria merge`"* —
which reaches the same conclusion from a two-document collision and goes
further, asking for a command that resolves one by rewriting references,
appending the old code to `formerly:`, and retiring rather than deleting the
loser. This record's contribution to it is scale and a second root cause: 67
instances at once, from a regeneration that used `git clean -fd` between two
generations of the same corpus while the first was already tracked.

## Alternatives considered

**A chain over `source:` with `invariant: primary_topic`.** The measurement
above: 73 edges, 64 practices, mostly correct. Rejected on the same grounds
luria rejected it, for a different reason than luria had.

**`network: require`, or promoting `source-unchecked`.** Both make "nobody
could check" a failure, so a green run would mean every reference was
verified rather than remembered. Both were in the first draft of this
decision and both are rejected for the same reason: the failure they add is
an upstream outage, and a contributor who did nothing wrong cannot act on it.
The escape hatch would be to ignore the dial, which costs the dial more than
the case is worth. `source-unchecked` stays a warning, which is the right
volume for it.

**Promote more classes while the dial is being opened.** `retired-citations`
and `legacy-spellings` have open findings; promoting them would fail the next
contribution for a pre-existing backlog. `pending-documents` counts undecided
ADRs, which is a fact about deliberation rather than a defect. The dial is
opened on the one class that is clean and load-bearing, and the rest stays
advice until someone clears it deliberately.
