---
number: 57
status: 'Active'
title: 'Implement multi-level checkpoint strategy'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2021-02-01'
source:
- LIT-059
summary: >-
  Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.
---

# SOTA-057: Implement multi-level checkpoint strategy

## Source

Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.

## What the practice means

Keeping checkpoints at more than one tier — a frequent, cheap one to local
NVMe or host memory for the common case of a single-node failure, and a rarer
durable one to shared storage for the case that loses the node. The recovery
time and the cost per checkpoint differ by orders of magnitude between the
tiers, so writing every checkpoint to the durable tier pays the worst price
for the commonest failure.

## The source is thin for it

[LIT-059](../literature.d/LIT-059.md)'s mechanisms are two-phase checkpointing ([SOTA-056](SOTA-056.md)), profiling-derived
frequency ([SOTA-054](SOTA-054.md)) and a resumable data loader. A storage hierarchy is not
among them; the paper's overhead result comes from pipelining the write, not
from writing it somewhere cheaper.

The recommendation is standard in large-scale training systems and is
probably right. What it does not have is this paper as its evidence, and the
record cannot currently say who does support it.

## What [LIT-059](../literature.d/LIT-059.md) does say that the record has missed

The paper's correctness point has no practice at all: **resuming must
preserve the invariant that each item is seen exactly once per epoch, which
means checkpointing the data loader's state and not just the model and
optimizer.** That is the detail the paper says most implementations get
wrong, it is actionable, and it is absent from a cluster of four practices
drawn from this paper — which says something about how the four were
produced.
