---
number: 85
status: 'Active'
title: 'Use flash attention for all attention computations when hardware supports it'
version: 1
tags:
- attention-techniques
- flash-attention
date: '2026-08-24'
published: '2022-05-01'
source:
- LIT-074
summary: >-
  Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).
extended_by:
- SOTA-161
---

# SOTA-085: Use flash attention for all attention computations when hardware supports it

## Source

Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).

## What "when hardware supports it" is carrying

The recommendation is easy because the result is exact. FlashAttention
computes the same attention as the unfused implementation — not an
approximation, not a sparsity pattern — so adopting it changes throughput and
memory and nothing else about the model. That is unusual among the
efficiency practices in this record and is why the title can be so
unconditional.

The condition in the title is doing real work, though. The kernel depends on
enough on-chip memory per SM to hold a tile ([SOTA-086](SOTA-086.md)), and on the head
dimension and dtype being ones a compiled path exists for. Off that path the
fallback is the unfused implementation, silently.

## Where the line goes from here

[SOTA-106](SOTA-106.md) supersedes the version of the kernel rather than the practice:
FlashAttention-2 rebalances the work partitioning for the same exact result.

The one thing adopting it changes numerically is the *order* of accumulation,
and that is not nothing at scale — [SOTA-161](SOTA-161.md) exists because the rounding bias
of the fused reduction compounds rather than cancelling over a long run, and
it is filed under stability rather than attention for exactly that reason.
