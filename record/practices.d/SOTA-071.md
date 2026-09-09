---
number: 71
status: 'Active'
title: 'Use gradient clipping with dynamic threshold'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2022-10-01'
source:
- LIT-054
summary: >-
  Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).
---

# SOTA-071: Use gradient clipping with dynamic threshold

## Source

Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).

## Clipping, and what "dynamic threshold" is doing

Clipping rescales the gradient when its global norm exceeds a threshold, so a
single anomalous batch cannot take a step large enough to leave the basin the
run is in. That is the standard fixed-threshold practice ([SOTA-035](SOTA-035.md)) and it is
not what this one adds.

The addition is that the threshold should track the run rather than being set
once. Gradient norms fall by orders of magnitude over training, so a
threshold chosen at step 1000 clips nothing by step 100,000 — the mechanism
is still configured and no longer does anything. Deriving it from a running
quantile of recent norms keeps the clip rate roughly constant instead.

## The cost, which is a real one

A threshold that adapts to the gradient norms will adapt to a *rising* one,
which is exactly the situation it was meant to catch. A run drifting into
instability raises its own threshold and clips nothing, and the failure is
silent because the clip rate — the metric you would watch — stays where it
always was.

So the adaptive form wants a ceiling, or a slow enough window that a fast
excursion still trips it. Neither [LIT-054](../literature.d/LIT-054.md) nor this record states one, which
is worth saying: the practice as written names a mechanism whose most
important parameter it does not give.
