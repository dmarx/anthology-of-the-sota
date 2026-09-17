---
status: Proposed
title: 'Evidence from outside the machine-learning literature, and what has to be true for the record to hold it'
version: 1
tags:
- record
date: '2026-09-17'
summary: >-
  A psycholinguistics paper arrived with a real measurement, no model, and no
  recommendation. The record already holds physics, control theory and pure
  mathematics, so "outside CS" is not the boundary — but every one of those is
  cited by work the record files, which is the trigger [ADR-032](ADR-032.md) supplies, and
  this is not. Proposed: such work is admissible as LIT when it measures
  something a topic's practices presuppose, and the note must say what it does
  NOT license. Rejected: declining it silently, inventing a practice for it,
  and adding a topic to hold it.
---

# ADR-NNN: Evidence from outside the machine-learning literature, and what has to be true for the record to hold it

## Context

[LIT-tmp5l55q](../literature.d/LIT-tmp5l55q.md) is a paper in *Language* about
English syntax. Four preregistered surveys, 755 participants, a corpus study,
and not one sentence about a machine. It was filed on request, and filing it
turned up a boundary nobody here has drawn.

**"Outside computer science" is not the boundary, and the corpus already says
so.** The record holds Physical Review, IEEE Transactions on Automatic
Control, SIAM, and a 1963 AMS proceedings — 27 notes carry no arXiv identifier
at all. Nobody argued about those, because each is machinery that ML work
runs on and each is cited by work the record files.

**That citation is the actual trigger, and this paper does not meet it.**
[ADR-032](ADR-032.md) admitted benchmarks, model reports and infrastructure and was explicit
about the limit: "the trigger for filing remains the one the sweep supplies:
**something in the record cites it**." Nothing here cites Goldberg and Shirtz.
On the letter of [ADR-032](ADR-032.md) this paper is not admissible, and it is also not the
kind of document [ADR-032](ADR-032.md) was about.

**But declining it is the move [DP-009](../../docs/design-principles.md#dp-9) names as self-confirming.** That
principle says a claim with no category is evidence about the vocabulary until
someone shows otherwise, and that showing otherwise "means an argument about
the *kind of claim* — not a shrug at the absence of a slot." The argument
available here is real but narrow: the anthology advises on machines, and a
measurement of human interpretation is not a measurement of one.

**The thing that makes it close is what the topic already presupposes.**
`representation-and-encoding` covers "how the signal is encoded before the
expensive network sees it — tokenizers and learned latents". Every practice
under it assumes there is a defensible answer to *where a unit of meaning
ends*. This paper measures a case where the answer is "a whole sentence, used
as one word" — the situation multi-word tokenization exists to handle. The
record holds no other evidence about it.

## Decision

**Work from outside the machine-learning literature is admissible as `LIT`
when it measures something a topic's practices presuppose, and the note says
what it does not license.**

Three conditions, and the third is the load-bearing one:

1. **It measures something**, rather than proposing a framework. Evidence, not
   position.
2. **What it measures is a presupposition of practices the record holds** —
   not a subject that is merely adjacent or interesting. "Where a unit of
   meaning ends" is assumed by every tokenization practice here; "how children
   acquire syntax" is not assumed by anything.
3. **The note states what it does not license, explicitly.** A paper admitted
   this way carries no practice and no theory by default, and the standing
   section has to say so *and why* — because the failure mode is not filing
   it, it is a later pass finding an unexplained note and reading a
   recommendation out of it.

This is deliberately narrower than "adjacent fields are in scope". It admits
a measurement of a thing the record already relies on, and nothing else.

## Alternatives

- **Decline it, and say so once.** The cheapest reading and the one
  [DP-009](../../docs/design-principles.md#dp-9) warns is self-confirming: declining leaves the vocabulary
  looking complete because the evidence that would have shown otherwise was
  turned away. It also loses the specific thing worth keeping — that the
  record's encoding practices rest on an assumption nothing here measures.
- **File it and source a practice from it.** The obvious way to make it "count"
  and the one that would be a fabrication. The paper ran no model and
  recommends nothing; a practice drawn from it would be this record's
  inference wearing the paper's citation, which is what
  [ADR-017](ADR-017.md) exists to prevent.
- **Add a topic for it** — `linguistics`, or similar. [DP-008](../../docs/design-principles.md#dp-8)'s corollary
  forbids exactly this: a category added to admit a single document is how a
  scope stops being one. If several such documents accumulate the calculus
  changes, and counting them is the antidote [DP-009](../../docs/design-principles.md#dp-9) names.
- **Widen [ADR-032](ADR-032.md)'s trigger to "anything a practice presupposes".** Rejected
  as too broad to be a limit: nearly anything can be described as presupposed
  by something. Condition 2 above is narrower on purpose — the presupposition
  has to be one the record's own documents visibly make.

## Consequences

**What it buys.** A note that would otherwise sit unexplained now carries its
own determination, and the boundary is a sentence somebody wrote rather than a
property of what the corpus happens to contain — which is the [DP-008](../../docs/design-principles.md#dp-8) failure,
avoided in the direction [ADR-032](ADR-032.md) avoided it from.

**What it costs.** The topic vocabulary now has a document under
`representation-and-encoding` that is not about encoding for a network, and
the tag is the closest available rather than a good fit. That is recorded here
rather than fixed, because one document is not enough to move a vocabulary and
pretending otherwise is the error this decision's third alternative describes.

**What it obliges.** Counting. If a second and third such paper arrive, the
question is no longer whether to admit them but whether the vocabulary is
short a category — and the answer has to come from the count, not from each
one looking individually marginal. `luria lint`'s unsourced-note reports are
where they will show up.

**Why it is `Proposed`.** One document is not a pattern, and the condition
that would settle this is a second case: a paper from outside the ML
literature that meets all three conditions and is filed under them. If none
arrives, this decision describes a single exception and should say so instead.
