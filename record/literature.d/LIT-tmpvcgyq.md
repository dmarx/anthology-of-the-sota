---
status: Active
title: 'Video Diffusion Models'
version: 1
tags:
- generative-modeling
- vision-and-graphics
date: '2026-09-24'
published: '2022-04-01'
arxiv: '2204.03458'
first_author: 'Ho'
keywords:
- 'video-diffusion'
- '3d-unet'
- 'factorized-space-time-attention'
- 'joint-image-video-training'
- 'reconstruction-guidance'
- 'classifier-free-guidance'
implementations: []
extends:
- LIT-036
summary: >-
  Ho, Salimans et al., Google (2022), [ARXIV-2204.03458](https://arxiv.org/abs/2204.03458). The first diffusion
  model for video: a U-Net factorized into space and time and trained jointly
  on videos and still frames. Adding eight still frames per video cuts FVD
  from 202 to 58 in a controlled ablation. The abstract's explanation, lower
  gradient variance, is never measured.
compared_against:
- LIT-tmpmi3yo
---

# LIT-tmpvcgyq: Video Diffusion Models

Ho, Salimans et al., Google (2022) — [ARXIV-2204.03458](https://arxiv.org/abs/2204.03458)

## Key takeaways

- **The architecture moves image diffusion into time with little change.**
  The 2D U-Net becomes 3D by using 1×3×3 convolutions and adding a
  temporal-attention block with relative position embeddings after every
  spatial-attention block (§3, Fig. 1). This factorization is adopted, not
  ablated.
- **Joint image-video training is the result that lasted.** Independent frames
  are appended to each video and temporal attention is masked off for them.
  On 16×64×64 text-to-video with the small model, FVD falls from 202.28 with
  no extra frames to 68.11 with four and 57.84 with eight (Table 4). This is a
  controlled comparison with one seed at one scale. Every later report in
  this line trains on images and video together, Wan ([LIT-tmpbr2sl](LIT-tmpbr2sl.md)) included.
- **Reconstruction guidance beats replacement** for extending a video
  autoregressively from an unconditional model. At 64 frames, FVD is 136
  against 451 at w=2 (Table 6), with the model and guidance weight held
  fixed.
- **Per-frame and video metrics disagree about guidance.** As the
  classifier-free guidance weight rises, IS keeps improving while FID-type
  metrics improve and then degrade (Table 5).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The mechanism is not measured.** The abstract says joint training
  reduces "the variance of minibatch gradients". §4.3.1 argues this, but no
  gradient variance or training curve is shown, only final metrics.
- **The guidance claim runs against the paper's own table.** The conclusion
  claims the benefits of classifier-free guidance "on both video and image
  sample quality metrics". At frameskip 1, FVD gets worse with guidance: 41.65
  at w=1, 50.19 at w=2, 163.74 at w=5 (Table 5).
- **The images come from the videos.** The "image" half of joint training is
  frames drawn from the same video dataset, and a separate image corpus is
  left to future work. Later reports use one, and this paper does not test
  that.
- **Not released.** "We have decided not to release our models" (§6).

## Standing in the anthology

This is the root of the video generation line. It is filed as the earliest
controlled evidence that video diffusion models should see still images as
well as video. The text-to-video results use an unnamed 10M-video dataset
and have no external baseline, so its benchmark results are not what the
record keeps it for.

Filed without a `NOTE`: the takeaways come from one full reading done for
this filing, including the appendix.
