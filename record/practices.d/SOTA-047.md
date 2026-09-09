---
number: 47
status: 'Active'
title: 'Overlap communication with backward pass'
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

# SOTA-047: Overlap communication with backward pass

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## The practice is right, and this is not where it comes from

Gradients become available in reverse layer order as the backward pass runs,
so the gradient for the last layer is ready long before the first layer's is
computed. Waiting for the whole backward pass and then reducing everything
leaves the network idle throughout the backward and the GPU idle throughout
the reduction. Issuing each layer's reduction as its gradient lands overlaps
the two, and on a well-tuned job most of the communication disappears behind
compute.

That is correct, and it is the foundation the rest of this cluster builds on.
It is also standard practice since well before [LIT-051](../literature.d/LIT-051.md) — it is what
Horovod and PyTorch's DistributedDataParallel do by default, and the
technique predates both.

## What [LIT-051](../literature.d/LIT-051.md) actually contributes

BytePS's argument is that all-reduce and parameter-server are two special
cases of one optimal communication framework for a cluster with spare CPU and
network capacity, and that reaching that optimum means splitting the
optimizer: a *Summation Service* on CPUs for the part every optimizer shares,
with the model-dependent step left on the GPUs. Its headline results are up
to 84% over the best open-source all-reduce and 245% over the best PS.

Overlapping communication with the backward pass is assumed by that work, not
introduced by it. The citation is not wrong so much as not load-bearing, and
the record should say which it is.

## The cost, since the title does not

The overlap is what makes the *bucket size* a tuning parameter: reduce too
eagerly and each collective is too small to reach peak bandwidth; too lazily
and there is nothing left to hide the last one behind. That trade is the real
content of [SOTA-048](SOTA-048.md) and [SOTA-049](SOTA-049.md).
