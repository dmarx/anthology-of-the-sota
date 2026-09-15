---
number: 118
status: Read
formerly:
- NOTE-tmpfbz2e
paper: LIT-296
title: 'The Variational Formulation of the Fokker-Planck Equation'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  Langevin dynamics — and hence SGLD — is not merely a diffusion process but
  gradient descent on the free energy functional F(ρ) = KL(ρ ‖ π) in the
  infinite-dimensional Riemannian manifold of probability measures equipped
  with the W₂ metric. The unique stationary point is the Gibbs measure π ∝
  exp(−V), which minimizes F.
---
# NOTE-118: The Variational Formulation of the Fokker-Planck Equation

## Contribution

Establishes that the Fokker-Planck equation ∂_t ρ = Δρ + ∇·(ρ∇V) is the
gradient flow of the free energy functional F(ρ) = ∫ ρ log ρ dx + ∫ V ρ dx
with respect to the 2-Wasserstein metric W₂ on the space of probability
measures. Introduces the JKO implicit time-discretization scheme as the
rigorous realization of this gradient flow, providing a purely variational
proof of existence and convergence of Fokker-Planck solutions. This paper
founded the field of Wasserstein gradient flows, unifying diffusion
processes, optimal transport, and free energy minimization in a single
geometric framework.

## Key insight

Langevin dynamics — and hence SGLD — is not merely a diffusion process but
gradient descent on the free energy functional F(ρ) = KL(ρ ‖ π) in the
infinite-dimensional Riemannian manifold of probability measures equipped
with the W₂ metric. The unique stationary point is the Gibbs measure π ∝
exp(−V), which minimizes F. The JKO scheme makes this precise: each time
step is a proximal minimization ρ^{n+1} = argmin_ρ { W₂(ρ, ρ^n)² / (2τ) +
F(ρ) }, and as τ→0 the iterates converge to the continuous-time Fokker-
Planck flow. The rate of convergence to stationarity is controlled by the
log-Sobolev inequality (LSI) constant of π: if π satisfies LSI(α), then
KL(ρ_t ‖ π) ≤ KL(ρ_0 ‖ π) exp(−2αt). This geometric perspective transforms
convergence analysis of Langevin-based algorithms from a study of SDEs into
a question about functional inequalities and optimal transport geometry.

## Assumptions

- Potential V : ℝ^d → ℝ is smooth (C² suffices) and grows sufficiently at
  infinity to ensure that π ∝ exp(−V) is a proper probability measure
- Initial density ρ_0 has finite free energy F(ρ_0) < ∞ and finite second
  moment
- The space of probability measures with finite second moment is equipped
  with the W₂ metric (Wasserstein-2)
- The JKO minimization problem has a unique minimizer at each step (ensured
  by convexity of F along generalized geodesics)
- Domain is ℝ^d (or a convex domain with Neumann boundary conditions); no
  topological obstructions

## Key results

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

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The Fokker-Planck equation is the W₂ gradient flow of the free energy F | strong | Proven by showing the Euler-Lagrange equation of the JKO scheme converges to the Fokker-Planck equation in the τ→0 limit; later made fully rigorous in the general theory of Ambrosio-Gigli-Savaré |
| C2 | The JKO scheme converges to the Fokker-Planck solution | strong | Established by compactness arguments and discrete free energy inequalities; rates of convergence in τ established in subsequent work |
| C3 | The geometry of W₂ is the natural metric for analyzing Langevin dynamics and related diffusions | strong | The gradient flow structure makes the LSI-controlled convergence rate a direct consequence of the Riemannian geometry; this has been confirmed by decades of subsequent work in the field |
| C4 | Log-Sobolev inequality constant α controls the convergence rate to stationarity | strong | Follows from the gradient flow identity and the Bakry-Émery criterion; α can be computed explicitly for strongly log-concave potentials (V with ∇²V ≽ αI) |

## Method

**JKO (Jordan-Kinderlehrer-Otto) implicit Euler scheme.**

At each time step, compute ρ^{n+1} as the minimizer of the sum of a W₂
proximity term (penalizing displacement from the current iterate ρ^n) and
the free energy F. This is an implicit (backward Euler) time discretization
of the W₂ gradient flow. As the step size τ→0, the discrete iterates
converge in the narrow topology to the continuous Fokker-Planck solution.
The scheme inherits unconditional stability from its variational structure:
free energy is non-increasing along iterates.

- W₂ proximity term W₂(ρ, ρ^n)²/(2τ) acting as a Riemannian metric
  regularizer
- Free energy functional F(ρ) = H(ρ) + E(ρ) splitting entropy H = ∫ ρ log ρ
  and potential energy E = ∫ Vρ
- Euler-Lagrange equation of the JKO step: log ρ^{n+1} + V = const − φ_τ,
  where φ_τ is the Kantorovich potential for the W₂ transport from ρ^{n+1}
  to ρ^n
- Passage to the continuous limit τ→0 via compactness in the narrow topology
  on probability measures

## Concepts

- **W₂ gradient flow** — A curve t ↦ ρ_t in the space of probability
  measures that is the steepest descent of a functional F with respect to
  the W₂ metric, satisfying the evolution variational inequality of De
  Giorgi
- **Free energy functional F** — F(ρ) = ∫ ρ log ρ dx + ∫ Vρ dx = KL(ρ ‖ Leb)
  + E_V(ρ); equivalently F(ρ) = KL(ρ ‖ π) + const where π ∝ exp(−V)
- **JKO scheme** — The variational time discretization ρ^{n+1} = argmin_ρ {
  W₂(ρ, ρ^n)²/(2τ) + F(ρ) }; the proximal point algorithm lifted to the
  Wasserstein space
- **Log-Sobolev inequality (LSI)** — A functional inequality H(ρ|π) ≤ (1/2α)
  I(ρ|π) relating relative entropy to Fisher information; implies
  exponential decay of KL divergence to stationarity at rate 2α under the
  Fokker-Planck flow
- **Fisher information** — I(ρ ‖ π) = ∫ |∇ log(ρ/π)|² ρ dx; equals the rate
  of free energy dissipation −dF/dt along the Fokker-Planck flow
- **Gibbs measure** — The probability measure π ∝ exp(−V) that is the unique
  minimizer of F and the stationary distribution of the Fokker-Planck /
  Langevin dynamics with potential V
- **Wasserstein-2 metric W₂** — The L² optimal transport distance on the
  space of probability measures with finite second moment: W₂(μ,ν)² =
  min_{γ∈Γ(μ,ν)} ∫|x−y|² dγ

## Connections

**Builds on.**

- Polar factorization and monotone rearrangement of vector-valued functions
  (Brenier 1991) — Brenier's theorem on optimal transport maps is the
  technical foundation for the W₂ geometry exploited in the JKO scheme
- Diffusions hypercontractives (Bakry-Émery 1985) — The Bakry-Émery
  criterion provides checkable conditions (∇²V ≽ αI) guaranteeing the LSI
  that controls JKO convergence rates

**Related.**

- Consensus Based Sampling ([LIT-262](../literature.d/LIT-262.md)) — CBS uses the W₂ gradient flow
  framework directly — the CBS drift is designed so that the mean-field
  McKean-Vlasov SDE implements gradient flow of a free energy in W₂,
  inheriting JKO convergence theory
- Convex Analysis of the Mean Field Langevin Dynamics ([LIT-282](../literature.d/LIT-282.md)) —
  Nitanda et al. use the JKO / W₂ gradient flow framework to analyze mean
  field Langevin dynamics for neural network training, applying exactly the
  free energy minimization perspective introduced by Jordan-Kinderlehrer-
  Otto

## Recommendations

- **R1** — Frame the convergence analysis of GELS in terms of the W₂
  gradient flow of a coupled free energy functional; the JKO scheme provides
  the natural implicit discretization and the LSI controls the convergence
  rate **[not filed as a practice: specific to the project these readings
  were made for]**
  *Topic:* GELS convergence theory · *Strength:* strong · *When:* Requires
  identifying the appropriate free energy for the coupled GELS system
  (individual SGLD entropy + gossip coupling energy) and verifying a log-
  Sobolev inequality for the joint stationary distribution
- **R2** — Use the Fisher information identity −dF/dt = I(ρ_t ‖ π) as a
  Lyapunov function for GELS convergence proofs, since the SGLD component of
  GELS is a time discretization of Langevin dynamics **[not filed as a
  practice: specific to the project these readings were made for]**
  *Topic:* GELS Lyapunov analysis · *Strength:* strong · *When:* Discretization
  error from SGLD time-stepping must be bounded separately; standard results
  give O(τ) bias in steady state
- **R3** — The optimal transport geometry of W₂ is the right language for
  comparing the stationary distributions of GELS vs. large-batch SGD; use W₂
  distance to quantify how gossip coupling shifts the stationary measure
  relative to the target π **[not filed as a practice: specific to the
  project these readings were made for]**
  *Topic:* GELS vs. large-batch SGD generalization (Q4) · *Strength:* moderate ·
  *When:* Requires extending the JKO analysis to the coupled multi-particle
  system; direct application of single-particle JKO results requires
  verification that the gossip coupling is compatible with the gradient flow
  structure

## Bearing on the record

The Fokker-Planck equation as a gradient flow of free energy in the
Wasserstein metric. This is the geometry the mean-field papers are working
in, and none of them is readable without it.

## Limitations

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

## Open questions

- What is the effective free energy of the full GELS system (N chains +
  gossip coupling), and does it admit a JKO gradient flow structure in the
  product W₂ space?
- Does the gossip coupling in GELS improve the LSI constant of the effective
  free energy relative to isolated SGLD chains, and by how much?
- Can the W₂ convergence rate for GELS be made explicit in terms of the
  gossip spectral gap and the SGLD step size?
- How does the JKO framework extend to the McKean-Vlasov free energy
  relevant when N→∞ in GELS (where each chain feels the mean-field of all
  others)?
