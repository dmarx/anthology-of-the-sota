---
number: 120
status: Read
formerly:
- NOTE-tmpg38ou
paper: LIT-366
title: 'Asynchronous Local Computations in Distributed Bayesian Learning'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  Replacing synchronous all-agent communication with pairwise gossip and
  filling the saved communication budget with multiple cheap local ULA
  gradient steps allows agents to exploit fast local computation while
  reducing expensive communication; because the extra stochasticity from
  gossip and mini-batch gradients is zero-mean with bounded variance, it does
  not break asymptotic convergence.
---
# NOTE-120: Asynchronous Local Computations in Distributed Bayesian Learning

## Contribution

Proposes a gossip-based asynchronous distributed Bayesian learning algorithm
where only two agents communicate per cycle (via a Poisson-clock gossip
protocol) and each active agent performs T local ULA MCMC steps between
communications. Provides theoretical convergence guarantees showing that
consensus and KL divergence from the true posterior both vanish
asymptotically at the same polynomial rate as canonical synchronous
distributed ULA, while yielding faster initial convergence.

## Key insight

Replacing synchronous all-agent communication with pairwise gossip and
filling the saved communication budget with multiple cheap local ULA
gradient steps allows agents to exploit fast local computation while
reducing expensive communication; because the extra stochasticity from
gossip and mini-batch gradients is zero-mean with bounded variance, it does
not break asymptotic convergence.

## Assumptions

- Log-Sobolev inequality (LSI) on the target posterior: bounds KL divergence
  by Fisher information, enables exponential convergence of Langevin
  dynamics
- Bounded stochastic gradient variance (mini-batch noise)
- Decaying step size alpha_k = a / (min(tau_i, tau_j) + 1)^{delta_alpha}
  with delta_alpha in (0,1)
- Step size parameter satisfies aT < p_m / (nL) where p_m is the minimum
  gossip activation probability
- Poisson-clock gossip: each agent's activation is an independent Poisson
  process
- Both active agents in a cycle synchronize on the same alpha_k and T
  (different values break guarantees)
- IID data across agents assumed implicitly; analysis is for shared
  posterior target

## Key results

- **Theorem 1.** Consensus error E[||x_i^k - x_j^k||^2] =
  O(k^{-delta_alpha}) for all agent pairs i,j
  *Holds when:* Requires aT < p_m/(nL); same polynomial decay rate as
  canonical synchronous distributed ULA regardless of T; only the constant
  factor improves with larger T
- **Theorem 2.** KL divergence KL(rho_k || pi) = O(k^{-delta_alpha}) where
  pi is the true posterior
  *Holds when:* Proved via log-Sobolev inequality and Fokker-Planck
  analysis; convergence rate dominated by step-size annealing exponent
  delta_alpha, independent of T

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The consensus error of the proposed algorithm vanishes asymptotically at rate O(k^{-delta_alpha}), the same polynomial rate as canonical synchronous distributed ULA, provided the step-size parameter satisfies aT < p_m/(nL). | strong | Formal proof in Theorem 1 (Section IV-A) using Fokker-Planck analysis; condition on aT is derived analytically. |
| C2 | The KL divergence from the true posterior converges to zero at rate O(k^{-delta_alpha}), dominated by the step-size annealing rate, regardless of the number of local computations T. | strong | Theorem 2 (Section IV-B) with full proof in Supplementary VII-B using log-Sobolev inequality and Fokker-Planck equation. |
| C3 | Increasing T from 1 to 5 local computations per gossip cycle yields faster initial convergence and higher classification accuracy in the low-data regime on Gamma Telescope and mHealth datasets. | moderate | Simulation experiments in Section V on real-world UCI datasets; results averaged over 10 trials but no formal statistical tests reported. |

## Method

**Distributed Gossip ULA with Multiple Asynchronous Local Computations.**

Each agent runs a local Poisson clock; when an agent's clock ticks, it
selects a random neighbor and the pair form the active agents for one cycle.
The cycle begins with a linear gossip fusion step in which each active agent
averages its parameter with the other's. Both agents then independently
perform T sequential ULA steps using their local data and a stochastic
gradient with a shared (synchronized) step size alpha_k and number of steps
T. No further communication occurs until the next cycle. Inactive agents
hold their parameters fixed. The step size decays as a/(min(tau_i, tau_j) +
1)^{delta_alpha} to ensure asymptotic convergence.

- Gossip protocol with Poisson-clock activation (pairwise, asynchronous)
- Linear gossip fusion step averaging active agents' parameters
- T local ULA steps with stochastic gradient (mini-batch) per cycle
- Synchronized step size and T across the two active agents each cycle
- Log-Sobolev inequality (LSI) assumption on the posterior for convergence

## Concepts

- **Gossip protocol** — Communication scheme where at each tick of a Poisson
  process one agent activates, selects a random neighbor, and only those two
  agents exchange information and update; all others remain dormant.
- **Unadjusted Langevin Algorithm (ULA)** — Discretization of Langevin
  dynamics used for MCMC sampling: w_{k+1} = w_k - alpha * nabla E(w_k) +
  sqrt(2*alpha) * v_k where v_k is standard Gaussian noise; converges
  exponentially to the target distribution with appropriate step sizes.
- **Log-Sobolev inequality (LSI)** — A condition on the target posterior
  weaker than log-concavity that bounds the KL divergence by the Fisher
  information, enabling exponential convergence of Langevin dynamics to the
  target.
- **Canonical distributed ULA** — Baseline where all agents synchronously
  communicate and each performs exactly T=1 ULA step per cycle; used as the
  benchmark comparison in theory and experiments.

## Connections

**Builds on.**

- Decentralized Langevin Dynamics for Bayesian Learning (Parayil et al.,
  NeurIPS 2020) — Extends the synchronous distributed ULA framework of
  Parayil et al. to the asynchronous gossip setting with multiple local
  computations.
- Distributed Asynchronous Deterministic and Stochastic Gradient
  Optimization (Tsitsiklis et al., 1986) — Draws on classical asynchronous
  distributed optimization theory to motivate the gossip-based asynchronous
  approach.

## Recommendations

- **R1** — Use T=3 to T=5 local ULA computations per gossip cycle instead of
  T=1, especially in the low-data regime, to achieve faster initial
  convergence without sacrificing asymptotic accuracy.
  *Topic:* local computation count · *Strength:* moderate · *When:* Requires the
  step-size parameter a to satisfy aT < p_m/(nL); a must be reduced
  proportionally if T is increased. Most beneficial when communication is
  expensive relative to computation.
- **R2** — Re-use the same mini-batch across all T local computations within
  a single gossip cycle to reduce gradient computation cost without
  introducing bias in expectation.
  *Topic:* stochastic gradient efficiency · *Strength:* moderate · *When:* Works
  because the mini-batch selection is random and independent across cycles;
  reuse within a cycle affects only variance, not mean, of the gradient
  estimate.

## Bearing on the record

Several local Langevin steps per communication round. Filed for the line.

## Limitations

- Both active agents in a gossip cycle must agree on and synchronize the
  same step size alpha_k and number of local steps T; allowing different
  values for the two agents breaks convergence guarantees.
- Asymptotic convergence rate is the same polynomial O(k^{-delta_alpha}) as
  canonical ULA regardless of T; only the constant and initial-phase speed
  improve.
- The constraint aT < p_m/(nL) means that safely increasing T requires a
  proportionally smaller step size, partially offsetting the gains from more
  local steps.
- The algorithm is analyzed and evaluated only for logistic regression and
  shallow Bayesian models; extension to deep neural network posteriors is
  not addressed.

## Open questions

- Can the two active agents be allowed to use different T values or step
  sizes per cycle without introducing a convergence-breaking bias, and if so
  under what conditions?
- How does the algorithm perform with non-uniform graph topologies (e.g.,
  star or scale-free graphs) where some agents are far more frequently
  active than others?
- Can the framework be extended to deep neural networks using stochastic
  gradient Langevin dynamics (SGLD) with the same convergence guarantees?
