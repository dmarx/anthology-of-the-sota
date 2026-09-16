---
number: 123
status: Read
formerly:
- NOTE-tmphpvzh
paper: LIT-245
title: 'Bayesian Learning via Stochastic Gradient Langevin Dynamics'
version: 1
date: '2026-09-15'
summary: >-
  SGD with a specific noise injection schedule performs approximate Langevin
  Monte Carlo. The noise term eps_t ~ N(0, eps_t) counteracts the bias from
  using stochastic (minibatch) gradients, so the iterates explore the
  posterior rather than collapsing to a mode. At large step sizes the
  algorithm behaves like standard SGD (optimization); as step size → 0 the
  Markov chain mixes and samples from the posterior.
---
# NOTE-123: Bayesian Learning via Stochastic Gradient Langevin Dynamics

## Contribution

Introduces Stochastic Gradient Langevin Dynamics (SGLD), which adds a
calibrated Gaussian noise term to SGD updates to perform approximate
Bayesian posterior sampling rather than point estimation. Shows that as step
size anneals to zero, the iterates converge to exact samples from the
posterior; at larger step sizes it acts like an efficient optimizer. Bridges
MCMC sampling and SGD in a single algorithm that scales to large datasets
via minibatch gradient estimates.

## Key insight

SGD with a specific noise injection schedule performs approximate Langevin
Monte Carlo. The noise term eps_t ~ N(0, eps_t) counteracts the bias from
using stochastic (minibatch) gradients, so the iterates explore the
posterior rather than collapsing to a mode. At large step sizes the
algorithm behaves like standard SGD (optimization); as step size → 0 the
Markov chain mixes and samples from the posterior. This duality makes SGLD a
principled alternative to SGD that provides uncertainty estimates without
the overhead of traditional MCMC.

## Assumptions

- The log-posterior log p(theta | X) is smooth (continuously differentiable)
  and satisfies mild regularity conditions (bounded third derivatives in the
  neighborhood of the posterior).
- Minibatch gradient noise is approximately Gaussian (CLT); this requires
  sufficiently large minibatch size n relative to the tail behavior of per-
  sample gradients.
- The step size schedule satisfies the Robbins-Monro conditions: sum_t eps_t
  = inf (ensures exploration) and sum_t eps_t^2 < inf (ensures convergence).
- The N/n scaling of minibatch gradients produces an unbiased estimator of
  the full-data gradient; this holds exactly only when minibatches are
  sampled with replacement.
- The KL divergence bound (Theorem 1) holds under the assumption that the
  posterior is log-concave or mildly non-convex; convergence guarantees for
  multimodal posteriors are not established.
- The stationary bias O(eps) (Theorem 2) assumes that the discretization of
  the continuous SDE is the dominant error source; this may not hold when
  minibatch variance is large.

## Key results

- **Theorem 1 (Posterior convergence).** Under a Robbins-Monro step size
  schedule, the KL divergence between the SGLD iterate distribution and the
  true posterior p(theta|X) converges to zero: KL(p_t || p*) → 0 as t → ∞.
  *Holds when:* Requires smooth log-posterior, unbiased gradient estimates,
  and Robbins-Monro schedule. Rate of convergence depends on mixing time of
  the Langevin diffusion.
- **Theorem 2 (Finite step-size bias).** At constant step size eps, the
  stationary distribution of SGLD is O(eps)-close to the true posterior in a
  suitable divergence metric.
  *Holds when:* Holds under the smoothness assumptions on the log-posterior;
  the bias constant depends on third derivatives of the log-posterior at the
  mode.
- **Optimizer-sampler duality.** At large eps, SGLD behaves like SGD (fast
  convergence to a mode); at small eps, it behaves like Langevin MCMC
  (posterior sampling). The same algorithm spans both regimes by adjusting
  eps.
  *Holds when:* No formal theorem; demonstrated empirically and argued via
  the SDE limit. The transition between regimes is continuous in eps.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | SGLD with annealing step sizes converges to exact posterior samples as eps_t → 0. | strong | Theorem 1: KL divergence to target posterior goes to zero under mild regularity conditions on the log-posterior and step size schedule. |
| C2 | At constant step size, SGLD admits an O(eps) bias relative to the true posterior, matching the discretization error of Langevin dynamics. | strong | Theorem 2: bounds the stationary distribution bias as a function of step size. |
| C3 | SGLD produces better-calibrated uncertainty estimates than MAP/SGD on logistic regression and ICA experiments. | moderate | Empirical comparison on MNIST and ICA; SGLD posteriors show better predictive uncertainty than SGD point estimates. |

## Method

**Stochastic Gradient Langevin Dynamics (SGLD).**

At each step t: 1. Sample a minibatch of n data points from N total 2.
Compute the scaled stochastic log-posterior gradient: g_t = (N/n) * sum_{i
in batch} nabla log p(x_i | theta) + nabla log p(theta) 3. Inject Gaussian
noise: eta_t ~ N(0, eps_t) 4. Update: theta_{t+1} = theta_t + (eps_t/2) *
g_t + eta_t Step size eps_t follows a Robbins-Monro schedule: sum eps_t =
inf, sum eps_t^2 < inf (e.g., eps_t ~ t^{-0.55}).

- Langevin noise injection calibrated to step size (eta_t ~ N(0, eps_t))
- Minibatch gradient estimation scaled by N/n to approximate full-data
  gradient
- Annealing schedule: eps_t → 0 for convergence; constant eps for
  exploration
- No Metropolis-Hastings correction needed (bias vanishes as eps → 0)

## Concepts

- **Langevin dynamics** — A continuous-time SDE dtheta = (1/2) nabla log
  p(theta|X) dt + dW where W is Brownian motion; stationary distribution is
  exactly p(theta|X).
- **Gradient noise scale** — The magnitude of the stochastic gradient noise
  from minibatch sampling; SGLD leverages this noise rather than eliminating
  it.
- **Posterior temperature** — The effective temperature of the posterior
  being sampled; in SGLD, step size controls temperature — larger eps →
  hotter (flatter) posterior.
- **Robbins-Monro schedule** — Step size schedule eps_t satisfying sum eps_t
  = inf and sum eps_t^2 < inf; guarantees convergence of stochastic
  approximation algorithms.

## Connections

**Builds on.**

- Langevin Monte Carlo (Roberts & Tweedie 1996) — SGLD replaces the exact
  gradient in continuous Langevin dynamics with a minibatch stochastic
  gradient, making it scalable.
- SGD (Robbins & Monro 1951) — SGLD adds a noise term to SGD whose magnitude
  matches the Langevin prescription; recovers SGD as a special case when
  noise is suppressed.

**Related.**

- Gossip ULA / Generalized EXTRA SGLD ([LIT-366](../literature.d/LIT-366.md)) — Decentralized
  extensions of SGLD using gossip averaging; Gossip ULA applies SGLD in a
  multi-agent gossip network.
- Generalized EXTRA Stochastic Gradient Langevin Dynamics ([LIT-345](../literature.d/LIT-345.md)) —
  Adds EXTRA-style gradient correction to decentralized SGLD to eliminate
  topology-induced bias.
- SGHMC, pSGLD, and the broader stochastic MCMC literature — SGLD spawned a
  family of algorithms adding momentum, preconditioning, and variance
  reduction to the basic SGLD update.

## Recommendations

- **R1** — Use SGLD instead of SGD when uncertainty quantification is needed
  and the dataset is too large for traditional MCMC.
  *Topic:* optimizer selection for Bayesian inference · *Strength:* strong ·
  *When:* Large datasets where full-batch gradients are computationally
  prohibitive; non-convex posteriors where variational approximations may be
  poor.
- **R2** — Run with constant step size during exploration, then anneal to
  zero for final posterior convergence; this exploits the optimizer-sampler
  duality.
  *Topic:* SGLD step size schedule · *Strength:* moderate · *When:* When both
  good initialization (optimization phase) and posterior coverage (sampling
  phase) are desired.

## Bearing on the record

SGLD, and the observation the whole Langevin line rests on — the same update
is an optimizer and a sampler, distinguished only by the step-size schedule.

## Limitations

- Requires careful tuning of step size schedule; too large causes bias, too
  small causes slow mixing.
- No Metropolis-Hastings correction means finite-step-size bias is
  uncontrolled in practice (later works like SGHMC address this).
- Mixing time can be slow for multimodal posteriors; gossip extensions
  (Gossip ULA) address this via distributed exploration.
- Theory assumes log-concave or mildly non-convex posteriors; convergence
  for deep network posteriors requires additional assumptions.

## Open questions

- What is the effective posterior temperature in practice for deep networks
  trained with SGLD?
- How does SGLD compare to modern variational inference (VI) for deep
  network uncertainty?
- Can the decentralized gossip extensions (Gossip ULA) be made as
  practically usable as SGLD while retaining the posterior sampling
  guarantee?
