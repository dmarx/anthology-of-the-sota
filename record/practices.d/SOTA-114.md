---
number: 114
status: 'Active'
title: 'Fuse attention operations where possible'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
source:
- LIT-074
introduced_by:
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

[LIT-074](../literature.d/LIT-074.md) is the evidence that full fusion pays in training. Its background
names the limit of naive fusion: the intermediates still have to be written
to HBM for the backward pass. Tiling and recomputation remove that, so one
CUDA kernel runs the matmul, softmax, optional mask and dropout, and the
second matmul, and Theorem 2 puts its HBM accesses at `Θ(N²d²M⁻¹)` against
standard attention's `Θ(Nd + N²)`. Against standard PyTorch attention on an
A100 it measures generally 2–4×, and more with dropout and masking, which
the paper attributes to the fusion.

[SOTA-088](SOTA-088.md) is the same recommendation reached from a different source and at
a different scope. Ivanov et al. measured that transformer training as a
whole is memory-bound and fused the elementwise, normalisation and dropout
operations between the matmuls; this practice confines fusion to the
attention chain. The cost below is shared by both.

## Cost

Fused kernels are rigid. Each supported combination of mask type, dropout,
head dimension and dtype is a separate code path, so an unusual attention
variant either falls back to the unfused implementation or needs a kernel
written for it. That is a real constraint on research code, and the reason
the practice is a default for standard attention rather than a rule.

The fallback is also silent: a model that quietly stops meeting the kernel's
preconditions gets the slow path and no warning, which is worth checking for
directly rather than inferring from step time.
