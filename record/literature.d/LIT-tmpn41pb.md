---
status: 'Deferred'
title: 'Overlap Local-SGD: An Algorithmic Approach to Hide Communication Delays in Distributed SGD'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2020-02-01'
arxiv: '2002.09539'
first_author: 'Wang'
keywords:
- 'local-sgd'
- 'communication-overlap'
- 'anchor-momentum'
implementations: []
summary: >-
  Wang et al. (2020), [ARXIV-2002.09539](https://arxiv.org/abs/2002.09539). Overlap Local-SGD hides the averaging
  latency behind local computation using an anchor model, so small H becomes
  affordable.
---
# LIT-tmpn41pb: Overlap Local-SGD: An Algorithmic Approach to Hide Communication Delays in Distributed SGD

Wang et al. (2020) — [ARXIV-2002.09539](https://arxiv.org/abs/2002.09539)

## What it is

Overlap Local-SGD hides the averaging latency behind local computation using
an anchor model, so small H becomes affordable.

From the paper's own abstract:

> Distributed stochastic gradient descent (SGD) is essential for scaling
> the machine learning algorithms to a large number of computing nodes.
> However, the infrastructures variability such as high communication
> delay or random node slowdown greatly impedes the performance of
> distributed SGD algorithm, especially in a wireless system or sensor
> networks. In this paper, we propose an algorithmic approach named
> Overlap-Local-SGD (and its momentum variant) to overlap the
> communication and computation so as to speedup the distributed training
> procedure.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.

