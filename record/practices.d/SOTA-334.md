---
number: 334
status: Proposed
formerly:
- SOTA-tmpb0fn3
promote_when: >-
  An independent group reports, for a style- or condition-modulated
  convolutional generator, demodulation against instance or adaptive
  normalization with the artifact measured, not only shown, and FID over
  more than one run. The source's evidence is one group's visual artifact
  plus a single-run FID that does not move.
title: 'In a style-modulated generator, demodulate the convolution weights instead of instance-normalizing the activations'
version: 1
tags:
- generative-modeling
- model-architecture
date: '2026-09-23'
source:
- LIT-560
introduced_by:
- LIT-560
consensus: unreplicated
consensus_note: >-
  Used by StyleGAN2 and StyleGAN3, both the same group's. The record holds
  no outside comparison.
implementations:
- StyleGAN2
- StyleGAN3
summary: >-
  Karras et al. (2019), [LIT-560](../literature.d/LIT-560.md) — AdaIN's instance normalization
  discards relative feature magnitudes, so the generator smuggles scale
  past it with a localized spike, the "water droplet" in every StyleGAN
  image. Scale each output channel's modulated weights by
  1/√(Σ w'² + ε) instead. It gives the same expected unit variance and style
  mixing still works. The artifact disappears and FID is unchanged (4.40 →
  4.39).
---

# SOTA-334: In a style-modulated generator, demodulate the convolution weights instead of instance-normalizing the activations

## Source

Karras et al. (2019), [LIT-560](../literature.d/LIT-560.md) — StyleGAN2. Read as [NOTE-301](../notes.d/NOTE-301.md).

## The practice

When a per-sample style scales a convolution's input channels
(`w'_ijk = s_i · w_ijk`):

- **Do not normalize the activations per sample and channel.** Instance
  normalization forces every feature map to unit statistics and throws away
  their relative magnitudes, and the generator learns to put a sharp spike
  somewhere to control its statistics
- **Demodulate the weights:** `w''_ijk = w'_ijk / √(Σ_{i,k} w'_ijk² + ε)`.
  Assuming unit-variance independent inputs, this gives unit-variance
  outputs without looking at the data, so the magnitude information
  survives. Implement it with grouped convolutions
- **Move bias and noise outside the style block**, onto normalized data

## What was measured

Droplet artifacts disappear from images and from intermediate activations
(Figure 3). FFHQ FID 4.40 → 4.39, and PPL 212 → 175.

## Conditions

- **The statistics assumption** (i.i.d. unit-variance inputs) is what
  makes it "expected" normalization, and it is not enforced
- **Evidence of the artifact is visual.** The FID does not register it,
  which is also the paper's point about FID
