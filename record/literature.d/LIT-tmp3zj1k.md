---
status: 'Deferred'
title: 'Neural Tangent Kernel: Convergence and Generalization in Neural Networks'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '2018-06-01'
arxiv: '1806.07572'
first_author: 'Jacot'
keywords:
- 'neural-tangent-kernel'
- 'infinite-width'
- 'lazy-training'
implementations: []
summary: >-
  Jacot et al. (2018), [ARXIV-1806.07572](https://arxiv.org/abs/1806.07572). In the infinite-width limit under
  standard parametrization, training follows a fixed kernel — the network is
  linear in its parameters around initialization, and no features are learned.
---
# LIT-tmp3zj1k: Neural Tangent Kernel: Convergence and Generalization in Neural Networks

Jacot et al. (2018) — [ARXIV-1806.07572](https://arxiv.org/abs/1806.07572)

## What it is

In the infinite-width limit under standard parametrization, training follows
a fixed kernel — the network is linear in its parameters around
initialization, and no features are learned.

From the paper's own abstract:

> At initialization, artificial neural networks (ANNs) are equivalent to
> Gaussian processes in the infinite-width limit, thus connecting them to
> kernel methods. We prove that the evolution of an ANN during training
> can also be described by a kernel: during gradient descent on the
> parameters of an ANN, the network function $f_θ$ (which maps input
> vectors to output vectors) follows the kernel gradient of the functional
> cost (which is convex, in contrast to the parameter cost) w.r.t. a new
> kernel: the Neural Tangent Kernel (NTK).

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the mean-field account of wide networks, where the object that
moves is the distribution of neurons.

