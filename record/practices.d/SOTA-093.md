---
number: 93
status: 'Active'
title: 'larger batch sizes are beneficial later in training due to better gradient estimates'
version: 1
tags:
# Retagged from the report of unbound lineage. `training-optimization` names
# batch size in its blurb. It carried `model-architecture` because its source
# is a model report, which is where it was found rather than what it is about.
- training-optimization
date: '2026-08-24'
source:
# LIT-017 added in the correction pass: PaLM states this and cites it, and
# McCandlish et al. are who measured it (noise scale rising through
# training, their Fig. 5).
- LIT-069
- LIT-017
introduced_by:
# Was LIT-069. PaLM credits the observation to Smith et al. (2018) and
# McCandlish et al. (2018). Smith et al. (arXiv 1711.00489) recommend
# growing the batch as a substitute for learning-rate decay, an annealing
# argument that says nothing about sample efficiency or gradient estimates,
# so it is not filed as the origin. McCandlish et al. state this in words.
- LIT-017
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-093: larger batch sizes are beneficial later in training due to better gradient estimates

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

McCandlish et al. (2018), [LIT-017](../literature.d/LIT-017.md) — [ARXIV-1812.06162](https://arxiv.org/abs/1812.06162).

## Known implementations

- PaLM

## The other end of [SOTA-092](SOTA-092.md)'s curve

As the model improves, the gradient's useful component shrinks relative to
its noise, so averaging more samples buys a more accurate step where before
it bought a redundant one. Past that point the larger batch is strictly
better per step and the question becomes whether the extra samples are worth
their wall-clock.

In [LIT-069](../literature.d/LIT-069.md) this is the second clause of the same sentence as [SOTA-092](SOTA-092.md):
PaLM 540B's batch doubles at step 50k and again at step 115k, from 1M to 4M
tokens, because larger batches are "beneficial later in training due to
better gradient estimates". The paper cites Smith et al. (2018) and
McCandlish et al. (2018) for that and does not test it.

The record names McCandlish et al., [LIT-017](../literature.d/LIT-017.md), as the origin, and as the
evidence. "Better gradient estimates" is their gradient noise scale: the
ratio of the per-example gradient variance to the squared true gradient,
which sets the batch size past which more samples stop speeding up training.
They measured it rising through training, tracking a critical batch size
that grows by an order of magnitude or more over a run, and analysed growing
the batch to follow it. Smith
et al. (arXiv 1711.00489), PaLM's other citation, also grow the batch late in
training, but their reason is that doing so anneals SGD's noise the way a
learning-rate decay does, not that the gradient estimate gets more valuable;
it is a different recommendation and is not filed here.

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
