---
number: 337
status: Active
formerly:
- SOTA-tmprzpgu
title: 'When an ImageNet classifier is anywhere in the pipeline — training the generator or steering its sampling — confirm FID gains with a Fréchet distance in a non-ImageNet feature space'
version: 3
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Widens the title to the scope the source already had. Kynkäänniemi et al.
    suspected classifiers "placed in the sampling loop" as well as pretrained
    discriminators, and the body said so from v1, but the title said "take part
    in training a generator" — which excludes the most widely deployed
    sampling-loop classifier there is. Adds LIT-699 as the case: classifier
    guidance maximises an ImageNet classifier's confidence during sampling, and
    that paper asserts it produces no adversarial examples without measuring it.
    Recommendation, status and consensus unchanged.
- version: 3
  date: '2026-09-25'
  note: >-
    v2's new Conditions bullet said precision and recall are "computed in the
    same ImageNet feature space" as FID. Wrong in the detail: LIT-tmptzz06 uses
    VGG-16 fc2 and FID uses Inception-v3. The conclusion the bullet drew survives
    and is arguably stronger — two *different* ImageNet classifiers that agree
    with each other is the situation this practice is about — but the stated
    reason was false.
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-23'
source:
- LIT-563
- LIT-699
introduced_by:
- LIT-563
consensus: unreplicated
consensus_note: >-
  One group's paper, but the central experiment involves no competitor: it
  holds a generator fixed and shows FID falling by two-thirds under
  resampling while non-ImageNet distances barely move. Whether the field
  has adopted non-ImageNet Fréchet distances as a routine check has not been
  assessed here.
implementations: []
summary: >-
  Kynkäänniemi et al. (2022), [LIT-563](../literature.d/LIT-563.md) — FID's features are nearly
  ImageNet class logits, so matching ImageNet-class statistics lowers it
  without improving images. Resampling a fixed StyleGAN2's outputs cuts
  FFHQ FID 5.30 → 1.78, while CLIP-space FD moves 2.76 → 2.64. A model whose
  discriminator uses ImageNet features exploited this by accident, and the
  authors suspect data filters and samplers can too. Report a CLIP or SwAV Fréchet distance beside FID
  whenever that is the case. Classifier guidance (LIT-699) is the
  sampling-loop instance and the least checked: it maximises an ImageNet
  classifier's confidence on every step, and its paper denies producing
  adversarial examples in one clause without running a test.
---

# SOTA-337: When an ImageNet classifier is anywhere in the pipeline — training the generator or steering its sampling — confirm FID gains with a Fréchet distance in a non-ImageNet feature space

## Source

Kynkäänniemi et al. (2022), [LIT-563](../literature.d/LIT-563.md). Read as [NOTE-304](../notes.d/NOTE-304.md).

## The practice

**If an ImageNet classifier touches the pipeline at all**, FID and KID are no
longer trustworthy for comparing the result with methods that do not use one.
The demonstrated case is a pretrained discriminator during training. The
authors suspect the same of classifiers used to curate the data or placed in
the sampling loop — and provenance is not what matters. A classifier trained
from scratch on ImageNet labels has the same feature space as one downloaded;
the hazard is the overlap with FID's features, not where the weights came from.

- **Report a Fréchet distance in a feature space not trained on ImageNet
  classification**, such as CLIP. SwAV is partly independent: self-supervised,
  but on ImageNet images
- **Treat a large FID gain that the other space does not show as
  suspect**, and look at samples, or better, run a human comparison
- **Do not take FID's ranking across very different training setups at
  face value.** Within one setup (sweeps, checkpoints, catching failed runs)
  the authors find it dependable

## What was measured

With the generator fixed and only the selection of its samples changed:

| FFHQ | FID | ResNet-50 FD | SwAV FD | CLIP FD |
|---|--:|--:|--:|--:|
| random samples | 5.30 | 6.11 | 1.42 | 2.76 |
| resampled to match fringe features | 1.78 | 3.85 | 1.24 | 2.64 |

The drop tracks how much ImageNet each feature space has seen. In the
practical case, Projected FastGAN matched StyleGAN2's FID (5.28 against
5.30) with CLIP-FD 4.67 against 2.76, and human raters preferred StyleGAN2.

## Conditions

- **CLIP is a partial check.** It has its own training data and biases
- **Complements [SOTA-307](SOTA-307.md)**, which is about FID's variance across seeds. This
  practice is about its bias
- **Says nothing about which side of a fidelity/diversity trade you are on.**
  That is [SOTA-425](SOTA-425.md), and precision and recall are subject to this practice too —
  not because they share FID's feature space, which they do not (VGG-16 fc2
  against Inception-v3, [LIT-tmptzz06](../literature.d/LIT-tmptzz06.md)), but because they are a *second* ImageNet
  classifier, and their own paper reports that Inception features give
  "substantially similar" results. Two ImageNet classifiers agreeing is not a
  cross-check

## The sampling-loop case

Classifier guidance (Dhariwal and Nichol 2021, [LIT-699](../literature.d/LIT-699.md)) is this practice's
sharpest instance and the reason v2 widened the title. The method takes gradient
steps that raise an ImageNet classifier's log-probability of the target class,
during sampling, on every step. FID and Inception Score are computed by passing
the results through an ImageNet classifier. This is not a classifier that
*happens* to share a feature space with the metric; it is a procedure whose
objective is the thing the metric measures.

The paper addresses it in one clause of its introduction — the scale can be
raised "by an order of magnitude without obtaining adversarial examples" — and
the word "adversarial" appears nowhere else in it. No test, no held-out
classifier, no non-Inception distance. Its memorization check (App. C) is run in
InceptionV3 feature space, which is the same problem again.

So for guided sampling this practice is unmet, not satisfied: **nobody has run
the CLIP or SwAV Fréchet distance on guided against unguided samples at matched
<!-- inactive-ok: THEORY-109 — Proposed, cited as the open question this practice's instrument would close rather than as a settled account; a promote_when naming this practice is what makes the pairing correct. -->
FID.** [THEORY-109](../theory.d/THEORY-109.md) is the open question, and this practice already names the
instrument that would close it
