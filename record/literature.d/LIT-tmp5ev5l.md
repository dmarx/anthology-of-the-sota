---
status: 'Active'
title: 'Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2018-03-01'
arxiv: '1803.01498'
first_author: 'Yin'
keywords:
- 'byzantine-robustness'
- 'trimmed-mean'
- 'coordinate-median'
- 'statistical-rates'
implementations: []
summary: >-
  Yin et al. (2018), [ARXIV-1803.01498](https://arxiv.org/abs/1803.01498). Coordinate-wise trimmed mean and
  coordinate-wise median as Byzantine-robust aggregators, with statistical
  rates that are order-optimal, and the median needs no knowledge of the
  corruption fraction.
---
# LIT-tmp5ev5l: Byzantine-Robust Distributed Learning: Towards Optimal Statistical Rates

Yin et al. (2018) — [ARXIV-1803.01498](https://arxiv.org/abs/1803.01498)

## Key takeaways

This paper provides the first sharp statistical analysis of Byzantine-robust
distributed gradient descent algorithms based on coordinate-wise median and
coordinate-wise trimmed mean. For strongly convex population losses, the
trimmed-mean algorithm achieves the order-optimal rate O-tilde(alpha/sqrt(n)
+ 1/sqrt(nm)), and the median algorithm achieves O-tilde(alpha/sqrt(n) +
1/sqrt(nm) + 1/n), which is also order-optimal when n >= m. A matching
information-theoretic lower bound Omega(alpha/sqrt(n) + sqrt(d/(nm)))
confirms tightness. Additionally, a one-round median-based algorithm
achieves the same rate as multi-round median GD for strongly convex
quadratic losses, enabling communication-efficient Byzantine-robust
learning.

- **Trimmed-mean GD — order-optimal rate (Theorems 4, 5, 6).** After T =
  O(condition_number * log(1/eps)) rounds, trimmed-mean GD achieves
  statistical error O-tilde(alpha/sqrt(n) + 1/sqrt(nm)). This matches the
  information-theoretic lower bound up to log factors.
  *Holds when:* Strongly convex, L-smooth loss; alpha < 1/2; beta >= alpha;
  sub-exponential gradient tails; n >= 1, m >= 1 workers.
- **Coordinate-wise median GD rate (Theorems 1, 2, 3).** Median GD achieves
  statistical error O-tilde(alpha/sqrt(n) + 1/sqrt(nm) + 1/n), which is
  order-optimal when n >= m. Does not require knowledge of alpha.
  *Holds when:* Strongly convex, L-smooth loss; alpha < 1/2; bounded
  gradient skewness (third moments); IID data.
- **Information-theoretic lower bound (Observation 1).** No algorithm can
  achieve statistical error better than Omega(alpha/sqrt(n) + sqrt(d/(nm)))
  for Byzantine-robust distributed learning, proving the trimmed-mean rate
  is unimprovable up to constants and log factors.
  *Holds when:* Any deterministic or randomized algorithm; arbitrary number
  of communication rounds; Gaussian gradient distributions.
- **One-round algorithm (Theorem 7).** Local ERM on each worker followed by
  coordinate-wise median of solutions achieves the same
  O-tilde(alpha/sqrt(n) + 1/sqrt(nm) + 1/n) rate as multi-round median GD,
  using only one communication round.
  *Holds when:* Strongly convex quadratic loss only; same Byzantine fraction
  and skewness assumptions as Theorem 1.

## What the evidence does not cover

- Dimension dependence may not be optimal: the rates hide factors in d
  (gradient variance V = O(sqrt(d)) for linear regression), and the paper
  acknowledges understanding optimal dimension dependence in high dimensions
  is an open problem.
- The one-round algorithm is only proven optimal for strongly convex
  quadratic losses; extending theoretical guarantees to general convex or
  non-convex losses is open.
- The trimmed-mean algorithm requires knowledge of (an upper bound on) alpha
  to set beta; using an overly conservative beta degrades performance.
- Sub-exponential gradient tails are required for trimmed mean, which may
  not hold for heavy-tailed losses; median-based GD only needs bounded
  skewness (third moments) but incurs the extra 1/n term.
- Analysis assumes the master machine is trusted and non-faulty; Byzantine
  failures in the master or decentralized (no-master) topologies are not
  addressed.
- The analysis assumes workers hold fixed, i.i.d. data; heterogeneous data
  distributions (as in federated learning) are not covered by these
  statistical guarantees.
- Number of iterations T required for convergence scales logarithmically
  with 1/epsilon but depends on the condition number (L_F +
  lambda_F)/lambda_F, which can be large for ill-conditioned problems.

## Standing in the anthology

Read — the reading is [NOTE-tmpfy0qu](../notes.d/NOTE-tmpfy0qu.md). Arrived in the imported batch, which
brought in the robust-aggregation branch, where some workers may return
anything.
