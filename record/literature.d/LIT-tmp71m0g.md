---
status: 'Deferred'
title: 'Smoothing DiLoCo with Primal Averaging for Faster Training of LLMs'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2025-12-01'
arxiv: '2512.17131'
first_author: 'Defazio'
keywords:
- 'primal-averaging'
- 'diloco'
- 'outer-optimizer'
- 'low-communication'
implementations: []
summary: >-
  Defazio et al. (2025), [ARXIV-2512.17131](https://arxiv.org/abs/2512.17131). Replace DiLoCo's outer optimizer
  with primal averaging, making the smoothing strength a continuous
  hyperparameter independent of the inner step count.
---
# LIT-tmp71m0g: Smoothing DiLoCo with Primal Averaging for Faster Training of LLMs

Defazio et al. (2025) — [ARXIV-2512.17131](https://arxiv.org/abs/2512.17131)

## What it is

Replace DiLoCo's outer optimizer with primal averaging, making the smoothing
strength a continuous hyperparameter independent of the inner step count.

From the paper's own abstract:

> We propose Generalized Primal Averaging (GPA), an extension of
> Nesterov's method that unifies and generalizes recent averaging-based
> optimizers like single-worker DiLoCo and Schedule-Free, within a non-
> distributed setting. While DiLoCo relies on a memory-intensive two-loop
> structure to periodically aggregate pseudo-gradients using Nesterov
> momentum, GPA eliminates this complexity by decoupling Nesterov's
> interpolation constants to enable smooth iterate averaging at every
> step. Structurally, GPA resembles Schedule-Free but replaces uniform
> averaging with exponential moving averaging.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.

