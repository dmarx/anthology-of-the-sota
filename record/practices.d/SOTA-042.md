---
number: 42
status: 'Active'
title: 'Memory-map large datasets'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
source:
- LIT-050
summary: >-
  Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).
---

# SOTA-042: Memory-map large datasets

## Source

Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).

## What it buys, and the failure it does not prevent

Memory-mapping hands the file to the page cache instead of reading it through
userspace buffers, so a second pass over an item that is still resident costs
no I/O and no copy. For a dataset that fits in RAM this is most of the
benefit available.

The important qualifier is what [LIT-050](../literature.d/LIT-050.md) found about the case where it does
*not* fit. Training reads items in a fresh random order every epoch, which is
close to the worst access pattern for an LRU cache: by the time an item comes
round again it has been evicted, so a dataset moderately larger than memory
thrashes and the cache does almost nothing. The paper's answer is to cache a
**fixed** subset and read the rest from storage every epoch — deliberately
never evicting — which beats the OS policy precisely because it stops
pretending the whole dataset is cacheable.

## Condition

So the practice holds cleanly while the working set fits, and past that point
it needs the fixed-subset discipline to be worth anything. Whether you are
past that point is [SOTA-045](SOTA-045.md)'s measurement, not a guess from the dataset size:
what matters is the resident working set after the loader's own pinned
buffers ([SOTA-044](SOTA-044.md)) have taken their share.

Memory-mapping also does nothing for per-item decode cost, which for image
and audio pipelines is usually the larger half of the stall.
