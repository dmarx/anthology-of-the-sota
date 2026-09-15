---
number: 146
status: Read
formerly:
- NOTE-tmptp14x
paper: LIT-310
title: 'Phase transitions, logarithmic Sobolev inequalities, and uniform-in-time propagation of chaos for weakly interacting diffusions'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  Both the N-particle Fokker-Planck equation and its McKean-Vlasov mean-field
  limit are 2-Wasserstein gradient flows of related free energies (E^N and
  E^MF), and E^N Gamma-converges to E^MF.
---
# NOTE-146: Phase transitions, logarithmic Sobolev inequalities, and uniform-in-time propagation of chaos for weakly interacting diffusions

## Contribution

The paper establishes precise links between (i) the non-degeneracy of the
log-Sobolev inequality (LSI) constant of the N-particle Gibbs measure as
N→∞, (ii) absence of phase transitions for the McKean-Vlasov mean-field
limit, and (iii) uniform-in-time propagation of chaos plus Gaussianity of
equilibrium fluctuations. It provides gradient-flow / Wasserstein-calculus
proofs of a generalized Talagrand inequality and quantitative propagation of
chaos, and proves uniform LSI at high temperature for weakly-interacting,
possibly non-convex potentials via the two-scale approach.

## Key insight

Both the N-particle Fokker-Planck equation and its McKean-Vlasov mean-field
limit are 2-Wasserstein gradient flows of related free energies (E^N and
E^MF), and E^N Gamma-converges to E^MF. Consequently, the large-N behavior
of the N-particle LSI constant λ_LS^N governs all important features of the
mean-field system: a non-minimising critical point of E^MF forces λ_LS^N→0,
while λ_LS^N bounded away from 0 yields a unique steady state, uniform-in-
time propagation of chaos (with O(1/√N) Wasserstein distance) and Gaussian
equilibrium fluctuations. Phase transitions of the mean-field PDE and
degeneracy of the uniform LSI are thus conjecturally equivalent.

## Assumptions

- V lower semicontinuous, bounded below, K_V-convex (semi-convex, possibly
  non-convex), with growth V(x) ≥ |x|^δ at infinity
- W is K_W-convex on R^{2d} (semi-convex pair potential)
- Doubling-type bound: ||∇_1 W(x,y)|| ≤ C(1+|W(x,y)|+V(x)+V(y))
- Exchangeable IID initial data ρ_in^{⊗N}; symmetric N-particle laws (IID
  across workers does NOT apply—this is a mean-field physics model)
- Far-field convexity D^2 H^N ≥ λ I for ||x||>R (used for LSI)
- For fluctuation theorem: Ω = T^d, V and W smooth, liminf λ_LS^N > 0

## Key results

- **Theorem 3.2 (generalised Talagrand).** E^N[ρ^N] - E^N[M_N] ≥ (λ_LS^N/2)
  d̄_2^2(ρ^N, M_N); analogously E^MF[ρ] - inf E^MF ≥ (λ_LS^∞/2) d_2^2(ρ, K)
  *Holds when:* Holds for gradient-flow-regular energies; proof via Otto
  calculus on (P(Ω), d_2)
- **Theorem 3.3.** limsup_{N→∞} λ_LS^N ≤ λ_LS^∞
  *Holds when:* Under Assumptions 2.1–2.2; mean-field LSI upper-bounds the
  large-N particle LSI
- **Theorem 3.6 (Gibbs approximation).** d̄_2^2(ρ_β^{⊗N}, M_N) ≤ (2/λ_LS^N)
  Ē(ρ_β^{⊗N}||M_N) ≤ C/N
  *Holds when:* Requires λ_LS^N bounded away from 0 uniformly in N
- **Theorem 3.7 (uniform-in-time propagation of chaos).** sup_{t≥0}
  d̄_2(ρ^N(t), ρ(t)^{⊗N}) ≤ C N^{-θ} for some θ>0
  *Holds when:* Requires uniform LSI (λ_LS^N bounded below) and E^MF[ρ_in] <
  ∞; θ not sharp when K_V+K_W(1-1/N)<0
- **Theorem 3.11 (equilibrium fluctuations).** η^N = √N(μ^N - ρ_β) converges
  in law to Gaussian field η^∞ solving linear SPDE with covariance Q_G
  *Holds when:* Ω = T^d, V,W smooth, liminf λ_LS^N > 0; convergence in
  C([0,T]; H^{-m}) for m > d/2+3
- **Theorem 3.14 (uniform LSI at high temperature).** λ_LS^N ≥ c > 0
  uniformly in N
  *Holds when:* Compact Ω, or bounded W with small ||W||_∞ and ||D^2_{xy}
  W||_∞ relative to temperature (β small); proved via two-scale LSI
- **Classical propagation of chaos (Theorem 10.1).** d̄_2(ρ^N(t), ρ(t)^{⊗N})
  ≤ [(1-e^{-Kt/2})/K] · C/√N where K = K_V+K_W(1-1/N)
  *Holds when:* Constants blow up exponentially if K<0 (non-convex)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Non-degenerate uniform LSI for the N-particle Gibbs measure implies uniform-in-time propagation of chaos at rate N^{-θ}. | strong | Theorem 3.7 |
| C2 | Phase transition (non-unique mean-field critical points) forces the N-particle LSI constant to degenerate as N→∞. | strong | Theorem 3.4 and the Talagrand inequality structure |
| C3 | Under uniform LSI, equilibrium fluctuations around ρ_β are Gaussian with explicit covariance operator. | strong | Theorem 3.11 |
| C4 | At high temperature (or small interaction) with bounded W, the uniform LSI holds. | strong | Theorem 3.14 via two-scale criterion of Otto-Reznikoff |
| C5 | lim_{N→∞} λ_LS^N = λ_LS^∞ (mean-field dissipation constant). | weak | Conjecture 1; only upper bound proved |

## Method

**Wasserstein gradient flow / Otto calculus approach to N-particle LSI.**

Treat both the N-particle Fokker-Planck equation and the McKean-Vlasov PDE
as 2-Wasserstein gradient flows of E^N and E^MF respectively. Use Gamma-
convergence of E^N → E^MF (via de Finetti / Hewitt-Savage) to transfer
properties between levels. Prove Talagrand-type inequalities using Otto
calculus on geodesics in (P(Ω), d_2). For uniform LSI, apply the two-scale
Otto-Reznikoff criterion to marginal and conditional measures of M_N. For
fluctuations, linearize around ρ_β and identify the limiting Ornstein-
Uhlenbeck SPDE.

- Gamma-convergence of free energies E^N → E^MF
- de Finetti/Hewitt-Savage limit for exchangeable measures
- Scaled 2-Wasserstein distance d̄_2 = d_2/√N
- Two-scale LSI criterion (marginal + conditional)
- HWI-type inequality via Otto calculus
- Linearised McKean-Vlasov operator L_{ρ_β}

## Concepts

- **Logarithmic Sobolev Inequality (LSI) constant λ_LS^N** — Largest
  constant such that β^{-1} Ī(ρ^N||M_N) ≥ λ_LS^N Ē(ρ^N||M_N) for all ρ^N on
  Ω^N, where Ē is the scaled relative entropy and Ī the scaled relative
  Fisher information.
- **Mean-field LSI constant λ_LS^∞** — inf over non-minimizers of
  D(ρ)/(E^MF[ρ] - min E^MF), where D(ρ) is the mean-field dissipation.
- **Scaled 2-Wasserstein distance** — d̄_2(ρ^N_1, ρ^N_2) = inf
  (E[||X-Y||^2]/N)^{1/2}; makes ρ → ρ^{⊗N} an isometry.
- **Phase transition (flat case)** — On T^d with V≡0, W(x-y), existence of
  β_c>0 beyond which local stability (Property A), self-consistency
  uniqueness (Property B), or dissipation inequality (Property C) fails.
- **Gibbs measure M_N** — M_N = Z_N^{-1} exp(-β H_N) dx, the invariant
  measure of the N-particle Langevin system.
- **Equilibrium fluctuation field** — η^N(t) = √N(N^{-1} Σ δ_{X_t^i} - ρ_β),
  an H^{-s}-valued process.

## Connections

**Builds on.**

- Ambrosio-Gigli-Savaré, Gradient flows in metric spaces (2008) —
  Foundational Wasserstein gradient flow framework used throughout.
- Otto-Reznikoff, A new criterion for the LSI (2007) — Two-scale LSI
  criterion used to prove Theorem 3.14.
- Hauray-Mischler, On Kac's chaos (2014) — Provides the gradient-flow/Gamma-
  convergence approach to propagation of chaos.
- Carrillo-Gvalani-Pavliotis-Schlichting, Long-time behaviour and phase
  transitions for McKean-Vlasov on the torus — Phase transition
  classification and linearisation machinery reused here.
- Bauerschmidt-Bodineau, Very simple proof of LSI for high-temperature spin
  systems (2019) — Yields sharp uniform LSI up to β_c for the Brownian mean-
  field / XY model.
- Malrieu, Convergence to equilibrium for granular media (2003) — Classical
  convex-case uniform-in-time propagation of chaos extended here to non-
  convex regime.

## Recommendations

- **R1** — When analyzing convergence of interacting-particle / SGD-like
  systems with pair-wise interactions, check whether the N-particle Gibbs
  measure satisfies a log-Sobolev inequality uniformly in N — it controls
  mixing, equilibrium accuracy, and fluctuation behaviour. **[not filed as a
  practice: advice on proof technique rather than on training]**
  *Topic:* log-Sobolev diagnostics · *Strength:* strong · *When:* Applies to
  reversible (Langevin/SDE) dynamics with a Gibbs stationary measure.
- **R2** —

## Bearing on the record

Uniform-in-N log-Sobolev inequalities, which is what makes propagation of
chaos hold uniformly in time. Filed for the mean-field line; no practice
here rests on it.
