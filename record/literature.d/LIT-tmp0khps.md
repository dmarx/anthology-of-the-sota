---
status: 'Deferred'
title: 'Deep learning with Elastic Averaging SGD'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2014-12-01'
arxiv: '1412.6651'
first_author: 'Zhang'
keywords:
- 'elastic-averaging'
- 'parameter-server'
- 'communication-period'
implementations: []
summary: >-
  Zhang et al. (2014), [ARXIV-1412.6651](https://arxiv.org/abs/1412.6651). Let each worker keep its own
  parameters and pull it toward a centre variable with an elastic force, so
  workers may explore apart and communication can be infrequent.
---
# LIT-tmp0khps: Deep learning with Elastic Averaging SGD

Zhang et al. (2014) — [ARXIV-1412.6651](https://arxiv.org/abs/1412.6651)

## What it is

Let each worker keep its own parameters and pull it toward a centre variable
with an elastic force, so workers may explore apart and communication can be
infrequent.

From the paper's own abstract:

> We study the problem of stochastic optimization for deep learning in the
> parallel computing environment under communication constraints. A new
> algorithm is proposed in this setting where the communication and
> coordination of work among concurrent processes (local workers), is
> based on an elastic force which links the parameters they compute with a
> center variable stored by the parameter server (master). The algorithm
> enables the local workers to perform more exploration, i.e.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.

