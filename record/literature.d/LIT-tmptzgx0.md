---
status: 'Deferred'
title: 'Communication-Efficient Learning of Deep Networks from Decentralized Data'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2016-02-01'
arxiv: '1602.05629'
first_author: 'McMahan'
keywords:
- 'federated-learning'
- 'local-updates'
- 'non-iid'
implementations: []
summary: >-
  McMahan et al. (2016), [ARXIV-1602.05629](https://arxiv.org/abs/1602.05629). FedAvg: average the weights of
  clients that each ran several local epochs, rather than averaging one
  gradient per round, and the round count falls by one to two orders of
  magnitude.
---
# LIT-tmptzgx0: Communication-Efficient Learning of Deep Networks from Decentralized Data

McMahan et al. (2016) — [ARXIV-1602.05629](https://arxiv.org/abs/1602.05629)

## What it is

FedAvg: average the weights of clients that each ran several local epochs,
rather than averaging one gradient per round, and the round count falls by
one to two orders of magnitude.

From the paper's own abstract:

> Modern mobile devices have access to a wealth of data suitable for
> learning models, which in turn can greatly improve the user experience
> on the device. For example, language models can improve speech
> recognition and text entry, and image models can automatically select
> good photos. However, this rich data is often privacy sensitive, large
> in quantity, or both, which may preclude logging to the data center and
> training there using conventional approaches.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the federated branch, where the workers hold different data.

