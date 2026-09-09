---
number: 74
status: 'Active'
title: 'Adapt buffer sizes to network conditions'
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

# SOTA-074: Adapt buffer sizes to network conditions

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## The same gap as [SOTA-073](SOTA-073.md), one step further

"Adapt buffer sizes to network conditions" names a mechanism nobody in the
record has and no source here describes. Adapting implies a controller — a
signal, a target, an update rule — and none of the three is stated. Without
them it is a wish rather than a practice.

There is a real version of it, and it is worth naming so the restatement has
somewhere to go: the fusion-buffer trade in [SOTA-048](SOTA-048.md) has an optimum that
depends on the fabric, so a system that measures achieved bandwidth during
the overlap window and adjusts the bucket size is doing something specific
and testable. That is closer to what CheckFreq does for checkpoint intervals
([SOTA-054](SOTA-054.md)'s source) than to anything in [LIT-051](../literature.d/LIT-051.md).

[LIT-051](../literature.d/LIT-051.md) does not support this. Its contribution is described under [SOTA-047](SOTA-047.md).

## Standing

Flagged for restatement or retirement, together with [SOTA-073](SOTA-073.md), [SOTA-049](SOTA-049.md) and
[SOTA-076](SOTA-076.md) — four of the seven practices in this cluster are in the same
position, which is what makes it a cluster-level problem rather than four
separate ones.
