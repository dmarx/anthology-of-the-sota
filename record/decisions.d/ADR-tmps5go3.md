---
status: Proposed
title: 'A claim about the signal is admissible however it was measured, including on people'
version: 1
tags:
- record
date: '2026-09-17'
summary: >-
  A psycholinguistics paper arrived with a real measurement, no model and no
  recommendation, and the first instinct was to file it as a LIT note that
  sources nothing — admitted on an exception. That was wrong twice over: the
  record already holds physics, control theory and pure mathematics, so
  "outside CS" was never the boundary; and the paper's finding is a claim
  about what is TRUE, which is what THEORY holds. Proposed: the scheme follows
  the kind of claim, not the apparatus that produced it, so a finding about
  the signal is a THEORY whether it was measured on a GPU or on 755 people —
  provided its document says what it does not license. Rejected: the
  exception framing, sourcing a practice from it, and adding a topic.
---

# ADR-NNN: A claim about the signal is admissible however it was measured, including on people

## Context

[LIT-tmp5l55q](../literature.d/LIT-tmp5l55q.md) is a paper in *Language* about
English syntax. Four preregistered surveys, 755 participants, a billion-word
corpus study, and not one sentence about a machine. Filing it on request
turned up a boundary nobody here has drawn, and the first attempt at drawing
it was wrong in a way worth recording.

**"Outside computer science" was never the boundary, and the corpus says so.**
The record holds *Physical Review Letters*, *Reviews of Modern Physics*, four
volumes of *IEEE Transactions on Automatic Control*, *SIAM*, and a 1963
*Proceedings of the AMS*; 27 notes carry no arXiv identifier at all. Nobody
argued about those, because each is machinery ML work runs on — and each is
cited by work the record files, which is [ADR-032](ADR-032.md)'s stated
trigger. Nothing here cites Goldberg and Shirtz, so on that trigger's letter
this paper is out.

**The first attempt therefore reached for an exception**: admit it as a `LIT`
note that sources nothing, on a narrow rule about measuring what a topic's
practices presuppose. That framing survived about as long as it took someone
to say the paper is a theory paper.

**Which it is, and the record's own test says so.** `CLAUDE.md`: *if it tells
the reader what to do it is a practice, and if it says what is true it is a
theory.* The test is about the kind of claim and mentions no apparatus. The
reflex that made this look hard — the subjects are people, so it cannot be
about our systems — is a claim about **where the measurement happened**, not
about what was claimed. And what was claimed is that a lexical unit can be an
arbitrary-length phrase, delimited by construction rather than by frequency.
**That is a fact about language, and language is the signal**, which is the
thing every practice under `representation-and-encoding` acts on.

[ADR-026](ADR-026.md) already draws this distinction on the other axis: a
preconditioning scheme discovered in diffusion takes its *kind*, not its
domain. Domain of discovery does not determine filing there, and apparatus of
measurement should not here.

## Decision

**A document is filed by the kind of claim it makes, not by the instrument
that produced it.** A finding about the signal — what the data is like — is a
`THEORY` and sources a `LIT` note, whether it was measured on a GPU, in a
corpus, or on 755 people.

Two conditions, and the second is the load-bearing one:

1. **The claim is about something the record's practices act on**: the signal,
   the systems, or the training process. Not about the measuring population.
   "Where a lexical unit ends" qualifies; "how children acquire syntax" does
   not, because no practice here acts on it.
2. **The document states what it does not license, explicitly** — and for work
   like this, that has to include *this was not measured on a model*. The
   failure mode is not the filing. It is a later pass reading a survey result
   as a result about transformers, which is the [LIT-052](../literature.d/LIT-052.md)
   and [LIT-025](../literature.d/LIT-025.md) failure with a new surface: two
   notes whose plausible-looking takeaways turned out not to be about their
   papers, and which eight practices were built on.

What this does *not* do is lower the bar for a practice. A finding about the
signal underwrites a recommendation only when someone has measured the cost of
acting on it, which is a separate document and usually a missing one.

## Alternatives

- **Decline it, and say so once.** The cheapest reading, and the one
  [DP-009](../../docs/design-principles.md#dp-9) names as self-confirming:
  declining leaves the vocabulary looking complete because the evidence that
  would have shown otherwise was turned away.
- **The exception framing — admit it as a `LIT` note that sources nothing.**
  What this decision replaces, and it is worth recording because it looked
  right. It treats the apparatus as the thing in question, so it has to build
  a special rule to get around it; the ordinary rules already work once the
  claim is classified correctly. A scheme that needs an exception for a
  well-evidenced finding about its own subject matter has mis-stated its
  subject matter.
- **File it and source a practice from it.** The way to make the filing
  self-justifying, and a fabrication: the paper ran no model and recommends
  nothing, so a practice would be this record's inference wearing the paper's
  citation. [ADR-017](ADR-017.md) is the rule against exactly that.
- **Add a topic for it** — `linguistics` or similar. [DP-008](../../docs/design-principles.md#dp-8)'s
  corollary forbids it: a category added to admit a single document is how a
  scope stops being one. If several accumulate the calculus changes, and
  counting them is the antidote [DP-009](../../docs/design-principles.md#dp-9) names.

## Consequences

**What it buys.** The boundary is a sentence somebody wrote rather than a
property of what the corpus happens to contain — the [DP-008](../../docs/design-principles.md#dp-8)
failure, avoided from the direction [ADR-032](ADR-032.md) avoided it from. And
it is the *general* rule rather than a carve-out, so the next such paper is an
ordinary filing decision instead of a second exception.

**What it costs.** `representation-and-encoding` now holds a theory that is
about the structure being encoded rather than about encoding it for a network,
and the tag is the closest available rather than a good fit. Recorded here
rather than fixed: one document is not enough to move a vocabulary, and
pretending otherwise is this decision's fourth rejected alternative.

**What it obliges.** Counting, and a specific piece of work. The bridge from a
claim about the signal to anything a model does is empirical, and for this
claim the record does not hold it — the detokenization and inner-lexicon line
(`ARXIV-2410.05864`, `ARXIV-2406.20086`) is unfiled. A record that admits
signal claims and never files the work connecting them to models ends up with
a shelf of true and inert facts.

**Why it is `Proposed`.** One document is not a pattern. What would settle it
is a second finding about the signal, measured outside the ML literature and
filed under these conditions — or a case where condition 1 does real work by
excluding something. If neither arrives, this describes a single exception
after all and should say so.
