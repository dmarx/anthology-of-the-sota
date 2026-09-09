---
number: 48
status: 'Active'
title: 'Group small tensors before communication'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2020-11-01'
source:
- LIT-051
summary: >-
  Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.
---

# SOTA-048: Group small tensors before communication

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## Tensor fusion, and whose it is

A collective has a fixed per-call cost — launch, handshake, latency across
the fabric — that a small tensor cannot amortise. A transformer has thousands
of small parameters (norms, biases) alongside a few large ones, so reducing
each as it arrives spends most of the step on overhead. Coalescing them into
a buffer and reducing once is the fix.

It is a real practice and a well-understood one. It is **Horovod's tensor
fusion**, and the equivalent bucketing in PyTorch DDP; [LIT-051](../literature.d/LIT-051.md) assumes it.
BytePS's contribution is the unified PS/all-reduce framework and the
Summation Service split (see [SOTA-047](SOTA-047.md)), not this.

## The trade the title hides

Fusing more means waiting longer for the buffer to fill, which delays the
reduction and eats into the overlap [SOTA-047](SOTA-047.md) depends on. The bucket size is
therefore a dial between two failures — too small and the collectives are
latency-bound, too large and the overlap collapses — and there is no setting
that is right for every fabric and model.

That is a better statement of what [SOTA-049](SOTA-049.md) is reaching for than the
bandwidth-delay product it currently names.
