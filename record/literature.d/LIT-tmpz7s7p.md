---
status: 'Active'
title: 'SlowMo: Improving Communication-Efficient Distributed SGD with Slow Momentum'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2019-10-01'
arxiv: '1910.00643'
first_author: 'Wang'
keywords:
- 'slow-momentum'
- 'local-sgd'
- 'decentralized-sgd'
implementations: []
summary: >-
  Wang et al. (2019), [ARXIV-1910.00643](https://arxiv.org/abs/1910.00643). SlowMo: wrap any local-update or
  decentralized base optimizer in an outer momentum step over the averaged
  iterates.
---
# LIT-tmpz7s7p: SlowMo: Improving Communication-Efficient Distributed SGD with Slow Momentum

Wang et al. (2019) — [ARXIV-1910.00643](https://arxiv.org/abs/1910.00643)

## Key takeaways

Proposes SlowMo, a meta-framework that wraps any communication-efficient
distributed base optimizer with a periodic slow momentum update, and proves
this achieves linear speedup on smooth non-convex objectives—also providing
the first convergence guarantee for BMUF and the Lookahead optimizer.

- **Theorem 1 (SlowMo convergence).** SlowMo with m workers and tau inner
  steps converges to a stationary point of smooth non-convex functions at
  rate O(1/sqrt(m*tau*T)), matching AR-SGD and achieving linear speedup.
  *Holds when:* Smooth non-convex objectives; T >= m^3 * tau^3; fixed slow
  LR alpha and momentum beta.
- **BMUF first convergence guarantee (Corollary).** BMUF (local SGD + slow
  momentum with beta=0) achieves linear speedup in m workers, providing its
  first theoretical convergence guarantee.
  *Holds when:* Same conditions as Theorem 1 with beta=0.
- **Lookahead convergence (Corollary).** Lookahead (single worker SlowMo
  with beta=0) converges to a stationary point, providing its first
  convergence guarantee.
  *Holds when:* m=1 worker; smooth non-convex objective.

## What the evidence does not cover

- Convergence proof covers smooth non-convex functions but requires T >= m^3
  * tau^3 for linear speedup to dominate, which may be impractical for large
  tau.
- SlowMo introduces three additional hyperparameters (alpha, beta, tau) that
  require tuning per task.
- When combined with SGP/OSGP base optimizers, the periodic AllReduce for
  synchronization doubles communication at each outer step.
- Experiments are limited to vision (CIFAR-10, ImageNet) and one NLP task;
  broader applicability to LLM-scale training is unvalidated.

## Standing in the anthology

Read — the reading is [NOTE-tmpzvqut](../notes.d/NOTE-tmpzvqut.md). Arrived in the imported batch, which
brought in the local-update branch — train apart for H steps, then average.
