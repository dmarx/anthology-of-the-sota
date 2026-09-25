---
number: 414
status: Proposed
formerly:
- SOTA-tmpaisvs
consensus: unreplicated
consensus_note: >-
  One group, one backbone (Stable Diffusion v2), no seeds. Concurrent work by
  Xu et al. (arXiv 2403.06090) also fine-tunes Stable Diffusion end to end and
  scores lower than some baselines. That is concurrent work, not a
  replication. Read as of 2026-09.
promote_when: >-
  A second group compares end-to-end one-step fine-tuning against diffusion
  fine-tuning with correctly spaced (trailing) multi-step inference, from the
  same initialization and data, and reports it with seeds. Another depth or
  normals model that ships single-step inference would not count, because
  that is adoption.
title: 'To make an image diffusion model a dense geometric predictor, fine-tune it end to end as a one-step model at t = T with a task loss'
version: 1
tags:
- vision-and-graphics
- adaptation-and-tuning
- inference-optimization
date: '2026-09-25'
source:
- LIT-687
introduced_by:
- LIT-687
implementations:
- 'diffusion-e2e-ft'
summary: >-
  Martin Garcia et al. (WACV 2025), [LIT-687](../literature.d/LIT-687.md). Fix the timestep at T, feed
  zeros as the noise, decode the prediction through the frozen VAE, and train
  on the task's own loss: affine-invariant L1 for depth, angular error for
  normals. From 20K iterations on 74K synthetic images, the one-step model
  beats Marigold's 50-step, 10-member ensemble on depth AbsRel on all five
  zero-shot sets, and on normals by 2.6–3.0° of mean error. Starting from
  plain Stable Diffusion is nearly as good.
---

<!-- inactive-ok-file: SOTA-416 — Proposed; named for the baseline comparison
     only, which this practice does not depend on -->

# SOTA-414: To make an image diffusion model a dense geometric predictor, fine-tune it end to end as a one-step model at t = T with a task loss

## Source

Martin Garcia, Knaebel, Schmidt, de Geus, Hermans and Leibe (2024; WACV 2025),
[LIT-687](../literature.d/LIT-687.md).

## What to do

Start from an image diffusion model (Stable Diffusion, or a diffusion-fine-tuned
depth model). Condition on the input image as usual. Then:

1. Fix `t = T`, and replace the noise input with zeros.
2. Convert the network's prediction to a clean latent (with v-prediction,
   `ẑ₀ = √ᾱ_T z_T − √(1−ᾱ_T) v̂`) and decode it through the **frozen** VAE
   decoder.
3. Train on the task loss in output space: an affine-invariant L1 after a
   least-squares scale and shift for depth, and angular error for normals.

Use one forward pass at inference, with no ensembling.

## Why it should work, and how far that is shown

For a near-unimodal conditional distribution, which is roughly what depth
given an image is, the optimal prediction at `t = T` is close to the
conditional mean. One step should then suffice, and a task loss trains
exactly that prediction. The source argues this from EDM's result on the
final-step prediction and does not isolate it. Its measured finding is that
the fine-tuned one-step model beats both the fixed one-step model and the
ensembled multi-step one.

## Evidence

Depth AbsRel, zero-shot: 5.2 / 9.6 / 6.2 / 5.8 / 30.2 on NYUv2 / KITTI /
ETH3D / ScanNet / DIODE, against 5.5 / 9.9 / 6.5 / 6.4 / 30.8 for Marigold at
50 steps × 10. That is 1 network evaluation against 500. Starting from plain
SD gives 5.4 / 9.6 / 6.4 / 5.8 / 30.3.

## Conditions

- **Dense geometry with a near-unimodal target.** The argument fails where
  the conditional distribution is multimodal, and image generation is the
  obvious case.
- **One backbone, one fine-tuning budget, no seeds.** The SD-against-Marigold
  initialization comparison rests on 0.0–0.2 AbsRel.
- **Depends on [SOTA-416](SOTA-416.md) only for the baseline.** The
  fine-tuning recipe fixes `t = T` directly. Scheduler spacing matters only to
  anyone comparing against multi-step inference, and that comparison is
  unfair until the spacing is trailing.
- **Relies on v-prediction to make the `t = T` prediction a clean one.** The
  source does not compare parameterizations. See [SOTA-195](SOTA-195.md).

## Known implementations

- diffusion-e2e-ft, the source's code.
