---
status: Active
title: 'No unbiased estimator of FID exists, so its plug-in bias can reverse a comparison while the sample variance stays small'
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-tmphun6n
explains:
- SOTA-tmpfcgzq
summary: >-
  Bińkowski et al. (2018), [LIT-tmphun6n](../literature.d/LIT-tmphun6n.md) — the FID is a non-linear
  functional of the two distributions, and by the Bickel–Lehmann argument no
  estimator of it is unbiased for all distributions. The bias is therefore a
  property of the quantity, not of the plug-in formula, and it does not
  appear in the standard error: at d=2048 and 50,000 samples the estimator
  reversed a true ordering in all 100 trials, with standard deviations of
  0.2 and 0.5 on a gap of 2.5. The non-existence proof needs a mixture family;
  what rescues it for practice is that Inception codes are not normal.
---

# THEORY-tmpb0yyu: No unbiased estimator of FID exists, so its plug-in bias can reverse a comparison while the sample variance stays small

## Source

Bińkowski, Sutherland, Arbel and Gretton (2018), [LIT-tmphun6n](../literature.d/LIT-tmphun6n.md), Appendix D.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-tmpfcgzq](../practices.d/SOTA-tmpfcgzq.md) | fix n before comparing, and settle a close call with an unbiased estimator instead of a tighter error bar | the error bar is measuring the wrong thing — it reports the spread of a statistic that is not centred on the quantity, and the offset shrinks with n while the spread shrinks faster |

## The account

The FID between two distributions is

    FID(P,Q) = ‖μ_P − μ_Q‖² + tr(Σ_P) + tr(Σ_Q) − 2·tr((Σ_P Σ_Q)^{1/2})

and the usual estimator plugs in the sample mean and sample covariance.
Those plug-ins are each unbiased; the functional they are fed to is not
linear, so the composition is not.

**That much is ordinary, and it would be fixable.** What makes this a claim
about the measure rather than about one formula is Appendix D.3, by the
Bickel & Lehmann (1969) argument the same paper uses for squared MMD. Fix a
target `Q` and two distributions `P₀ ≠ P₁`, and look at the mixture family
`(1−α)P₀ + αP₁`. If an estimator on `n` samples were unbiased across that
family, expanding the product of `n` mixture measures makes

    R(α) = FID((1−α)P₀ + αP₁, Q)

**a polynomial in `α` of degree at most `n`**. Take all three to be
one-dimensional normals: `μ_α` is linear in `α` and `σ²_α` quadratic, so every
term of `R(α)` is polynomial except the cross term `−2σσ_α` — and `σ_α`,
the square root of a genuine quadratic, is polynomial only when `P₀ = P₁`.
So `R` is not a polynomial and no such estimator exists.

**The limit on that result, which the paper states and which is easy to
overstate:** the argument needs the mixture, so it rules out unbiasedness on
*any class containing two-component Gaussian mixtures* and, in their words,
"can tell us nothing about whether there exists an estimator which is
unbiased on normal distributions". Their own bridge back to practice is that
Inception codes are clearly not normal — the same ReLU observation that
undermines FID's Gaussian fit in the first place — so **a practical
unbiased estimator is impossible**, which is the claim this document makes.
A reader who assumes the Gaussian fit is exact is not covered by the proof,
and is already assuming the thing `LIT-tmphun6n` measures to be false.

**The consequence that matters is not imprecision but confident inversion.**
Bias moves every estimate in the same direction, but not by the same amount,
because how much depends on the distribution being estimated. Two models
whose true FIDs differ by less than the difference in their biases come out
in the wrong order — and they come out that way *consistently*, so repeating
the measurement does not reveal it. The standard error describes the spread
around the estimator's own mean, which is not the quantity of interest, so a
small standard error is evidence that the wrong number has been pinned down
precisely.

The measured instance: at `d = 2048`, on ReLU-censored normals chosen to
resemble Inception codes, `FID(P₁,Q) ≈ 1123.0 > 1114.8 ≈ FID(P₂,Q)` while at
50,000 samples the estimates were `1133.7 (sd 0.2)` and `1136.2 (sd 0.5)` —
reversed, in all 100 trials, with the largest `P₁` estimate below the
smallest `P₂` estimate. At 100,000 samples the order came out right every
time. The bias is consistent, so it dies with `n`; it just had not died at
the sample size the field uses.

## What follows, and what does not

- **It follows that FID values from different `n` are not comparable at all**,
  which is stronger than the usual advice to hold the evaluation protocol
  fixed. On CIFAR-10 train-vs-test, where the true distance is 0, the
  estimate is still about 8.1 at n=10,000 and still falling.
- **It does not follow that FID is uninformative.** Consistency still holds,
  so a large enough gap at a large enough `n` is real. The claim is about
  where the reported uncertainty comes from, not about whether the measure
  tracks anything.
- **It does not subsume the seed-variance floor.** [SOTA-307](../practices.d/SOTA-307.md) is about the
  spread across training seeds at fixed `n`; this is about the offset at
  fixed seed. They are different terms and they add.
- **It says nothing about which features to compute the distance in.** That
  is [LIT-563](../literature.d/LIT-563.md)'s question and a separate one — a distance in CLIP or DINOv2
  features computed by the same plug-in recipe inherits this bias too.
