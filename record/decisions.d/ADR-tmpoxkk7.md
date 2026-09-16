---
status: Proposed
title: 'A document may carry more than one topic; the first is the primary'
version: 1
tags:
- taxonomy
- record
date: '2026-09-16'
summary: >-
  The topic group moves from `exactly-one` to `any` on all four schemes. A
  document is often about two of the thirteen — a positional-encoding scheme
  is also an attention technique — and under `exactly-one` recording the
  second meant deleting the first, which is what the retagging pass in [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140)
  did to eleven documents. `primary_topic` still derives `{tags[0]}`, so the
  primary is still exactly one value and every chain invariant compares one
  against one: the unbound-lineage report is byte-identical before and after.
  The cost is that tag ORDER becomes load-bearing where it was conventional.
---

# ADR-tmpoxkk7: A document may carry more than one topic; the first is the primary

## Context

The retagging pass in [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140) moved fifteen documents to the topic that names
their claim. Reviewed, the objection was: *"you've replaced a bunch of tags
where you just needed to add an additional tag. the old tags still seem
applicable in the cases I reviewed."*

That is right, and re-reading them it is right about most of them. `LIT-192`
(Positional Interpolation) and `LIT-193` (YaRN) moved from
`attention-techniques` to `representation-and-encoding` — but
`attention-techniques` names *context length* in its own blurb, and both
papers are context-extension papers. `LIT-208` proposes a hybrid **attention**
strategy; its title says so. `LIT-045` and `LIT-048` describe components of
the architecture as well as schemes for encoding position. In each case the
new topic is better and the old one was not wrong.

**It could not have been additive.** `fields.tags.groups.primary_topic`
required `exactly-one` of the thirteen, so a second topic is a hard lint
violation:

    `primary_topic` wants exactly one of … — has model-architecture,
    representation-and-encoding

So the pass had one move available, and it took it. That is the same corner
`luria.yaml` already records from [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101) — *"the only move available under
`exactly-one` — it satisfied the check rather than answering it"* — reached
from the other side: there the constraint forced an incidental secondary tag
in, here it forced a true topic out.

## Decision

**`require: exactly-one` becomes `require: any` on the topic group, in all
four schemes that declare it** — `LIT`, `SOTA`, `NOTE`, `THEORY`.

**The primary topic is unchanged in meaning: it is the first topic listed.**
`primary_topic` already derives `{tags[0]}`, so nothing downstream moves. The
indexes still file a document under one topic, and the chain invariants still
compare one scalar against one scalar — `invariants.held()` reads
`primary_topic`, not `tags`. Verified: with the group relaxed and a second
topic added, `docs/reports/unbound-lineage.md` is byte-identical at **24
unbound relations and 10 unbound lines**.

That last point is the one that makes this safe. The alternative anybody would
reach for — put the invariant on `tags` and let a shared secondary bind a
relation — is the thing `luria.yaml` rejects by name: *"any shared tag is too
weak to carry it — two practices bound by an incidental label read as bound
when nothing about their subject matter is."* This decision does not touch
that. It widens what a document may *say*, not what a relation may *assert*.

**Eleven of [#140](https://github.com/dmarx/anthology-of-the-sota/issues/140)'s fifteen get their old topic back as a secondary**, plus
`NOTE-028` following its paper: the eight positional-encoding papers,
`LIT-211`, `SOTA-098` and `SOTA-099`.

**Four stay replacements, because the old topic was not applicable:**

- `SOTA-060` — an initialization rule for stability, filed
  `distributed-optimization` because its source is a Megatron paper. The claim
  is not about distribution.
- `SOTA-092`, `SOTA-093`, `SOTA-094` — three claims about batch size, filed
  `model-architecture` because their source is a model report. A claim about
  sample efficiency is not about architecture.

Those four are the cases where the old tag named *where the claim was found*
rather than what it is about, which is the filing error [ADR-026](ADR-026.md)'s rule is
against. Keeping them would preserve a mistake, not information.

## Consequences

**Tag order is now load-bearing.** Under `exactly-one`, reordering `tags:`
could not change `primary_topic` while only one entry was a topic. Under
`any`, moving the second topic to the front silently retags the document —
and nothing checks it. The convention was already unguarded (a free-form tag
listed first would always have produced a wrong `primary_topic`) and it holds
in all 596 documents today, measured. But the ways to break it just got more
plausible, and `LU-#229` is the upstream ask for a guard.

**Documents will appear under more than one topic in the generated views.**
That is the point — a reader looking for context extension under
`attention-techniques` will now find YaRN there — and it makes the per-topic
pages less of a partition than they were.

**`exactly-one` was load-bearing for one thing and is no longer.** [ADR-003](ADR-003.md)
introduced it and [ADR-026](ADR-026.md) reaffirmed it while merging the two vocabularies,
and in both the argument was about the vocabulary being *shared and small*,
not about a document having only one subject. Nothing in either turns on the
cardinality. This decision is filed `Proposed` because that reading should be
checked by someone who was there.

**It does not settle the cases where a second topic would be a dodge.** The
flash-attention pair (`SOTA-085` / `SOTA-161`) is unbound because a technique
and its numerical-stability fix are genuinely different kinds of claim, and
giving both an `attention-techniques` secondary would now be *possible* and
still wrong — it would bind the edge without answering it. The invariant
comparing `primary_topic` is what keeps that honest, which is why this
decision leaves it alone.

## Alternatives considered

**Leave the replacements as they are.** They discard a true statement about
eleven documents, and the review objected to exactly that.

**Keep `exactly-one` and record the old topic in `keywords:`.** Keywords are
the paper's own subject words, not the record's filing, and nothing indexes
them as topics. It would hide the fact rather than carry it.

**Move the chain invariant to `tags`.** The obvious follow-on and explicitly
not taken: a shared incidental tag would bind relations that share nothing
about their subject, which is the failure `luria.yaml` documents and the
reason the invariant moved to `primary_topic` in the first place.

**`at-most-one`.** The other available rule, and it permits zero topics, which
is worse than what we have — every document should be about something.
