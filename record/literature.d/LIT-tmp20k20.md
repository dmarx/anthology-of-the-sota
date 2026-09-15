---
status: 'Deferred'
title: 'Can Decentralized Algorithms Outperform Centralized Algorithms? A Case Study for Decentralized Parallel Stochastic Gradient Descent'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2017-05-01'
arxiv: '1705.09056'
first_author: 'Lian'
keywords:
- 'decentralized-sgd'
- 'gossip'
- 'spectral-gap'
- 'bandwidth'
implementations: []
summary: >-
  Lian et al. (2017), [ARXIV-1705.09056](https://arxiv.org/abs/1705.09056). Decentralized parallel SGD, in which
  workers average only with neighbours, matches centralized SGD in rate while
  removing the server bottleneck, and wins outright on low-bandwidth or high-
  latency networks.
---
# LIT-tmp20k20: Can Decentralized Algorithms Outperform Centralized Algorithms? A Case Study for Decentralized Parallel Stochastic Gradient Descent

Lian et al. (2017) — [ARXIV-1705.09056](https://arxiv.org/abs/1705.09056)

## What it is

Decentralized parallel SGD, in which workers average only with neighbours,
matches centralized SGD in rate while removing the server bottleneck, and
wins outright on low-bandwidth or high-latency networks.

From the paper's own abstract:

> Most distributed machine learning systems nowadays, including TensorFlow
> and CNTK, are built in a centralized fashion. One bottleneck of
> centralized algorithms lies on high communication cost on the central
> node. Motivated by this, we ask, can decentralized algorithms be faster
> than its centralized counterpart?

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the decentralized branch, where there is no parameter server and
the topology is the hyperparameter.

