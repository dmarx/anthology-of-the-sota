---
status: Read
paper: LIT-tmp63rr1
title: 'The effective parameter count is a volume exponent, and the Hessian is measuring the wrong thing'
version: 1
date: '2026-09-22'
summary: >-
  Read as the trunk under a school the record was already citing. Its single
  most consequential sentence for this record is that the RLCT matters more
  than the curvature of the directions it counts — a published argument that
  the quantity a sharpness visualisation displays is not the quantity that
  governs generalisation, which is what `SOTA-012` rests on.
---

# NOTE-tmpeplml: The effective parameter count is a volume exponent, and the Hessian is measuring the wrong thing

## Contribution

It argues that deep learning has been using the wrong asymptotics. Classical
model selection and most flatness intuitions assume the loss is locally
quadratic at a minimum, which is what makes `d/2` the effective parameter count
and the Hessian the object of interest. Neural networks are singular: that
assumption fails, the set of optimal parameters is a variety rather than a
manifold, and the correct replacement — Watanabe's real log canonical threshold
— is a volume exponent that counts degenerate directions and ignores curvature.

## Key insight

**Count the directions that matter, not the steepness in them.** Near a true
parameter, some directions change the model and some do not. In a regular model
every direction changes it, `λ = d/2`, and the interesting variation is the
curvature. In a singular model the number of *live* directions is itself the
variable, it is generally far below `d`, and it need not even be an even
integer. Once that is the picture, "flat versus sharp" is asking about the
second-order coefficients in the live directions while the count of live
directions is doing the work.

## Assumptions

- **Bayesian and asymptotic.** Every result quoted is a statement about the
  Bayes posterior or predictive distribution as `n → ∞`. Nothing here is about
  SGD.
- **A (model, truth, prior) triplet**, with the truth realisable in the
  experiments; the RLCT is a function of all three, unlike the regular
  effective parameter count.
- Multiplicity `m = 1` is assumed in a small enough neighbourhood for the
  volume-codimension limit to exist.
- The experiments are small: feedforward ReLU and SiLU families, `q(x) =
  N(0, I₃)`, full-batch gradient descent for MAP.

## Key results

- **Singular vs regular.** A model is regular iff `w ↦ p(y|x,w)` is one-to-one
  **and** the Fisher information `I(w)` is positive definite. DNNs are neither.
- **The criterion.** `BIC = n L_n(w_MLE) + (d/2) log n` follows from the
  Laplace approximation and therefore only from regularity. Watanabe (2013):
  the correct criterion for both cases is **`n L_n(w_0) + λ log n`**. Since
  `λ ≪ d/2` is possible, a network can have high marginal likelihood.
- **The RLCT as volume codimension.** `V(t, v_0) = ∫_{K(w)<t} φ(w) dw` behaves
  as `c t^λ + o(t^λ)`; in the minimally singular case where
  `K(w) = Σ_{i=1}^{d′} cᵢ wᵢ²`, the true parameters form a submanifold of
  codimension `d′` and **`λ = d′/2`**. There are `d − d′` directions in which
  the parameter moves without changing the model. *The coefficients `cᵢ` do not
  appear in `λ`.*
- **Generalisation.** `E_n G(n) = λ/n + o(1/n)` for the Bayes predictive
  distribution (Watanabe 2009, Thms 1.2, 7.2); `E_n G(n) = C/n + o(1/n)` for
  MAP and MLE with `C` the maximum of a Gaussian process (Thm 6.4). Regular:
  `λ = C = d/2`. Singular: `C > λ` in general. *Holds when:* the truth is
  realisable and the Bayes predictive distribution is used, which is
  intractable in practice.
- **`2λ` need not be an integer** for strictly singular models, and the paper
  argues it is nonetheless the only geometrically meaningful count.
- **Experiments.** Being Bayesian in only the final layers beats MAP; the
  Laplace approximation performs poorly as well as being theoretically
  inapplicable; RLCT rises as the true distribution becomes complex relative to
  the model.

## Limitations

**It is an invitation and it says so in the abstract.** The theorems are
Watanabe's. What this paper adds is the argument for relevance to deep
learning, small confirming experiments, and a research agenda.

**The central result is about an object nobody can compute.**
`E_n G(n) = λ/n` holds for the Bayes predictive distribution, which is
intractable; the paper notes that variational approximations may not inherit
the relationship, because free energy and generalisation error can have
*different* learning coefficients for approximate posteriors — documented for
one-hidden-layer networks by Nakajima and Watanabe (2007). That is a real gap
and `LIT-tmp6dook` is the attempt to close the estimation half of it.

**Nothing here is about training dynamics.** The whole framework is Bayesian.
`LIT-tmpjlg44` is the paper that takes that seriously rather than eliding it.

## Bearing on the record

**It resolves a citation `LIT-476` could not.** That note compares its own
local-volume power law — log-log slope consistent with `d/2` — against "Local
Learning Coefficient results where `d/2` is a strict upper bound not seen in
practice", and attributes the difference to using KL rather than the training
loss. The `d/2` it is comparing against is this paper's regular-model case, and
`λ ≤ d/2` is the content of the singular one.

**It is why `SOTA-012` moves to v3.** That practice rests on `LIT-014`'s
filter-normalised visualisations and is already careful — correlation, not
causation, and a diagnostic rather than an objective. What it does not say, and
now can, is that there is a published argument that **curvature is not the
load-bearing quantity at all**, independent of whether the visualisation is
normalised correctly. Filter normalisation fixes the artefact of rescaling; it
does not make the Hessian the right object.

## Open questions

- **Does the `λ/n` relationship survive an approximate posterior?** The paper
  raises this and cites a counterexample from 2007. Nothing this record holds
  answers it, and every practical LLC estimate depends on the answer.
- **What is the RLCT of a transformer?** Theoretical values exist for a handful
  of architectures, most from decades ago. `LIT-tmp6dook` estimates rather than
  derives, and the derivation gap is the school's own stated bottleneck.
