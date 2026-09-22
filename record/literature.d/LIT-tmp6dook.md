---
status: Active
title: 'The Local Learning Coefficient: A Singularity-Aware Complexity Measure'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-22'
published: '2023-08-23'
arxiv: '2308.12108'
first_author: 'Lau'
keywords:
- 'local learning coefficient'
- 'singular learning theory'
- 'model complexity'
- 'SGLD'
- 'implicit regularization'
implementations: []
summary: >-
  Lau, Furman, Wang, Murfet and Wei (2023), [ARXIV-2308.12108](https://arxiv.org/abs/2308.12108) — the instrument.
  It localizes Watanabe's learning coefficient to a single minimum, defines it
  as the exponent in `V(ε) = c ε^λ (−log ε)^{m−1} + …`, and gives an
  SGLD-based estimator `λ̂(w*) = n β* [E_{w|w*,β*,γ} L_n(w) − L_n(w*)]` with
  `β* = 1/log n`. Validated against known theoretical values on deep linear
  networks **up to 100M parameters**. On ResNet18/CIFAR10 it separates training
  configurations whose training losses have all collapsed to zero. Read as
  [NOTE-tmp13c7y](../notes.d/NOTE-tmp13c7y.md).
---

# LIT-tmp6dook: The Local Learning Coefficient: A Singularity-Aware Complexity Measure

Lau, Furman, Wang, Murfet and Wei (2023) — [ARXIV-2308.12108](https://arxiv.org/abs/2308.12108). Read as
[NOTE-tmp13c7y](../notes.d/NOTE-tmp13c7y.md).

## Key takeaways

- **Definition 1.** There is a unique rational `λ(w*)`, a positive integer
  multiplicity `m(w*)` and `c > 0` with
  `V(ε) = c ε^{λ(w*)} (−log ε)^{m(w*)−1} + o(…)` as `ε → 0`; when `m = 1`,
  `V(ε) ∝ ε^{λ(w*)}`. So `λ(w*)` is the **volume scaling exponent** of the set
  of near-optimal parameters around `w*`: raise the error tolerance by `a` and
  the volume grows by `a^λ`. Its rationality follows from Hironaka's resolution
  of singularities.
- **The information reading.** `λ(w*)` is the number of additional bits needed
  to halve an already small error: `−log₂[V(ε/2)/V(ε)] ≈ λ(w*)`.
- **What it replaces.** In the regular case `V(ε) ≈ c ε^{d/2}`, which is why
  `d/2` is the classical complexity — and the curvature constant `c` is, in the
  paper's words, "less significant than the scaling exponent".
- **The estimator.** `λ̂(w*) := n β* [E_{w|w*,β*,γ} L_n(w) − L_n(w*)]` with
  `β* = 1/log n`, the expectation taken over a localized tempered posterior and
  computed by SGLD. If the loss barely moves under perturbation near `w*`, the
  estimate is small.
- **Validated against ground truth.** On deep linear networks up to **100M
  parameters**, the estimates track Aoyagi (2024)'s theoretical learning
  coefficients — and keep doing so when evaluated at an SGD-found minimum
  rather than at a minimum of the population loss, which was the authors'
  stated worry about using the data twice.
- **The result that makes it a practice.** ResNet18 on CIFAR10, sweeping
  learning rate, batch size and momentum one at a time: stronger implicit
  regularization (higher LR, lower batch size, higher momentum) gives **lower**
  LLC and **higher** test accuracy. "Even though most training losses collapse
  to zero, the LLC can discern the implicit regularization pressure."
- **Invariance.** Proved invariant to local diffeomorphism, so it is not
  confounded by a reparameterization of the same function.

## Standing in the anthology

**`Active`. This is the paper [LIT-476](LIT-476.md) was comparing itself against**, and the
one that makes the school's central quantity something a practitioner can
compute rather than a theorem about an object nobody can reach.

**The gap between theory and instrument is real and the record states it.**
The theorems concern the Bayesian posterior and are asymptotic in `n`; what is
computed is an SGLD sample at `β* = 1/log n` with a localizing `γ`. The paper
is careful about the engineering steps between the two, and the deep-linear
validation is the strongest evidence that the gap is small — in the one
realistic setting where the true value is known.
