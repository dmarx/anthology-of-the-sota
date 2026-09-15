---
status: 'Deferred'
title: 'HOGWILD!: A Lock-Free Approach to Parallelizing Stochastic Gradient Descent'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2011-06-01'
arxiv: '1106.5730'
first_author: 'Niu'
keywords:
- 'asynchronous-sgd'
- 'lock-free'
- 'shared-memory'
- 'sparsity'
implementations: []
summary: >-
  Niu et al. (2011), [ARXIV-1106.5730](https://arxiv.org/abs/1106.5730). Lock-free parallel SGD on shared memory:
  let cores overwrite each other without locks, and when the problem is sparse
  enough the collisions are rare and the convergence rate is nearly the same.
---
# LIT-tmp6w725: HOGWILD!: A Lock-Free Approach to Parallelizing Stochastic Gradient Descent

Niu et al. (2011) — [ARXIV-1106.5730](https://arxiv.org/abs/1106.5730)

## What it is

Lock-free parallel SGD on shared memory: let cores overwrite each other
without locks, and when the problem is sparse enough the collisions are rare
and the convergence rate is nearly the same.

From the paper's own abstract:

> Stochastic Gradient Descent (SGD) is a popular algorithm that can
> achieve state-of-the-art performance on a variety of machine learning
> tasks. Several researchers have recently proposed schemes to parallelize
> SGD, but all require performance-destroying memory locking and
> synchronization. This work aims to show using novel theoretical
> analysis, algorithms, and implementation that SGD can be implemented
> without any locking.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the asynchronous and bounded-delay branch of distributed
training.

