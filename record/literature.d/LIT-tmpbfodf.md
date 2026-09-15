---
status: 'Deferred'
title: 'Epidemic Learning: Boosting Decentralized Learning with Randomized Communication'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2023-10-01'
arxiv: '2310.01972'
first_author: 'Vos'
keywords:
- 'decentralized-learning'
- 'randomized-topology'
- 'sampling'
- 'convergence'
implementations: []
summary: >-
  Vos et al. (2023), [ARXIV-2310.01972](https://arxiv.org/abs/2310.01972). Epidemic Learning: sample a fresh
  random set of s neighbours each round instead of using a fixed topology,
  which converges faster than any static graph.
---
# LIT-tmpbfodf: Epidemic Learning: Boosting Decentralized Learning with Randomized Communication

Vos et al. (2023) — [ARXIV-2310.01972](https://arxiv.org/abs/2310.01972)

## What it is

Epidemic Learning: sample a fresh random set of s neighbours each round
instead of using a fixed topology, which converges faster than any static
graph.

From the paper's own abstract:

> We present Epidemic Learning (EL), a simple yet powerful decentralized
> learning (DL) algorithm that leverages changing communication topologies
> to achieve faster model convergence compared to conventional DL
> approaches. At each round of EL, each node sends its model updates to a
> random sample of $s$ other nodes (in a system of $n$ nodes). We provide
> an extensive theoretical analysis of EL, demonstrating that its changing
> topology culminates in superior convergence properties compared to the
> state-of-the-art (static and dynamic) topologies.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the decentralized branch, where there is no parameter server and
the topology is the hyperparameter.

