---
number: 26
status: 'Active'
title: 'Initialize LayerNorm bias to 0'
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

# SOTA-026: Initialize LayerNorm bias to 0

## Source

Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — [ARXIV-1911.07013](https://arxiv.org/abs/1911.07013).

## Zero is the identity here too

The bias is added after the normalised activation is scaled, so initialising
it to zero means the layer starts as pure normalisation-and-scale with no
offset. Any other starting value asserts a preferred direction in feature
space before training has said anything, which is the thing initialisation
schemes generally try to avoid.

There is no interesting trade here, which is worth stating plainly: this is a
convention with no live alternative, and the practice's value is as a
statement of what the default is rather than as advice between options.

## Where it stops applying

RMSNorm has no bias at all. It normalises by root-mean-square without
centring, on the finding that the mean subtraction contributes little, and
drops both the centring and the offset — so in the models this record mostly
concerns itself with ([SOTA-006](SOTA-006.md)), there is no parameter for this practice to
initialise.

Kept rather than retired because BatchNorm and LayerNorm are both still in
use and the convention is real. But it is a practice about a component the
frontier has largely moved past, which the record should say rather than
leave the reader to infer from its absence elsewhere.
