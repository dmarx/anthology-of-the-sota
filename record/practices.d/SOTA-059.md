---
number: 59
status: 'Active'
title: 'Overlap communication with computation when possible'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-043
summary: >-
  Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).
---

# SOTA-059: Overlap communication with computation when possible

## Source

Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).

## The same principle as [SOTA-047](SOTA-047.md), at a different layer

[SOTA-047](SOTA-047.md) overlaps the data-parallel gradient reduction with the backward
pass. This is the same move applied to the other two axes of a 3D-parallel
job: a pipeline stage's activation send to the next stage can be issued while
the current micro-batch's compute continues, and a tensor-parallel
all-gather can be started before the operation that consumes it.

What makes it worth stating separately is that the three axes contend for the
same links. A job running data, tensor and pipeline parallelism together has
three families of collective in flight, and overlapping each with compute in
isolation can still leave them serialised against each other.

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
