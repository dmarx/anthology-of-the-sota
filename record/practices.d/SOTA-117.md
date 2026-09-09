---
number: 117
status: 'Active'
title: 'Overlap communication with computation using backward prefetch'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2023-04-01'
source:
- LIT-083
summary: >-
  Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).
---

# SOTA-117: Overlap communication with computation using backward prefetch

## Source

Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).

## What is being overlapped, and with what

Sharding costs an all-gather of each unit's parameters before it runs. Left
serial, the GPU idles through every one of them. Backward prefetch issues the
gather for unit *i−1* while unit *i*'s gradients are still being computed, so
the collective runs against compute that is already scheduled.

The forward direction has the same shape and is easier — the execution order
is known — which is why the backward case is the one with a name: the order
is discovered by autograd, so the prefetch has to predict it from the
forward's recorded sequence.

## Cost

Prefetching means two units' parameters are resident at once instead of one,
so the peak footprint rises by roughly one unit. On a job that chose FSDP
because it was out of memory ([SOTA-116](SOTA-116.md)) that is not free, and the knob is the
first thing to turn off when the run OOMs near the peak rather than at the
start.

It also depends on the predicted order being right. A model whose backward
order differs from the reverse of its forward — conditional branches, shared
modules used twice — prefetches the wrong unit and pays the gather twice.
