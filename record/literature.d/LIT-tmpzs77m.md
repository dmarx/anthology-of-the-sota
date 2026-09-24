---
status: Active
title: 'Imagen Video: High Definition Video Generation with Diffusion Models'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- inference-optimization
date: '2026-09-24'
published: '2022-10-01'
arxiv: '2210.02303'
first_author: 'Ho'
keywords:
- 'cascaded-diffusion'
- 'text-to-video'
- 'v-prediction'
- 'progressive-distillation'
- 'video-image-joint-training'
- 'classifier-free-guidance'
implementations: []
extends:
- LIT-627
- LIT-067
summary: >-
  Ho et al., Google (2022), [ARXIV-2210.02303](https://arxiv.org/abs/2210.02303). VDM scaled into a seven-model,
  11.6B cascade producing 128 frames at 1280×768. It is the first report to
  add a separate image-text corpus (60M internal pairs plus LAION-400M) to
  joint training, and it asserts the benefit without an ablation. Its tested
  results are that v-prediction beats ε-prediction for video
  super-resolution, and that distillation to 8 steps is 18× faster at a
  small metric cost.
compared_against:
- LIT-tmpyt5og
---

# LIT-tmpzs77m: Imagen Video: High Definition Video Generation with Diffusion Models

Ho et al., Google Research, Brain Team (2022) — [ARXIV-2210.02303](https://arxiv.org/abs/2210.02303)

## Key takeaways

- **The cascade.** A base model, three spatial and three temporal
  super-resolution models, 11.6B diffusion parameters, and a frozen T5-XXL
  text encoder produce 128 frames at 1280×768 and 24 fps (§2.2).
- **v-prediction for video super-resolution.** On the same spatial
  super-resolution task and steps, v-prediction converges much faster than
  ε-prediction and avoids colour shift across frames (Figs. 12–13, curves
  only). This is independent support for [SOTA-195](../practices.d/SOTA-195.md).
- **Model size matters more than it did for images.** With only the base
  model's size changed (500M, 1.6B, 5.6B), FVD and CLIP score improve (Fig.
  11). The paper notes this runs "contrary" to Imagen's image result.
- **Distillation.** Distilling each stage to 8 steps cuts sampling from 618s
  to 35s. With constant guidance, CLIP score goes from 25.19 to 25.03 and
  R-precision from 92.12 to 89.68 (Table 1).
- **The joint-training corpus.** All seven models train on 14M video-text
  pairs, 60M image-text pairs and LAION-400M, with images packed as
  single-frame videos and temporal layers masked (§§2.6, 3).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The version of joint training everyone now uses is asserted here.**
  "Consistent with Ho et al. (2022b), we observe that joint training with
  images significantly increases the overall quality" (§2.6). There are no
  numbers. VDM ([LIT-627](LIT-627.md)) tested joint training on frames drawn from its own
  videos. This paper adds a separate image corpus, which is the version in
  use now, and shows nothing for it. Style transfer from images to video is
  shown qualitatively (Fig. 8).
- **Nothing external is compared.** No table includes another system.
- **"Without any noticeable loss in perceptual quality"** (§2.7) sits next
  to R-precision falling 2.4 points in Table 1.
- **Neither the model nor the code was released** (§4).

## Standing in the anthology

This is the bridge between VDM and the current line. It is the first
report whose joint training looks like modern practice: a large, separate
image corpus. It gives no evidence for it, which is why [SOTA-386](../practices.d/SOTA-386.md) cites VDM
and not this report. Where the record needs this paper is its two
controlled results: v-prediction for high-resolution video, and guided
distillation of a cascade.

Filed without a `NOTE`: the takeaways come from one full reading done for
this filing, appendices included.
