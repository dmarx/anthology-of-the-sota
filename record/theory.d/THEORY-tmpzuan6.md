---
status: Active
title: 'Neural networks are singular, so effective complexity is how the volume of near-optimal parameters scales, not how curved the optimum is'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-22'
source:
- LIT-tmp63rr1
- LIT-tmp6dook
explains:
- SOTA-tmpnp2m8
summary: >-
  Watanabe's singular learning theory, as this record receives it from
  [LIT-tmp63rr1](../literature.d/LIT-tmp63rr1.md) and [LIT-tmp6dook](../literature.d/LIT-tmp6dook.md). The set of parameters realising a given
  function is a variety with singularities, not a point, so the loss is not
  locally quadratic and `d/2` is not the effective parameter count. What is, is
  the exponent `λ` in `V(ε) ∝ ε^λ` — the rate at which the volume of
  near-optimal parameters shrinks. It fixes the model-selection criterion
  (`n L_n(w_0) + λ log n`, not BIC), the Bayes generalisation error
  (`λ/n`), and the sense in which one trained network is simpler than another.
  Curvature is the prefactor, and the prefactor is not what governs any of them.
extended_by:
- THEORY-tmpgrdfw
- THEORY-tmpzq41c
---

# THEORY-tmpzuan6: Neural networks are singular, so effective complexity is how the volume of near-optimal parameters scales, not how curved the optimum is

<!-- inactive-ok-file: THEORY-tmpzq41c — Proposed, filed in this same contribution as the caution that extends this account; new, not retired. -->

## The account

Classical statistics assumes a *regular* model: the parameter-to-function map
is one-to-one and the Fisher information is positive definite. Then the loss is
locally quadratic at an optimum, the Laplace approximation applies, and the
number of parameters is the complexity.

Neural networks satisfy neither condition. Permutations, rescalings, dead units
and rank deficiencies mean that many parameters give the same function, so the
set of optima is a **real analytic variety with singularities**. The quadratic
picture fails, and with it everything derived from it.

The replacement is a scaling exponent. Take the volume of parameters within
`ε` of the optimal loss near `w*`. Watanabe's theorem says

    V(ε) = c ε^λ (−log ε)^{m−1} + o(…)

and `λ` — the real log canonical threshold, or locally the **local learning
coefficient** — is the quantity that does the work:

- **Model selection.** `BIC = n L_n(w_MLE) + (d/2) log n` comes from the
  Laplace approximation and therefore only from regularity. The correct
  criterion for both regular and singular models is **`n L_n(w_0) + λ log n`**.
- **Generalisation.** `E_n G(n) = λ/n + o(1/n)` for the Bayes predictive
  distribution, against `C/n` for MAP and MLE. Regular models have
  `λ = C = d/2`; singular models generally have `C > λ`.
- **Counting.** In the minimally singular case `λ = d′/2` where `d′` is the
  number of directions that change the function — so `d − d′` directions are
  free. For strictly singular models `2λ` need not be an integer.
- **Information.** `λ` is the number of extra bits needed to halve an already
  small error.

**And the curvature is the constant `c`.** In the regular case `V(ε) ≈ c ε^{d/2}`
and the second derivatives live entirely in `c`. They do not enter `λ`, they do
not enter the criterion, and they do not enter the generalisation rate.

## Why `Active`

**The mathematics is Watanabe's and is not in dispute.** What was in dispute is
whether it reaches practice, and [LIT-tmp6dook](../literature.d/LIT-tmp6dook.md) answers the measurement half:
an SGLD estimator, `λ̂(w*) = n β* [E_{w|w*,β*,γ} L_n(w) − L_n(w*)]` at
`β* = 1/log n`, reproduces known theoretical learning coefficients on deep
linear networks **up to 100M parameters**, including when evaluated at an
SGD-found minimum. It is also proved invariant to local diffeomorphism, which
is the minimum any complexity measure should satisfy and which several do not.

Two `Proposed` accounts in this record are downstream of it and their status
does not propagate up: what is `Active` here is that the exponent is the right
quantity, not any particular claim about what it does during training.

## What it corrects, and what it does not

**It corrects the flatness intuition at its foundation, not at its edges.**
The record's `SOTA-012` reports that sharpness correlates with test error,
carefully — correlation, not causation, and only with filter normalisation,
which is what stopped earlier sharpness claims being rescaling artefacts. This
account says something stronger and orthogonal: filter normalisation fixes the
*artefact*, and curvature would still be the wrong object if it were measured
perfectly, because the exponent and not the prefactor is what the theorems
contain. `SOTA-012` moves to v3 with that stated as a condition rather than a
refutation, because the correlation it reports is real and the practice's own
advice — treat a visibly sharp basin as worth suspecting — survives.

**It says nothing about training.** Every result above concerns the Bayesian
posterior, asymptotically in sample size. Reading it as a claim about what SGD
does is the error `THEORY-tmpzq41c` exists to prevent.

## What would change this

A demonstration that the estimated exponent and the theoretical one come apart
in a realistic setting — the deep-linear validation is the only place both are
available, and it is a setting chosen because it is tractable. Or a
demonstration that the free energy and the generalisation error carry
*different* learning coefficients under the approximate posteriors anyone can
actually compute, which [LIT-tmp63rr1](../literature.d/LIT-tmp63rr1.md) raises as a live concern, citing a
one-hidden-layer counterexample from 2007.
