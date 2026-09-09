---
status: Active
title: 'PyTorch Distributed: Experiences on Accelerating Data Parallel Training'
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
published: '2020-06-28'
arxiv: '2006.15704'
first_author: 'Li'
keywords:
- 'distributed-training'
- 'data-parallel'
- 'gradient-bucketing'
summary: >-
  Li et al. (2020), [ARXIV-2006.15704](https://arxiv.org/abs/2006.15704). The design and evaluation of PyTorch's
  DistributedDataParallel, whose three acceleration techniques are "bucketing
  gradients, overlapping computation with communication, and skipping gradient
  synchronization" — near-linear scalability on 256 GPUs.
---

# LIT-tmpfh75h: PyTorch Distributed: Experiences on Accelerating Data Parallel Training

Li et al. (2020) — [ARXIV-2006.15704](https://arxiv.org/abs/2006.15704)

## Key takeaways

- The paper of record for `DistributedDataParallel`, and it names its three
  techniques in the abstract: **bucketing gradients, overlapping computation
  with communication, and skipping gradient synchronization**. Near-linear
  scalability on 256 GPUs when configured appropriately.
- Overlap is the one the anthology was missing a source for. Gradients become
  ready in reverse layer order during the backward pass, so a bucket can be
  reduced while earlier layers are still computing — which is what keeps the
  network busy through a phase that would otherwise be pure compute.
- Bucketing is the same problem Horovod's Tensor Fusion ([LIT-tmpoxpda](LIT-tmpoxpda.md))
  solves, arrived at independently in a different framework, and the two
  together are why the practice is standard rather than novel.
- "Skipping gradient synchronization" is gradient accumulation stated as a
  communication decision rather than a batch-size one — reducing every *k*
  steps instead of every step, which trades staleness for traffic.

## Standing in the anthology

The source for [SOTA-047](../practices.d/SOTA-047.md) (overlap communication with the backward pass), which
had been credited to [LIT-051](LIT-051.md) — a paper that assumes overlap rather than
introducing it.

Filed alongside [LIT-tmpoxpda](LIT-tmpoxpda.md) for the same reason: the practices were right and
their citations were not.
