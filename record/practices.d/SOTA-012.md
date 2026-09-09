---
number: 12
status: 'Active'
title: 'sharpness in the loss landscape correlates with test error'
version: 2
history:
- version: 1
  note: >-
    Titled "sharpness in loss landscape corerlates with test error" — a typo in
    the claim itself, carried since the migration.
- version: 2
  note: >-
    Spelling corrected. The claim is unchanged; this is not a restatement, and
    is recorded only because a title is the thing citations resolve against.
tags:
- training-optimization
date: '2026-08-24'
published: '2017-12-01'
source:
- LIT-014
compared_against:
- SOTA-010
- SOTA-011
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).
---

# SOTA-012: sharpness in the loss landscape correlates with test error

## Source

Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).

## The correlation, and what it is not

[LIT-014](../literature.d/LIT-014.md) visualises the loss surface around trained minima by filter-normalised
random directions, and the visible regularity is that solutions sitting in
wide, flat basins generalise better than solutions in sharp ones. The
filter normalisation is what makes the comparison meaningful — without it,
rescaling a network's weights changes the apparent sharpness without changing
the function at all, which is how earlier sharpness claims were shown to be
artefacts.

So the practice is a diagnostic reading rather than an objective: sharpness is
*correlated* with test error across the architectures and training
configurations examined, and the paper does not establish that flattening a
minimum causes better generalisation.

## Why the distinction matters here

Methods that optimise for flatness directly — sharpness-aware minimisation and
its relatives — exist and sometimes help, and they are a different claim with
their own evidence, which this record does not currently hold.

Reading this practice as "make the minimum flatter and the model generalises"
is the failure it invites. What it supports is narrower and still useful: a
model whose basin is visibly sharp is worth suspecting, and a change that
sharpens the landscape (removing skip connections, per [SOTA-010](SOTA-010.md), or raising
depth without them) has a known cost that shows up in the surface before it
shows up in the metric.
