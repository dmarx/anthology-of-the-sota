---
number: 249
status: Active
formerly:
- SOTA-tmpz59lh
consensus: universal
consensus_note: >-
  Every large-model training stack in the record ships this: SOTA-087 for
  attention specifically, and the memory accounting behind SOTA-017,
  SOTA-019 and SOTA-031 assumes activations are recomputed rather than
  stored. DP-005 keeps adoption separate from evidence — the evidence is
  LIT-004's measurement, and the adoption is why nobody states the rule.
title: 'Recompute activations from a sqrt(n) subset of checkpoints when activation memory is the binding constraint'
version: 1
tags:
- distributed-optimization
- systems-optimization
date: '2026-09-19'
source:
- LIT-004
introduced_by:
- LIT-004
extended_by:
- SOTA-087
implementations: []
summary: >-
  Chen et al. (2016), [LIT-004](../literature.d/LIT-004.md) — [ARXIV-1604.06174](https://arxiv.org/abs/1604.06174). Store activations at
  O(sqrt(n)) checkpoints and recompute the rest during the backward pass. The
  price is one extra forward pass per minibatch; the measured case is a
  1000-layer ResNet at 48G to 7G for 30% more wall clock.
---

# SOTA-249: Recompute activations from a sqrt(n) subset of checkpoints when activation memory is the binding constraint

## Source

Chen et al. (2016), [LIT-004](../literature.d/LIT-004.md) — [ARXIV-1604.06174](https://arxiv.org/abs/1604.06174).

## The rule

Do not store every intermediate feature map for the backward pass. Keep them
at a subset of layers — the checkpoints — and recompute the segments between
them when the gradient needs them.

For an `n`-layer network the checkpoint set that minimises memory is
`O(sqrt(n))`, and the cost of that choice is **one extra forward pass per
minibatch**. The trade is continuous rather than binary: the same analysis
gives `O(log n)` memory for `O(n log n)` extra forward computation, so the
question is never *whether* to recompute but where on the curve to sit.

## When it applies

**When activation memory is what stops you, and compute is not.** That is the
condition, and it is worth stating because the practice is a loss when it is
not met — you are paying real FLOPs for headroom you were not short of.

The measured case: a 1,000-layer deep residual network on ImageNet, **48G to
7G, for 30% additional running time**. The same reduction is reported for
recurrent networks on very long sequences, which is the shape that carries
over to long-context language-model training.

## What the record already had, and what it did not

The attention-specific case is [SOTA-087](SOTA-087.md), and it is much better
evidenced here than this general rule is — [LIT-074](../literature.d/LIT-074.md) argues it from HBM
traffic, with a mechanism this paper does not have. But `SOTA-087` recommends
recomputation *for attention*, and the memory accounting underneath
[SOTA-017](SOTA-017.md), [SOTA-019](SOTA-019.md) and [SOTA-031](SOTA-031.md) assumes activations are recomputed
without any practice saying so.

Filed because that is `DP-007` exactly: recomputation is universal enough in
large-model training that nobody writes the rule down, so the record held the
narrow case and not the general one for a year.

## What this is not

Not the same thing as [SOTA-054](SOTA-054.md). That practice is about **fault-tolerance
checkpointing** — how often to write model state to durable storage so a
crash costs little. This is about **activation checkpointing**, which never
leaves the device and exists to fit the backward pass in memory. The two
share a word and nothing else, which is the kind of collision worth naming
once.
