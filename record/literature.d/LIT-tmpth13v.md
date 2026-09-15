---
status: 'Active'
title: 'Byzantine-Tolerant Machine Learning'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2017-03-01'
arxiv: '1703.02757'
first_author: 'Blanchard'
keywords:
- 'byzantine-robustness'
- 'gradient-aggregation'
- 'krum'
implementations: []
summary: >-
  Blanchard et al. (2017), [ARXIV-1703.02757](https://arxiv.org/abs/1703.02757). Averaging gradients is not
  Byzantine-tolerant at any cluster size — one worker can steer the average
  anywhere. Krum instead selects the gradient closest to its own nearest
  neighbours.
---
# LIT-tmpth13v: Byzantine-Tolerant Machine Learning

Blanchard et al. (2017) — [ARXIV-1703.02757](https://arxiv.org/abs/1703.02757)

## Key takeaways

The paper proves that no linear combination of worker gradient estimates
(including averaging) can tolerate even a single Byzantine worker in
distributed SGD. It then introduces Krum, the first gradient aggregation
rule proven to be Byzantine-resilient in arbitrary dimension d with
polynomial time complexity O(n²·(d + log n)). Krum selects the worker vector
with the smallest sum of squared distances to its n-f-2 nearest neighbors,
provably converging under the condition 2f+2 < n. An m-Krum extension
averages the top-m selected vectors to make better use of correct workers.

- **Lemma 1 (Impossibility of linear aggregation).** For any linear
  combination F(V_1,...,V_n) = Σ λ_i V_i with λ_n ≠ 0, there exists a
  Byzantine worker sending V_n = (1/λ_n)·U - Σᵢ₌₁ⁿ⁻¹(λᵢ/λ_n)·Vᵢ that forces
  F to equal any target U regardless of correct workers.
  *Holds when:* Holds for any fixed coefficients λ_i with at least one
  nonzero λ_n; applies to averaging, weighted averaging, and any linear
  rule.
- **Proposition 1 (Krum Byzantine resilience).** Krum is (α, f)-Byzantine
  resilient with sin α = η(n,f)·√d·σ / ‖g‖, where η(n,f) =
  √(2(n-f+f(n-f-2)+f²(n-f-1))/(n-2f-2)).
  *Holds when:* Requires 2f+2 < n; η = O(√n) when f = O(1), η = O(n) when f
  = O(n); convergence basin scales as η·√d·σ.
- **Proposition 2 (Krum-SGD convergence).** SGD with Krum aggregation
  converges almost surely to a flat region ‖∇Q(x)‖ ≤ η(n,f)·√d·σ for non-
  convex objectives with Robbins-Monro step sizes.
  *Holds when:* Requires (α,f)-Byzantine resilience of Krum (Proposition 1);
  non-convex convergence; no convergence to local minimum guaranteed.
- **Lemma 2 (Krum complexity).** The Krum function can be computed in
  O(n²·(d + log n)) time.
  *Holds when:* Dominant cost is n² pairwise squared-distance computations,
  each O(d); sorting costs O(n log n) per worker.

## What the evidence does not cover

- Krum selects a single vector (or m vectors), discarding n-m gradient
  estimates. This reduces statistical efficiency relative to averaging — in
  the failure-free case, 1-Krum wastes n-1 gradient computations per step.
- The convergence result only guarantees reaching a "flat region" where ‖∇Q‖
  ≤ η(n,f)·√d·σ, not convergence to a local or global minimum. With large f
  or large d, this basin can be far from any true minimum.
- Time complexity is O(n²·(d + log n)) at the parameter server each round.
  In high-throughput settings with many workers and very high-dimensional
  models (d ~ 10¹¹), this is a non-trivial bottleneck.
- The analysis assumes a reliable parameter server. Making the parameter
  server itself fault-tolerant requires additional state-machine
  replication, which is noted but not solved.
- The paper assumes synchronous rounds. Extending Byzantine resilience to
  asynchronous distributed SGD (where workers may be arbitrarily slow) is
  listed as an open problem.
- The condition 2f+2 < n is a strict lower bound on the ratio of correct
  workers. It is unknown whether this bound is tight.
- Krum's Byzantine resilience degrades gracefully but does not recover when
  Byzantine workers learn and adapt over time (it assumes Byzantine
  knowledge is static per round).

## Standing in the anthology

Read — the reading is [NOTE-tmpywc4x](../notes.d/NOTE-tmpywc4x.md). Arrived in the imported batch, which
brought in the robust-aggregation branch, where some workers may return
anything.
