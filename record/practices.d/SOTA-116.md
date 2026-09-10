---
number: 116
status: 'Active'
title: 'Use FSDP over DDP when model size exceeds single GPU memory'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-083
extends:
- SOTA-030
summary: >-
  Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).
extended_by:
- SOTA-117
- SOTA-118
- SOTA-119
---

# SOTA-116: Use FSDP over DDP when model size exceeds single GPU memory

## Source

Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).

## The threshold in the title is the whole condition

DDP replicates the model on every rank, so the largest model it can train is
the largest that fits on one GPU alongside its gradients, optimizer state and
activations. Past that point no amount of adding ranks helps: each new rank
holds another full copy.

FSDP shards parameters, gradients and optimizer state across the group and
gathers each unit's parameters only for the moment it is being used, so the
resident footprint falls roughly with the group size. That is the same
partitioning ZeRO-3 describes ([SOTA-030](SOTA-030.md)); FSDP is its integration into
PyTorch, with the sharding expressed as a wrapping of module units rather
than as a separate runtime.

## Cost, and why the title says "when" rather than "always"

The parameters have to be gathered before each unit's forward and again for
its backward, then freed. That is communication DDP does not do, and on a
slow interconnect it is the step time. DDP's single all-reduce per step,
overlapped with the backward pass, is hard to beat when the model does fit.

So the recommendation is a threshold rather than a preference, and the
threshold is about *memory*, not model size in parameters: activations at
long context can put a model that nominally fits over the edge, and the same
model at short context back under it.
