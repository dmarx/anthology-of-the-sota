---
number: 88
status: 'Active'
title: 'Fuse small operations into larger kernels'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
source:
- LIT-066
compared_against:
- SOTA-081
- SOTA-114
summary: >-
  Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).
---

# SOTA-088: Fuse small operations into larger kernels

## Source

Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).

## Same principle as [SOTA-081](SOTA-081.md), arrived at from measurement

Fusing memory-bound elementwise chains into one kernel is the graph-level
transformation TVM automates ([SOTA-081](SOTA-081.md)) and the one FlashAttention applies by
hand to attention ([SOTA-114](SOTA-114.md)). This practice is the version [LIT-066](../literature.d/LIT-066.md) reached
empirically: having established that transformer training is memory-bound, the
fix that follows is to stop moving tensors that are used once.

The record holds the same recommendation three times because three sources
arrived at it independently, which is worth leaving visible rather than
deduplicating — a technique that three groups converge on from different
directions is better evidenced than one that appears once.

## What is specific to this source

The scope. [LIT-066](../literature.d/LIT-066.md) is about the *whole* transformer rather than one operator:
the elementwise, normalisation and dropout operations between the matmuls are
individually trivial and collectively a large share of the time, and the
paper's point is that this had gone unmeasured because attention had absorbed
the optimisation attention.

The cost is the usual one for fusion ([SOTA-114](SOTA-114.md)): each fused variant is a code
path, and the set of supported combinations is what a framework can actually
maintain. That is precisely the constraint TVM's search exists to relax.
