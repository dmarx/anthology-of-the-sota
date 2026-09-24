---
status: Proposed
promote_when: >-
  A second group fine-tunes an image autoencoder's decoder, or an image
  upsampler, on video and compares it against the frame-wise original in
  the same latent video model, reporting generation quality and not only
  reconstruction. A comparison against a natively trained 3D video
  autoencoder at matched compute would also settle whether the practice is
  still the right starting point.
consensus: unreplicated
consensus_note: >-
  One controlled source, Video LDM (LIT-621), measured on three datasets.
  The current line mostly
  replaces the image autoencoder with a causal 3D video autoencoder trained
  for video (CogVideoX LIT-622, HunyuanVideo LIT-620, Wan LIT-619), so the
  practice matters when reusing an image model's components. Read as of
  2026-09.
title: 'When a latent video model reuses an image autoencoder or upsampler, fine-tune them on video so they see time'
version: 1
tags:
- representation-and-encoding
- generative-modeling
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-621
introduced_by:
- LIT-621
implementations:
- 'Video LDM'
summary: >-
  Blattmann et al. (2023), [LIT-621](../literature.d/LIT-621.md). An image autoencoder decodes each frame
  independently and flickers. Fine-tuning its decoder on video, with a video
  discriminator, cuts reconstruction FVD on three datasets: 390.88 to 32.94,
  35.82 to 18.66, and 73.78 to 25.55. Making the upsampler temporal cuts FVD
  from 165.98 to 45.39. Reconstruction FID worsens on one dataset and
  improves on two.
---

# SOTA-tmpi9445: When a latent video model reuses an image autoencoder or upsampler, fine-tune them on video so they see time

## Source

Blattmann et al. (2023), [LIT-621](../literature.d/LIT-621.md) — Video LDM, Tables 3 and 11.

## The claim

Building a video model on an image latent diffusion model makes the
generator temporal, but leaves everything after it frame-wise. The image
autoencoder decodes each latent frame on its own, and an image upsampler
upsamples each frame on its own. Both introduce flicker that the temporal
generator cannot remove. **Fine-tune the decoder on video, and make the
upsampler temporal.**

Video LDM measures both, with the rest of the pipeline held fixed.

**The decoder**, fine-tuned on video with a video discriminator. Reconstruction
FVD, before → after:

| Dataset | Before | After |
|---|---|---|
| Driving | 390.88 | 32.94 (Table 3) |
| WebVid | 35.82 | 18.66 (Table 11) |
| Mountain biking | 73.78 | 25.55 (Table 11) |

Per-frame reconstruction FID gets worse on driving (7.61 → 9.17) and better
on WebVid (13.89 → 11.68) and mountain biking (20.76 → 18.65). Adding an
image discriminator back raises driving FVD from 32.94 to 51.01. The
discriminator should see video.

**The upsampler.** A video-fine-tuned upsampler reaches FVD 45.39 against
165.98 for frame-wise upsampling, with FID unchanged (19.85 against 19.71,
Table 3).

## Conditions

- **Most of the evidence is reconstruction.** The decoder numbers measure how
  well real video survives the autoencoder, not how good generated video
  looks. The upsampler comparison is in the generation pipeline.
- **The encoder stays frame-wise.** Only the decoder is fine-tuned, so the
  latent space the generator was trained on does not move.
- **The current line designs this away.** CogVideoX, HunyuanVideo and Wan
  train causal 3D autoencoders for video from the start, and CogVideoX's
  ablation ([LIT-622](../literature.d/LIT-622.md), Table 1) favours that over a 2D autoencoder on flicker.
  This practice is for the case where you are reusing image components, as
  Video LDM did.
- **One group, three datasets.** The consistency across datasets is the
  practice's strength. That all three come from one paper is its weakness.
