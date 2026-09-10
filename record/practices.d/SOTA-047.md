---
number: 47
status: 'Active'
title: 'Overlap communication with backward pass'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Corrected `published:`, which is derived from the primary source and
    had gone stale: LIT-051's date survived the re-source to LIT-219.
    Found by the #119 backfill. The recommendation and the source list
    are unchanged.
tags:
- distributed-optimization
date: '2026-08-24'
published: '2020-06-28'
source:
# Re-sourced: LIT-051 assumes overlap rather than introducing it. The
# PyTorch DDP paper names it as one of its three techniques.
- LIT-219
summary: >-
  Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.
compared_against:
- SOTA-048
- SOTA-079
---

# SOTA-047: Overlap communication with backward pass

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## The practice is right, and this is not where it comes from

Gradients become available in reverse layer order as the backward pass runs,
so the gradient for the last layer is ready long before the first layer's is
computed. Waiting for the whole backward pass and then reducing everything
leaves the network idle throughout the backward and the GPU idle throughout
the reduction. Issuing each layer's reduction as its gradient lands overlaps
the two, and on a well-tuned job most of the communication disappears behind
compute.

That is correct, and it is the foundation the rest of this cluster builds on.
It is also standard practice since well before [LIT-051](../literature.d/LIT-051.md) — it is what
Horovod and PyTorch's DistributedDataParallel do by default, and the
technique predates both.

## What [LIT-051](../literature.d/LIT-051.md) actually contributes

This practice used to cite [LIT-051](../literature.d/LIT-051.md), whose contribution is a unified
parameter-server/all-reduce framework and a CPU-side Summation Service. That
paper assumes overlap; it does not introduce it, and citing it here credited
the wrong work.

The source is now [LIT-219](../literature.d/LIT-219.md), the PyTorch `DistributedDataParallel` paper,
which names the technique in its abstract — "bucketing gradients, overlapping
computation with communication, and skipping gradient synchronization" — and
reports near-linear scalability on 256 GPUs with them.

## The cost, since the title does not

The overlap is what makes the *bucket size* a tuning parameter: reduce too
eagerly and each collective is too small to reach peak bandwidth; too lazily
and there is nothing left to hide the last one behind. That trade is the real
<!-- inactive-ok: SOTA-049 — Rejected, named as the practice whose content this one absorbs -->
content of [SOTA-048](SOTA-048.md) and [SOTA-049](SOTA-049.md).
