---
status: Active
title: 'Analyzing and Improving the Image Quality of StyleGAN'
version: 1
tags:
- generative-modeling
- model-architecture
- vision-and-graphics
date: '2026-09-23'
published: '2019-12-01'
arxiv: '1912.04958'
first_author: 'Karras'
keywords:
- 'stylegan2'
- 'weight-demodulation'
- 'progressive-growing'
- 'path-length-regularization'
- 'lazy-regularization'
implementations:
- StyleGAN2
extends:
- LIT-tmppzrje
summary: >-
  Karras et al. (2019), [ARXIV-1912.04958](https://arxiv.org/abs/1912.04958). StyleGAN2 traces StyleGAN's
  droplet artifacts to instance normalization and replaces it with weight
  demodulation (FID unchanged, artifacts gone). It traces its phase
  artifacts to progressive growing and replaces growing with a fixed
  output-skip generator and residual discriminator (FFHQ FID 4.34 → 3.31).
  It runs R1 only every 16 minibatches at no cost, and adds path-length
  regularization, which trades FID against smoothness on less structured
  data.
extended_by:
- LIT-tmp8n96l
---

<!-- inactive-ok-file: SOTA-tmpld8su SOTA-tmpb0fn3 — both Proposed, filed in this same contribution from this paper -->

# LIT-tmppdats: Analyzing and Improving the Image Quality of StyleGAN

Karras, Laine, Aittala, Hellsten, Lehtinen, Aila, NVIDIA and Aalto (2019) —
[ARXIV-1912.04958](https://arxiv.org/abs/1912.04958)

## Key takeaways

- **Droplets come from AdaIN.** Instance normalization discards feature
  magnitudes, so the generator smuggles scale past it with a localized spike.
  Removing normalization removes the droplets. *Weight demodulation*,
  scaling each output channel's weights by `1/√Σ w'²` after modulation,
  restores the expected unit variance without normalizing the data
- **Phase artifacts come from progressive growing.** Each resolution is
  briefly the output, so it learns maximum-frequency detail, which leaves
  details stuck to pixel positions. A fixed topology with output skips in
  the generator and a residual discriminator keeps the coarse-to-fine
  emphasis without growing
- **Table 1 (FFHQ 1024², FID / PPL):** baseline 4.40 / 212 → demodulation
  4.39 / 175 → lazy R1 4.38 / 158 → path-length reg 4.34 / 123 → no growing,
  new G and D 3.31 / 125 → larger networks 2.84 / 145. On LSUN Car,
  path-length regularization *raises* FID from 2.83 to 3.43
- **Table 2 (architecture grid, no growing):** on FFHQ, output-skip G with
  residual D is 3.31, against 4.32 for the original feedforward pair
- **Lazy regularization:** R1 computed every 16 minibatches, with no harm
- Metrics are averaged over 10 evaluation seeds. Each configuration is one
  training run, selected at its best-FID snapshot

## Standing in the anthology

**Filed from `#163`** (StyleGAN/2/3, "progressive training"). It sources
[SOTA-tmpld8su](../practices.d/SOTA-tmpld8su.md) (no progressive growing) and [SOTA-tmpb0fn3](../practices.d/SOTA-tmpb0fn3.md) (weight
demodulation). It `extends` StyleGAN ([LIT-tmppzrje](LIT-tmppzrje.md)), and StyleGAN3
([LIT-tmp8n96l](LIT-tmp8n96l.md)) extends it.

**FID's blind spot is part of the paper's argument.** It shows images with
equal FID and precision/recall but visibly different quality, and uses PPL
as the metric that tracks them. That is the reason path-length
regularization exists, and also a caution against reading its FID trade-off
on LSUN Car as the whole story.

Read — [NOTE-tmpejv2l](../notes.d/NOTE-tmpejv2l.md).
