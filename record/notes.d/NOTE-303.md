---
number: 303
status: Read
formerly:
- NOTE-tmp4h72t
paper: LIT-562
title: 'Projected GAN'
version: 1
date: '2026-09-23'
summary: >-
  A GAN discriminator on frozen, randomly mixed, multi-scale pretrained
  features reaches prior-best FIDs up to 40× faster and sets new FIDs on 22
  datasets. Everything is measured in FID or ImageNet-derived metrics, and
  the discriminator is ImageNet-pretrained, which [LIT-563](../literature.d/LIT-563.md) later shows
  distorts FID. Read §1–5; the appendix was not read.
---

<!-- inactive-ok-file: SOTA-338 — Proposed and contested, filed in this same contribution from this paper -->

# NOTE-303: Projected GAN

## Contribution

A discriminator design that puts pretrained representations into
unconditional GAN training without letting the discriminator win the game
outright. Its components are multi-scale discriminators, fixed random
feature mixing and a compact feature network.

## Key insight

**Strong features alone make the discriminator too strong, and random
mixing makes it use them all.** A naive perceptual discriminator dominates
and starves the generator of gradient. Spreading prominent features across
channels and scales with fixed random convolutions stops it latching onto
a subset.

## Assumptions

- **FastGAN generator** for most results, with differentiable augmentation
  (reported as required for state-of-the-art results)
- **EfficientNet-Lite1 pretrained on ImageNet** as the feature network
- **FID** as the primary metric, best snapshot per method, all models
  trained to 10M images unless stated

## Key results

- **Table 2 (feature network, LSUN-Church):** EfficientNet-Lite1 FID 1.65,
  R50 4.40, R50-CLIP 3.80, ViT 12.38. Random (untrained) feature networks
  converge much worse (appendix)
- **Table 3:** large-dataset FIDs 0.89 (CLEVR), 3.39 (FFHQ), 3.41
  (Cityscapes), 1.52 (Bedroom), 1.59 (Church), against StyleGAN2-ADA's
  10.17 / 7.32 / 8.35 / 11.53 / 5.85
- **Figure 4:** Projected FastGAN passes StyleGAN2's best Church FID after
  1.1M images against 88M
- **§5.2:** the paper attributes the gains mainly to diversity (recall)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Projected discrimination reaches a given FID far faster | strong, as a statement about FID | Figure 4, Table 3 |
| C2 | It improves image quality | contested | FID-based; [LIT-563](../literature.d/LIT-563.md) finds human raters and CLIP-FD disagree on FFHQ |
| C3 | ImageNet features are not required | weak | R50-CLIP slightly beats R50, while the best results use an ImageNet EfficientNet |
| C4 | Random mixing improves use of deep features | moderate | Table 1 ablation of per-layer Fréchet distances |

## Connections

It generalizes perceptual discriminators from image translation, where its
related work cites an adversarial loss on frozen VGG features that improves
CycleGAN ([LIT-564](../literature.d/LIT-564.md)), to unconditional synthesis. Its evaluation is
examined by Kynkäänniemi et al. ([LIT-563](../literature.d/LIT-563.md)).

## Recommendations

- **R1** — Discriminate on frozen pretrained multi-scale features with
  random mixing, for speed. Filed as [SOTA-338](../practices.d/SOTA-338.md), `contested`
- **R2** — Evaluate such a model in a non-ImageNet feature space. Filed
  from [LIT-563](../literature.d/LIT-563.md) as [SOTA-337](../practices.d/SOTA-337.md)

## Limitations

- **Evaluation leans on ImageNet features** on both sides
- **Appendix metrics** (KID, SwAV-FID, P&R) not read

## Open questions

- How much of the speed-up survives in a feature space unrelated to
  ImageNet
