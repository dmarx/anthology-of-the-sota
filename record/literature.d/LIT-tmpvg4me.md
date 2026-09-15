---
status: 'Deferred'
title: 'Moshpit SGD: Communication-Efficient Decentralized Training on Heterogeneous Unreliable Devices'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2021-03-01'
arxiv: '2103.03239'
first_author: 'Ryabinin'
keywords:
- 'decentralized-averaging'
- 'all-reduce'
- 'heterogeneous-workers'
- 'fault-tolerance'
implementations: []
summary: >-
  Ryabinin et al. (2021), [ARXIV-2103.03239](https://arxiv.org/abs/2103.03239). Moshpit SGD: average over a random
  grid of small groups rather than by gossip, reaching exponentially fast
  averaging on unreliable heterogeneous workers.
---
# LIT-tmpvg4me: Moshpit SGD: Communication-Efficient Decentralized Training on Heterogeneous Unreliable Devices

Ryabinin et al. (2021) — [ARXIV-2103.03239](https://arxiv.org/abs/2103.03239)

## What it is

Moshpit SGD: average over a random grid of small groups rather than by
gossip, reaching exponentially fast averaging on unreliable heterogeneous
workers.

From the paper's own abstract:

> Training deep neural networks on large datasets can often be accelerated
> by using multiple compute nodes. This approach, known as distributed
> training, can utilize hundreds of computers via specialized message-
> passing protocols such as Ring All-Reduce. However, running these
> protocols at scale requires reliable high-speed networking that is only
> available in dedicated clusters.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the volunteer- and internet-scale branch, where workers join and
leave.

