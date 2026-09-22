---
status: Active
title: "Deep Learning is Singular, and That's Good"
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-22'
published: '2020-10-22'
arxiv: '2010.11560'
first_author: 'Murfet'
keywords:
- 'singular learning theory'
- 'real log canonical threshold'
- 'effective parameters'
- 'flat minima'
- 'Bayesian generalisation'
implementations: []
summary: >-
  Murfet, Wei, Gong, Li, Gell-Redman and Quella (2020), [ARXIV-2010.11560](https://arxiv.org/abs/2010.11560) — the
  invitation, and the trunk under a school the record has been citing without
  holding. Neural networks are *singular* statistical models: the set of
  optimal parameters is a real analytic variety with singularities, so the
  Laplace approximation and anything that divides by the determinant of the
  Hessian do not apply. The correct effective parameter count is the real log
  canonical threshold `λ`, which counts **how many** directions change the
  model, not how sharply the loss rises in them. Read as [NOTE-tmpeplml](../notes.d/NOTE-tmpeplml.md).
---

# LIT-tmp63rr1: Deep Learning is Singular, and That's Good

Murfet, Wei, Gong, Li, Gell-Redman and Quella (2020) — [ARXIV-2010.11560](https://arxiv.org/abs/2010.11560).
Read as [NOTE-tmpeplml](../notes.d/NOTE-tmpeplml.md).

## Key takeaways

- **The distinction the whole school rests on.** A model is *regular* if the
  map `w ↦ p(y|x,w)` is one-to-one **and** the Fisher information matrix is
  positive definite; otherwise it is *strictly singular*. Neural networks have
  been known to be singular since Amari et al. (2003) and Watanabe (2007): the
  set of weights equivalent to the truth under KL divergence is a real analytic
  variety that fails to be a manifold.
- **BIC is derived from an approximation that does not hold here.**
  `BIC = n L_n(w_MLE) + (d/2) log n` comes from the Laplace approximation,
  which applies to regular models. Watanabe (2013)'s correct criterion, for
  regular and singular models alike, is `n L_n(w_0) + λ log n` with `λ` the
  RLCT — and since `λ` may be far below `d/2`, a network can have high marginal
  likelihood, which BIC says it cannot.
- **`λ` is a volume codimension, not a curvature.** For the volume of almost-true
  parameters `V(t, v_0) = ∫_{K(w)<t} φ(w) dw`, one has `V(t, v_0) = c t^λ +
  o(t^λ)`. In the minimally singular case `K(w) = Σᵢ cᵢ wᵢ²` over `d′ < d`
  coordinates, `λ = d′/2`: there are `d − d′` directions in which the parameter
  can move without changing the model at all. **The constants `cᵢ` — the
  curvature — do not enter.** For strictly singular models `2λ` need not even be
  an integer.
- **The generalisation result.** `E_n G(n) = λ/n + o(1/n)` when `q̂_n` is the
  Bayes predictive distribution (Watanabe 2009, Thm 1.2 and 7.2), against
  `E_n G(n) = C/n + o(1/n)` for MAP or MLE, where `C` is the maximum of a
  Gaussian process. Regular models have `λ = C = d/2`; singular models
  generally have `C > λ`, so the Bayes predictive distribution should be
  preferred. Experimentally, being Bayesian in *just the final layers* beats
  MAP, and the Laplace approximation performs poorly as well as being
  inappropriate.
- **`λ` depends on the truth, not only the model.** In regular models the
  effective parameter count is a function of the (model, prior) pair; the RLCT
  is a function of the (model, truth, prior) triplet, and rises as the true
  distribution grows complex relative to the model. Verified on ReLU and SiLU
  families.

## Standing in the anthology

**`Active`, and it closes a citation the record could not resolve.**
[LIT-476](LIT-476.md) compares its own local-volume power law against "Local Learning
Coefficient results where `d/2` is a strict upper bound not seen in practice",
and [NOTE-225](../notes.d/NOTE-225.md) names the LLC as "the singular-learning-theory neighbour". The
record was citing this school's findings while holding none of its papers.

**It is a position paper and says so** — "an invitation to singular learning
theory ... and suggest important future work to make singular learning theory
directly applicable to how deep learning is performed in practice". The
theorems it relies on are Watanabe's and are not proved here; what is new is
the argument for relevance plus small confirming experiments.

**Its bearing on [SOTA-012](../practices.d/SOTA-012.md) is direct and is why that practice moves to v3.**
The sentence "we will explain why this matters more than the curvature of
those directions (as measured for example by eigenvalues of the Hessian)
laying bare some of the confusion over 'flat' minima" is a published argument
that the quantity a sharpness visualisation displays is not the quantity that
governs generalisation.
