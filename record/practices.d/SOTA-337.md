---
number: 337
status: Active
formerly:
- SOTA-tmprzpgu
title: 'When ImageNet-pretrained networks take part in training a generator, confirm FID gains with a Fréchet distance in a non-ImageNet feature space'
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-23'
source:
- LIT-563
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
  whenever that is the case.
---

# SOTA-337: When ImageNet-pretrained networks take part in training a generator, confirm FID gains with a Fréchet distance in a non-ImageNet feature space

## Source

Kynkäänniemi et al. (2022), [LIT-563](../literature.d/LIT-563.md). Read as [NOTE-304](../notes.d/NOTE-304.md).

## The practice

**If an ImageNet-pretrained network touches the generator's training**,
FID and KID are no longer trustworthy for comparing it with methods that do
not use one. The demonstrated case is a pretrained discriminator. The
authors suspect the same of classifiers used to curate the data or placed in
the sampling loop.

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
