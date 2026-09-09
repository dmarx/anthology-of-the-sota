---
number: 44
status: 'Active'
title: 'Pin memory for CPU-GPU transfers'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2020-07-01'
source:
- LIT-050
summary: >-
  Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).
---

# SOTA-044: Pin memory for CPU-GPU transfers

## Source

Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).

## What pinning actually buys

Pageable host memory cannot be the source of an asynchronous DMA transfer:
the driver has to stage it through an internal pinned buffer first, so the
copy is synchronous from the program's point of view and cannot overlap with
compute. Allocating the staging buffer as page-locked from the start removes
the extra copy and lets the transfer run on a separate stream while the GPU
is still working on the previous batch.

For an input pipeline that is already close to keeping up, that overlap is
the difference between a small stall per step and none.

## The cost is real and is a system-wide one

Pinned pages cannot be swapped or moved. Pinning aggressively — many worker
processes each with a large prefetch depth — takes memory away from the page
cache that the same pipeline depends on for repeat reads ([SOTA-042](SOTA-042.md)), and on a
shared machine it takes it away from other jobs. The failure is not an error;
it is the loader getting slower for reasons that do not appear in its own
metrics.

So this is a default worth having and not a knob worth maximising, and
whether it is helping at all is a question for [SOTA-045](SOTA-045.md)'s measurement rather
than for argument.
