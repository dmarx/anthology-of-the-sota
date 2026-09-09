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
# Re-sourced: Tensor Fusion is Horovod's, and PyTorch DDP arrived at the
# same technique as bucketing. LIT-051 assumed both.
- LIT-220
- LIT-219
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

It is **Horovod's Tensor Fusion**, [LIT-220](../literature.d/LIT-220.md), and PyTorch DDP reached the
same technique independently as gradient bucketing, [LIT-219](../literature.d/LIT-219.md). Horovod
states the problem exactly: ring-allreduce "utilizes the network in an optimal
way if the tensors are large enough, but does not work as efficiently or
quickly if they are very small." Fusing first gave **up to 65% improvement**
on models with many layers over an unoptimized TCP network.

It also supplies the number the record was missing: Horovod's **default fusion
buffer is 64 MB**. That is a real, attributable default — and, like the loss
scaling constants in [SOTA-013](SOTA-013.md), a tested default rather than a measured
optimum. The citation this practice carried before, [LIT-051](../literature.d/LIT-051.md), assumes fusion
rather than introducing it.

## The trade the title hides

Fusing more means waiting longer for the buffer to fill, which delays the
reduction and eats into the overlap [SOTA-047](SOTA-047.md) depends on. The bucket size is
therefore a dial between two failures — too small and the collectives are
latency-bound, too large and the overlap collapses — and there is no setting
that is right for every fabric and model.

<!-- inactive-ok: SOTA-049 — Rejected, named as the practice whose fusion-buffer half landed here -->
That is a better statement of what [SOTA-049](SOTA-049.md) is reaching for than the
bandwidth-delay product it currently names.
