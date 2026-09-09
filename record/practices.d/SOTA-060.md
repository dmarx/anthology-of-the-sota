---
number: 60
status: 'Active'
title: 'Initialize layer norms with smaller variance (0.02) for stability'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2021-04-01'
source:
- LIT-043
summary: >-
  Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).
compared_against:
- SOTA-051
---

# SOTA-060: Initialize layer norms with smaller variance (0.02) for stability

## Source

Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).

## What the smaller variance is protecting against

The residual stream accumulates the output of every layer, so its variance
grows with depth unless something holds it down. Initialising the output
projection of each block with a smaller standard deviation — scaled down by
the number of layers — keeps each block's contribution small relative to what
is already in the stream, so the signal at the top of a deep model is not
dominated by initialisation noise.

That is the same reasoning that puts a 1/√(2·n_layers) factor on the output
projections in GPT-2-style initialisations, and the same problem ReZero
([SOTA-051](SOTA-051.md)) attacks by starting the residual branch at literally zero.

## What the title gets wrong

It says "layer norms", and the initialisation that matters here is the
*output projections* of the attention and MLP blocks. LayerNorm's own
parameters are conventionally initialised to weight 1 and bias 0 — which is
what [SOTA-025](SOTA-025.md) and [SOTA-026](SOTA-026.md) say, and 0.02 is not that.

0.02 is also a familiar number for a different reason: it is the standard
deviation of the normal distribution GPT-2 and its descendants use to
initialise *all* weights, before the depth scaling is applied on top. Two
distinct conventions have been merged into one sentence.

Flagged rather than rewritten: fixing it means deciding which of the two the
practice is about, which changes what it claims.
