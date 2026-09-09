---
number: 99
status: 'Active'
title: 'Track gradient norm statistics to detect training instabilities'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2022-10-01'
source:
- LIT-054
compared_against:
- SOTA-070
summary: >-
  Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).
---

# SOTA-099: Track gradient norm statistics to detect training instabilities

## Source

Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).

## Overlap with [SOTA-070](SOTA-070.md), stated plainly

This and [SOTA-070](SOTA-070.md) are the same recommendation at different resolutions:
track gradient norms to detect instability, per layer there and in aggregate
here. Both are sourced to [LIT-054](../literature.d/LIT-054.md) and both arrived in the same import.

The distinct content is the aggregate statistic itself — the global norm,
which is what clipping already computes ([SOTA-071](SOTA-071.md)), so on a run that clips
the signal is free. Its usefulness is in the trend rather than the value: a
norm that has been falling for 50,000 steps and turns upward is the earliest
of the signals in this cluster, ahead of the loss spike that [SOTA-098](SOTA-098.md) watches
for and well ahead of the NaN that [SOTA-072](SOTA-072.md) catches.

## Standing

Kept rather than merged into [SOTA-070](SOTA-070.md), because the free-with-clipping
aggregate and the deliberate per-layer pass are genuinely different in cost.
But the record should not pretend they are independent findings: they are one
paper's stability section split into bullets, which is the pattern [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) is
about.
