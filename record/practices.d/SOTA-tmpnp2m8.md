---
status: Proposed
title: 'When the training loss has saturated and runs still differ, measure loss-landscape degeneracy rather than curvature'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- model-stability
date: '2026-09-22'
source:
- LIT-tmp6dook
introduced_by:
- LIT-tmp6dook
contested_by: []
explained_by:
- THEORY-tmpzuan6
promote_when: >-
  A group other than the measure's authors reports the lower-LLC/better-
  generalization relation on a workload they were not studying the measure with,
  with the knobs varied jointly rather than one at a time. The relation is
  currently three one-dimensional sweeps on one model and one dataset, and
  `Active` needs it to survive somebody else's confounds.
summary: >-
  Lau, Furman, Wang, Murfet and Wei (2023), [LIT-tmp6dook](../literature.d/LIT-tmp6dook.md) — on ResNet18/CIFAR10,
  stronger implicit regularization (higher learning rate, lower batch size,
  higher momentum) gives a lower local learning coefficient and higher test
  accuracy, **while every training loss has collapsed to zero**. The estimator
  is `λ̂(w*) = n β* [E_{w|w*,β*,γ} L_n(w) − L_n(w*)]` at `β* = 1/log n`, run by
  SGLD, validated against theory on deep linear networks to 100M parameters.
  Where the loss has stopped distinguishing runs, the geometry has not.
---

# SOTA-tmpnp2m8: When the training loss has saturated and runs still differ, measure loss-landscape degeneracy rather than curvature

<!-- inactive-ok-file: THEORY-tmpgrdfw — Proposed, filed in this same contribution as the account of what the measure finds during training; new, not retired. -->

## Source

Lau, Furman, Wang, Murfet and Wei (2023), [LIT-tmp6dook](../literature.d/LIT-tmp6dook.md). Read as
[NOTE-tmp13c7y](../notes.d/NOTE-tmp13c7y.md). Explained by [THEORY-tmpzuan6](../theory.d/THEORY-tmpzuan6.md).

## The practice

Training loss going to zero is where most comparisons between configurations
stop being informative, and it is also where a lot of interesting variation
lives. Two runs at identically zero training loss can differ in test accuracy,
in robustness, and in what they have internally become.

**Measure the volume scaling exponent of the near-optimal set.** The estimator

    λ̂(w*) = n β* [ E_{w|w*,β*,γ} L_n(w) − L_n(w*) ],   β* = 1/log n

is the expected loss under a localized tempered perturbation around `w*`, minus
the loss at `w*`, rescaled. It is computed by SGLD, runs at the scale of real
models, and needs nothing known in advance about what the network computes.

What it reports is **how much room the parameters have to move without changing
the function**. Where the loss is flat because the model has fit the data, this
is not.

## What was measured

ResNet18 on CIFAR10, sweeping learning rate, batch size and momentum
independently: **stronger implicit regularization — higher learning rate, lower
batch size, higher momentum — gives lower `λ̂` and higher test accuracy**. The
authors' own framing: "Even though most training losses collapse to zero, the
LLC can discern the implicit regularization pressure applied by various
training heuristics."

The estimator's credibility rests on a separate experiment: on **deep linear
networks up to 100M parameters** it reproduces Aoyagi (2024)'s theoretical
learning coefficients, and keeps doing so when evaluated at an SGD-found
minimum rather than a minimum of the population loss.

## Not curvature — and this is the part that is not obvious

The nearby practice is `SOTA-012`: sharpness in the loss landscape correlates
with test error, on filter-normalised visualisations. That practice is careful
and its advice survives. But filter normalisation fixes the *rescaling
artefact*; it does not make curvature the right quantity. Per
[THEORY-tmpzuan6](../theory.d/THEORY-tmpzuan6.md), the theorems contain the **exponent** of the volume law, and
curvature is its prefactor — it does not appear in the model-selection
criterion `n L_n(w_0) + λ log n`, nor in the Bayes generalisation rate `λ/n`.

So this is not "compute sharpness more carefully". It is a different number,
with a different theory behind it, that happens to answer the question people
were asking sharpness to answer.

**No `compared_against` is declared with `SOTA-012`, and the reason is
`ADR-011`.** That relation means somebody ran the comparison. Nobody has
run filter-normalised sharpness and the local learning coefficient against
each other as predictors of test error on the same models; the argument
that the exponent is the right quantity is theoretical, from
[LIT-tmp63rr1](../literature.d/LIT-tmp63rr1.md), and this record labels it as one.

## Conditions

**The relation between LLC and generalization is correlational, and the sweeps
are one-dimensional.** The source says so: "we do so in isolation, i.e., we do
not look at interactions between these factors". One architecture, one dataset,
three knobs varied one at a time. That is what `promote_when` asks somebody to
improve on, and it asks for someone else's workload rather than a second paper
agreeing (`DP-005`).

**The estimator carries assumptions the number does not display.** A localizing
radius `γ` suppressed in the notation, an SGLD sampler with its own burn-in and
step size, an inverse temperature `1/log n`, and a Bayesian quantity evaluated
at a point SGD found. The deep-linear result is the evidence that the
composition is faithful in one regime where the truth is known — and theoretical
learning coefficients are unavailable almost everywhere else, which is the
school's own stated bottleneck.

**Lower is not automatically better.** The reported direction is that stronger
implicit regularization lowers `λ̂` and raises accuracy on this workload. It is
not a claim that minimising `λ̂` is an objective, and [LIT-tmpgj3s9](../literature.d/LIT-tmpgj3s9.md) observes
stages where `λ̂` falls during ordinary training for reasons nobody has
explained.

## Where it is worth reaching for

- Comparing training recipes whose training losses have all converged.
- Detecting that *something* changed during a run when the loss curve is
  smooth — [LIT-tmpgj3s9](../literature.d/LIT-tmpgj3s9.md) is that use, and [THEORY-tmpgrdfw](../theory.d/THEORY-tmpgrdfw.md) is what the record
  thinks of it.
- As an alternative to a hand-built progress measure when no mechanistic
  hypothesis is available yet. `SOTA-200` records that `LIT-085`'s measures
  require reverse-engineering the network first; this does not, and returns
  less.
