---
status: Read
paper: LIT-tmpcxaow
title: 'SDXL'
version: 1
date: '2026-09-23'
summary: >-
  A larger latent diffusion UNet with two text encoders, micro-conditioning
  on original size and crop, multi-aspect training and a refiner. Size
  conditioning is ablated on ImageNet: most of the gain is from keeping the
  data, and conditioning adds about 3 FID. Read §1–2.5 and Appendix B; the
  rest was skimmed.
---

# NOTE-tmpwcj43: SDXL

## Contribution

A technical report on the next Stable Diffusion, whose reusable parts are
two data-side conditioning tricks that let a model use all of a
heterogeneous dataset without learning its artifacts.

## Key insight

**Tell the model about the preprocessing instead of hiding it.** Upsampling
small images and random cropping both leak into outputs (blur, cut-off
heads). Conditioning on the original size and the crop offsets lets the
model learn those factors separately, and inference sets them to the values
you want.

## Key results

- **Table 2:** FID-5k 43.84 (discard) → 39.76 (keep, unconditioned) → 36.53
  (keep, size-conditioned)
- **Figure 1:** users prefer SDXL, and SDXL with the refiner, over SD 1.5
  and 2.1

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Conditioning on original size beats discarding or ignoring small images | moderate | one class-conditional ImageNet experiment, FID-5k, single runs |
| C2 | Crop conditioning removes cut-off objects | weak | qualitative |
| C3 | SDXL beats SD 1.5 and 2.1 | moderate | user study by the model's developers |

## Limitations

- **Appendix B:** complex spatial prompts, hands and concept bleeding
- **The only quantitative ablation is on ImageNet**, not the text-to-image
  model
