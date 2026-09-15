---
status: 'Active'
title: 'Can Decentralized Algorithms Outperform Centralized Algorithms? A Case Study for Decentralized Parallel Stochastic Gradient Descent'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2017-05-01'
arxiv: '1705.09056'
first_author: 'Lian'
keywords:
- 'decentralized-sgd'
- 'gossip'
- 'spectral-gap'
- 'bandwidth'
implementations: []
summary: >-
  Lian et al. (2017), [ARXIV-1705.09056](https://arxiv.org/abs/1705.09056). Decentralized parallel SGD, in which
  workers average only with neighbours, matches centralized SGD in rate while
  removing the server bottleneck, and wins outright on low-bandwidth or high-
  latency networks.
---
# LIT-tmphrzo0: Can Decentralized Algorithms Outperform Centralized Algorithms? A Case Study for Decentralized Parallel Stochastic Gradient Descent

Lian et al. (2017) — [ARXIV-1705.09056](https://arxiv.org/abs/1705.09056)

## Key takeaways

Proves for the first time that decentralized parallel SGD (D-PSGD) achieves
the same computational complexity as centralized mini-batch SGD while
requiring only O(Deg(network)) communication per node instead of O(n), and
validates empirically that D-PSGD is up to 10x faster than parameter-server
or AllReduce baselines on bandwidth- or latency-constrained networks.

- **Theorem 1 / Corollary 2.** D-PSGD converges at rate (1/K) * sum_k
  E[||grad f(x_avg_k)||^2] = O(sigma / sqrt(nK) + poly(rho) / K)
  *Holds when:* Non-convex L-smooth objectives; step size gamma = 1/(2L +
  sigma*sqrt(K/n)); linear speedup holds when K = Omega(n^3 * sigma^4 /
  ((1-rho)^4 * L^4)) approximately
- **Theorem 3 (ring topology).** Linear speedup for ring topology holds when
  n = O(K^{1/9}) with shared data, or n = O(K^{1/13}) with partitioned data
  *Holds when:* Ring graph where spectral gap satisfies rho ~ 1 -
  16*pi^2/(3n^2); speedup regime requires K = Omega(n^{13}) for partitioned
  data

## What the evidence does not cover

- Linear speedup requires K = Omega(n^5/(1-sqrt(rho))^4), which grows
  rapidly with n and poor spectral gap.
- Synchronous algorithm — a single straggler stalls all nodes.
- Convergence theory assumes bounded gradient variance and spectral gap;
  does not handle adversarial or highly heterogeneous data.

## Standing in the anthology

Read — the reading is [NOTE-tmp5xv87](../notes.d/NOTE-tmp5xv87.md). Arrived in the imported batch, which
brought in the decentralized branch, where there is no parameter server and
the topology is the hyperparameter.
