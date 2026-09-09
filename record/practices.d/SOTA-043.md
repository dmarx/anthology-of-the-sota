---
number: 43
status: 'Active'
title: 'Use mixed precision during data loading'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2020-07-01'
source:
- LIT-050
summary: >-
  Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).
---

# SOTA-043: Use mixed precision during data loading

## Source

Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).

## What this practice would mean

Decoding and augmenting into half precision on the host, so that what crosses
the bus is half the bytes and no cast is needed on the far side. Where the
step already runs in mixed precision ([SOTA-016](SOTA-016.md)) the conversion has to happen
somewhere, and doing it before the transfer rather than after is free.

## The source does not carry this one

[LIT-050](../literature.d/LIT-050.md)'s contribution is the measurement of data stalls and three
mitigations in CoorDL — caching, coordinated prefetch across jobs, and
avoiding redundant preprocessing. Half-precision decode is not among them,
and the note's own summary of the paper does not mention it.

The recommendation may well be right; what it lacks is this paper as
evidence for it. Recorded as a citation to check rather than a body making a
case, because the alternative is a body that reasons from a source that does
not say what it is credited with — which is the failure the whole worklist in
[#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) exists to find.

Two things would settle it: a source that actually measures the transfer
saving, or the observation that on a pipeline whose stall is decode-bound
rather than bandwidth-bound the practice buys nothing, in which case the
condition belongs in the title.
