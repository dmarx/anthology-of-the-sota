---
number: 87
status: 'Active'
title: 'Recompute attention during backward pass instead of storing it'
version: 1
tags:
- attention-techniques
date: '2026-08-24'
source:
- LIT-074
extends:
- SOTA-086
summary: >-
  Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).
---

# SOTA-087: Recompute attention during backward pass instead of storing it

## Source

Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).

## Why recomputation is cheaper here than storing

Standard attention materialises the N×N score matrix, writes it to HBM,
reads it back for the softmax, writes that, and reads it again for the
backward pass. The arithmetic is trivial next to the traffic, so attention is
memory-bound and the N² term is a *bandwidth* cost before it is a compute one.

FlashAttention keeps the block of scores in on-chip SRAM, consumes it
immediately, and never writes it out. The backward pass then recomputes each
block from Q, K and V — which is more FLOPs and less time, because the FLOPs
were never the bottleneck. Memory falls from quadratic to linear in sequence
length.

This is why the practice is not the usual activation-checkpointing trade. The
ordinary version buys memory with compute at a real cost in step time; here
the recomputation is close to free, because the thing it avoids is the
expensive one.

## Condition

It holds while the kernel is memory-bound, which is where attention lives at
the head dimensions transformers use. It also depends on the softmax being
computable blockwise — the online, running-maximum formulation — so a variant
that needs the whole row at once cannot be done this way.

The saved memory is what makes the long-context regime affordable at all;
[SOTA-086](SOTA-086.md) is the constraint on how the blocks are sized.
