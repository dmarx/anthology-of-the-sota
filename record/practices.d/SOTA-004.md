---
number: 4
status: 'Active'
title: 'Place BatchNorm after linear/conv layers but before activation functions'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2015-02-01'
source:
- LIT-002
summary: >-
  Ioffe et al. (2015), [LIT-002](../literature.d/LIT-002.md) — [ARXIV-1502.03167](https://arxiv.org/abs/1502.03167).
compared_against:
- SOTA-006
---

# SOTA-004: Place BatchNorm after linear/conv layers but before activation functions

## Source

Ioffe et al. (2015), [LIT-002](../literature.d/LIT-002.md) — [ARXIV-1502.03167](https://arxiv.org/abs/1502.03167).

## Why before the activation

Batch normalization standardises its input to zero mean and unit variance,
then applies a learned scale and shift. Placed between the linear map and the
nonlinearity, it acts on the pre-activation distribution — which is what
keeps the nonlinearity operating in its useful range rather than saturated,
and is the placement [LIT-002](../literature.d/LIT-002.md) introduces and evaluates.

Placed *after* the activation it standardises a distribution the nonlinearity
has already shaped — a ReLU's output is non-negative, so forcing zero mean
undoes what the unit just did.

## Condition, and what happened to this practice since

It is a claim about convolutional networks with batch normalization, which is
the setting [LIT-002](../literature.d/LIT-002.md) is about, and both halves of that have moved. Transformers
use LayerNorm or RMSNorm ([SOTA-006](SOTA-006.md)), where the placement question is a
different one — inside or outside the residual branch ([SOTA-032](SOTA-032.md)) — and the
modern answer there is pre-norm, which is *not* the analogue of this rule.

The bias term in the preceding linear layer also becomes redundant, since
normalisation removes any constant offset before the learned shift restores
one. Omitting it costs nothing and is the usual convention.

<!-- inactive-ok: SOTA-022 — Superseded by this practice, and named as the duplicate it is -->
[SOTA-022](SOTA-022.md) states this same rule from a different source and is superseded by
this practice.
