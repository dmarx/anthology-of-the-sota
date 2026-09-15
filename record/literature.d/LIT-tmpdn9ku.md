---
status: 'Active'
title: 'The Kuramoto model: A simple paradigm for synchronization phenomena'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '2005-04-01'
doi: '10.1103/RevModPhys.77.137'
first_author: 'Acebron'
keywords:
- 'kuramoto'
- 'synchronization'
- 'coupled-oscillators'
- 'phase-transition'
implementations: []
summary: >-
  Acebron et al. (2005), [DOI:10.1103/RevModPhys.77.137.](https://doi.org/10.1103/RevModPhys.77.137.) The standard review of
  the Kuramoto model: the synchronization transition, the order parameter, and
  what noise does to the critical coupling.
---
# LIT-tmpdn9ku: The Kuramoto model: A simple paradigm for synchronization phenomena

Acebron et al. (2005) — [DOI:10.1103/RevModPhys.77.137](https://doi.org/10.1103/RevModPhys.77.137)

## Key takeaways

Comprehensive review of the Kuramoto model of coupled phase oscillators,
establishing its mathematical analysis, mean-field theory, and phase diagram
as a canonical reference. Derives the critical coupling strength K_c = 2/(π
g(0)) at which a synchronization phase transition occurs, and analyzes the
stochastic (noisy) variant in which individual oscillators are driven by
independent Brownian motions. Covers extensions to finite-N fluctuations,
non-mean-field topologies, and connections to other collective phenomena,
making it the standard entry point for mean-field synchronization theory.

- Phase transition at K_c = 2/(π g(0)): for K < K_c, the unique stationary
  state is incoherent (r = 0); for K > K_c, a branch of partially
  synchronized states with r > 0 bifurcates continuously from the incoherent
  state
- Mean-field (N→∞) description: the empirical distribution ρ(θ, ω, t)
  satisfies the nonlinear Fokker-Planck equation ∂_t ρ = −∂_θ [(ω + Kr
  sin(ψ−θ))ρ] + D ∂²_θ ρ where r e^{iψ} = ∫∫ e^{iθ} ρ dθ dω
- The incoherent state ρ = 1/(2π) is always a fixed point of the nonlinear
  Fokker-Planck; it is linearly stable for K < K_c and linearly unstable for
  K > K_c
- Near K_c the order parameter scales as r ~ √(K − K_c) (supercritical
  pitchfork bifurcation)
- Noisy Kuramoto (D > 0): the incoherent state remains stable for K < K_c(D)
  > K_c(0); the transition is smoothed and the stationary distribution is
  always diffuse, but a peak emerges at K > K_c(D)
- Finite-N fluctuations: r ~ O(1/√N) even in the incoherent phase due to
  shot noise; the phase transition sharpens as N → ∞
- Identical oscillators (g(ω) = δ(ω)): any K > 0 leads to full synchrony r =
  1; no phase transition

## What the evidence does not cover

- The Kuramoto model uses all-to-all mean-field coupling (1/N scaling); GELS
  uses sparse gossip on a fixed topology (fat-tree), so the exact K_c
  formula does not apply directly
- Kuramoto oscillators live on S^1 (circle); GELS parameters live in ℝ^d
  with d ~ 10^9, and the geometry of high-dimensional parameter space
  changes the synchronization analysis qualitatively
- The frequency distribution g(ω) in Kuramoto corresponds to heterogeneity
  in local loss gradients across GELS workers; in practice this
  heterogeneity is data-dependent and not i.i.d. from a fixed g
- The review covers the thermodynamic limit N→∞; finite-N corrections
  (O(1/√N) fluctuations in r) are important for the cluster sizes relevant
  to GELS (N ~ 10^3 – 10^4)
- The review's analysis is primarily for stationary distributions and
  steady-state synchrony; transient dynamics during training (non-stationary
  loss landscape) require additional analysis
- The connection between Kuramoto coupling K and GELS spectral gap is
  qualitative; making it quantitative requires deriving the GELS mean-field
  Fokker-Planck and its linear stability analysis from scratch

## Standing in the anthology

Read — the reading is [NOTE-tmp2qedl](../notes.d/NOTE-tmp2qedl.md). Arrived in the imported batch, which
brought in the consensus, synchronization and flocking literature that the
decentralized-training results rest on.
