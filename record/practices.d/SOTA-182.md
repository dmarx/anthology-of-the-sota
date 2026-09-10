---
number: 182
status: Active
formerly:
- SOTA-tmp5bfj6
title: 'Compute the normalization statistic without centering (RMSNorm)'
version: 1
tags:
- model-stability
consensus: universal
date: '2026-09-08'
published: '2019-10-01'
source:
- LIT-023
implementations:
- llama2
summary: >-
  Zhang and Sennrich (2019), [LIT-023](../literature.d/LIT-023.md) — [ARXIV-1910.07467](https://arxiv.org/abs/1910.07467). Drop the mean
  subtraction from layer normalization and rescale by the root mean square
  alone.
compared_against:
- SOTA-191
---

# SOTA-182: Compute the normalization statistic without centering (RMSNorm)

## Source

Zhang and Sennrich (2019), [LIT-023](../literature.d/LIT-023.md) — [ARXIV-1910.07467](https://arxiv.org/abs/1910.07467).

## What it drops

Layer normalization does two things to a vector: re-centers it on its mean
and re-scales it by its standard deviation. RMSNorm keeps only the second,
dividing by the root mean square and learning a gain. The paper's claim is
that the re-scaling is what buys the stability and the re-centering is
close to free to drop — the same convergence, 7–64% less time per step in
the settings it measures.

## Independent of placement

This is independent of where the normalization sits. Centering and placement are
separate choices, and this practice is about the statistic; [SOTA-032](SOTA-032.md) is
about the position. Nothing stops a Post-LN model from using RMSNorm, and
GPT-2 is Pre-LN with full LayerNorm.

## Why `universal`

In the record's modern half a
model using centered LayerNorm is the one that would need to explain
itself.

## Known implementations

- llama2, and effectively every open-weight decoder since
