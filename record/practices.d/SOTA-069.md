---
number: 69
status: 'Active'
title: 'Monitor exp(loss) for stability'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2022-10-01'
source:
- LIT-054
summary: >-
  Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).
compared_against:
- SOTA-098
---

# SOTA-069: Monitor exp(loss) for stability

## Source

Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).

## Why the exponential, and not the loss

A language model's loss is a log quantity, so a spike that matters is
compressed on the axis you are watching. `exp(loss)` is perplexity, and it is
the scale on which the same event is visible: a loss moving from 2.5 to 2.9
looks like noise and is a perplexity moving from 12 to 18.

That is the whole content of the practice, and it is a monitoring choice
rather than a training one — the run is not changed, only what the operator
can see in time to act.

## Condition and limits

It helps for spike *detection* and not much else. Perplexity is unusable for
comparing models at different vocabularies or tokenisations, and past the
early part of training the interesting movements are small enough that either
scale shows them.

The practice belongs with the rest of [LIT-054](../literature.d/LIT-054.md)'s stability set — [SOTA-070](SOTA-070.md)'s
per-layer gradient norms, [SOTA-071](SOTA-071.md)'s clipping, [SOTA-098](SOTA-098.md)'s validation-loss
watch — and none of them is worth much alone. What the paper actually
describes is an operator watching several signals with a rehearsed response
([SOTA-095](SOTA-095.md)'s rewind), which is a *procedure*, and the record has it split into
four monitoring bullets with the procedure missing.
