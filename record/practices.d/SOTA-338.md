---
number: 338
status: Proposed
formerly:
- SOTA-tmptfakt
promote_when: >-
  A comparison at matched training budget in which projected discrimination
  beats a standard discriminator on a Fréchet distance computed in a
  non-ImageNet feature space (CLIP, SwAV or DINOv2) and in a human
  preference study. FID or KID alone cannot settle it, because the
  discriminator's ImageNet pretraining is what distorts them.
title: 'Train the GAN discriminator on frozen multi-scale pretrained features with fixed random channel and scale mixing'
version: 1
tags:
- generative-modeling
- training-optimization
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-562
introduced_by:
- LIT-562
consensus: contested
contested_by:
- LIT-563
consensus_note: >-
  Kynkäänniemi et al. (LIT-563) trained Projected FastGAN with the
  released code on FFHQ. At FID 5.28 against StyleGAN2's 5.30, a CLIP-space
  Fréchet distance was 4.67 against 2.76, and human raters preferred
  StyleGAN2, which they say agrees with this paper's own human study on
  FFHQ. Their reading is that ImageNet pretraining in the discriminator
  leaks ImageNet-like statistics into the samples, which FID then rewards.
implementations:
- Projected GAN
summary: >-
  Sauer et al. (2021), [LIT-562](../literature.d/LIT-562.md) — project real and generated images
  through a frozen EfficientNet, mix channels and scales with fixed random
  convolutions, and train one small discriminator per scale. It reaches
  StyleGAN2's best LSUN-Church FID after 1.1M images instead of 88M. The
  speed-up is measured in FID, and at equal FID on FFHQ a CLIP-space
  distance and human raters prefer StyleGAN2 ([LIT-563](../literature.d/LIT-563.md)).
---

# SOTA-338: Train the GAN discriminator on frozen multi-scale pretrained features with fixed random channel and scale mixing

## Source

Sauer et al. (2021), [LIT-562](../literature.d/LIT-562.md) — Projected GAN. Read as [NOTE-303](../notes.d/NOTE-303.md).
Contested by [LIT-563](../literature.d/LIT-563.md).

## The practice

To make a GAN converge in a fraction of the usual training:

- **Project both real and generated images** through a frozen pretrained
  network and take features at four scales (64² down to 8² in the paper)
- **Mix them with fixed random convolutions:** 1×1 across channels (CCM)
  and 3×3 with upsampling across scales (CSM), Kaiming-initialized and never
  trained. Without mixing, the discriminator uses only part of the deeper
  features
- **One small discriminator per scale**, with spectral normalization and
  logits at a common resolution, summed
- **Prefer a compact feature network.** EfficientNet-Lite1 beat larger
  ResNets and ViTs
- **Keep differentiable augmentation**, reported as required for the best
  results

## What is contested

Every number behind this practice is FID. The discriminator is itself
ImageNet-pretrained, and FID's feature space is so close to ImageNet
classes that matching their statistics lowers FID without improving images
([LIT-563](../literature.d/LIT-563.md)). On FFHQ at equal FID, this model loses to StyleGAN2 in CLIP
space and with human raters. The speed-up in reaching a given FID is real.
Whether it is a speed-up in quality is what is disputed. Evaluate with
[SOTA-337](SOTA-337.md) before relying on it.

## Conditions

- **FastGAN generator**, 256² to 1024²
- **ImageNet-pretrained feature network.** Randomly initialized feature
  networks do much worse (per the appendix, not read)
