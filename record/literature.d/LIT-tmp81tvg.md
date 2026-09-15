---
status: 'Deferred'
title: 'Local SGD Converges Fast and Communicates Little'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2018-05-01'
arxiv: '1805.09767'
first_author: 'Stich'
keywords:
- 'local-sgd'
- 'communication-frequency'
- 'linear-speedup'
implementations: []
summary: >-
  Stich (2018), [ARXIV-1805.09767](https://arxiv.org/abs/1805.09767). Local SGD keeps the linear speedup of
  minibatch SGD while communicating only every H = O(sqrt(T/(Kb))) steps.
---
# LIT-tmp81tvg: Local SGD Converges Fast and Communicates Little

Stich (2018) — [ARXIV-1805.09767](https://arxiv.org/abs/1805.09767)

## What it is

Local SGD keeps the linear speedup of minibatch SGD while communicating only
every H = O(sqrt(T/(Kb))) steps.

From the paper's own abstract:

> Mini-batch stochastic gradient descent (SGD) is state of the art in
> large scale distributed training. The scheme can reach a linear speedup
> with respect to the number of workers, but this is rarely seen in
> practice as the scheme often suffers from large network delays and
> bandwidth limits. To overcome this communication bottleneck recent works
> propose to reduce the communication frequency.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.

