---
status: 'Deferred'
title: 'Byzantine-Tolerant Machine Learning'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2017-03-01'
arxiv: '1703.02757'
first_author: 'Blanchard'
keywords:
- 'byzantine-robustness'
- 'gradient-aggregation'
- 'krum'
implementations: []
summary: >-
  Blanchard et al. (2017), [ARXIV-1703.02757](https://arxiv.org/abs/1703.02757). Averaging gradients is not
  Byzantine-tolerant at any cluster size — one worker can steer the average
  anywhere. Krum instead selects the gradient closest to its own nearest
  neighbours.
---
# LIT-tmph4do5: Byzantine-Tolerant Machine Learning

Blanchard et al. (2017) — [ARXIV-1703.02757](https://arxiv.org/abs/1703.02757)

## What it is

Averaging gradients is not Byzantine-tolerant at any cluster size — one
worker can steer the average anywhere. Krum instead selects the gradient
closest to its own nearest neighbours.

From the paper's own abstract:

> The growth of data, the need for scalability and the complexity of
> models used in modern machine learning calls for distributed
> implementations. Yet, as of today, distributed machine learning
> frameworks have largely ignored the possibility of arbitrary (i.e.,
> Byzantine) failures. In this paper, we study the robustness to Byzantine
> failures at the fundamental level of stochastic gradient descent (SGD),
> the heart of most machine learning algorithms.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the robust-aggregation branch, where some workers may return
anything.

