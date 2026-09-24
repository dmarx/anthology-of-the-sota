---
status: Active
title: 'Open-Sora 2.0: Training a Commercial-Level Video Generation Model in $200k'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- training-optimization
- representation-and-encoding
date: '2026-09-24'
published: '2025-03-01'
arxiv: '2503.09642'
first_author: 'Peng'
keywords:
- 'video-diffusion'
- 'training-cost'
- 'image-to-video'
- 'high-compression-autoencoder'
- 'flow-matching'
- 'low-resolution-pretraining'
implementations:
- 'Open-Sora 2.0'
extends:
- LIT-449
compared_against:
- LIT-620
- LIT-624
summary: >-
  The Open-Sora team, HPC-AI Tech (2025), [ARXIV-2503.09642](https://arxiv.org/abs/2503.09642). An 11B video
  model initialized from FLUX, with most of its compute at 256px and a short
  768px stage run as image-to-video. The "$200k" is one final
  diffusion-model run at an assumed H200 rental rate. It excludes the
  autoencoder, data, captioning, failed runs and FLUX. The efficiency case
  rests on a 4×32×32 autoencoder, but the evaluated model runs on
  HunyuanVideo's VAE.
---

# LIT-tmprr82r: Open-Sora 2.0: Training a Commercial-Level Video Generation Model in $200k

The Open-Sora team (Peng, Zheng et al.), HPC-AI Tech (2025) — [ARXIV-2503.09642](https://arxiv.org/abs/2503.09642)

## Key takeaways

- **The cost accounting is explicit, and narrow.** Table 2 covers "a single
  full training run, assuming the rental price of H200 is $2 per GPU hour":
  - 256px text-to-video: 2240 GPU-days, $107.5K
  - 256px text/image-to-video: 384 GPU-days, $18.4K
  - 768px text/image-to-video: 1536 GPU-days, $73.7K
  - total: 4160 GPU-days, $199.6K

  This is the only report in the line that states its training cost at all.
- **It is initialized from a distilled image model.** Training starts from
  FLUX. The authors "empirically find that, despite it being a distilled
  model, this initialization is effective" (§4.1.1). No comparison is shown.
- **Images are in every stage, as a buried detail.** Appendix D gives image
  buckets at 256, 768 and 1024px in stages 1–2 and 768px images in stage 3
  (Tables 4–5). The main text never says so.
- **High resolution is reached through image-to-video.** The authors
  "hypothesize" that adapting from 256px to 768px is much more efficient as
  image-to-video than as text-to-video (§4.1.4). At inference the pipeline is
  text to image (FLUX) to video.
- **Video DC-AE.** A non-causal 4×32×32 autoencoder cuts tokens from 76K to
  19K and raises training throughput 5.2× (Fig. 4). Its reconstruction
  matches HunyuanVideo's VAE, with LPIPS 0.049–0.051 against 0.046 (Table 1).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"$200k"** (title) leaves out several costs:
  - the autoencoder (450K steps) and the adaptation runs to it
  - data filtering and captioning, partly with a proprietary model
  - failed runs and hyperparameter search
  - FLUX's pretraining, which the initialization inherits

  The comparison figure labels GPU-hours "in H100" for a run on H200, and the
  Movie Gen and Step-Video costs it compares against are estimates.
- **The efficiency claim and the evaluated model don't match.** The model is
  "initially trained on HunyuanVideo's VAE and later adapted to our Video
  DC-AE" (§3). The DC-AE version "does not fully converge… underperforms the
  original" (§4.3.3), shown only qualitatively.
- **"Comparable to HunyuanVideo"** (abstract) comes from a text-to-image-to-
  video pipeline, with FLUX supplying the first frame, evaluated against
  text-to-video baselines (Fig. 10 caption).
- **Asserted, not ablated:** FLUX initialization, low-resolution motion
  learning, image-to-video-first adaptation, and ">99%" GPU utilization.

## Standing in the anthology

The record keeps this report for its cost accounting, which no other video
report gives. The honest reading of the figure is the price of the last
run, not the price of the model. That distinction is worth writing down
because "$200k" is the sentence that travels.

On [SOTA-386](../practices.d/SOTA-386.md) it is adoption in both halves: image initialization, and images
in every stage. It is one more report that does the practice without
testing it. The initialization from a *distilled* image model is new, and
untested.

Filed without a `NOTE`: the takeaways come from one full reading of v3
(checked against v1) done for this filing, appendices A–I included.
