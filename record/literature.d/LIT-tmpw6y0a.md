---
status: 'Deferred'
title: 'Subspace Networks: Scaling Decentralized Training with Communication-Efficient Model Parallelism'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2025-06-01'
arxiv: '2506.01260'
first_author: 'Ramasinghe'
keywords:
- 'subspace-compression'
- 'pipeline-parallelism'
- 'grassmann'
- 'decentralized-training'
implementations: []
summary: >-
  Ramasinghe et al. (2025), [ARXIV-2506.01260](https://arxiv.org/abs/2506.01260). Project the model-parallel
  communication onto a low-rank subspace updated every few hundred steps,
  reaching about 100x compression for pipeline-parallel decentralized
  training.
---
# LIT-tmpw6y0a: Subspace Networks: Scaling Decentralized Training with Communication-Efficient Model Parallelism

Ramasinghe et al. (2025) — [ARXIV-2506.01260](https://arxiv.org/abs/2506.01260)

## What it is

Project the model-parallel communication onto a low-rank subspace updated
every few hundred steps, reaching about 100x compression for pipeline-
parallel decentralized training.

From the paper's own abstract:

> Scaling models has led to significant advancements in deep learning, but
> training these models in decentralized settings remains challenging due
> to communication bottlenecks. While existing compression techniques are
> effective in data-parallel, they do not extend to model parallelism.
> Unlike data-parallel training, where weight gradients are exchanged,
> model-parallel requires compressing activations and activation gradients
> as they propagate through layers, accumulating compression errors.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the communication-compression branch.

