---
number: 83
status: 'Active'
title: 'Implement custom kernels for critical ops'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
published: '2018-02-01'
source:
- LIT-063
summary: >-
  Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).
---

# SOTA-083: Implement custom kernels for critical ops

## Source

Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).

## This is the practice its source argues against

[LIT-063](../literature.d/LIT-063.md)'s premise is that hand-optimisation does not scale. Frameworks lean
on vendor-specific operator libraries tuned for a narrow range of server-class
GPUs, so every new target — mobile, embedded, FPGA, ASIC — costs a manual
re-optimisation, and TVM exists to replace that manual work with a compiler
and a search.

"Implement custom kernels for critical ops" is the manual work. Citing this
paper for it credits the argument to the position it was written against.

## What survives, and what it should say

Something real does survive, and it is narrower: **there are operations no
compiler covers well, and for those a hand-written kernel is still the
answer.** The fused attention kernels in [SOTA-085](SOTA-085.md) and [SOTA-106](SOTA-106.md) are exactly
that case, and they are hand-written for reasons a search does not reach —
the algorithm is different, not just the schedule.

So the honest form is a fallback rather than a default: automate first,
measure, and hand-write the few operations where the generated code is
materially short of what the hardware can do. Stated as a general
recommendation with TVM as its source, it inverts both halves.

Flagged rather than retired: unlike [SOTA-055](SOTA-055.md), the recommendation is not
*wrong*, it is mis-framed and mis-cited. Retiring it would lose the real
narrow claim, and rewriting the title changes what it asserts — which is a
call for its own contribution.
