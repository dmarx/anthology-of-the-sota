---
status: 'Deferred'
title: 'SlowMo: Improving Communication-Efficient Distributed SGD with Slow Momentum'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2019-10-01'
arxiv: '1910.00643'
first_author: 'Wang'
keywords:
- 'slow-momentum'
- 'local-sgd'
- 'decentralized-sgd'
implementations: []
summary: >-
  Wang et al. (2019), [ARXIV-1910.00643](https://arxiv.org/abs/1910.00643). SlowMo: wrap any local-update or
  decentralized base optimizer in an outer momentum step over the averaged
  iterates.
---
# LIT-tmpu6kep: SlowMo: Improving Communication-Efficient Distributed SGD with Slow Momentum

Wang et al. (2019) — [ARXIV-1910.00643](https://arxiv.org/abs/1910.00643)

## What it is

SlowMo: wrap any local-update or decentralized base optimizer in an outer
momentum step over the averaged iterates.

From the paper's own abstract:

> Distributed optimization is essential for training large models on large
> datasets. Multiple approaches have been proposed to reduce the
> communication overhead in distributed training, such as synchronizing
> only after performing multiple local SGD steps, and decentralized
> methods (e.g., using gossip algorithms) to decouple communications among
> workers. Although these methods run faster than AllReduce-based methods,
> which use blocking communication before every update, the resulting
> models may be less accurate after the same number of updates.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.

