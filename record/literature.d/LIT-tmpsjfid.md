---
status: Active
title: 'Movie Gen: A Cast of Media Foundation Models'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- model-architecture
- training-optimization
- representation-and-encoding
date: '2026-09-24'
published: '2024-10-01'
arxiv: '2410.13720'
first_author: 'Polyak'
keywords:
- 'text-to-video'
- 'flow-matching'
- 'temporal-autoencoder'
- 'joint-image-video-generation'
- 'video-personalization'
- 'video-to-audio'
implementations: []
extends:
- LIT-449
- LIT-062
compared_against:
- LIT-448
- LIT-tmpkcchp
- LIT-tmpqns7l
summary: >-
  The Movie Gen team, Meta (2024), [ARXIV-2410.13720](https://arxiv.org/abs/2410.13720). A 30B video model built
  from a Llama 3-style transformer, flow matching and an 8×8×8 temporal
  autoencoder, with the most controlled ablations in the video line. At 5B,
  flow matching beats diffusion and video captions beat frame captions. The
  "LLaMa3 scaling laws" claim rests on image-only runs at four sizes.
---

# LIT-tmpsjfid: Movie Gen: A Cast of Media Foundation Models

The Movie Gen team, Meta (2024) — [ARXIV-2410.13720](https://arxiv.org/abs/2410.13720)

## Key takeaways

- **The ablations are controlled.** Each Table 8 comparison is a 5B model at
  352×192, trained on 21M videos and judged by humans on 381 prompts, with
  "every aspect of the model except for the design decision being tested …
  held constant".
  - **Flow matching beats diffusion** (v-prediction, zero terminal SNR) by a
    net win of +16.5 on overall quality and +7.1 on text alignment (Table 8a).
  - **Video captions beat frame captions** by +10.8 on alignment, almost all
    of it motion alignment (+16.1 on high-motion prompts; Table 8b).
  - **The Llama 3 block ([LIT-179](LIT-179.md)) beats the DiT block** by +18.6 on quality and +12.6
    on alignment (Table 8c).
- **The temporal autoencoder.** It compresses 8×8×8 into 16 channels and is
  inflated from an image autoencoder. On video it is close to a frame-wise
  autoencoder, PSNR 32.25 against 34.11. On images it is better, 32.16
  against 30.83 (Table 11). An outlier-penalty loss removes "spot" artifacts
  in the latent (Table 13).
- **Fine-tuning is where much of the quality comes from.** Supervised
  fine-tuning on a small curated set gives a +34.7 net win over the
  pretrained model (Table 7).
- **Sampling.** A 50-step linear-quadratic schedule matches 250 linear steps
  (Fig. 10).
- **External comparisons.** Movie Gen is on par with Kling 1.5 (+3.9) and
  ahead of Sora (+8.2, σ = 5.1), Runway Gen-3 and Luma (Table 6). It loses to
  Kling on motion completeness.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The scaling claim is image-only and narrow.** Four sizes (5B–30B) are
  trained only on the 256px text-to-image stage, over 1e22–1.7e22 FLOPs,
  under a quarter of a decade. IsoFLOP minima are then plotted against the
  Llama 3 law, which is overlaid and not refit. The caption says that law
  "may serve as a reasonable predictor … even for media generation models"
  (Table 10). No video scaling experiment backs the abstract's "reap the
  benefits of scaling".
- **"Llama 3 beats DiT" is narrower than it sounds.** The two blocks differ
  only in norm, activation and bias (Table 9). Both keep adaLN and
  cross-attention. The ablation compares two versions of one block design,
  not two architectures.
- **"Holds across a range of model sizes"** for flow matching comes with no
  data. The alignment win (+7.1) is under twice the annotation σ the paper
  reports elsewhere (Table 40).
- **The Sora comparison uses a different recipe.** It used 500 linear steps
  and a manual best-of-5 selection (App. C.2), not the 50-step recipe of §3.4.
- **No weights were released.** Only the benchmark prompts and generations
  were published.

## Standing in the anthology

**This is the line's source for flow matching over diffusion, and the only
controlled test of it at video scale.** Every later model here (HunyuanVideo,
Step-Video, Wan) trains with flow matching. None of them tests it, and
Movie Gen is the report that did. It is equally the source for video-native
captioning, which the others assert.

The scaling claim is the sentence to watch. It will be quoted as "video
models follow LLM scaling laws", and the evidence is image-only, four
points, and an overlaid rather than fitted curve. HunyuanVideo
([LIT-tmpkcchp](LIT-tmpkcchp.md)) fits its own video law, on a proxy model.

Filed without a `NOTE`: the takeaways come from one reading of the video
sections (§§1–3 in full, §8, App. A.1, C.1–C.2), done for this filing. The
audio, editing and personalization sections were skimmed.
