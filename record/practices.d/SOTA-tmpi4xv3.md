---
status: Proposed
promote_when: >-
  A group outside the StyleGAN authors reports equivariance (an EQ-T or
  EQ-R style measurement) and quality for an alias-free generator against
  a standard one, in a video or animation setting where the difference is
  what matters. The source measures equivariance on single images under
  synthetic transforms.
title: 'When generated content must move continuously, as in video or animation, build the generator alias-free: treat features as continuous signals and low-pass filter around every nonlinearity'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- model-architecture
date: '2026-09-23'
source:
- LIT-tmp8n96l
introduced_by:
- LIT-tmp8n96l
consensus: unreplicated
consensus_note: >-
  One group's paper. The record holds no outside measurement of the
  equivariance it buys.
implementations:
- StyleGAN3
summary: >-
  Karras et al. (2021), [LIT-tmp8n96l](../literature.d/LIT-tmp8n96l.md) — fine detail in GAN output sticks to
  pixel coordinates because the generator aliases. Apply each nonlinearity
  at 2× temporary resolution and low-pass filter back, start from Fourier
  features rather than a learned constant, remove per-pixel noise, and
  handle boundaries properly. On FFHQ-U, translation equivariance goes to
  63 dB (and rotation to 40 dB for the -R variant) at StyleGAN2's FID.
---

# SOTA-tmpi4xv3: When generated content must move continuously, as in video or animation, build the generator alias-free: treat features as continuous signals and low-pass filter around every nonlinearity

## Source

Karras et al. (2021), [LIT-tmp8n96l](../literature.d/LIT-tmp8n96l.md) — StyleGAN3. Read as [NOTE-tmp508h6](../notes.d/NOTE-tmp508h6.md).
Filed for `#163`'s "equivariant representation".

## The practice

If the generated image will be **transformed or animated** (latent
walks, video, anything where detail should move with the surface it
belongs to), design the generator so that absolute pixel position cannot
leak into it:

- **Filter around nonlinearities:** upsample 2×, apply the pointwise
  nonlinearity, low-pass filter, downsample. Use radially symmetric filters
  for rotation equivariance
- **Treat each layer's cutoff as the budget for new detail** at that layer
- **Start from a Fourier-feature input** ([LIT-550](../literature.d/LIT-550.md)), not a learned constant,
  and drop per-pixel noise inputs, which are tied to pixel positions

| FFHQ-U 256² | FID | EQ-T (dB) | EQ-R (dB) |
|---|--:|--:|--:|
| StyleGAN2 | 5.14 | – | – |
| StyleGAN3-T | 4.62 | 63.0 | 13.1 |
| StyleGAN3-R | 4.50 | 66.7 | 40.5 |

## Conditions

- **For still images, this buys nothing measurable in FID.** The case for
  it is motion
- **It costs compute.** Larger filters and upsampling factors raise
  equivariance at up to 2.3× the time
- **Equivariance is measured on synthetic transforms** of generated
  images, not on real video
