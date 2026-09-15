---
status: 'Deferred'
title: 'Large Batch Optimization for Deep Learning: Training BERT in 76 minutes'
version: 1
tags:
- training-optimization
date: '2026-09-15'
published: '2019-04-01'
arxiv: '1904.00962'
first_author: 'You'
keywords:
- 'large-batch'
- 'layerwise-adaptation'
- 'lamb'
- 'bert'
implementations: []
summary: >-
  You et al. (2019), [ARXIV-1904.00962](https://arxiv.org/abs/1904.00962). LAMB: normalize each layer's update by
  the ratio of weight norm to update norm, which lets BERT train at batch size
  32k without per-batch-size retuning.
---
# LIT-tmpkdxvb: Large Batch Optimization for Deep Learning: Training BERT in 76 minutes

You et al. (2019) — [ARXIV-1904.00962](https://arxiv.org/abs/1904.00962)

## What it is

LAMB: normalize each layer's update by the ratio of weight norm to update
norm, which lets BERT train at batch size 32k without per-batch-size
retuning.

From the paper's own abstract:

> Training large deep neural networks on massive datasets is
> computationally very challenging. There has been recent surge in
> interest in using large batch stochastic optimization methods to tackle
> this issue. The most prominent algorithm in this line of research is
> LARS, which by employing layerwise adaptive learning rates trains ResNet
> on ImageNet in a few minutes.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the batch-size line — how large a batch buys speed, and what it
costs.

