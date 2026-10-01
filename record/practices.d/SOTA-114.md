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
# CORRECTED. Was `introduced_by: LIT-074`, which passed only because it is
# also the source. FlashAttention presents fusion as prior art: §2.2 cites
# fusing masking with softmax to Megatron-LM (LIT-022, whose paper does not
# describe it; the kernel is in its code), and App. E says Apex FMHA already
# fused the whole chain into one CUDA kernel and was FlashAttention's starting
# code. FMHA is code, not a paper. The earliest paper found recommending it is
# Ivanov et al. (2020), which fuses the attention chain's scaling, softmax and
# dropout into one kernel as part of fusing the whole layer.
introduced_by:
- LIT-066
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

The fusion itself is older than [LIT-074](../literature.d/LIT-074.md), which says so. Its background
cites earlier work fusing the mask into the softmax, and its appendix
names Apex FMHA, which already ran the matmul, mask, softmax, dropout and
second matmul as one CUDA kernel but stored the attention matrix for the
backward pass; FlashAttention started from that code and added tiling and
recomputation. The first paper to recommend fusing attention's operations is
[LIT-066](../literature.d/LIT-066.md), two years earlier. Ivanov et al. fused the scaled softmax with its
dropout into one kernel and the attention input biases into another, as part
of fusing every elementwise and normalisation chain in a BERT layer. They
stopped at the matmuls: fusing an elementwise operator into a CUTLASS batched
matmul cost more than it saved, so their contractions stayed in cuBLAS. What
FlashAttention added is the step they judged unprofitable, made to pay by
never writing the intermediates at all.

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
