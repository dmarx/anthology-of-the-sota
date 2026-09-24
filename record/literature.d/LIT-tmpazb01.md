---
status: Active
title: 'From Slow Bidirectional to Fast Autoregressive Video Diffusion Models'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- inference-optimization
date: '2026-09-24'
published: '2024-12-01'
arxiv: '2412.07772'
first_author: 'Yin'
keywords:
- 'autoregressive-video-diffusion'
- 'asymmetric-distillation'
- 'distribution-matching-distillation'
- 'block-causal-attention'
- 'ode-initialization'
- 'kv-caching'
implementations:
- 'CausVid'
compared_against:
- LIT-622
- LIT-626
summary: >-
  Yin et al., MIT and Adobe (2024), [ARXIV-2412.07772](https://arxiv.org/abs/2412.07772). CausVid distills a
  bidirectional video DiT into a 4-step block-causal student with
  distribution matching, cutting first-frame latency from 219s to 1.3s at
  9.4 fps. The controlled result is that a bidirectional teacher makes a
  better causal student than a causal one, which avoids inheriting the
  teacher's error accumulation. The paper does not claim real time, and it
  reports that the student flickers more and is less diverse.
extended_by:
- LIT-tmp0kzd1
---

# LIT-tmpazb01: From Slow Bidirectional to Fast Autoregressive Video Diffusion Models

Yin et al., MIT and Adobe (2024) — [ARXIV-2412.07772](https://arxiv.org/abs/2412.07772). Known as "CausVid".

## Key takeaways

- **Asymmetric distillation.** A bidirectional teacher, "similar to
  CogVideoX", is distilled into a block-causal student with DMD2-style
  distribution matching, sampling in 4 steps (§4). Attention is
  bidirectional within each 5-latent-frame chunk and causal across chunks,
  with a KV cache.
- **A bidirectional teacher beats a causal one** at the same ODE
  initialization, architecture, data and steps (Table 4). Scores are
  temporal quality / frame quality / text alignment: 94.7 / 64.4 / 30.1
  against 91.9 / 61.7 / 28.2. The causal teacher's error accumulation
  carries into its student (Fig. 8).
- **ODE-regression initialization helps.** Initializing the student by
  regressing onto the teacher's ODE endpoints gives 94.7 / 64.4 / 30.1,
  against 93.4 / 60.6 / 29.4 without it (Table 4).
- **Latency.** First-frame latency is 1.3s and throughput 9.4 fps, against
  219s and 0.6 fps for the teacher, on one H100 at 640×352 for 120 frames,
  including the VAE and text encoder (Table 3).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Effectively mitigates error accumulation"** (abstract) sits against "we
  still observe quality degradation when generating videos that are
  extremely long" (§6).
- **The student is worse than the teacher on two axes.** It "performs worse
  in temporal flickering and output diversity" (§5.2, last lines). Its
  flicker score is the lowest in the VBench table (App. Table 7). The
  diversity loss is "characteristic of reverse KL" (§6).
- **It does not claim real time.** "Limited to generating videos at around
  10 FPS… could potentially enable real-time" (§6). The VAE sets the latency
  floor, since it needs five latent frames before producing any pixels.
- **The 14-minute video is one example.** The user study is 29 prompts × 3
  raters.

## Standing in the anthology

This opens the causal branch of the line. Every other video model in the
record generates a fixed clip bidirectionally. The transferable result is
the asymmetric one: when distilling into a causal few-step generator, the
teacher should not be causal, because its accumulated errors distill
through. Self Forcing ([LIT-tmp0kzd1](LIT-tmp0kzd1.md)) builds directly on it.

DMD and DMD2, the distillation method it extends, are not held in the
record.

Filed without a `NOTE`: the takeaways come from one full reading done for
this filing, appendix included. Figures were read from their captions.
