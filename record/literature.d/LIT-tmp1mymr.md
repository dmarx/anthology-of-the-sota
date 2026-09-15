---
status: 'Deferred'
title: 'Proving the Limited Scalability of Centralized Distributed Optimization via a New Lower Bound Construction'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2025-06-01'
arxiv: '2506.23836'
first_author: 'Tyurin'
keywords:
- 'lower-bounds'
- 'compression'
- 'communication-complexity'
- 'centralized-optimization'
implementations: []
summary: >-
  Tyurin (2025), [ARXIV-2506.23836](https://arxiv.org/abs/2506.23836). A lower-bound construction showing that
  unbiased compression cannot improve both the uplink and downlink terms at
  once, which bounds what centralized compression schemes can buy.
---
# LIT-tmp1mymr: Proving the Limited Scalability of Centralized Distributed Optimization via a New Lower Bound Construction

Tyurin (2025) — [ARXIV-2506.23836](https://arxiv.org/abs/2506.23836)

## What it is

A lower-bound construction showing that unbiased compression cannot improve
both the uplink and downlink terms at once, which bounds what centralized
compression schemes can buy.

From the paper's own abstract:

> We consider centralized distributed optimization in the classical
> federated learning setup, where $n$ workers jointly find an
> $\varepsilon$-stationary point of an $L$-smooth, $d$-dimensional
> nonconvex function $f$, having access only to unbiased stochastic
> gradients with variance $σ^2$. Each worker requires at most $h$ seconds
> to compute a stochastic gradient, and the communication times from the
> server to the workers and from the workers to the server are $τ_{s}$ and
> $τ_{w}$ seconds per coordinate, respectively. One of the main
> motivations for distributed optimization is to achieve scalability with
> respect to $n$.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the communication-compression branch.

