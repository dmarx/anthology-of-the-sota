---
status: Active
title: 'Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks'
version: 1
tags:
- generative-modeling
- vision-and-graphics
date: '2026-09-23'
published: '2017-03-01'
arxiv: '1703.10593'
first_author: 'Zhu'
keywords:
- 'cyclegan'
- 'unpaired-translation'
- 'cycle-consistency'
- 'image-to-image'
implementations:
- CycleGAN
summary: >-
  Zhu, Park, Isola, Efros (2017), [ARXIV-1703.10593](https://arxiv.org/abs/1703.10593). Learn G: X → Y and
  F: Y → X from unpaired collections, with adversarial losses in each domain
  and a cycle-consistency loss that makes F(G(x)) ≈ x and G(F(y)) ≈ y. The
  cycle term turns an under-constrained mapping into a usable one for colour
  and texture changes (horse → zebra, photo ↔ painting, summer ↔ winter).
  The authors report that it fails on geometric changes. Its own ablation
  has a one-directional cycle beating the full model on labels → photo.
---

<!-- inactive-ok-file: SOTA-tmpw7xk8 — Proposed, filed in this same contribution from this paper -->

# LIT-tmpm6lfm: Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks

Zhu, Park, Isola, Efros, UC Berkeley (2017) — [ARXIV-1703.10593](https://arxiv.org/abs/1703.10593)

## Key takeaways

- **Two generators and two discriminators.** The loss is
  `L_GAN(G, D_Y) + L_GAN(F, D_X) + λ·(‖F(G(x)) − x‖₁ + ‖G(F(y)) − y‖₁)`
- **Why the cycle:** with an adversarial loss alone, any mapping onto the
  target distribution is optimal, including one that ignores the input. The
  cycle term requires the translation to keep enough of the input to invert
  it
- **Ablation (Cityscapes, FCN scores):**
  - labels → photo (Table 4): cycle alone 0.22 / 0.07 / 0.02, GAN alone
    0.51 / 0.11 / 0.08, **GAN + forward cycle 0.55 / 0.18 / 0.12**, full
    CycleGAN 0.52 / 0.17 / 0.11
  - photo → labels (Table 5): GAN alone 0.53 / 0.11 / 0.07, GAN + backward
    cycle 0.01 / 0.06 / 0.01, **full 0.58 / 0.22 / 0.16**
- **Human study (AMT, maps ↔ aerial):** it fools raters on about a quarter
  of trials, where the unpaired baselines almost never do
- **The limits, stated by the authors:** colour and texture translation
  usually works. Geometric change (dog → cat) degenerates into minimal
  edits. Paired pix2pix remains better where pairs exist

## Standing in the anthology

**Filed from `#163`** (CycleGAN). Sources [SOTA-tmpw7xk8](../practices.d/SOTA-tmpw7xk8.md), scoped to
appearance changes.

**The sentence to be careful with** is "both terms are critical". The paper
supports it for the full loss against either term *alone*. Its own
labels → photo table has a one-directional cycle beating the bidirectional
one, and the authors' argument for keeping both directions is the
instability and mode collapse they observed qualitatively in the dropped
direction ([DP-010](../../docs/design-principles.md#dp-10)).

Read — [NOTE-tmp36vxd](../notes.d/NOTE-tmp36vxd.md).
