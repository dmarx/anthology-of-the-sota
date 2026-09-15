---
status: 'Active'
title: 'The Variational Formulation of the Fokker-Planck Equation'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '1998-01-01'
doi: '10.1137/S0036141096303359'
first_author: 'Jordan'
keywords:
- 'fokker-planck'
- 'wasserstein-gradient-flow'
- 'variational-scheme'
- 'free-energy'
implementations: []
summary: >-
  Jordan et al. (1998), [DOI:10.1137/S0036141096303359.](https://doi.org/10.1137/S0036141096303359.) The Fokker-Planck
  equation is the gradient flow of free energy in the Wasserstein metric,
  realized by an implicit variational scheme.
---
# LIT-tmpg3bdr: The Variational Formulation of the Fokker-Planck Equation

Jordan et al. (1998) — [DOI:10.1137/S0036141096303359](https://doi.org/10.1137/S0036141096303359)

## Key takeaways

Establishes that the Fokker-Planck equation ∂_t ρ = Δρ + ∇·(ρ∇V) is the
gradient flow of the free energy functional F(ρ) = ∫ ρ log ρ dx + ∫ V ρ dx
with respect to the 2-Wasserstein metric W₂ on the space of probability
measures. Introduces the JKO implicit time-discretization scheme as the
rigorous realization of this gradient flow, providing a purely variational
proof of existence and convergence of Fokker-Planck solutions. This paper
founded the field of Wasserstein gradient flows, unifying diffusion
processes, optimal transport, and free energy minimization in a single
geometric framework.

- The Fokker-Planck equation ∂_t ρ = Δρ + ∇·(ρ∇V) is the W₂ gradient flow of
  F(ρ) = ∫ ρ log ρ dx + ∫ Vρ dx
- JKO scheme: ρ^{n+1} = argmin_ρ { W₂(ρ,ρ^n)²/(2τ) + F(ρ) } converges to the
  Fokker-Planck solution as τ→0
- The Gibbs measure π ∝ exp(−V) is the unique global minimizer of F and the
  unique stationary distribution of the Fokker-Planck flow
- If π satisfies a log-Sobolev inequality with constant α, the Fokker-Planck
  flow satisfies KL(ρ_t ‖ π) ≤ KL(ρ_0 ‖ π) exp(−2αt)
- The entropy production −d/dt F(ρ_t) equals the Fisher information I(ρ_t ‖
  π) = ∫ |∇ log(ρ_t/π)|² ρ_t dx ≥ 0

## What the evidence does not cover

- Original paper proves convergence of JKO scheme but does not establish
  quantitative rates in τ (step size); those came in subsequent work
- Analysis is for continuous-space, exact-gradient Fokker-Planck; stochastic
  gradient noise (as in SGLD) introduces an additional O(τ) bias at
  stationarity
- The gradient flow structure is for the single-particle Fokker-Planck;
  extending to the coupled N-particle GELS system requires a tensor-product
  or mean-field extension of the W₂ geometry
- LSI constants are typically computable only for log-concave or strongly
  structured potentials; for non-convex neural network losses the LSI may
  fail or hold only locally
- The JKO scheme is computationally intractable in high dimensions due to
  the W₂ minimization; practical algorithms (SGLD, ULA) are approximations
  whose JKO interpretation is approximate

## Standing in the anthology

Read — the reading is [NOTE-tmpfbz2e](../notes.d/NOTE-tmpfbz2e.md). Arrived in the imported batch, which
brought in the mean-field account of wide networks, where the object that
moves is the distribution of neurons.
