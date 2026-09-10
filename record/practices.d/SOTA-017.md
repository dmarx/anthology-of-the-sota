---
number: 17
status: 'Active'
title: 'Use micro-batch splitting for pipeline parallelism'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Gained the source's threshold on reading it for #114: bubble
    overhead is O((K-1)/(M+K-1)) and the paper reports it negligible
    once M >= 4*K. The recommendation is unchanged.
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-016
summary: >-
  Huang et al. (2018), [LIT-016](../literature.d/LIT-016.md) — [ARXIV-1811.06965](https://arxiv.org/abs/1811.06965).
---

# SOTA-017: Use micro-batch splitting for pipeline parallelism

## Source

Huang et al. (2018), [LIT-016](../literature.d/LIT-016.md) — [ARXIV-1811.06965](https://arxiv.org/abs/1811.06965).

## What the micro-batches are for

Splitting a layer group across devices and running them in sequence keeps
every stage but one idle: stage 2 cannot start until stage 1 finishes, and
the utilisation of a *k*-stage pipeline on one batch is 1/*k*. Pipeline
parallelism is only worth anything because the batch can be cut into
micro-batches that flow through the stages, so stage 1 starts micro-batch 2
while stage 2 works on micro-batch 1.

The result is arithmetically simple and is the whole design: with *m*
micro-batches and *k* stages the idle fraction — the bubble — is
(*k*−1)/(*m*+*k*−1). More micro-batches, smaller bubble.

## How many micro-batches

[LIT-016](../literature.d/LIT-016.md) gives the idle time introduced by partitioning — the **bubble
overhead** — in closed form, for `K` partitions and `M` micro-batches:

    O( (K − 1) / (M + K − 1) )

and reports it **negligible once `M ≥ 4 × K`**. That is the number this
practice was missing. Part of why so few suffice is that backward
re-computation can be scheduled early, without waiting for gradients from
earlier layers.

The competing constraint is that `M` micro-batches of a fixed mini-batch means
each is `1/M` the size, and past some point the per-device work is too small
to keep the accelerator busy. So `4K` is a floor to clear, not a target to
maximise.

## Cost

Each micro-batch's activations have to be kept until its backward pass, so
memory rises with *m* at exactly the moment the technique is being used to
fit a model that did not fit. GPipe's answer is recomputation — store only
stage boundaries and recompute the rest in the backward — which is the real
version of the memory-for-compute trade that [SOTA-087](SOTA-087.md) turns out *not* to be.

Micro-batches also shrink the per-device batch, so normalisation layers that
compute statistics over the batch see fewer samples. That is a correctness
consideration rather than a performance one, and it is why the technique sits
more comfortably with LayerNorm than with BatchNorm ([SOTA-006](SOTA-006.md)).
