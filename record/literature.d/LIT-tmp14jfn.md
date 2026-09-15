---
status: 'Active'
title: 'Bayesian Learning via Stochastic Gradient Langevin Dynamics'
version: 1
tags:
- training-optimization
date: '2026-09-15'
published: '2011-06-01'
url: 'https://icml.cc/2011/papers/398_icmlpaper.pdf'
first_author: 'Welling'
keywords:
- 'langevin'
- 'posterior-sampling'
- 'stochastic-gradient'
- 'uncertainty'
implementations: []
summary: >-
  Welling and Teh (2011), [Bayesian Learning via Stochastic Gradient Langevin
  Dynamics](https://icml.cc/2011/papers/398_icmlpaper.pdf). Adding correctly
  scaled Gaussian noise to a decaying-step-size SGD update turns the optimizer
  into a posterior sampler, with no accept-reject step.
---
# LIT-tmp14jfn: Bayesian Learning via Stochastic Gradient Langevin Dynamics

Welling and Teh (2011) — [Bayesian Learning via Stochastic Gradient Langevin Dynamics](https://icml.cc/2011/papers/398_icmlpaper.pdf)

## Key takeaways

Introduces Stochastic Gradient Langevin Dynamics (SGLD), which adds a
calibrated Gaussian noise term to SGD updates to perform approximate
Bayesian posterior sampling rather than point estimation. Shows that as step
size anneals to zero, the iterates converge to exact samples from the
posterior; at larger step sizes it acts like an efficient optimizer. Bridges
MCMC sampling and SGD in a single algorithm that scales to large datasets
via minibatch gradient estimates.

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

## What the evidence does not cover

- Requires careful tuning of step size schedule; too large causes bias, too
  small causes slow mixing.
- No Metropolis-Hastings correction means finite-step-size bias is
  uncontrolled in practice (later works like SGHMC address this).
- Mixing time can be slow for multimodal posteriors; gossip extensions
  (Gossip ULA) address this via distributed exploration.
- Theory assumes log-concave or mildly non-convex posteriors; convergence
  for deep network posteriors requires additional assumptions.

## Standing in the anthology

Read — the reading is [NOTE-tmphpvzh](../notes.d/NOTE-tmphpvzh.md). Arrived in the imported batch, which
brought in the Langevin branch, where the training noise is the sampler.
