---
status: Read
paper: LIT-tmp6dook
title: 'A complexity measure that discriminates where the training loss is identically zero'
version: 1
date: '2026-09-22'
summary: >-
  Read as the instrument that makes the school usable. The LLC is the volume
  scaling exponent of the near-optimal set around one minimum, estimated by
  SGLD at inverse temperature `1/log n`. Validated against known theoretical
  values on deep linear networks to 100M parameters. The result that makes it a
  practice: on ResNet18/CIFAR10 it separates learning rate, batch size and
  momentum settings whose training losses have all collapsed to zero.
---

# NOTE-tmp13c7y: A complexity measure that discriminates where the training loss is identically zero

<!-- inactive-ok-file: SOTA-tmpnp2m8 — Proposed, filed in this same contribution as the practice this reading supports; new, not retired. -->

## Contribution

It takes Watanabe's global learning coefficient — a property of a
(model, truth, prior) triplet, historically computed by hand for a handful of
model classes — and does two things to it. It localizes it to a neighbourhood
of a single minimum, so it becomes a property of a trained network rather than
of a model class. And it gives a scalable estimator, so it becomes something
you run rather than something you derive.

## Key insight

**Ask how fast the good region grows, not how deep the hole is.** Take the
volume of parameters within `ε` of the loss at `w*`. In a regular model that
volume goes like `ε^{d/2}` and the prefactor carries the curvature. In a
singular model the exponent itself is the free variable, and it is the exponent
— not the prefactor — that controls the free energy and the generalisation
error. So a complexity measure should read the exponent. `λ(w*)` is exactly
"the number of extra bits you need to halve an already small error".

## Assumptions

- `w*` is a local minimum of the loss; in practice `ŵ*_n = argmin L_n(w)` found
  by SGD is substituted, which uses the dataset twice. The authors flag this and
  test it.
- The estimator sets **`β* = 1/log n`**, the optimal temperature from Watanabe
  (2013), and depends on a localizing radius `γ` suppressed in the notation.
- The expectation is taken by **SGLD** on minibatches, so every estimate
  inherits that sampler's burn-in, step-size and mixing behaviour.
- The asymptotic expansion justifying the estimator is in sample size `n`.
- The theory is Bayesian; the object being measured is a point found by SGD.

## Key results

- **Definition 1 (the LLC).** There is a unique rational `λ(w*)`, a positive
  integer `m(w*)` and `c > 0` with
  `V(ε) = c ε^{λ(w*)} (−log ε)^{m(w*)−1} + o(ε^{λ(w*)} (−log ε)^{m(w*)−1})`.
  At `m = 1`, `V(ε) ∝ ε^{λ(w*)}`. Rationality follows from Hironaka's
  resolution of singularities.
- **Definition 2 (the estimator).**
  `λ̂(w*) := n β* [E_{w|w*,β*,γ} L_n(w) − L_n(w*)]`, `β* = 1/log n`.
  Its shape is the whole intuition: the expected loss under perturbation near
  `w*`, minus the loss at `w*`. Barely moves ⟹ small `λ̂` ⟹ simple.
- **Accuracy against ground truth.** Deep linear networks **up to 100M
  parameters**, compared against Aoyagi (2024)'s theoretical learning
  coefficients. Accurate at a global minimum of the population loss *and* at an
  SGD-found minimum. DLNs are used because they are the most realistic setting
  where theoretical coefficients exist at all.
- **ResNet18 / CIFAR10.** Varying learning rate, batch size and momentum one at
  a time: stronger implicit regularization → **lower LLC and higher test
  accuracy**. The authors' own emphasis: "Even though most training losses
  collapse to zero, the LLC can discern the implicit regularization pressure
  applied by various training heuristics."
- **Invariance to local diffeomorphism**, proved in an appendix — two
  parameterizations of the same function get the same complexity.

## Limitations

**The ResNet result is correlational and the sweeps are one-at-a-time.** The
paper says so — "we do so in isolation, i.e., we do not look at interactions
between these factors". Lower LLC accompanying higher test accuracy across
three knobs is a pattern, not a demonstration that reducing LLC causes
generalisation.

**The theory is Bayesian and the measurement is at an SGD point.** Several
approximations separate `λ̂` from `λ`: a localizing radius, a finite-`n`
temperature, an SGLD sample in place of an expectation, and a minimum found by
the wrong procedure. The deep-linear validation is the evidence that the
composition is small in at least one realistic regime, and it is one regime.

**`d/2` is an upper bound that DLNs may not stress.** The record's `LIT-476`
observes a `d/2`-consistent slope for its own volume measure and contrasts it
with LLC work where `d/2` is not attained; the two measures differ in what they
hold fixed, and nobody has reconciled them.

## Bearing on the record

**It is the paper `LIT-476` was comparing against**, and filing it turns a
dangling comparison into a relation the record can carry.

**It supplies what `SOTA-200` says is expensive.** That practice records that
`LIT-085`'s progress measures require reverse-engineering the network first,
and calls that "the cost of recovering a continuous measure when no continuous
metric over the *outputs* exists". The LLC is a continuous measure over the
*parameters* that needs no reverse-engineering, and it is the reason
`SOTA-tmpnp2m8` is filed as a practice rather than left as a finding.

## Open questions

- **How sensitive is `λ̂` to `γ` and to SGLD hyperparameters?** The estimator
  depends on a localizing radius the notation suppresses, and on a sampler; the
  paper's appendices discuss this and the record cannot tell from the outside
  how much of a reported change is landscape and how much is sampler.
- **Does the lower-LLC/higher-accuracy relation hold when the knobs interact?**
  Every sweep is one-dimensional.
