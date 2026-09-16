---
status: Proposed
title: 'Only one cross-scheme relation asserts a topic invariant: a note and its paper'
version: 1
tags:
- record
- taxonomy
date: '2026-09-16'
issue: '#142'
summary: >-
  luria 0.23.0 lets a relation declare `invariant`, including one that crosses
  schemes. Measured over all six of this record's heterogeneous relations, only
  `NOTE.paper` earns it — 4 findings in 158 edges, every one a disagreement
  about the same paper. The other five join a claim to a paper or to an
  explanation, which [ADR-026](ADR-026.md)'s filing rule expects to differ, and they report
  20-47% of their edges. Rejected: declaring it on `source` and
  `introduced_by`, which would report the record for following its own rule.
---

# ADR-tmpvv2d8: Only one cross-scheme relation asserts a topic invariant: a note and its paper

<!-- inactive-ok-file: ADR-035, ADR-036 — both Proposed, and both are the
     decisions this one continues: ADR-035 chose `tags` over `primary_topic`
     for an edge, ADR-036 read the same-scheme findings through and named the
     four categories this decision measures the cross-scheme relations
     against. Nothing here rests on either being in force; they are cited as
     the reasoning already on the record. -->

## Context

Until now this record could assert a topic invariant only along a chain, and a
chain walks one scheme. `practice` and `lineage` declare `invariant: tags`
([ADR-035](ADR-035.md)); every relation that crosses a scheme boundary asserted nothing,
because there was nowhere to say it. Declaring a chain over `SOTA.source` did
not fail — it raised `KeyError` part-way through `luria index`, which is what
[LU-#272](https://github.com/dmarx/luria/issues/272) was filed about.

luria 0.23.0 moves the edge half of the check onto the relation itself, where
it holds with no chain and may cross schemes. So the question this record now
has to answer is which of its heterogeneous relations actually assert
something a topic can express.

There are six:

| relation | joins | unbound on `tags` |
|---|---|---|
| `NOTE.paper` | a reading → the paper read | **4 / 158 (3%)** |
| `SOTA.introduced_by` | a practice → the paper that first stated it | 45 / 220 (20%) |
| `THEORY.source` | an explanation → its paper | 4 / 19 (21%) |
| `SOTA.source` | a practice → its evidence | 67 / 298 (22%) |
| `SOTA.contested_by` | a practice → a paper against it | 4 / 13 (31%) |
| `SOTA.explained_by` | a practice → why it works | 7 / 15 (47%) |

Measured on the record as it stands, before any retag.

## Decision

**`NOTE.paper` declares `invariant: tags`. The other five declare nothing.**

The line is not the rate — the rate is the evidence. It is what the two ends
of the relation *are*.

A note and its paper are **the same object**. The scheme exists so a reading
can be filed separately from the paper's standing, and `NOTE.published` is
already derived from the paper for that reason. Two documents about one paper
that share no topic have disagreed about that paper, and one of them is
wrong. That is a finding with an answer.

The other five join **two different things filed on two different axes**, and
[ADR-026](ADR-026.md)'s filing rule is what puts them there: a practice takes the topic of
*the claim it makes*, a paper takes the topic of *what it is about*. A
practice extracted from a vision paper about a training technique is
`training-optimization` under a `vision-and-graphics` source, and the record
decided that on purpose. Declaring the invariant there reports the record for
following its own rule.

`explained_by` is the sharpest case and the one that settles it at 47%: a
THEORY is pulled toward `analysis-and-evaluation` by the vocabulary itself —
*"theory, interpretability and debugging belong here too"* — while the
practice it explains is filed by subject. [ADR-036](ADR-036.md) already named this as the
third of its four categories, over the same-scheme chains: *"twelve of the
thirteen topics name a subject; `analysis-and-evaluation` names a kind of
work, and it will unbind a relation whenever one end does something and the
other end measures it."* Every one of the seven is that.

The two small ones are the same four categories again. `THEORY.source`'s four
are the `analysis-and-evaluation` pull in both directions. `contested_by`'s
four are two model reports ([ADR-036](ADR-036.md)'s trunk-paper shape), one critique paper
pulled to analysis, and one activation-function pair that is genuinely short a
tag — 13 edges is too few to read a rate off, and nothing in the four argues
the relation asserts a shared topic.

## Alternatives considered

- **Declare it on `source` and `introduced_by` too.** These are the relations
  the report was originally imagined for, and 20-22% is not an absurd rate.
  It loses because of what the findings *are*: read individually in [LU-#272](https://github.com/dmarx/luria/issues/272)
  they were four kinds — multi-topic model reports, practices resting on
  analysis papers, the domain-vs-kind filing rule working as designed, and a
  minority of genuine mis-filings. A check whose majority finding is the
  record doing what it decided to do trains the reader to skip the report,
  which costs the minority that were real.
- **Declare it on `contested_by` only, of the claim-to-paper relations.** It
  has the best constructional argument of the five — a paper cannot contest a
  practice without being about the same thing. Thirteen edges is not enough
  to know, and 4 of 13 is not encouraging; revisit if it grows.
- **Use `primary_topic` rather than `tags`.** Worse everywhere it differs and
  never better: 73/298 against 67/298 on `source`, identical on the small
  relations and on `NOTE.paper`. [ADR-035](ADR-035.md) already settled the reading — what a
  relation asserts is that its ends have something in common, not that the
  something is the first thing each is about.
- **Retag the four `NOTE.paper` findings in this contribution so the check
  lands green.** Refused on [ADR-036](ADR-036.md)'s own terms: [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101) bound a pair by giving
  both a `flash-attention` tag and *satisfied the check rather than answering
  it*. Two of the four are clear mis-filings and two are two-topic papers
  where a secondary tag is exactly that move; they want a reading each, not a
  config commit.
- **Status quo.** The record keeps asserting nothing across any scheme
  boundary, including between a note and the paper it reads, which is the one
  place the assertion is true by construction.

## Consequences

`docs/reports/unbound-lineage.md` goes from 22 unbound relations to 26, and
gains a `Declared by` column — luria 0.23.0 prints what declared each finding,
so `NOTE.paper` rows are distinguishable from the two chains' at a glance. The
10 unbound lines are unchanged: a relation asserts the edge and not the line,
which is the chain's to assert.

The four new findings, all of them a note and its paper disagreeing:

- `LIT-014` / `NOTE-008` — *Visualizing the Loss Landscape of Neural Nets*,
  `analysis-and-evaluation` against `model-stability`. Both are true of it;
  `THEORY-011` reads it as a stability result. A second tag on the paper.
- `LIT-024` / `NOTE-016` — multi-query attention, filed `model-architecture`
  while the note says `attention-techniques`. The note is right and the paper
  is wrong read alone: the `attention-techniques` blurb names attention
  variants and implementation optimizations, which is all MQA is.
- `LIT-096` / `NOTE-018` — *Segment Anything*, `vision-and-graphics` against
  the note's `data-pipeline`. The data engine is a real second contribution;
  which document moves is the open question.
- `LIT-112` / `NOTE-023` — vLLM and PagedAttention, filed
  `attention-techniques` while `inference-optimization`'s blurb names
  serving-time cache layout in as many words. The paper is wrong read alone.

Left open: those four, deliberately. Also that `NOTE.tags` still declares no
vocabulary (the gap [ADR-035](ADR-035.md) named), so a free-form tag on a note can never
intersect LIT's closed list and would read as an unbound edge. No note carries
one today — all 158 draw from the thirteen — so the check is safe until one
does, and the finding it would produce is arguably the right one anyway.
