---
number: 79
status: 'Active'
title: 'Pre-fetch next batch during compute'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
source:
- LIT-053
extends:
- SOTA-077
compared_against:
- SOTA-047
summary: >-
  Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).
---

# SOTA-079: Pre-fetch next batch during compute

## Source

Aizman et al. (2020), [LIT-053](../literature.d/LIT-053.md) — [ARXIV-2001.01858](https://arxiv.org/abs/2001.01858).

## The other half of every overlap in this record

Prefetching is [SOTA-047](SOTA-047.md)'s principle applied to the input pipeline: work that
does not depend on the current step should be running during it. The next
batch's read, decode and collation are exactly that, so a loader that starts
them while the GPU is busy turns a serial fetch-then-compute loop into two
overlapping ones.

It is what makes a streaming format work at all ([SOTA-077](SOTA-077.md)): sequential reads
are only fast if somebody is reading ahead.

## The parameter, and the cost that is easy to miss

Depth. One batch ahead hides one batch's latency and no more, and a pipeline
with occasional slow items — a large image, a shard boundary, a cold read —
needs enough depth to absorb the worst case rather than the average. Beyond
that, depth is memory: every prefetched batch is resident, and in a pinned
loader ([SOTA-044](SOTA-044.md)) it is pinned memory, which competes with the page cache the
same pipeline depends on ([SOTA-042](SOTA-042.md)).

The failure mode is the one [SOTA-045](SOTA-045.md) exists for. Prefetch depth cannot fix a
pipeline whose steady-state throughput is below the GPU's demand — it only
hides variance. A loader that is genuinely too slow looks, from the outside,
exactly like one that needs more depth, and the difference is visible only in
the measurement.
