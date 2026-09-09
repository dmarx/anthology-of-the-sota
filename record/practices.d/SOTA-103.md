---
number: 103
status: 'Active'
title: 'Adjust mixing ratios based on validation performance'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2023-12-01'
source:
- LIT-117
compared_against:
- SOTA-102
summary: >-
  Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).
---

# SOTA-103: Adjust mixing ratios based on validation performance

## Source

Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).

## Close to the source, and wrong about where the signal comes from

[LIT-117](../literature.d/LIT-117.md)'s loop does adjust mixing ratios from a measured signal, which is the
half this gets right. The signal is not validation performance: it is
perplexity on the training batches the run is already taking, which is the
entire point of the method's efficiency claim. Adding a validation pass per
domain per update is exactly the cost ODM exists to avoid.

The distinction matters because it changes what the practice costs. A
validation-driven loop needs held-out data per domain and a forward pass over
it at every adjustment, which is expensive enough that the interval becomes
coarse — and a coarse interval cannot track a quantity that moves during
training. An online reward has no such tension.

## What survives

The recommendation, restated: **adjust mixing ratios continuously from a
signal you are already computing.** Validation is the natural-seeming choice
and the wrong one, for a reason worth writing down rather than discovering.

With [SOTA-102](SOTA-102.md) this is one practice split in two — one naming a knob the
source does not use, one naming the right loop with the wrong input. They
want merging into a single practice describing ODM, which is a restatement
rather than a body, and belongs in its own contribution.
