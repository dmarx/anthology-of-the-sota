---
status: 'Deferred'
title: 'Cooperative SGD: A unified Framework for the Design and Analysis of Communication-Efficient SGD Algorithms'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2018-08-01'
arxiv: '1808.07576'
first_author: 'Wang'
keywords:
- 'periodic-averaging'
- 'mixing-matrix'
- 'unified-analysis'
implementations: []
summary: >-
  Wang and Joshi (2018), [ARXIV-1808.07576](https://arxiv.org/abs/1808.07576). Cooperative SGD: one framework
  whose special cases are local SGD, elastic averaging and decentralized SGD,
  so their error floors can be compared in the same terms.
---
# LIT-tmpq96o6: Cooperative SGD: A unified Framework for the Design and Analysis of Communication-Efficient SGD Algorithms

Wang and Joshi (2018) — [ARXIV-1808.07576](https://arxiv.org/abs/1808.07576)

## What it is

Cooperative SGD: one framework whose special cases are local SGD, elastic
averaging and decentralized SGD, so their error floors can be compared in
the same terms.

From the paper's own abstract:

> Communication-efficient SGD algorithms, which allow nodes to perform
> local updates and periodically synchronize local models, are highly
> effective in improving the speed and scalability of distributed SGD.
> However, a rigorous convergence analysis and comparative study of
> different communication-reduction strategies remains a largely open
> problem. This paper presents a unified framework called Cooperative SGD
> that subsumes existing communication-efficient SGD algorithms such as
> periodic-averaging, elastic-averaging and decentralized SGD.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.

