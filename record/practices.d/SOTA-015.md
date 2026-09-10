---
number: 15
status: 'Active'
title: 'Store optimizer states in FP32'
version: 1
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-011
extends:
- SOTA-014
summary: >-
  Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).
---

# SOTA-015: Store optimizer states in FP32

## Source

Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).

## Condition

Same argument as [SOTA-014](SOTA-014.md), one level down: Adam's second moment is a running
average of squared gradients, so it spans a far wider dynamic range than the
weights do, and FP16 cannot hold it. The exponent range runs out before the
mantissa does — small squared gradients flush to zero, ε stops doing its job,
and the effective step size drifts.

## Cost, and what has changed since

8 bytes per parameter for Adam's two moments, on top of the 4 for the master
weights. That is the 12 bytes of optimizer state per parameter that dominates
the memory of a data-parallel run and that ZeRO ([LIT-027](../literature.d/LIT-027.md)) exists to
partition — the reason [SOTA-028](SOTA-028.md) buys as much as it does is that this practice
is being followed.

This is the part of the mixed-precision recipe most actively contested since.
Eight-bit optimizer states, and stochastic rounding in place of
round-to-nearest, both recover most of the memory while holding accuracy on
many workloads. The practice as stated is the conservative default, not a
settled bound.
