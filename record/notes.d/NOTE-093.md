---
number: 93
status: Read
formerly:
- NOTE-tmp3kdcw
paper: LIT-365
title: 'Trainability and Accuracy of Neural Networks: An Interacting Particle System Approach'
version: 1
date: '2026-09-15'
summary: >-
  When the width n is large, the n hidden units behave as exchangeable
  particles whose empirical distribution μ_t evolves by gradient descent in
  2-Wasserstein metric on a *convex* energy functional E[μ] — even though the
  finite-n loss in parameter space is non-convex.
---
# NOTE-093: Trainability and Accuracy of Neural Networks: An Interacting Particle System Approach

## Contribution

Reinterprets SGD training of wide two-layer neural networks as an
interacting particle system and establishes a Law of Large Numbers and
Central Limit Theorem for the empirical distribution of parameters. Shows
that training descends gradient-like on a convex functional in 2-Wasserstein
metric, converging at a rate independent of n, and that the approximation
error universally scales as O(1/n). Also quantifies the SGD noise and gives
guidance on scaling step size and batch size with n.

## Key insight

When the width n is large, the n hidden units behave as exchangeable
particles whose empirical distribution μ_t evolves by gradient descent in
2-Wasserstein metric on a *convex* energy functional E[μ] — even though the
finite-n loss in parameter space is non-convex. This reframes training as a
mean-field PDE: the LLN gives global convergence at n-independent timescale
(dynamical universal approximation), and the CLT quantifies O(n^{-1/2})
fluctuations that "self-heal" to O(n^{-1}) at long times, explaining the
universal O(1/n) approximation error.

## Assumptions

- Quadratic loss L[f] = (1/2) E_ν |f - f^(n)|^2 (extensions to convex losses
  noted)
- Input space Ω and feature space D̂ are closed smooth compact Riemannian
  manifolds
- Unit φ̂(x,z) is C^1 in z
- Target function f is representable: f ∈ F_1 (integral representation
  exists)
- Discriminating kernel: ∫ g(x) φ̂(x,·) ν(dx) = 0 a.e. ⇒ g = 0 a.e.
- Initial distribution μ_in has finite exponential moments in c and support
  separating c>c_0 from c<-c_0
- IID draws of θ_i(0) from μ_in (IID satisfied in our setting)
- For SGD: batch points x_p drawn IID from ν at each step

## Key results

- **Proposition 3.5 (LLN / global convergence).** As n→∞, μ_t^(n) ⇀ μ_t
  solving ∂_t μ = ∇·(∇V(θ,[μ])μ), and lim_{t→∞} ∫φ(·,θ)μ_t(dθ) = f
  (dynamical universal approximation)
  *Holds when:* n-independent convergence timescale; requires μ_in
  regularity and discriminating kernel
- **Proposition 3.7 (CLT).** n^{1/2}(f_t^(n) - f_t) → g_t in law, where g_t
  is a zero-mean Gaussian process; fluctuations O(n^{-1/2}) at finite t
  *Holds when:* Finite t, assumes LLN holds
- **Proposition 3.9 (self-healing at long time).** For any ξ < 1, lim_{n→∞}
  n^{2ξ} E ∫ |f_{a_n}^(n)(x) - f(x)|^2 ν(dx) = 0 along suitable time a_n
  *Holds when:* Requires positive-definite kernel M([μ_t],x,x') along the
  trajectory and supp μ̂* = D̂
- **Proposition 4.x (SGD scaling).** With σ = Δt/P = a n^{-2α}, α ∈ (0,1],
  SGD admits LLN toward same μ_t and CLT with fluctuations O(n^{-α})
  *Holds when:* Choose Δt and batch size P such that Δt/P ~ n^{-2α}; α=1/2
  during training, α=1 for final quench

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Infinite-width training of two-layer networks is gradient descent on a convex functional in Wasserstein metric | strong | Propositions 3.2, 3.5 (LLN + Wasserstein gradient flow structure) |
| C2 | Approximation error of trained wide networks scales universally as O(1/n) in any input dimension d | strong | CLT (Prop 3.7) + self-healing (Prop 3.9); empirical verification up to d=25 |
| C3 | SGD noise scales as σ = Δt/P; batch size should be increased (quench to α=1) near end of training to reduce fluctuating error | moderate | Section 4 analysis; empirical 3-spin experiments with batch quench |
| C4 | Non-convexity of the finite-n parameter-space loss is benign at large n because the mean-field dynamics is convex | strong | LLN + convexity of E[μ]; empirical absence of plateaus during training |

## Method

**Mean-field / interacting particle analysis of two-layer NN training.**

Represent f^(n)(x) = (1/n) Σ c_i φ̂(x, z_i) and treat θ_i = (c_i, z_i) as n
exchangeable particles. Write GD/SGD dynamics on quadratic loss as particle
dynamics with interaction kernel K(θ,θ') derived from the loss. Define
empirical measure μ_t^(n) and derive its weak-form evolution (Liouville /
Dean-type equation). Take n→∞ to obtain deterministic PDE (LLN), then
linearize around μ_t to get CLT for fluctuations. For SGD, include
correlated noise term from batch sampling and track its effect via Dean's
equation; scale σ = Δt/P = a n^{-2α} to control fluctuation order.

- Empirical measure μ_t^(n) = (1/n) Σ δ_{θ_i(t)}
- Nonlinear Liouville / McKean-Vlasov PDE: ∂_t μ = ∇·(∇V(θ,[μ])μ)
- Wasserstein gradient flow on convex energy E[μ]
- Linearized fluctuation equation for ω_t = n^{1/2}(μ_t^(n) - μ_t)
- Dean's equation with correlated noise for SGD
- Batch-size quench: α from 1/2 to 1 near end of training

## Concepts

- **Empirical distribution (of parameters)** — μ^(n) = (1/n) Σ_i δ_{θ_i};
  the point cloud of unit parameters viewed as a probability measure on D.
- **Self-healing fluctuations** — The phenomenon that O(n^{-1/2})
  fluctuations of μ_t^(n) around its mean-field limit decay to O(n^{-1}) in
  the long-time limit under GD.
- **Mean-field / McKean-Vlasov limit** — Deterministic PDE ∂_t μ =
  ∇·(∇V(θ,[μ])μ) obtained as n→∞ limit of interacting particle dynamics.
- **Dean's equation** — Stochastic evolution equation for the empirical
  density of interacting Langevin particles; here generalized to correlated
  SGD noise.
- **Convexification at distributional level** — Though L is non-convex in
  {θ_i}, the functional E[μ] is convex (quadratic) in the measure μ when
  loss is quadratic in f.

## Connections

**Builds on.**

- Bach, Breaking the curse of dimensionality with convex neural networks
  (JMLR 2017) — Uses Bach's integral representation F_1 of functions
  representable by infinite-width networks.
- Mei, Montanari, Nguyen — A mean field view of the landscape of two-layer
  NNs (PNAS 2018) — Parallel and complementary mean-field analysis; this
  paper additionally establishes CLT and self-healing scaling, and treats
  low-temperature regime.
- Sirignano, Spiliopoulos — Mean Field Analysis of Neural Networks (LIT-
  tmp7pep0) — Contemporaneous mean-field treatment of two-layer NN training.
- Chizat, Bach — Global convergence of GD for over-parameterized models via
  optimal transport (NeurIPS 2018) — Uses Wasserstein gradient flow
  framework for NN training, same conceptual framework.

**Related.**

- Li, Tai, E — Stochastic modified equations and adaptive SGD algorithms —
  Related SDE-based analysis of SGD noise; cited here for diffusion
  approximations.

## Recommendations

- **R1** — Initialize two-layer networks with IID draws covering the
  parameter space broadly (ensuring c can take both signs with enough
  spread)
  *Topic:* initialization · *Strength:* moderate · *When:* Wide two-layer
  networks; mean-field scaling f = (1/n) Σ c_i φ(·,z_i)
- **R2** — Couple batch size and step size via σ = Δt/P; increase batch size
  (quench) near end of training to reduce fluctuating approximation error
  *Topic:* batch size scheduling · *Strength:* moderate · *When:* Mean-field
  regime; two-layer networks; training to near-zero loss
- **R3** — Expect approximation error of wide two-layer networks to scale as
  O(1/n) in n (not O(1/√n)) after sufficient training
  *Topic:* width scaling · *Strength:* strong · *When:* Target function
  representable in F_1; sufficient training time; kernel M positive-definite
  along trajectory
- **R4** — Use mean-field (1/n) parameterization rather than standard (1/√n)
  when analyzing or targeting feature-learning regime
  *Topic:* parameterization · *Strength:* strong · *When:* Two-layer network
  analysis; when feature learning / non-NTK regime is desired

## Bearing on the record

The interacting-particle route to the same limit, and the width scaling that
comes with it — approximation error `O(1/n)` rather than `O(1/sqrt(n))`.
Four groups reached this limit within about a year; that is a convergence
worth a `THEORY` document, and this record does not have one yet.
