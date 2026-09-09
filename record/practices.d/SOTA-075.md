---
number: 75
status: 'Active'
title: 'Use gradient compression for slow networks'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2017-12-01'
source:
- LIT-056
# inactive-ok-block: SOTA-155 — Proposed, and declared as a rival rather than
# a replacement precisely because it is not yet in force
# SOTA-155 attacks the same problem — a slow interconnect — by reducing the
# frequency of synchronisation rather than the volume of each one. Rivals,
# not lineage.
compared_against:
- SOTA-155
summary: >-
  Lin et al. (2017), [LIT-056](../literature.d/LIT-056.md) — [ARXIV-1712.01887](https://arxiv.org/abs/1712.01887).
---

# SOTA-075: Use gradient compression for slow networks

## Source

Lin et al. (2017), [LIT-056](../literature.d/LIT-056.md) — [ARXIV-1712.01887](https://arxiv.org/abs/1712.01887).

## The measurement the practice rests on

[LIT-056](../literature.d/LIT-056.md) opens with the number: **99.9% of the gradient exchange in distributed
SGD is redundant.** Send only the largest-magnitude components, accumulate the
rest locally, and send them when they grow large enough to matter — with
momentum correction, local gradient clipping and warmup on the sparsity ratio
to keep the accumulated staleness from changing the optimisation.

That last list is the part that gets dropped when this practice is quoted, and
it is what makes the technique work rather than merely compress. Naive
top-k sparsification without momentum correction loses accuracy; the paper's
contribution is the corrections, not the observation that gradients are sparse.

## When the condition in the title is met, and when it is not

"Slow networks" is doing real work. Compression trades computation and
accumulated staleness for bytes, so it pays only when the interconnect is the
bottleneck — commodity Ethernet, multi-datacentre, anything where the
collectives dominate step time (which [SOTA-045](SOTA-045.md)'s kind of measurement is what
establishes).

Inside a modern training cluster it usually is not met. NVLink and InfiniBand
move gradients fast enough that the overlap in [SOTA-047](SOTA-047.md) hides most of the
cost, and the compression's own compute and its interaction with the
optimizer are then pure loss.

<!-- inactive-ok: SOTA-155 — Proposed; named as where the record's current answer sits, with its status the reason this one is not simply retired -->
The record's more current answer for the genuinely-slow case is [SOTA-155](SOTA-155.md) —
many local steps with an outer optimizer over the deltas — which attacks
frequency rather than volume and composes better with everything else.
