---
number: 91
status: 'Active'
title: 'Profile and optimize memory access patterns'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
published: '2020-06-01'
source:
- LIT-066
compared_against:
- SOTA-045
summary: >-
  Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).
---

# SOTA-091: Profile and optimize memory access patterns

## Source

Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).

## The claim this practice is the operational half of

[LIT-066](../literature.d/LIT-066.md)'s finding is that transformer training has become **memory-bound**,
and that the mental model stayed on FLOPs while compute throughput ran ahead
of bandwidth. That is a claim about where time goes, and it is only
actionable if you can see it — which is what this practice is for.

The measurement to make is not "how long did this kernel take" but "how many
bytes did it move, and how close is that to the device's peak bandwidth". A
kernel at 90% of peak bandwidth and 5% of peak FLOPs is finished; a kernel at
20% of both has a problem that fusion ([SOTA-088](SOTA-088.md)) or layout ([SOTA-090](SOTA-090.md)) can
fix. Kernel time alone cannot tell those apart, which is the same trap
[SOTA-045](SOTA-045.md) describes in the input pipeline.

## Condition

It applies wherever the operation is memory-bound, which after [LIT-066](../literature.d/LIT-066.md) is
most of a transformer outside the big matmuls. It says nothing useful about
the matmuls themselves, which are compute-bound and where the interesting
question is occupancy and tensor-core utilisation instead.

The cost is instrumentation and the discipline to look. The paper's own
contribution is a systematic recipe rather than an exhortation, and the record
holding it as "profile and optimize memory access patterns" keeps the
exhortation and drops the recipe.
