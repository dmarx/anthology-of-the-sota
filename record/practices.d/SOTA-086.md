---
number: 86
status: 'Active'
title: 'Tiling size should match hardware SRAM size'
version: 1
tags:
- attention-techniques
date: '2026-08-24'
published: '2022-05-01'
source:
- LIT-074
summary: >-
  Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).
extended_by:
- SOTA-087
---

# SOTA-086: Tiling size should match hardware SRAM size

## Source

Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).

## What the tiling is actually constrained by

The block sizes exist to make one tile of Q, K and V, plus the running
softmax statistics, fit in the streaming multiprocessor's on-chip memory at
once. That is the whole mechanism: if the working set fits, the score block
is produced and consumed without ever touching HBM ([SOTA-087](SOTA-087.md)); if it does not,
the kernel spills and the advantage disappears.

So "match hardware SRAM size" is not a tuning heuristic. It is the condition
under which the algorithm is the algorithm.

## What that means in practice

Not that anybody sets it by hand. The block sizes are chosen per architecture
and per head dimension by the kernel, because SRAM per SM, head dimension and
occupancy all move together — a tile large enough to be efficient and small
enough that enough tiles are resident to hide latency. Hard-coding a size
tuned for one generation is how a kernel gets slower on the next.

The practice is best read as a constraint to respect when writing or
selecting a kernel, and as a reason a fused attention implementation is
hardware-specific in a way an unfused one is not.
