---
status: Active
title: 'Wonderland: Navigating 3D Scenes from a Single Image'
version: 1
tags:
- vision-and-graphics
- generative-modeling
- representation-and-encoding
- data-pipeline
- adaptation-and-tuning
date: '2026-10-01'
published: '2024-12-16'
arxiv: '2412.12091'
first_author: 'Liang'
keywords:
- '3d-scene-generation'
- 'single-image-to-3d'
- '3d-gaussian-splatting'
- 'camera-controlled-video-diffusion'
- 'feed-forward-reconstruction'
- 'latent-large-reconstruction-model'
- 'dual-branch-camera-conditioning'
- 'progressive-training'
summary: >-
  Liang et al. (2024), [ARXIV-2412.12091](https://arxiv.org/abs/2412.12091) — Wonderland (CVPR 2025). Fine-tune
  CogVideoX-5B-I2V for camera control with a ControlNet branch plus LoRA,
  then train a reconstructor (LaLRM) that regresses 3D Gaussians directly
  from the video latents rather than decoded frames. Reading latents beat
  reading RGB at matched cost (RealEstate10K PSNR 27.10 against 25.06).
  The reconstructor is trained on captured RealEstate10K, ACID and DL3DV
  first, then fine-tuned on those plus 20K videos the video model generated,
  supervised by its own decoded frames; that addition moved benchmark PSNR
  by at most 0.09.
compared_against:
- LIT-tmp5yash
---
<!-- inactive-ok-file: SOTA-tmpqmoen — Proposed; named to say this paper is its precedent, not its origin -->

# LIT-tmpnsayq: Wonderland: Navigating 3D Scenes from a Single Image

Liang, Cao, Goel, Qian, Korolev, Terzopoulos, Plataniotis, Tulyakov and Ren,
University of Toronto, Snap and UCLA (2024; CVPR 2025) — [ARXIV-2412.12091](https://arxiv.org/abs/2412.12091)

## Key takeaways

- **Two stages, one latent space.** A camera-guided video model generates a
  49-frame latent along a given trajectory from one image; a feed-forward
  Latent Large Reconstruction Model (LaLRM), 24 transformer blocks at width
  1,024, reads that latent with Plücker camera embeddings and outputs
  pixel-aligned 3D Gaussians. End to end it takes about 5 minutes on one
  A100, against about 16 for Cat3D, over 6 for ViewCrafter and 3 hours for
  ZeroNVS.
- **Camera control by a dual branch (Table 1).** A trainable copy of the
  first 21 of CogVideoX's 42 blocks as a ControlNet, plus LoRA of rank 256
  in the frozen main branch, both fine-tuned on static-scene datasets. On
  RealEstate10K, FID 16.16 and FVD 153.48 against ViewCrafter's 20.89 and
  203.71, with lower rotation and translation error. Either branch alone is
  worse (FID 18.75 ControlNet only, 19.02 LoRA only, 17.22 both, on a
  100-clip ablation set).
- **Latents beat pixels for the reconstructor (Table 3).** At matched
  compute, with RGB inputs patchified down to the latent size, RGB-14 and
  RGB-49 reach RealEstate10K PSNR 21.39 and 25.06; latents with the VAE
  encoder fine-tuned reach 26.14, and with it frozen 27.10. On
  Tanks-and-Temples, 22.66 for frozen latents against 20.54 for RGB-49.
  Fine-tuning the encoder jointly hurt, which the authors read as eroding
  the pretrained latent space.
- **Supervision is mostly captured data, with generated data added late.**
  The LaLRM trains 200K iterations at low resolution on RealEstate10K, ACID
  and DL3DV, each video supplying seen and unseen views. It then fine-tunes
  100K iterations at high resolution on those datasets plus 20K videos
  generated from Flux.1 images along RealEstate10K camera paths, where "the
  decoded video frames from these latents provide supervision views".
  Removing the generated videos (LaLRM–, Table A3) costs little on the
  benchmarks: RealEstate10K PSNR 17.06 against 17.15, DL3DV 16.62 against
  16.64, Tanks-and-Temples 15.85 against 15.90. The visible gain is
  qualitative, on 20 in-the-wild prompts (Fig. A2).
- **Single image to 3D (Table 2).** PSNR / SSIM / LPIPS 17.15 / 0.550 /
  0.292 on RealEstate10K, 16.64 on DL3DV and 15.90 on Tanks-and-Temples,
  against ViewCrafter's 16.84, 15.53 and 14.93 and ZeroNVS's 13.01, 13.35 and
  12.94. Scored only on the 14 frames nearest the conditioning image,
  because, the authors say, generated views drift from ground truth further
  out and similarity metrics stop meaning much there. One run per cell, no
  variance.

## Standing in the anthology

Filed because Lyra ([LIT-tmp5yash](LIT-tmp5yash.md)) names it "closely related to our work" and
runs its evaluation protocol. Wonderland is the earlier of the two designs
and Lyra keeps its two load-bearing choices: a 3DGS decoder that reads a
camera-controlled video model's latents instead of its frames, and training
signal taken from that model's own decoded frames. What Lyra changes is the
proportion. In Wonderland generated videos are a 20K-video supplement in
the final fine-tuning stage, after a stage on captured data alone; in Lyra
they are all of it. That makes Wonderland the precedent but not the origin of
[SOTA-tmpqmoen](../practices.d/SOTA-tmpqmoen.md), which recommends the substitution. Its Table A3 is the
one measurement on real held-out views of what generated supervision adds
on top of captured data, and it is near zero on all three benchmarks.

The video model is CogVideoX ([LIT-622](LIT-622.md)) fine-tuned with a ControlNet
([LIT-089](LIT-089.md)) and LoRA ([LIT-046](LIT-046.md)) branch, and the output is 3D Gaussian
Splatting ([LIT-108](LIT-108.md)), predicted feed-forward rather than fitted per scene,
the way [SOTA-205](../practices.d/SOTA-205.md)'s compact explicit structure is otherwise fitted. Its
latent-against-pixel ablation is the measured basis for the design Lyra
calls its enabling choice. Like DUSt3R ([LIT-385](LIT-385.md)) and VGGT ([LIT-384](LIT-384.md)), the
sources of [SOTA-236](../practices.d/SOTA-236.md), it predicts geometry in one pass, but from generated
views of an unseen scene rather than from captured images of a real one, and
it compares against neither.

Unread — no NOTE.
