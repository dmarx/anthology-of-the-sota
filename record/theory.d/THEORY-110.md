---
number: 110
status: Proposed
formerly:
- THEORY-tmpv11wm
promote_when: >-
  A controlled sweep that moves fidelity and coverage by comparable amounts in a
  common unit and shows FID responding more to the coverage arm — ideally on a
  second architecture family and a second dataset, with the feature network held
  fixed. The two instances the record holds are suggestive and neither isolates
  the magnitudes: Kynkäänniemi et al. compare six StyleGAN configurations that
  differ in more than one thing, and ADM's table compares a GAN with a diffusion
  model. A negative result would be as useful: a family where FID's best
  configuration is the high-precision one.
title: 'FID is not neutral between fidelity and coverage: it weights coverage more, so optimizing it walks toward variety at the cost of per-sample quality'
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-25'
source:
- LIT-703
- LIT-699
summary: >-
  Kynkäänniemi et al. (2019), [LIT-703](../literature.d/LIT-703.md), measured on StyleGAN: "FID favors
  configurations with high recall over the ones with high precision", and the
  best-recall configuration set a new state-of-the-art FID. The mechanism they
  give is that FID is a Wasserstein-2 distance in feature space, so low intrinsic
  variation yields low FID even when much of that variation is missed. [LIT-699](../literature.d/LIT-699.md)
  is an independent instance in another family: ADM-G beats BigGAN-deep on FID at
  three resolutions while losing precision at all three and winning recall. So
  FID does not merely *mix* fidelity and coverage — it mixes them with a
  direction, and a model tuned on FID is tuned toward coverage.
---

# THEORY-110: FID is not neutral between fidelity and coverage: it weights coverage more, so optimizing it walks toward variety at the cost of per-sample quality

## Source

Kynkäänniemi, Karras, Laine, Lehtinen and Aila (2019), [LIT-703](../literature.d/LIT-703.md), for the
measurement and the mechanism. Dhariwal and Nichol (2021), [LIT-699](../literature.d/LIT-699.md), for an
instance in an unrelated model family.

## The account

That FID conflates fidelity and coverage is the premise of [SOTA-425](../practices.d/SOTA-425.md) and is not
in dispute — it is a distance between distributions and both aspects move it.
The claim here is stronger and more useful: **the conflation has a direction.**

**The mechanism.** FID is a Wasserstein-2 distance between Gaussians fitted in a
feature space. What that distance can see about missed variation is bounded by
how much variation the reference distribution has. Kynkäänniemi et al. state it
directly: "Since FID corresponds to a Wasserstein-2 distance in the feature
space, low intrinsic variation implies low FID even when much of that variation
is missed." A generator that covers a narrow region of a narrow distribution is
barely penalised. The corollary is that FID's sensitivity to coverage is not a
property of the metric alone but of the metric *and the dataset*, and it is
weakest exactly where coverage is hardest to verify by eye.

**The measurement.** Across six StyleGAN training configurations on FFHQ,
evaluated on their Pareto frontiers, "FID favors configurations with high recall
(A, F) over the ones with high precision (B, C), and the same is also true for
the individual snapshots". The configuration with the best recall — instance
normalization disabled in AdaIN, which the authors found improves recall
"unexpectedly" — produced a new state-of-the-art FID for the dataset. Minibatch
standard deviation and `R₁` regularization both shift the balance toward
precision, and FID rates them worse.

**The independent instance.** [LIT-699](../literature.d/LIT-699.md) reports ImageNet at three resolutions:

| ImageNet | model | FID ↓ | Prec ↑ | Rec ↑ |
| --- | --- | --- | --- | --- |
| 128 | BigGAN-deep | 6.02 | **0.86** | 0.35 |
| 128 | ADM-G | **2.97** | 0.78 | **0.59** |
| 256 | BigGAN-deep | 6.95 | **0.87** | 0.28 |
| 256 | ADM-G | **4.59** | 0.82 | **0.52** |
| 512 | BigGAN-deep | 8.43 | **0.88** | 0.29 |
| 512 | ADM-G | **7.72** | 0.87 | **0.42** |

FID prefers the higher-recall model at every resolution while the
higher-precision model loses. Different architecture family, different dataset,
different group, same direction — and neither paper cites the other for this.

## What follows if it is right

**A field that selects on FID has been selecting for coverage.** Not
deliberately, and not visibly, because the metric reports one number. Every
ablation whose verdict was "FID improved, so keep it" was partly a vote about a
trade nobody stated, and the papers that ship a truncated or guided model for
their *figures* while reporting FID for their *tables* are resolving that
inconsistency by hand, per publication. Kynkäänniemi et al. note exactly this:
state-of-the-art methods "claim to optimize FID" and then produce their
uncurated results with a model that "explicitly sacrifices variation, and often
FID, in favor of higher quality samples".

**It makes [SOTA-425](../practices.d/SOTA-425.md) a correction, not just a caveat.** Reporting precision and
recall beside FID is not extra diligence about a neutral instrument; it is the
only way to see which way a biased one is pulling.

## What this does not say

**Not that FID is wrong, or that the bias is large.** The direction is measured
twice; the magnitude is measured nowhere, which is what the `promote_when` asks
for. A small asymmetry that never reverses a ranking would make this true and
unimportant.

**Not that precision and recall are the neutral alternative.** They have their
own feature network — VGG-16 fc2, per [LIT-703](../literature.d/LIT-703.md), not the Inception-v3 FID
uses — their own `k` parameter, and their own saturation behaviour. [SOTA-337](../practices.d/SOTA-337.md) is
the record's holding on what an ImageNet feature space does to any of these
numbers, and it covers all three metrics.

**Not the same claim as [THEORY-095](THEORY-095.md).** That is about FID's *estimator*: no
unbiased estimator exists, so plug-in bias can reverse a comparison at small
sample counts. This is about what the *quantity* weights, and it would hold for
a perfectly estimated FID.

**Not an account of sFID.** Nash et al.'s spatial variant might weight the two
components differently, and nothing here bears on it. [LIT-699](../literature.d/LIT-699.md) reports sFID
beside FID throughout and the two do not always move together: in its Table 6 at
ImageNet 512×512 the best FID is 3.85 (guidance plus upsampling, 250/250 steps)
while the best sFID is 5.62, on the upsampling-only row. Different rows, so sFID
is not simply FID with a different lens, and it is the obvious next thing to
look at.
