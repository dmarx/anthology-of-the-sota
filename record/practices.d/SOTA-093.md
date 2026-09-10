---
number: 93
status: 'Active'
title: 'larger batch sizes are beneficial later in training due to better gradient estimates'
version: 1
tags:
- model-architecture
date: '2026-08-24'
source:
- LIT-069
compared_against:
- SOTA-092
- SOTA-094
- SOTA-031
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-093: larger batch sizes are beneficial later in training due to better gradient estimates

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

## Known implementations

- PaLM

## The other end of [SOTA-092](SOTA-092.md)'s curve

As the model improves, the gradient's useful component shrinks relative to
its noise, so averaging more samples buys a more accurate step where before
it bought a redundant one. Past that point the larger batch is strictly
better per step and the question becomes whether the extra samples are worth
their wall-clock.

The two halves together are the empirical content of critical batch size: a
threshold below which more samples help and above which they mostly do not,
which moves upward through training.

## Condition, and the thing to hold fixed

Growing the batch changes the effective learning rate per sample, so a ramp
that does not adjust the schedule alongside it is running a different
optimisation problem after the change than before. That interaction is the
usual reason a ramp underperforms in practice, and neither this practice nor
[SOTA-092](SOTA-092.md) mentions it.

Under gradient accumulation the ramp is nearly free — more micro-batches per
step rather than more memory ([SOTA-031](SOTA-031.md)) — which is worth knowing, because it
makes the recommendation actionable on fixed hardware rather than only on a
bigger cluster.
