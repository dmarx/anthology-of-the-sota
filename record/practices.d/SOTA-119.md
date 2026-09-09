---
number: 119
status: 'Active'
title: 'Choose sharding factor based on model and GPU memory size'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2023-04-01'
source:
- LIT-083
extends:
- SOTA-116
summary: >-
  Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).
---

# SOTA-119: Choose sharding factor based on model and GPU memory size

## Source

Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).

## The dial between the two extremes

Full sharding across every rank minimises memory and maximises communication:
every unit's parameters cross the network before use. Full replication is
DDP. Sharding within a node and replicating across nodes — hybrid sharding —
puts the expensive collective on the fast intra-node links and leaves the
slow inter-node path carrying one gradient reduction per step.

That is why the choice is stated as a factor rather than a switch. The right
value is the smallest group that makes the model fit, because everything
beyond that buys memory nobody needs at the price of traffic on links that
are slower the further the group spans.

## Condition

It depends on the interconnect being genuinely heterogeneous — fast inside a
node, slow between — which is the common case and not a universal one. On a
uniform fabric the argument for a group smaller than the world collapses to
the memory question alone.

Sizing it also needs the activation footprint, not just parameters and
optimizer state: those are what [SOTA-116](SOTA-116.md)'s threshold is really about, and
they do not shard.
