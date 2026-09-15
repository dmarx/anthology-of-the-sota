---
status: Read
paper: LIT-tmp5zf18
title: 'The mean field analysis of the Kuramoto model on graphs II. Asymptotic stability of the incoherent state, center manifold reduction, and bifurcations'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  The network's structural imprint on synchronization onset is fully captured
  by the spectrum of the graphon kernel operator W: the critical coupling is
  2/(π g(0) μ_max) and the bifurcating partially synchronized state is a
  scalar multiple of the eigenfunction w_max of the largest eigenvalue μ_max,
  with √(K-K_c) amplitude (pitchfork).
---
# NOTE-tmpcs9g8: The mean field analysis of the Kuramoto model on graphs II. Asymptotic stability of the incoherent state, center manifold reduction, and bifurcations

## Contribution

Extends the rigorous bifurcation analysis of the classical Kuramoto model to
the KM on convergent graph sequences (graphons). Establishes asymptotic
stability of the incoherent state (via Landau damping in a rigged-Hilbert-
space/weak-dual sense) for K in [K_c^-, K_c^+], derives a center manifold
reduction at the critical coupling, and shows that the onset of
synchronization is a pitchfork bifurcation whose amplitude and spatial
pattern are given explicitly by the principal eigenvalue/eigenfunction of
the graphon kernel operator W.

## Key insight

The network's structural imprint on synchronization onset is fully captured
by the spectrum of the graphon kernel operator W: the critical coupling is
2/(π g(0) μ_max) and the bifurcating partially synchronized state is a
scalar multiple of the eigenfunction w_max of the largest eigenvalue μ_max,
with √(K-K_c) amplitude (pitchfork). Continuous-spectrum obstacles are
circumvented by generalized spectral theory on a rigged Hilbert space X ⊂ H
⊂ X', where the resolvent admits meromorphic continuation and generalized
eigenvalues drive the center manifold reduction.

## Assumptions

- Intrinsic-frequency density g(ω) is even, analytic (in Exp class), with
  g(0)>0 and g''(0)<0.
- Graphon W : I×I → R is symmetric and L^2, so W is a compact symmetric
  operator on L^2(I) with discrete real spectrum accumulating only at 0.
- μ_max = largest eigenvalue of W is simple (Section 5); in Section 6 it has
  a 2D eigenspace from translation symmetry W(x,y)=G(x-y).
- K ≥ 0 (negative K handled by sign flip of W); existence of the center
  manifold is assumed rather than rigorously proved.
- Not directly applicable to our IID/SGD optimization setting: assumptions
  concern continuous graphon limits and oscillator dynamics, not stochastic
  gradients.

## Key results

- **Theorem 4.1 (asymptotic stability of incoherent state).** For K ∈ [0,
  K_c^+), the trivial solution Z=0 of the linearized Fourier system is
  asymptotically stable for initial data in X ⊂ X' with respect to the weak
  dual topology on X' (Landau damping).
  *Holds when:* K_c^+ = 2/(π g(0) μ_max); holds despite continuous spectrum
  filling the imaginary axis and no negative-real-part eigenvalues.
- **Pitchfork bifurcation at K_c^+ (Section 5).** Order parameter on the
  stable bifurcating branch: h_∞(K) = g(0)^2 π^{3/2} / √(-g''(0)) ·
  μ_max^{3/2} · √(1/C(x)) · √(K - K_c^+) + o(√(K - K_c^+)).
  *Holds when:* Valid for K slightly above K_c^+ with μ_max simple; spatial
  profile proportional to w_max(x).
- **2D bifurcation with translation-invariant graphon (Section 6).** For
  W(x,y)=G(x-y) with dominant Fourier mode ±m, amplitude equations ṙ_± = p_1
  r_± (ε - α² p_2 (r_±² + 2 r_∓²)) yield bifurcating m-twisted states as
  stable equilibria.
  *Holds when:* p_2 = -8 g''(0)/(π³ g(0)^4); for W=cos(2π(x-y)), 1-twisted
  states emerge at K_c^+ ≈ 3.2.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Incoherent state in the graph KM is asymptotically stable (weak-dual) below critical coupling despite lacking spectral gap — a graph-analog of Landau damping. | strong | Theorem 4.1 via generalized resolvent / rigged Hilbert space construction. |
| C2 | Onset of synchronization on graphs is a supercritical pitchfork governed by the principal eigenpair (μ_max, w_max) of the graphon kernel operator. | strong | Center manifold reduction in Section 5; explicit amplitude formula (5.1). |
| C3 | Graphon symmetries (translation invariance) produce higher-dimensional center manifolds and give bifurcations to twisted states rather than uniform partial synchronization. | moderate | Section 6 amplitude ODEs plus numerical simulations (Fig. 2) for W=cos(2π(x-y)). |
| C4 | Explicit K_c^+ formulas for Erdős–Rényi, small-world, and weighted-circle graphs link network structure to synchronization threshold. | moderate | Section 5.3 examples, K_c^+ = 2/(π g(0)(2r+p-4pr)) for small-world. |

## Method

**Generalized spectral / center-manifold reduction for KM on graphons.**

1) Fourier-decompose the mean-field density ρ(t,θ,ω,x) in θ to obtain an
infinite hierarchy for z_j(t,ω,x); linearize at the incoherent state, giving
a linear operator T coupling z_1 through the kernel operator W. 2) Build a
rigged Hilbert space X ⊂ H ⊂ X' where X is the projective tensor product of
an exponential-class space Exp(β) of holomorphic functions in ω and L²(I).
3) Analytically continue the resolvent R(λ) = (λ - T)^{-1} from Re λ > 0
into the left half plane as an X → X' map (generalized resolvent R(λ)),
using Sokhotski–Plemelj. 4) Define generalized eigenvalues as singularities
of R(λ); the critical condition is 2/(Kμ) = D(λ), giving K_c^+ = 2/(π g(0)
μ_max). 5) Construct generalized Riesz projection Π_0 onto the 1D (or 2D)
null space at K=K_c^+. 6) Center-manifold reduction: set z_1 = α c(t) v_c^+
+ O(α²), ε = K - K_c^+ = α², project the dynamics with Π_0 to obtain a
scalar (or 2D) amplitude ODE; identify pitchfork form.

- Rigged Hilbert space via exponential-class functions Exp(β) ⊗ L²(I).
- Generalized resolvent and Riesz projection Π_0.
- Principal eigenpair (μ_max, w_max) of kernel operator W as the driver of
  the bifurcation.
- Amplitude equation for order parameter h, analogous to Kuramoto's original
  pitchfork but with graphon-weighted spatial profile.

## Concepts

- **Graphon kernel operator W** — Compact symmetric integral operator
  `W[f](x) = ∫ W(x,y) f(y) dy` on L²(I) whose spectrum encodes the limiting
  network structure of a convergent graph sequence.
- **Incoherent state ρ_u** — Uniform density 1/(2π) in θ, the mixing steady
  state of the mean-field PDE; synchronization onset is its loss of
  stability.
- **Generalized eigenvalue** — Singularity of the analytically continued
  resolvent R(λ): X → X' past the continuous spectrum of T; plays the role
  of ordinary eigenvalue inside the rigged Hilbert framework.
- **Landau damping (KM version)** — Decay of the order parameter to zero
  under the linearized dynamics even though the linear operator has
  continuous spectrum on the imaginary axis and no stable eigenvalues.
- **Twisted state** — Phase configuration θ(x) = 2π m x + φ on the circle
  with winding number m, emerging as a bifurcating attractor when the
  dominant Fourier mode of W is e^{±2π i m (x-y)}.

## Connections

**Builds on.**

- The mean field analysis of the Kuramoto model on graphs I (Chiba &
  Medvedev) — Part I derives and justifies the mean-field PDE for the KM on
  graphs and identifies K_c^±; this paper carries out the bifurcation
  analysis at those critical couplings.
- Chiba, A proof of the Kuramoto conjecture (Ergodic Theory Dynam. Syst.
  2015) — Adapts the rigged-Hilbert-space / generalized spectral theory
  Chiba developed for the classical all-to-all KM to the graphon setting.
- Mouhot & Villani, On Landau damping (Acta Math. 2011) — Provides the PDE
  Landau-damping toolkit underlying alternative analyses and conceptual
  framing of decay without spectral gap.

## Recommendations

- **R1** — When diagnosing 'synchronization/consensus onset' in a networked
  dynamical system, compute the top eigenvalue and eigenvector of the
  (weighted) adjacency/graphon operator — these set both the critical
  coupling and the spatial pattern of the bifurcating state.
  *Topic:* spectral network analysis · *Strength:* strong · *When:* System whose
  linearization at a symmetric fixed point couples through a compact
  symmetric operator derived from the network.
- **R2** — In systems where the linearized operator has continuous spectrum
  on the stability boundary, do not rely on eigenvalue gaps to infer
  stability; work in a rigged Hilbert space and analytically continue the
  resolvent to obtain generalized eigenvalues. **[not filed as a practice:
  advice on proof technique rather than on training]**
  *Topic:* spectral methods · *Strength:* moderate · *When:* Linearization
  admits no spectral gap (e.g. transport-like operators multiplying by iω).

## Bearing on the record

The stability half of the graph-Kuramoto analysis. Nothing here cites it. It
is filed because its companion is, and because the consensus results the
gossip line depends on are not legible without it.

## Limitations

- Existence of the center manifold and nonlinear estimates are assumed
  rather than proved; only formal reduction is carried out.
- Analyticity/exponential-class assumption on g(ω) is restrictive; weaker
  regularity (as in Dietert, Fernandez–Gérard-Varet–Giacomin) requires
  different techniques.
