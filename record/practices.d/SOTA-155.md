---
number: 155
status: Proposed
formerly:
- SOTA-tmpgyaw3
promote_when: >-
  A pretraining report that trains a released model across separated clusters
  and describes the algorithm, or an independent group running the method at
  frontier parameter count against a fully synchronous baseline. Both results
  here are one group's, and the second is the first group correcting itself.
consensus: unreplicated
consensus_note: >-
  One group across both papers. Nothing in the record disputes it, and
  nothing corroborates it either — no second lab has published a run, and no
  frontier report trains this way.
title: 'Train across poorly connected islands: many inner steps per worker, an outer momentum optimizer over the deltas, and a streamed synchronisation'
version: 1
tags:
- distributed-optimization
date: '2026-09-07'
source:
# Two papers, one line: the first establishes that infrequent synchronisation
# need not cost quality, the second that the synchronisation itself need not
# be expensive. The recommendation rests on both — a practice built on the
# first alone would recommend an arrangement whose peak bandwidth is
# unchanged, which is the thing that decides whether it is cheaper at all.
- LIT-212
- LIT-214
implementations: []
summary: >-
  Douillard et al. (2023, 2025), [LIT-212](../literature.d/LIT-212.md) and [LIT-214](../literature.d/LIT-214.md) — federated
  averaging with the constants pushed hard: many inner AdamW steps per
  worker, Nesterov momentum as the outer optimizer over the accumulated
  deltas, synchronised rarely and in streamed subsets. 500× less
  communication at matched quality, then two more orders off the peak. Filed
  `Proposed`: one group, and no frontier report trains this way.
compared_against:
- SOTA-075
---

# SOTA-155: Train across poorly connected islands: many inner steps per worker, an outer momentum optimizer over the deltas, and a streamed synchronisation

## Source

Douillard et al. (2023), [LIT-212](../literature.d/LIT-212.md) — DiLoCo; Douillard et al. (2025),
[LIT-214](../literature.d/LIT-214.md) — Streaming DiLoCo, for the bandwidth half.

The constraint being attacked is co-location, not bandwidth. Standard
distributed training exchanges gradients every step, so every accelerator has
to sit behind a low-latency high-bandwidth link — which means one cluster,
and a big one. The premise here is that several small clusters are easier to
obtain than one large one.

What you run:

- **Many inner steps per worker**, with AdamW as the inner optimizer, between
  synchronisations.
- **Nesterov momentum as the outer optimizer**, applied to the accumulated
  worker deltas. This is the part that is not standard federated averaging,
  and it is what recovers the quality that infrequent synchronisation would
  otherwise cost.
- **Streamed, overlapped, quantised synchronisation**: exchange subsets of
  parameters in sequence rather than the whole model at once, let workers
  keep training while an exchange is in flight, and quantise what crosses the
  link.

## Why both papers, and why the second is not optional

DiLoCo alone reduces *how often* the link is used and not *how much* it must
carry: every synchronisation still exchanges all parameters across all
workers, so peak bandwidth is what fully synchronous training needs. A link
provisioned for the peak is a link that was never cheap, which is why a
recommendation resting on the first paper alone would be recommending
something whose economic case is unmade. The second paper is filed as
`corrects:` the first for exactly that reason ([ADR-017](../decisions.d/ADR-017.md)).

## Conditions, and what is not established

Reported results: 500× less communication at matched quality on C4 with 8
workers against fully synchronous optimization, robust to workers holding
differently distributed data and to resources disappearing mid-run; then two
orders of magnitude less bandwidth at billion scale with the streamed form,
at comparable quality.

Eight workers on C4 is a long way from the arrangement the motivation
describes, and one group published both halves. No report in this record
trains a released model this way.

What this is *not* advice about: the record's existing distributed material —
pipeline parallelism, the ZeRO stages, allreduce tuning, sharding factors —
is tuning within a synchronous regime. This is a different regime. Those
practices neither apply here nor conflict with this one, and reading either
as contradicting the other is a category error.

## Known implementations

- None in this record. The published results are the authors' own.
