---
number: 28
status: 'Active'
title: 'Stage optimizer states across data parallel ranks (ZeRO-1)'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-027
introduced_by:
- LIT-027
summary: >-
  Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).
extended_by:
- SOTA-029
---

# SOTA-028: Stage optimizer states across data parallel ranks (ZeRO-1)

## Source

Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).

## What it partitions, and what it does not cost

With Adam and mixed precision, a data-parallel run holds 16 bytes per
parameter on every rank: 2 for the FP16 weights, 2 for the FP16 gradients,
and 12 for the FP32 master weights and two moments ([SOTA-014](SOTA-014.md), [SOTA-015](SOTA-015.md)). The
12 are the target here, and the observation is that every rank holds an
identical copy of state that only ever gets read by the rank that owns the
corresponding slice of the update.

ZeRO-1 gives each of the N ranks 1/N of the optimizer state, taking the
per-rank cost to 4Ψ + 12Ψ/N — approaching a 4× reduction as N grows.

The stage and its arithmetic come from [LIT-027](../literature.d/LIT-027.md), which introduces
optimizer-state partitioning as the first of ZeRO-DP's three stages. The
paper counts mixed-precision Adam at K = 12 bytes of FP32 optimizer state per
parameter, which is where the 12 above comes from, and in its worked example
a 7.5B-parameter model on 64-way data parallelism falls from 120 GB of model
state per GPU to 31.4 GB.

The reason this is the first stage to reach for is that it is close to free.
The update becomes a reduce-scatter followed by an all-gather of the updated
weights, and the total volume moved is the same as the all-reduce it
replaces. Memory falls; the network sees no additional traffic.

## Condition

The saving scales with the data-parallel degree, so it does nothing on a
single rank and little on two. It also assumes the optimizer state is the
dominant term, which is what makes Adam the case it was designed for — an
optimizer carrying less state per parameter has correspondingly less to
partition.
