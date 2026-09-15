---
status: 'Deferred'
title: 'Asynchronous Stochastic Gradient Descent with Delay Compensation'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2016-09-01'
arxiv: '1609.08326'
first_author: 'Zheng'
keywords:
- 'asynchronous-sgd'
- 'gradient-delay'
- 'taylor-expansion'
implementations: []
summary: >-
  Zheng et al. (2016), [ARXIV-1609.08326](https://arxiv.org/abs/1609.08326). Asynchronous SGD applies a gradient
  computed at stale parameters; a first-order Taylor correction using a cheap
  Hessian approximation recovers most of the accuracy the delay costs.
---
# LIT-tmpftboy: Asynchronous Stochastic Gradient Descent with Delay Compensation

Zheng et al. (2016) — [ARXIV-1609.08326](https://arxiv.org/abs/1609.08326)

## What it is

Asynchronous SGD applies a gradient computed at stale parameters; a first-
order Taylor correction using a cheap Hessian approximation recovers most of
the accuracy the delay costs.

From the paper's own abstract:

> With the fast development of deep learning, it has become common to
> learn big neural networks using massive training data. Asynchronous
> Stochastic Gradient Descent (ASGD) is widely adopted to fulfill this
> task for its efficiency, which is, however, known to suffer from the
> problem of delayed gradients. That is, when a local worker adds its
> gradient to the global model, the global model may have been updated by
> other workers and this gradient becomes "delayed".

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the asynchronous and bounded-delay branch of distributed
training.

