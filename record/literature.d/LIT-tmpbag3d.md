---
status: 'Active'
title: 'signSGD: Compressed Optimisation for Non-Convex Problems'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2018-02-01'
arxiv: '1802.04434'
first_author: 'Bernstein'
keywords:
- 'gradient-compression'
- 'sign-sgd'
- 'majority-vote'
implementations: []
summary: >-
  Bernstein et al. (2018), [ARXIV-1802.04434](https://arxiv.org/abs/1802.04434). Sending only the sign of each
  gradient coordinate is a 32x compression that still converges, and with
  majority-vote aggregation the reduction also applies to the return path.
---
# LIT-tmpbag3d: signSGD: Compressed Optimisation for Non-Convex Problems

Bernstein et al. (2018) — [ARXIV-1802.04434](https://arxiv.org/abs/1802.04434)

## Key takeaways

signSGD provides the first rigorous convergence theory for sign-based
gradient compression in non-convex stochastic optimization, showing that
transmitting only the sign of each gradient coordinate achieves SGD-level
convergence rates under an ℓ1 geometry condition. The paper also proves that
distributed majority-vote aggregation of gradient signs achieves the same
variance reduction as full-precision distributed SGD, enabling 1-bit
compression in both directions.

- **Theorem 3.1 (signSGD convergence).** signSGD finds a point with E[||grad
  f||_1] <= O(||l||_1 * ||sigma||_1 / sqrt(N)) after N gradient steps.
  *Holds when:* Non-convex objective; coordinate-wise Lipschitz smoothness
  with constants l_i; bounded coordinate-wise noise sigma_i; learning rate
  eta = sqrt(||l||_1 / (||sigma||_1 * N)).
- **Theorem 4.1 (distributed variance reduction).** Majority-vote signSGD
  with M workers reduces effective noise from ||sigma||_1 to ||sigma||_1 /
  sqrt(M), achieving the same linear speedup as full-precision distributed
  SGD.
  *Holds when:* Unimodal symmetric gradient noise; M workers each
  contributing one sign vote per coordinate.

## What the evidence does not cover

- Convergence requires large mini-batches (batch size growing as O(K) with
  iterations) to make the sign a reliable gradient estimator; small-batch
  convergence requires unimodal symmetric noise assumption.
- Majority vote aggregation uses all-gather (not all-reduce), causing
  communication cost and decompression time to scale linearly with number of
  workers.
- Signum loses ~2% test accuracy vs. well-tuned SGD on ImageNet, possibly
  due to implicit gradient noise reduction conflicting with beneficial SGD
  noise.
- Theoretical framework does not handle heterogeneous (non-i.i.d.) data
  distributions across workers.
- Sign compression discards magnitude information entirely, which may be
  harmful when gradient magnitudes vary widely across parameters.

## Standing in the anthology

Read — the reading is [NOTE-tmpxa9f4](../notes.d/NOTE-tmpxa9f4.md). Arrived in the imported batch, which
brought in the communication-compression branch.
