---
number: 106
status: 'Active'
title: 'Use flash-attention-2 over original flash-attention when available'
version: 1
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-07-01'
source:
- LIT-106
summary: >-
  Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).
---

# SOTA-106: Use flash-attention-2 over original flash-attention when available

## Source

Dao et al. (2023), [LIT-106](../literature.d/LIT-106.md) — [ARXIV-2307.08691](https://arxiv.org/abs/2307.08691).

## What the second version changed

Not the algorithm. FlashAttention-2 computes the same exact attention by the
same tiled, never-materialised route ([SOTA-087](SOTA-087.md)); what it rewrites is how the
work is divided.

Three changes, and the first is the largest: the inner loop is restructured
so that far fewer of the operations are *non*-matmul. GPUs run matmul on
tensor cores at many times the rate of everything else, so a kernel spending
a noticeable fraction of its time on rescaling and bookkeeping is leaving
most of the hardware idle even when it is fully occupied. The second is
parallelising over the sequence-length dimension as well as batch and heads,
which matters exactly when batch × heads is too small to fill the GPU — long
context, small batch, the regime the kernel exists for. The third is a better
split of work between warps inside a block, cutting shared-memory traffic.

## So the recommendation is nearly free, with one condition

Same outputs, better occupancy: there is no accuracy argument to have and the
upgrade is a kernel swap.

The condition is the usual one for fused kernels ([SOTA-114](SOTA-114.md)) — the supported
paths are specific, and a head dimension or mask type outside them falls back
silently. The second version supports a wider set than the first, which is
part of why the recommendation is unconditional in the title, and it is still
not everything.
