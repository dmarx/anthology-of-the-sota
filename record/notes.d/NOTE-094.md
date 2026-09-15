---
number: 94
status: Read
formerly:
- NOTE-tmp4hp6m
paper: LIT-328
title: 'Spectrum Dependent Learning Curves in Kernel Regression and Wide Neural Networks'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  For kernel/NTK regression with eigenvalue decay λ_k ∝ k^{-β}: ε(n) ∝ n^{-α},
  where α = β / (1 + β) The exponent α is determined entirely by the data
  spectrum β, not by architecture beyond the NTK.
---
# NOTE-094: Spectrum Dependent Learning Curves in Kernel Regression and Wide Neural Networks

## Contribution

Derives exact learning curves for kernel regression and NTK-equivalent wide
neural networks as a function of the eigenvalue spectrum of the data
covariance (or kernel matrix). Shows that when the eigenvalue spectrum
decays as a power law λ_k ∝ k^{-β}, the generalization error follows ε(n) ∝
n^{-β/(1+β)} exactly in the large-n limit. Two-layer ReLU networks in the
NTK regime have polynomial eigenvalue decay, giving power-law learning
curves — not exponential. This is the theoretical justification for why
empirical neural network learning curves follow power laws.

## Key insight

For kernel/NTK regression with eigenvalue decay λ_k ∝ k^{-β}: ε(n) ∝ n^{-α},
where α = β / (1 + β)

The exponent α is determined entirely by the data spectrum β, not by
architecture beyond the NTK. Key consequences: - β → ∞ (exponential decay):
α → 1 (fastest possible power law) - β = 1 (flat spectrum): α = 1/2 - β < 1
(slow decay): α < 1/2 (slow learning)

For two-layer ReLU NTK, β ≈ (d+1)/d for d-dimensional inputs, giving α ≈
(d+1)/(2d+1) (slightly above 1/2 for large d).

The additive decomposition: ε(n) = bias²(n) + variance(n) where each term
decays as a power law with the same exponent α. There is no irreducible
floor unless the target function lies outside the RKHS (unrealizable case),
in which case ε → ε_∞ > 0.

## Assumptions

- Kernel regression (or NTK-equivalent wide neural network)
- IID data drawn from a distribution with known eigenspectrum
- Ridge regression with optimal or tuned regularization
- Asymptotic regime n → ∞ (large sample count)
- Gaussian process / RKHS framework for the target function

## Key results

- **Power-law learning curve from power-law spectrum.** If the kernel
  eigenvalues satisfy λ_k ∝ k^{-β} and the target function has bounded RKHS
  norm, then: ε_gen(n) = C · n^{-β/(1+β)} + O(n^{-(β+ε)/(1+β)}) The exponent
  α = β/(1+β) ∈ (0, 1) is a strictly increasing function of β. The constant
  C depends on the RKHS norm of the target and the noise level.
  *Holds when:* β = eigenvalue decay exponent; α = β/(1+β)
- **Two-layer ReLU NTK has power-law spectrum.** The NTK of a two-layer ReLU
  network on S^{d-1} has eigenvalues λ_k ∝ k^{-(d+1)/d}. This gives α =
  (d+1)/(2d+1). For d=1: α = 2/3. For d → ∞: α → 1/2. Power law spectra →
  power law learning curves (not exponential).
  *Holds when:* d = input dimension; ReLU activation
- **Bias-variance decomposition in power-law regime.** Generalization error
  decomposes as: ε(n) = bias²(n) + variance(n) bias²(n) ∝ n^{-α} variance(n)
  ∝ n^{-α} (same exponent, different constant) Both terms decay at the same
  rate, so their ratio is asymptotically constant. The learning curve
  exponent is the same for both noise-free and noisy targets.
  *Holds when:* Optimal ridge regularization parameter
- **Unrealizable case: irreducible floor.** If the target function has
  components outside the RKHS (unrealizable), ε(n) → ε_∞ > 0 as n → ∞. The
  floor ε_∞ is the squared projection of the target onto the complement of
  the RKHS. In the realizable case ε_∞ = 0.
  *Holds when:* General RKHS setting

## Concepts

- **Eigenvalue decay exponent β** — Controls how quickly kernel eigenvalues
  decay: λ_k ∝ k^{-β}. Large β = fast decay = smooth function class. Small β
  = slow decay = rough function class.
- **Learning curve exponent α** — α = β/(1+β): the rate at which
  generalization error decays with sample count n. Set by data spectrum β,
  not architecture (in NTK regime).
- **NTK (Neural Tangent Kernel)** — The kernel that a wide neural network
  converges to at initialization. Learning dynamics are equivalent to kernel
  regression with this kernel. Holds exactly in the infinite-width limit.
- **RKHS (Reproducing Kernel Hilbert Space)** — The function space induced
  by the kernel. Functions in the RKHS can be learned; components outside it
  contribute irreducible floor error (unrealizable case).
- **Bias-variance tradeoff at optimal regularization** — At optimal ridge
  parameter, bias² ∝ n^{-α} and variance ∝ n^{-α} with matching exponents.
  The total error is 2× either term asymptotically.

## Connections

**Builds on.**

- Kernel regression / Gaussian process learning curve literature (Sollich,
  Williams, etc.) — Extends classical kernel learning curve results to
  explicit eigenspectrum dependence and to the NTK of wide neural networks.

**Related.**

- Kaplan et al. 2020 ([LIT-028](../literature.d/LIT-028.md)) — Kaplan empirically fits power-law + floor.
  Bordelon et al. provide the theoretical mechanism: data eigenspectrum β
  determines the exponent α = β/(1+β). Together they justify the power-law
  curve family.
- Caballero et al. 2023 ([LIT-324](../literature.d/LIT-324.md)) — BNSL handles the case where two
  distinct β regimes appear in the same learning curve (kink). Bordelon et
  al. give the single-regime theory underlying each piece.
- Saad & Solla 1995 — Saad-Solla gives exponential learning curves (via
  R(t)) in the two-layer teacher-student model. Bordelon et al. shows NTK
  gives power-law curves instead. The two curve families apply to different
  regimes: feature learning (Saad-Solla) vs kernel/lazy (Bordelon).

## Recommendations

- **R1** — When fitting our teacher-student MSE curves, check whether the
  late-training regime follows a power law in steps (Bordelon/Kaplan) or an
  exponential (Saad-Solla). If the network has converged into a lazy/kernel
  regime, expect α = β/(1+β) where β is set by the teacher's weight
  spectrum. This gives a spectral diagnostic: estimate β from the teacher's
  covariance eigenvalues, predict α, and check against the empirical curve.
  **[not filed as a practice: specific to the project these readings were
  made for]**
  *Topic:* curve fitting / regime identification · *Strength:* moderate ·
  *When:* Wide networks or networks in NTK/lazy regime; large-n asymptotics
- **R2** — In gossip training, each node sees an effective distribution that
  is a mixture of its own data and its neighbors'. This mixture changes the
  effective spectrum β, which changes α. Gossip averaging may soften extreme
  eigenvalues, reducing β and hence reducing α (slower learning). Measuring
  α empirically under different gossip periods T is a spectral probe of the
  gossip mixing effect. **[not filed as a practice: specific to the project
  these readings were made for]**
  *Topic:* gossip penalty characterization · *Strength:* moderate · *When:*
  NTK/kernel regime; requires fitting power-law curves to per-node MSE

## Bearing on the record

Learning-curve exponents follow from the kernel-target spectrum. This is the
closest the batch comes to explaining *why* scaling laws are power laws
rather than fitting that they are, and the record holds several practices
fitted to scaling laws and no account of them.

## Limitations

- NTK regime only (infinite width, lazy training); feature learning (Saad-
  Solla regime) requires different analysis.
- Asymptotic (n → ∞); finite-sample corrections may be large.
- Requires knowledge of kernel eigenspectrum; hard to measure for real
  datasets.
- Does not cover training dynamics explicitly — only generalization vs n,
  not vs steps t.
- Minibatch SGD introduces additional noise; exact results are for full-
  batch ridge regression.

## Open questions

- Does gossip averaging change the effective eigenvalue decay exponent β
  seen by each node?
- Is there a transition from S-curve (feature learning) to power law
  (kernel) regime in our experiments?
- Can we compute β analytically for the teacher-student setup under gossip?
