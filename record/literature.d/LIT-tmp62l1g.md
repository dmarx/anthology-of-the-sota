---
status: 'Active'
title: 'Consensus Based Sampling'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '2021-06-01'
arxiv: '2106.02519'
first_author: 'Carrillo'
keywords:
- 'derivative-free'
- 'bayesian-inversion'
- 'interacting-particles'
- 'sampling'
implementations: []
summary: >-
  Carrillo et al. (2021), [ARXIV-2106.02519](https://arxiv.org/abs/2106.02519). Consensus-based sampling: an
  interacting-particle method that produces Gaussian posterior approximations
  without derivatives, tuned by an interpolation parameter between
  optimization and sampling.
---
# LIT-tmp62l1g: Consensus Based Sampling

Carrillo et al. (2021) — [ARXIV-2106.02519](https://arxiv.org/abs/2106.02519)

## Key takeaways

Introduces Consensus Based Sampling (CBS), a derivative-free, affine-
invariant interacting particle method that, via a single parameter choice,
performs either Bayesian posterior sampling or MAP optimization, with
convergence analysis in Gaussian and near-Gaussian settings.

- CBS unifies sampling and MAP optimization in a single particle system via
  a single parameter λ
- In the mean-field Gaussian setting, converges to the exact posterior with
  closed-form rates
- Affine invariance: dynamics is unchanged under reparameterization θ → Bθ+b
- Adaptive β via effective-sample-size criterion gives large practical
  speedups
- Theorem 3.10 (1D): nonlinear CBS sampling has a Gaussian fixed point
  O(1/β) close to the Laplace approximation

## What the evidence does not cover

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

## Standing in the anthology

Read — the reading is [NOTE-tmpmo2jn](../notes.d/NOTE-tmpmo2jn.md). Arrived in the imported batch, which
brought in the consensus, synchronization and flocking literature that the
decentralized-training results rest on.
