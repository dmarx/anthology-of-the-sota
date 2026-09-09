---
number: 20
status: 'Active'
title: 'Use larger learning rates with batch normalization'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2018-06-01'
source:
- LIT-015
summary: >-
  Santurkar et al. (2018), [LIT-015](../literature.d/LIT-015.md) — [ARXIV-1806.02375](https://arxiv.org/abs/1806.02375).
---

# SOTA-020: Use larger learning rates with batch normalization

## Source

Santurkar et al. (2018), [LIT-015](../literature.d/LIT-015.md) — [ARXIV-1806.02375](https://arxiv.org/abs/1806.02375).

## This is [LIT-015](../literature.d/LIT-015.md)'s actual claim

Bjorck et al.'s argument is that permitting a much larger learning rate is
batch normalization's central benefit, and that most of the accuracy and
speed improvement follows from it rather than from normalisation as such.
Without BN, large rates at initialisation drive activations and gradients that
grow with depth, which is what makes them divergent; BN bounds them, so the
same rate becomes usable.

The practice is therefore not "BN lets you be sloppy about the learning rate"
but "BN moves the stable range upward, so a rate tuned for an unnormalised
network is leaving most of the benefit unused."

## Condition, and a correction to the record around it

Larger rates also carry their own regularising effect, which is part of why BN
is described as a regulariser — the regularisation is downstream of the rate,
not a separate property.

This practice was correctly sourced all along, which is the reason worth
recording: [LIT-015](../literature.d/LIT-015.md) carried the wrong author and the wrong takeaways until this
contribution, but the paper the identifier names really does argue this, and
SOTA-020 really does follow from it. The two practices beside it in the
<!-- inactive-ok-block: SOTA-021, SOTA-022 — the two retired beside this one; naming them is the point of the paragraph -->
cluster did not fare as well — [SOTA-021](SOTA-021.md) turns on a mechanism belonging to a
different paper, and [SOTA-022](SOTA-022.md) duplicates [SOTA-004](SOTA-004.md).
