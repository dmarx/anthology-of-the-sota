---
status: Active
title: 'Lyra: Generative 3D Scene Reconstruction via Video Diffusion Model Self-Distillation'
version: 1
tags:
- vision-and-graphics
- generative-modeling
- data-pipeline
- model-architecture
date: '2026-10-01'
published: '2025-09-23'
arxiv: '2509.19296'
first_author: 'Bahmani'
keywords:
- '3d-gaussian-splatting'
- 'video-diffusion'
- 'self-distillation'
- 'camera-controlled-video-generation'
- 'feed-forward-3d-reconstruction'
- '4d-generation'
- 'latent-space-decoding'
- 'synthetic-supervision'
summary: >-
  Bahmani et al. (2025), [ARXIV-2509.19296](https://arxiv.org/abs/2509.19296) — Lyra. Train a 3D Gaussian
  Splatting decoder on the latents of a frozen camera-controlled video
  diffusion model (GEN3C), supervised only by that model's own RGB decodings
  along six camera trajectories per image, with no real multi-view data.
  Decoding latents rather than pixels is what makes 726 views per scene fit in
  memory. Single image to 3D beats the reported numbers of ZeroNVS,
  ViewCrafter, Wonderland and Bolt3D on RealEstate10K, DL3DV and
  Tanks-and-Temples, and adding real multi-view data to the synthetic
  supervision does not help.
---
<!-- inactive-ok-file: SOTA-tmpqmoen — Proposed, named as the practice filed from this paper, pending the comparison it asks for -->
<!-- inactive-ok-file: SOTA-394 — Proposed; named as neighbours this paper informs or tests, with their standing stated where they are cited -->

# LIT-tmp5yash: Lyra: Generative 3D Scene Reconstruction via Video Diffusion Model Self-Distillation

Bahmani et al., NVIDIA, University of Toronto, Vector Institute and Simon Fraser University (2025) — [ARXIV-2509.19296](https://arxiv.org/abs/2509.19296)

## Key takeaways

- **The setup.** GEN3C, a camera-controlled video diffusion model built on
  Cosmos, generates a video latent for an input image along a sampled camera
  path. The latent is decoded twice: by the frozen RGB VAE decoder into
  frames (the teacher) and by a new 3DGS decoder into Gaussians, whose
  renderings are trained to match those frames (the student). Only the 3DGS
  decoder is trained; the VAE and the diffusion model stay frozen, and at
  inference the RGB decoder is not used at all.
- **All supervision is generated.** Text prompts from LLMs, images from an
  image diffusion model, then six camera trajectories per image through
  GEN3C: 59,031 images give 354,186 videos for 3D, and 7,378 videos give
  44,268 for 4D.
- **Latent-space decoding is the enabling choice.** Six trajectories of 121
  frames at 704×1280 is 726 views per scene; pixel-space feed-forward
  reconstructors handle 2–24 (GS-LRM, AnySplat) or 12 (BTimer). Patchifying
  the 8×-compressed latents 2×2 and decoding from there fits; the pixel-space
  version runs out of memory (Table 2).
- **Decoder.** Long-LRM's block, one Transformer layer then seven Mamba-2
  layers, twice, for 16 layers at width 512, with Plücker ray embeddings
  encoded by the same VAE encoder. Replacing Mamba-2 with Transformer layers
  is slightly worse (PSNR 24.58 against 24.77) and 6.5× slower per forward
  pass (20,922 against 3,213 ms).
- **Losses.** MSE plus LPIPS against the teacher frames, a scale-invariant
  depth loss against ViPE video depth (without it geometry goes flat), and an
  L1 opacity penalty with the lowest-opacity 80% of Gaussians pruned (render
  time 30 → 18 ms).
- **Main results (Table 1).** Single image to 3D, PSNR / SSIM / LPIPS:
  RealEstate10K 21.79 / 0.752 / 0.219 against Bolt3D's 21.54 / 0.747 / 0.234;
  DL3DV 20.09 against Wonderland's 16.64; Tanks-and-Temples 19.24 against
  15.90. The baselines' numbers are taken from their papers, since no code was
  available to rerun them, and Bolt3D reports RealEstate10K only.
- **Ablations (Table 2), on the generated Lyra dataset.** Real multi-view
  data only (RealEstate10K + DL3DV): PSNR 19.08 against 24.77. Self-distilled
  plus real data: 24.74, no better. Per-trajectory Gaussians fused afterwards
  instead of a learned fusion across trajectories: 17.73, the largest drop.
  Without LPIPS, 23.74. These are scored against the video model's own
  renderings on out-of-distribution prompts, so the comparison with real-data
  training is measured on the teacher's distribution and favours the student
  trained on it; the benchmark results in Table 1 are the fairer test.
- **4D.** Time-conditioned Gaussians (BTimer's bullet-time design) trained
  from multi-view videos the teacher generates from a single input video.
  Supervising with only the outward trajectories leaves early timesteps
  poorly covered and low in opacity; adding six motion-reversed trajectories,
  so each timestep is seen from near and far, fixes it. Against BTimer on
  100 generated videos: PSNR 23.07 against 20.29.
- **Limit stated by the authors.** The scale and consistency of what Lyra
  produces is bounded by the video model; the student cannot be more 3D
  consistent than its teacher's frames.

## Standing in the anthology

The output representation is 3D Gaussian Splatting ([LIT-108](LIT-108.md)), which [SOTA-205](../practices.d/SOTA-205.md)
recommends as one of its compact explicit structures; Lyra is evidence that
the structure can be predicted feed-forward at scene scale rather than fitted
per scene. It sits beside [SOTA-236](../practices.d/SOTA-236.md) and its sources DUSt3R ([LIT-385](LIT-385.md)) and VGGT
([LIT-384](LIT-384.md)) in predicting geometry directly from images in one pass, but none of
those are compared against, and its supervision is a generator's output
rather than captured scenes.

The decoder's seven Mamba-2 layers per Transformer layer are a vision-side
instance of the hybrid [SOTA-132](../practices.d/SOTA-132.md) recommends for language, at about three
linear-attention layers per global one. The ablation agrees on the
direction, near-equal quality for a large speed gain, at a ratio the
practice does not discuss. The Mamba-2 layers are [LIT-162](LIT-162.md)'s state-space
duality design, used here unmodified.

For video diffusion the record's neighbours are about generating video, not
consuming it: Wan ([LIT-619](LIT-619.md)), which the 4D data pipeline also uses to generate
its source videos, and the distillation of video generators into few-step
students ([SOTA-394](../practices.d/SOTA-394.md), [LIT-631](LIT-631.md)). Lyra's "self-distillation" is a different
thing: distilling the model's implicit 3D into an explicit representation,
not distilling its sampler.

The candidate claim, that a frozen camera-controlled video model can stand
in for captured multi-view data when training a 3D reconstructor, rests on
one ablation measured on the teacher's own distribution. It is filed as a
Proposed practice, [SOTA-tmpqmoen](../practices.d/SOTA-tmpqmoen.md), whose promotion condition asks for that
comparison scored on real held-out views.

Unread — no NOTE.
