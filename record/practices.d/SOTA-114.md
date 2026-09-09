---
number: 114
status: 'Active'
title: 'Fuse attention operations where possible'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
published: '2022-05-01'
source:
- LIT-074
summary: >-
  Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).
compared_against:
- SOTA-088
---

# SOTA-114: Fuse attention operations where possible

## Source

Dao et al. (2022), [LIT-074](../literature.d/LIT-074.md) — [ARXIV-2205.14135](https://arxiv.org/abs/2205.14135).

## The general form of the practice above it

[SOTA-087](SOTA-087.md) and [SOTA-086](SOTA-086.md) describe one fused attention kernel; this is the
principle they are an instance of. Attention as written is a chain of
separate operations — matmul, scale, mask, softmax, dropout, matmul — and
each boundary between them is a round trip through HBM for a tensor that is
about to be read straight back. Fusing the chain into one kernel keeps the
intermediates on chip.

The win is bandwidth, not arithmetic, which is why it is worth doing even
though the fused kernel does *more* FLOPs ([SOTA-087](SOTA-087.md)).

## Cost

Fused kernels are rigid. Each supported combination of mask type, dropout,
head dimension and dtype is a separate code path, so an unusual attention
variant either falls back to the unfused implementation or needs a kernel
written for it. That is a real constraint on research code, and the reason
the practice is a default for standard attention rather than a rule.

The fallback is also silent: a model that quietly stops meeting the kernel's
preconditions gets the slow path and no warning, which is worth checking for
directly rather than inferring from step time.
