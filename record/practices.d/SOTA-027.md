---
number: 27
status: 'Active'
title: 'Use a smaller learning rate for LayerNorm parameters'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2019-11-01'
source:
- LIT-025
summary: >-
  Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — [ARXIV-1911.07013](https://arxiv.org/abs/1911.07013).
---

# SOTA-027: Use a smaller learning rate for LayerNorm parameters

## Source

Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — [ARXIV-1911.07013](https://arxiv.org/abs/1911.07013).

## Why the norm parameters might want a different rate

LayerNorm's scale and bias are few, they are shared across every position in
a sequence, and they multiply rather than add to the representation — so a
step that is small for a weight matrix can be large in its effect here. The
argument for a reduced rate is that these parameters need less movement to do
their job and that overshooting them destabilises everything downstream.

The same reasoning produces the more common modern convention, which is not
a different rate but **no weight decay** on norm parameters and biases:
decaying a scale toward zero is decaying the network toward passing nothing
through, which is not what regularisation is for.

## The record cannot support the rate half

"Smaller" is not a number, and [LIT-025](../literature.d/LIT-025.md) is an analysis of LayerNorm's gradients
rather than a sweep over per-parameter-group learning rates. Nothing here says
how much smaller, or that a separate rate beats a single global one at all.

What large runs actually do is the excluded-from-weight-decay convention
<!-- inactive-ok-block: SOTA-144, SOTA-159 — Proposed, cited as the µP line whose per-group scaling is better evidenced than this practice's -->
above, and — under µP ([SOTA-144](SOTA-144.md), [SOTA-159](SOTA-159.md)) — a principled per-group scaling
that falls out of the parameterisation rather than being tuned. Both are
better-evidenced than this practice, and both are elsewhere in the record.

Flagged for restatement: the durable claim is *treat norm parameters as their
own group*, of which the rate is one instance and weight decay the one that
matters more. As written it recommends the weaker half with no quantity.
