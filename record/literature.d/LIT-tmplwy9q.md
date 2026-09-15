---
status: 'Deferred'
title: 'Generalized EXTRA stochastic gradient Langevin dynamics'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2024-12-01'
arxiv: '2412.01993'
first_author: 'Gurbuzbalaban'
keywords:
- 'langevin'
- 'decentralized-sampling'
- 'extra'
- 'bias-correction'
implementations: []
summary: >-
  Gurbuzbalaban et al. (2024), [ARXIV-2412.01993](https://arxiv.org/abs/2412.01993). A generalized EXTRA
  correction removes the network-induced bias that decentralized SGLD
  otherwise leaves in the sampled posterior.
---
# LIT-tmplwy9q: Generalized EXTRA stochastic gradient Langevin dynamics

Gurbuzbalaban et al. (2024) — [ARXIV-2412.01993](https://arxiv.org/abs/2412.01993)

## What it is

A generalized EXTRA correction removes the network-induced bias that
decentralized SGLD otherwise leaves in the sampled posterior.

From the paper's own abstract:

> Langevin algorithms are popular Markov Chain Monte Carlo methods for
> Bayesian learning, particularly when the aim is to sample from the
> posterior distribution of a parametric model, given the input data and
> the prior distribution over the model parameters. Their stochastic
> versions such as stochastic gradient Langevin dynamics (SGLD) allow
> iterative learning based on randomly sampled mini-batches of large
> datasets and are scalable to large datasets. However, when data is
> decentralized across a network of agents subject to communication and
> privacy constraints, standard SGLD algorithms cannot be applied.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the Langevin branch, where the training noise is the sampler.

