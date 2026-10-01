---
number: 59
status: 'Active'
title: 'Overlap communication with computation when possible'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
# Was LIT-043 (Narayanan et al. 2021), which neither proposes nor measures
# overlap; the word appears only where its related work describes ZeRO.
# Jangda et al. (2021) is the earliest paper found that recommends and
# measures overlap on the tensor- and pipeline-parallel axes of a Megatron
# job. Searched for an earlier origin: PipeDream (arXiv 1806.03377, 2018)
# claims overlap of pipeline communication with compute, but has no tensor
# axis; the data-parallel case is SOTA-047's, from PyTorch DDP (LIT-219).
source:
- LIT-735
introduced_by:
- LIT-735
summary: >-
  Jangda et al. (2021), [LIT-735](../literature.d/LIT-735.md) — [ARXIV-2105.05720](https://arxiv.org/abs/2105.05720).
---

# SOTA-059: Overlap communication with computation when possible

## Source

Jangda et al. (2021), [LIT-735](../literature.d/LIT-735.md) — [ARXIV-2105.05720](https://arxiv.org/abs/2105.05720).

CoCoNet, [LIT-735](../literature.d/LIT-735.md), is where the move was made and measured on the axes
this practice is about. On the tensor-parallel MatMul and the AllReduce that
follows it, overlapping the two in chunks hides more than 80% of the MatMul
and runs up to 1.36x faster than issuing them in sequence; in Megatron-LM the
overlapped schedule cuts inference time of an 8.3B GPT-2 by 1.48x. On the
pipeline axis its best schedule overlaps the ReduceScatter, the cross-node
sends and the AllGather with each other, over NVLink and InfiniBand at once,
which is the contention described below. Two limits: those tensor- and
pipeline-parallel numbers are for inference, and the pipeline gain is
reported jointly with slicing and fusion rather than for overlap alone.
Training-side evidence on the tensor axis is narrower: Korthikanti et al.
([LIT-736](../literature.d/LIT-736.md)) overlap a backward-pass all-gather with the weight-gradient
computation as part of sequence parallelism. Narayanan et al. ([LIT-043](../literature.d/LIT-043.md)), cited
here before, does not propose or measure overlap.

## The same principle as [SOTA-047](SOTA-047.md), at a different layer

[SOTA-047](SOTA-047.md) overlaps the data-parallel gradient reduction with the backward
pass. This is the same move applied to the other two axes of a 3D-parallel
job: a pipeline stage's activation send to the next stage can be issued while
the current micro-batch's compute continues, and a tensor-parallel
all-gather can be started before the operation that consumes it.

What makes it worth stating separately is that the three axes contend for the
same links. A job running data, tensor and pipeline parallelism together has
three families of collective in flight, and overlapping each with compute in
isolation can still leave them serialised against each other. That is this
record's reasoning, not a measurement: no paper the record holds states it
or tests overlap on all three axes at once in training. CoCoNet's
pipeline schedule, which overlaps collectives across NVLink and InfiniBand
at once, is the nearest thing, and it is an inference result.

## Where it stops being free

The overlap needs something to hide behind, and the axes differ in how much
they have. Tensor-parallel collectives sit between two matmuls in the same
layer, so the window is small and the traffic large — which is why tensor
parallelism is kept inside a node. Pipeline sends are small and have a whole
micro-batch to hide behind. The data-parallel reduction has the entire
backward pass.

So this is a recommendation to overlap where a window exists, and a reminder
that whether one exists is a property of the axis, not of the effort put into
scheduling it.
