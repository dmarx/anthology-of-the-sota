---
status: Active
title: 'Fix the sample count before comparing FID values, and settle a close comparison with an unbiased estimator rather than a tighter error bar'
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-tmphun6n
introduced_by:
- LIT-tmphun6n
consensus: unreplicated
consensus_note: >-
  One group, and nobody has agreed or disagreed since — the record holds two
  later papers on FID's failure modes and neither mentions estimator bias or
  sample count. Half the claim is a proof rather than a measurement, so
  replication is the wrong test for it; the other half, the 50,000-sample
  reversal, is a construction by the same group and nobody has reproduced it
  or built the equivalent from real generators. What is unambiguously
  measured, and cheap for anyone to repeat, is the CIFAR-10 train-vs-test
  curve: an estimate of a true zero still reading about 8.1 at n=10,000.
extends:
- SOTA-307
implementations: []
explained_by:
- THEORY-tmpb0yyu
summary: >-
  Bińkowski et al. (2018), [LIT-tmphun6n](../literature.d/LIT-tmphun6n.md) — the FID estimator is biased,
  the bias depends on the distribution being measured, and no unbiased
  estimator exists. So two FID numbers are comparable only at equal `n`, and
  a small standard deviation is not evidence of a converged estimate: at
  d=2048 and 50,000 samples their construction reversed a true ordering in
  100 trials out of 100, with standard deviations of 0.2 and 0.5.
---

# SOTA-tmpfcgzq: Fix the sample count before comparing FID values, and settle a close comparison with an unbiased estimator rather than a tighter error bar

## Source

Bińkowski, Sutherland, Arbel and Gretton (2018), [LIT-tmphun6n](../literature.d/LIT-tmphun6n.md). The account
of why is [THEORY-tmpb0yyu](../theory.d/THEORY-tmpb0yyu.md).

## When this applies

You are comparing two generative models, or one model against a baseline
number from a paper, using a Fréchet distance in some feature space — the
Inception FID and its CLIP, SwAV and DINOv2 relatives alike, since all of
them use the same plug-in recipe.

## Do this

**1. State the sample count, and match it.** FID estimates computed at
different `n` are not comparable, and the difference is not a rounding
concern: estimating the distance between the CIFAR-10 train and test sets,
where the true value is 0, the estimate is still about **8.1 at n=10,000** —
the whole CIFAR test set — and still falling. A number copied from a paper
that used a different `n` is not a baseline.

**2. Do not read a small standard deviation as a converged estimate.** The
bias is systematic, so repeating the measurement does not expose it; the
error bar reports the spread of the wrong quantity. In the paper's
construction the reported standard deviations were 0.2 and 0.5 on a gap of
2.5, and the ordering was still wrong in every one of 100 trials.

**3. When the gap is small, settle it with an unbiased estimator.** KID —
the squared MMD in the same Inception features, under the cubic kernel
`k(x,y) = ((1/d)xᵀy + 1)³` — has a simple unbiased estimator and is
asymptotically normal, so a confidence interval on it means what it looks
like. Compute it as a small-`n` estimate averaged over several draws; the
MMD estimator is O(n²d) where FID's is O(nd² + d³), which at d=2048 makes
KID the cheaper of the two.

**4. Or raise `n` until the ordering stops moving.** The estimator is
consistent, so the bias does go away. In their d=2048 example it had gone by
100,000 samples. This is the option that requires no new tooling and it is a
real one — it just has to be checked rather than assumed.

## Why this and not more error bars

Because they answer different questions, and the record already recommends
the other one. [SOTA-307](SOTA-307.md) says to report FID as an error bar over several
training seeds and treat a gap below about 2% of the mean as inconclusive.
That is the right response to seed noise, measured by [LIT-501](../literature.d/LIT-501.md) at ≈1.3%.
It does not respond to this at all: seed variance is spread around the
estimator's own mean at fixed `n`, and the bias is an offset of that mean
which every seed shares.

The two terms add, and only one of them shrinks when you average runs.

## Limitations

- **Half the argument is one group's construction.** The distributions in
  Appendix D.2 are ReLU-censored normals chosen to resemble Inception codes,
  not two real generators. Nobody has produced the equivalent reversal
  between models anyone has trained, and it would be worth having.
- **The non-existence result needs a mixture family.** It rules out an
  estimator unbiased on any class containing two-component Gaussian
  mixtures, and says nothing about a class of exactly normal distributions.
  The bridge to practice is that Inception codes are visibly not normal —
  about 2% of components are exactly zero — which is the same observation
  that undermines FID's Gaussian fit.
- **KID is not a free upgrade in what it measures.** It answers the
  estimator problem and inherits the feature-space problem untouched: a
  KID in Inception features carries [LIT-563](../literature.d/LIT-563.md)'s ImageNet-class dependence
  exactly as FID does, which is why
  [SOTA-338](SOTA-338.md) says FID **or KID** alone cannot settle its question.
