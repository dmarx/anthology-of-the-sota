---
number: 423
status: Proposed
formerly:
- SOTA-tmpzrrgi
consensus: unreplicated
consensus_note: >-
  One paper, with a qualitative sweep on three prompts. The setting is exposed
  as a pipeline argument (`guidance_rescale`) and widely used on stock models,
  where its source never tested it. That is adoption. Read as of 2026-09.
promote_when: >-
  A comparison of guidance rescale against plain classifier-free guidance at
  matched *effective* guidance, for example a quality-against-alignment curve
  over the guidance scale for each, that shows a gain on the frontier and
  not just at a lower-guidance point. Its exposure as a library option would
  not count.
title: "When classifier-free guidance over-exposes a latent diffusion model, rescale the guided prediction toward the conditional prediction's standard deviation"
version: 1
tags:
- generative-modeling
- inference-optimization
date: '2026-09-25'
source:
- LIT-689
introduced_by:
- LIT-689
implementations:
- 'diffusers (guidance_rescale)'
summary: >-
  Lin et al. (WACV 2024), [LIT-689](../literature.d/LIT-689.md). Compute `x_cfg` as usual, rescale it by
  `std(x_pos)/std(x_cfg)`, and blend with weight `φ` back toward `x_cfg`. The
  source uses `φ ≈ 0.7` at `w = 7.5`. It is the latent-space counterpart of
  Imagen's dynamic thresholding, which needs a known pixel range. The
  evidence is qualitative, and part of the effect may simply be lower
  effective guidance.
---

<!-- inactive-ok-file: SOTA-422 — Proposed; named as the change that motivates this one -->

# SOTA-423: When classifier-free guidance over-exposes a latent diffusion model, rescale the guided prediction toward the conditional prediction's standard deviation

## Source

Lin, Liu, Li and Yang (2023; WACV 2024), [LIT-689](../literature.d/LIT-689.md), §3.4 and §5.3.

## What to do

```
x_cfg      = x_neg + w · (x_pos − x_neg)
x_rescaled = x_cfg · std(x_pos) / std(x_cfg)
x_final    = φ · x_rescaled + (1 − φ) · x_cfg
```

The source uses `w = 7.5`, `φ = 0.7`. Its sweep found `φ` between 0.5 and 0.75
"produces the most appealing results". At `φ = 1` images are "overly plain".

## Why

A large guidance weight inflates the prediction's scale, and the result
over-exposes. [SOTA-202](SOTA-202.md) handles this for pixel-space models by clamping
to the training range. A latent has no known range, so this rescales to the
conditional prediction's own spread instead. "Inspired by" Imagen,
"applicable to both image-space and latent-space models".

## Conditions

- **Never compared with [SOTA-202](SOTA-202.md).** The source cites dynamic thresholding
  as its inspiration and does not run it, so no `compared_against` is
  declared.

- **The evidence is qualitative.** Five values of `φ` on three prompts. Its one
  numeric result (COCO FID) bundles it with three other fixes.
- **It is partly a guidance-strength change.** Pulling toward the conditional
  std lowers effective guidance, and FID usually improves as guidance drops.
  Nothing in the source separates the two.
- **Motivated by zero terminal SNR, not shown to need it.** The source says
  guidance "becomes very sensitive" as terminal SNR approaches zero. It never
  shows over-exposure, or the fix, on a model without it
  ([SOTA-422](SOTA-422.md)).

## Known implementations

- diffusers `guidance_rescale`.
