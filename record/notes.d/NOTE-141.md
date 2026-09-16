---
number: 141
status: Read
formerly:
- NOTE-tmpqvvkl
paper: LIT-345
title: 'Generalized EXTRA stochastic gradient Langevin dynamics'
version: 1
date: '2026-09-15'
summary: >-
  Standard decentralized SGLD (DE-SGLD) suffers from a bias due to network
  effects that does not vanish even with full-batch gradients; adapting the
  EXTRA correction mechanism from decentralized optimization to Langevin
  dynamics eliminates this bias and yields faster convergence.
---
# NOTE-141: Generalized EXTRA stochastic gradient Langevin dynamics

## Contribution

Proposes generalized EXTRA SGLD, a decentralized Bayesian sampling algorithm
that eliminates the persistent network-induced bias present in standard DE-
SGLD algorithms in the full-batch setting. Provides non-asymptotic
convergence bounds in 2-Wasserstein distance that improve on prior DE-SGLD
bounds by a factor of at least L^2 (the smoothness coefficient squared).

## Key insight

Standard decentralized SGLD (DE-SGLD) suffers from a bias due to network
effects that does not vanish even with full-batch gradients; adapting the
EXTRA correction mechanism from decentralized optimization to Langevin
dynamics eliminates this bias and yields faster convergence.

## Assumptions

- Strongly convex and smooth local objectives: each f_i is mu-strongly
  convex and L-smooth
- Bounded stochastic gradient variance: E[||g_i - grad f_i(x)||^2] <=
  sigma^2
- Connected fixed network topology with doubly stochastic symmetric mixing
  matrix W
- Two communication matrices W and W-tilde satisfying null{W - W-tilde} =
  span{1_N}
- Correction matrix W-tilde = h*I + (1-h)*W with h in (0, 1/2] for null-
  space condition
- IID data assumed implicitly (strongly convex posteriors); non-IID setting
  not analyzed

## Key results

- **Proposition 5 (complexity comparison).** Generalized EXTRA SGLD achieves
  an O(L^2) improvement in iteration complexity over DE-SGLD in
  2-Wasserstein distance
  *Holds when:* Full-batch or large-batch gradient regime; strongly convex
  and L-smooth objectives; comparison holds for the same step size eta and
  same network topology
- **Theorem 4 (geometric convergence).** W_2(rho_k, pi)^2 <= C * (1 -
  c*eta)^k + O(eta * sigma^2 + eta^2 * L^2)
  *Holds when:* Geometric (linear) convergence in 2-Wasserstein distance to
  a neighborhood of size O(eta*sigma^2 + eta^2*L^2); neighborhood does not
  shrink to zero — persistent bias proportional to step size remains

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Generalized EXTRA SGLD is unbiased in the full-batch setting, whereas DE-SGLD retains a persistent network-induced bias. | strong | Proved analytically by showing that the fixed-point of the EXTRA update coincides with the true consensus point, in contrast to DE-SGLD. |
| C2 | Generalized EXTRA SGLD achieves an O(L^2) improvement in iteration complexity over DE-SGLD. | strong | Formal comparison in Proposition 5 using non-asymptotic 2-Wasserstein bounds for both algorithms. |
| C3 | The iterates of generalized EXTRA SGLD converge geometrically (linearly in k) in 2-Wasserstein distance to a neighborhood of the posterior. | strong | Theorem 4, proved by bounding L^2 consensus error, deviation from Euler-Maruyama, and proximity of Euler-Maruyama to the Gibbs target. |

## Method

**Generalized EXTRA SGLD.**

Each agent maintains a local parameter and a correction variable tracking
gradient differences across successive iterates. The update combines a
weighted-average gossip step using two communication matrices W and W-tilde
(satisfying specific null-space conditions) with a stochastic gradient step
and Gaussian noise injection. Subtracting consecutive updates eliminates the
consensus bias that plagues standard DE-SGLD. The correction is analogous to
the EXTRA trick in decentralized optimization.

- Two communication matrices W (gossip) and W-tilde (correction) satisfying
  null{W - W-tilde} = span{1_N}
- Gradient-difference correction term (analogous to EXTRA in optimization)
- Gaussian noise injection scaled as sqrt(2*eta) for Langevin dynamics
- Mini-batch stochastic gradient with bounded variance sigma^2

## Concepts

- **Stochastic Gradient Langevin Dynamics (SGLD)** — Markov Chain Monte
  Carlo method that adds Gaussian noise to stochastic gradient steps to
  sample from a posterior distribution.
- **DE-SGLD** — Decentralized SGLD where agents gossip local parameters over
  a network and apply individual noisy gradient steps; suffers from a
  network-induced bias at the stationary point.
- **EXTRA (EXact firsT-ordeR Algorithm)** — Decentralized optimization
  method that uses a gradient-difference correction to eliminate the
  consensus bias of gradient tracking, extended here to the Langevin
  (sampling) setting.
- **2-Wasserstein distance** — Optimal transport metric between probability
  distributions measuring the minimum expected squared distance under any
  coupling.
- **Overdamped Langevin diffusion** — Continuous-time SDE dX = -grad f(X) dt
  + sqrt(2) dW whose stationary measure is the Gibbs distribution
  proportional to exp(-f).

## Connections

**Builds on.**

- EXTRA: An Exact First-Order Algorithm for Decentralized Consensus
  Optimization (Shi et al., 2015) — Directly adapts the EXTRA gradient-
  correction mechanism from decentralized optimization to the Langevin
  sampling setting.
- Decentralized Langevin dynamics for Bayesian learning (Gao et al., 2021) —
  Prior DE-SGLD algorithm whose bias and complexity this paper improves
  upon.

## Recommendations

- **R1** — Use generalized EXTRA SGLD instead of DE-SGLD for decentralized
  Bayesian inference when full-batch or large-batch gradients are feasible,
  to eliminate network-induced bias.
  *Topic:* decentralized Bayesian inference · *Strength:* strong · *When:*
  Strongly convex and smooth local objectives; connected network with a
  symmetric doubly stochastic mixing matrix.
- **R2** — Choose the interpolation parameter h in W-tilde = h*I + (1-h)*W
  within the range (0, 1/2] to satisfy the required null-space conditions
  and obtain the tightest convergence bounds.
  *Topic:* hyperparameter selection · *Strength:* moderate · *When:* When
  constructing the correction matrix W-tilde for generalized EXTRA SGLD.

## Bearing on the record

Removing the network-induced bias from decentralized Langevin sampling.
Filed for the line.

## Limitations

- Analysis requires strongly convex and smooth component functions; non-
  convex posteriors are not covered.
- The correction step requires storing an extra momentum-like variable per
  agent, doubling memory relative to DE-SGLD.
- Convergence neighborhood does not shrink to zero; a persistent bias
  proportional to the step size and mini-batch noise remains.
- Assumes a connected, fixed network topology with a doubly stochastic
  weight matrix.

## Open questions

- Can the EXTRA-Langevin idea be extended to non-log-concave (non-convex)
  target distributions?
- What is the optimal communication matrix pair (W, W-tilde) for a given
  network topology?
- Can the O(L^2) complexity improvement be shown to be tight, or is there a
  further gap to close?
