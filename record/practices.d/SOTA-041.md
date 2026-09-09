---
number: 41
status: 'Active'
title: 'lr tuning less important for larger models'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2020-01-01'
source:
- LIT-028
compared_against:
- SOTA-040
summary: >-
  Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).
---

# SOTA-041: lr tuning less important for larger models

## Source

Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).

## Why sensitivity falls with scale

The power-law fits in [LIT-028](../literature.d/LIT-028.md) flatten near the optimum as model size grows:
the loss penalty for being some factor away from the best learning rate is
smaller for a larger model than for a smaller one. So a rate tuned at one
scale is less wrong at the next, and the sweep that a small model needs is
worth less on a large one.

This is the observation that made large-model hyperparameter practice
tractable at all, and it is the empirical ancestor of a stronger idea the
<!-- inactive-ok-block: SOTA-144, SOTA-159 — Proposed, cited as the µP line this observation is the empirical ancestor of -->
record holds elsewhere: µP ([SOTA-144](SOTA-144.md), [SOTA-159](SOTA-159.md)) makes transfer a property of
the parameterisation rather than a lucky flatness, so the rate is measured on
a small proxy and carried over by construction.

## What it should not be read as

Not "large models do not need tuning". The penalty for a badly wrong rate is
still large, and the cost of a wrong choice is far higher at scale because
there is no second run. Less sensitive is not insensitive.

And the claim is about the *learning rate*, not about hyperparameters
generally. Batch size ([SOTA-062](SOTA-062.md)), weight decay and the schedule shape
([SOTA-140](SOTA-140.md)) do not obviously inherit it, and the record has no source saying
they do.
