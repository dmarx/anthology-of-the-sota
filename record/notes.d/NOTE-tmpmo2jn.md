---
status: Read
paper: LIT-tmp62l1g
title: 'Consensus Based Sampling'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  By replacing the empirical covariance in a CBO-like consensus update with a
  Gibbs-weighted covariance and scaling the noise by a parameter λ, the same
  interacting particle dynamics can converge to a Gaussian approximation of
  the posterior (λ = 1/(1+β), sampling mode) or collapse to the MAP estimator
  (λ = 1, optimization mode), while preserving affine invariance.
---
# NOTE-tmpmo2jn: Consensus Based Sampling

## Contribution

Introduces Consensus Based Sampling (CBS), a derivative-free, affine-
invariant interacting particle method that, via a single parameter choice,
performs either Bayesian posterior sampling or MAP optimization, with
convergence analysis in Gaussian and near-Gaussian settings.

## Key insight

By replacing the empirical covariance in a CBO-like consensus update with a
Gibbs-weighted covariance and scaling the noise by a parameter λ, the same
interacting particle dynamics can converge to a Gaussian approximation of
the posterior (λ = 1/(1+β), sampling mode) or collapse to the MAP estimator
(λ = 1, optimization mode), while preserving affine invariance.

## Assumptions

- Forward model evaluations available but gradients are not (derivative-free
  setting)
- Target posterior unimodal or near-Gaussian for rigorous convergence
  results
- Mean-field limit (J → ∞ particle count) for the main theoretical analysis
- Linear forward model and Gaussian prior for sharp closed-form rates (Props
  2.4–2.6)

## Key results

- CBS unifies sampling and MAP optimization in a single particle system via
  a single parameter λ
- In the mean-field Gaussian setting, converges to the exact posterior with
  closed-form rates
- Affine invariance: dynamics is unchanged under reparameterization θ → Bθ+b
- Adaptive β via effective-sample-size criterion gives large practical
  speedups
- Theorem 3.10 (1D): nonlinear CBS sampling has a Gaussian fixed point
  O(1/β) close to the Laplace approximation

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | For linear forward models and Gaussian initial data, CBS in sampling mode (λ = 1/(1+β)) converges in the mean-field limit to the true Gaussian posterior with explicit sharp rates. | strong | Propositions 2.4–2.6: closed-form analysis of moment evolution yielding rates like (1+αβ)/(1+β) per iteration. |
| C2 | For linear forward models and Gaussian initial data, CBS in optimization mode (λ = 1) converges to a Dirac at the MAP with algebraic rate O(1/n). | strong | Explicit moment recursions and matrix inequalities giving covariance decay (k₀+β)/(k₀+β+β(1−α²)n). |
| C3 | CBS is affine invariant in both discrete and continuous time. | strong | Direct algebraic verification that reparameterization θ̃ = Bθ+b commutes with the dynamics. |
| C4 | For nonlinear f with bounded-from-above/below Hessian, CBS in sampling mode admits a Gaussian steady state that is close (O(1/β)) to the Laplace approximation of the target, with a local contraction rate. | moderate | Theorem 3.10 (d=1), via Laplace's method expansion and Banach fixed-point argument on the mean/covariance map. |
| C5 | For 1D non-Gaussian convex f, the optimization mode converges to the global minimizer with rate O(log n / n) when α=0. | moderate | Proposition 3.8; extensions to α ∈ (0,1] yield weaker non-optimal rates. |
| C6 | Dynamically adapting β via an effective-sample-size criterion dramatically improves CBS performance in practice. | moderate | Numerical experiments on Ackley/Rastrigin (Tables 3–7) showing orders-of-magnitude fewer iterations and much higher accuracy with adaptive β. |

## Method

**Consensus Based Sampling (CBS).**

CBS evolves an ensemble of particles {θ⁽ʲ⁾} that interact through Gibbs-
weighted mean M_β(ρ) and covariance C_β(ρ) with weights e^{-βf(θ)}. Each
step moves particles toward M_β with inertia α and injects Gaussian noise
with covariance (1-α²)λ⁻¹ C_β(ρ). Choosing λ = 1/(1+β) targets the posterior
(sampling mode); choosing λ = 1 drives collapse to the MAP (optimization
mode). Continuous-time analogs are mean-field SDEs whose steady states are
Gaussian.

- Gibbs-weighted mean M_β and covariance C_β (no gradients required)
- Inertia parameter α ∈ [0,1] interpolating between discrete-time and
  continuous-time regimes
- Mode parameter λ selecting sampling vs optimization
- Finite-particle Monte Carlo approximation of M_β and C_β
- Optional adaptive β schedule via effective sample size criterion

## Concepts

- **CBS sampling mode** — Parameter choice λ = 1/(1+β) under which the CBS
  mean-field steady state is Gaussian matching (or approximating via
  Laplace) the target posterior.
- **CBS optimization mode** — Parameter choice λ = 1 under which CBS
  particles collapse to a point approximating the MAP/global minimizer.
- **Affine invariance** — The dynamics is unchanged (up to an affine map of
  the state) under θ → Bθ+b, giving conditioning-independent convergence
  rates for linear Gaussian problems.
- **Gibbs-weighted moments M_β, C_β** — First and second moments of ρ
  reweighted by e^{-βf}/Z, acting as a softmax-like consensus point and
  spread used to drive the particle dynamics.

## Connections

**Builds on.**

- A consensus-based model for global optimization and its mean-field limit
  (Pinnau, Totzeck, Tse, Martin, 2017) — CBS extends the CBO optimization
  paradigm by introducing a sampling variant with rescaled noise and Gibbs-
  weighted covariance.
- Interacting Langevin diffusions: gradient structure and ensemble Kalman
  sampler (Garbuno-Inigo, Hoffmann, Li, Stuart, 2020) — Parallels the
  EKI→EKS development; CBS provides a consensus-based, derivative-free
  analog of EKS with similar affine invariance.
- An analytical framework for consensus-based global optimization (Carrillo,
  Choi, Totzeck, Tse, 2018) — Shares convexity-type assumptions on f used
  here for non-Gaussian analysis.

**Related.**

- Generalized EXTRA Stochastic Gradient Langevin Dynamics ([LIT-tmptm9xf](../literature.d/LIT-tmptm9xf.md)) —
  GELS is gossip SGLD — CBS provides the mean-field theory for its
  stationary distribution that EXTRA SGLD theory lacks
- A Bayesian Perspective on Generalization and Stochastic Gradient Descent
  ([LIT-tmpjdj3o](../literature.d/LIT-tmpjdj3o.md)) — Both interpret sampling / noise injection as temperature
  control; CBS gives a particle-system view of the same posterior

## Recommendations

- **R1** — Use CBS with λ = 1/(1+β) to obtain Gaussian posterior
  approximations for Bayesian inverse problems when derivatives are
  unavailable or expensive.
  *Topic:* derivative-free Bayesian inversion · *Strength:* moderate · *When:*
  Target posterior is unimodal and close to Gaussian; forward model
  evaluations are the dominant cost.
- **R2** — For optimization tasks, prefer α = 0 (no inertia) and increase J
  (ensemble size) when f has many local minima.
  *Topic:* hyperparameter choice · *Strength:* moderate · *When:* Non-convex
  objectives in moderate dimension; confirmed on Ackley/Rastrigin
  benchmarks.
- **R3** — Adapt β during iterations using the effective sample size
  criterion J_eff(β) = ηJ rather than fixing β a priori.
  *Topic:* cooling schedule · *Strength:* strong · *When:* Whenever Gibbs
  weights risk being dominated by a few particles; gives large speedups in
  practice.
- **R4** — Leverage the invariant subspace property: initialize particles in
  a subspace containing the expected support of the target to control
  effective dimensionality.
  *Topic:* initialization · *Strength:* moderate · *When:* High-dimensional
  inverse problems where low-dimensional structure is known.

## Bearing on the record

Derivative-free sampling by an interacting ensemble. Nothing here cites it;
it is filed with the consensus line it belongs to.

## Limitations

- Laplace-approximation convergence result (Theorem 3.10) is proven only in
  dimension d=1.
- Accuracy is only rigorously characterized for unimodal, near-Gaussian
  posteriors; multimodal distributions are not handled.
- Analysis of the nonlinear Fokker–Planck equation (2.14) assumes
  existence/uniqueness of strong solutions without proof.
- No theory for the finite-particle system (only mean-field limit analyzed)
  or for the adaptive β scheme.
- Optimal convergence rates in the non-Gaussian optimization setting are
  obtained only for α=0; α ∈ (0,1] yields suboptimal rates.

## Open questions

- Can the Laplace-approximation result be extended to arbitrary dimension d?
- What is the rigorous relationship between particle count J and β needed
  for good finite-ensemble performance?
- Can the adaptive-β effective-sample-size heuristic be given a theoretical
  foundation?
- Can random batch or generalized square-root techniques (as in ALDI) make
  CBS efficient when J ∼ d?
- Is there a variant of CBS that provably handles multimodal target
  distributions?
