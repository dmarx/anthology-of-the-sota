---
status: 'Deferred'
title: 'Stochastic Gradient Push for Distributed Deep Learning'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2018-11-01'
arxiv: '1811.10792'
first_author: 'Assran'
keywords:
- 'stochastic-gradient-push'
- 'directed-graphs'
- 'overlap'
- 'exponential-graph'
implementations: []
summary: >-
  Assran et al. (2018), [ARXIV-1811.10792](https://arxiv.org/abs/1811.10792). Stochastic gradient push over
  directed, time-varying graphs, with the communication overlapped against the
  next local step.
---
# LIT-tmpcari4: Stochastic Gradient Push for Distributed Deep Learning

Assran et al. (2018) — [ARXIV-1811.10792](https://arxiv.org/abs/1811.10792)

## What it is

Stochastic gradient push over directed, time-varying graphs, with the
communication overlapped against the next local step.

From the paper's own abstract:

> Distributed data-parallel algorithms aim to accelerate the training of
> deep neural networks by parallelizing the computation of large mini-
> batch gradient updates across multiple nodes. Approaches that
> synchronize nodes using exact distributed averaging (e.g., via
> AllReduce) are sensitive to stragglers and communication delays. The
> PushSum gossip algorithm is robust to these issues, but only performs
> approximate distributed averaging.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the decentralized branch, where there is no parameter server and
the topology is the hyperparameter.

