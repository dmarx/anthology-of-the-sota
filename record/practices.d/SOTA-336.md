---
number: 336
status: Proposed
formerly:
- SOTA-tmpld8su
promote_when: >-
  A group other than NVIDIA's StyleGAN authors compares progressive growing
  against a fixed skip/residual topology at 512² or above, in a GAN not
  built on StyleGAN's style modulation, with more than one run per arm. The
  source is one group's single runs on two datasets, with an architecture
  the same paper introduced.
title: 'Train high-resolution GANs at a fixed topology with output skips in the generator and a residual discriminator, not by progressive growing'
version: 1
tags:
- generative-modeling
- model-architecture
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-560
introduced_by:
- LIT-560
consensus: unreplicated
consensus_note: >-
  StyleGAN2 and its successor StyleGAN3 train without growing, but both are
  the same group's. The record holds no outside comparison.
implementations:
- StyleGAN2
- StyleGAN3
summary: >-
  Karras et al. (2019), [LIT-560](../literature.d/LIT-560.md) — progressive growing makes each
  resolution briefly the output, so it learns output-level detail and
  leaves features stuck to pixel positions. A fixed generator that sums
  upsampled RGB outputs from every resolution, with a residual
  discriminator, keeps the coarse-to-fine emphasis without changing
  topology. FFHQ FID 4.34 → 3.31, and the phase artifacts are gone.
---

# SOTA-336: Train high-resolution GANs at a fixed topology with output skips in the generator and a residual discriminator, not by progressive growing

## Source

Karras et al. (2019), [LIT-560](../literature.d/LIT-560.md) — StyleGAN2. Read as [NOTE-301](../notes.d/NOTE-301.md).
Filed for `#163`'s "progressive training".

## The practice

**Do not grow the networks during training.** Progressive growing, adding
resolution blocks as training proceeds, stabilized early high-resolution
GANs. It also leaves details that stay glued to image coordinates as
content moves (teeth that do not turn with the head), because every
intermediate resolution was once trained as the final output.

**Instead, fix the topology from the start:**

- **Generator with output skips:** each resolution block emits an RGB
  image, and the outputs are upsampled bilinearly and summed. Early in
  training the low-resolution outputs dominate, so the coarse-to-fine
  emphasis happens by itself
- **Residual discriminator**, with the downsampled image fed at each
  resolution

| FFHQ FID (no growing) | D original | D input skips | D residual |
|---|--:|--:|--:|
| G original | 4.32 | 4.18 | 3.58 |
| G output skips | 4.33 | 3.77 | **3.31** |
| G residual | 4.35 | 3.96 | 3.79 |

In the main ablation this change takes FFHQ FID from 4.34 to 3.31.

## Conditions

- **StyleGAN's modulated generator.** The grid was run on it
- **Dataset-dependent winner.** On LSUN Car the best pair is residual G
  with residual D (2.66). The skip-G/residual-D choice is FFHQ's
- **Single training runs**, snapshot selected by lowest FID
- **The skips are the replaceable part.** StyleGAN3 ([LIT-559](../literature.d/LIT-559.md)) keeps
  the fixed topology but removes the output skips, on the hypothesis that
  their benefit was mainly gradient-magnitude dynamics, which it handles
  with an EMA normalization instead. What survives both papers is *no
  growing*, not the particular skip wiring
