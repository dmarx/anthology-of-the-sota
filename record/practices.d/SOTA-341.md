---
number: 341
status: Proposed
formerly:
- SOTA-tmpalcy0
promote_when: >-
  An ablation by another group on a text-to-image model, not
  class-conditional ImageNet alone, comparing size conditioning against
  discarding small images and against training on them unconditioned, at
  equal compute, with more than one run per arm. The source is one
  FID-5k run per arm on ImageNet.
title: 'Condition an image generator on each training image''s original size instead of discarding or upsampling small images'
version: 1
tags:
- generative-modeling
- data-pipeline
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-566
introduced_by:
- LIT-566
consensus: unassessed
consensus_note: >-
  SDXL ships it. Whether later image models kept micro-conditioning has not
  been assessed here.
implementations:
- SDXL
summary: >-
  Podell et al. (2023), [LIT-566](../literature.d/LIT-566.md) — embed each training image's original
  height and width, like the timestep, and give it to the model. Then keep
  the small images that a minimum-resolution filter would drop (39% of
  SDXL's pretraining data below 256²) without teaching the model their
  blur. At inference, set the size you want. On class-conditional ImageNet
  512²: FID-5k 43.84 discarding, 39.76 keeping unconditioned, 36.53 keeping
  with size conditioning.
---

# SOTA-341: Condition an image generator on each training image's original size instead of discarding or upsampling small images

## Source

Podell et al. (2023), [LIT-566](../literature.d/LIT-566.md) — SDXL. Read as [NOTE-306](../notes.d/NOTE-306.md).

## The practice

When the training set mixes resolutions and the model trains at a fixed
size:

- **Do not filter out images below the training resolution.** Doing so
  threw away 39% of SDXL's pretraining data at 256², and in the ImageNet
  ablation discarding cost more than anything else (FID-5k 43.84 against
  39.76 for simply keeping them)
- **Do not just upsample them either.** The model learns the upsampling
  blur as part of the distribution
- **Condition on `(h_original, w_original)`**, Fourier-embedded ([LIT-550](../literature.d/LIT-550.md))
  and added to the timestep embedding, and set it to the target size at
  inference (36.53). The same idea extends to random-crop offsets, set to
  zero at inference to avoid cut-off subjects, though that part is shown
  only qualitatively

## Conditions

- **Most of the measured gain is from keeping the data** (43.84 → 39.76).
  The conditioning adds 3.2 FID-5k on top
- **One run per arm, FID-5k, class-conditional ImageNet**, not the
  text-to-image model the practice is used in
