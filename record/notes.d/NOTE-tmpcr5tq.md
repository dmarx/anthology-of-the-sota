---
status: Read
paper: LIT-tmppo845
title: 'FLUX.2 latent-space report'
version: 1
date: '2026-09-23'
summary: >-
  A controlled comparison of four autoencoder latents for flow models on
  ImageNet, with the timestep schedule swept per latent. The schedule
  decides the ranking. FLUX.2's VAE gets near-RAE learnability with the
  best reconstruction. Read in full from the rendered report, except the
  interactive Table 2, which did not load.
---

# NOTE-tmpcr5tq: FLUX.2 latent-space report

## Contribution

A fair comparison of latent spaces for generation, where "fair" means
each space gets its own best timestep schedule, and a measurement of how
much that tuning is worth.

## Key insight

**A latent space's learnability cannot be read off one schedule.** The
optimal noise shift depends on the representation's dimensionality and
spectrum. Compared at a shared schedule, the space the schedule happens to
suit wins.

## Key results

- Best gFID: RAE 3.10, FLUX.2 3.70, SD 7.73, FLUX.1 10.13. LPIPS: FLUX.2
  0.27, FLUX.1 0.34, SD 0.95, RAE 1.67
- At 300k steps, best-to-worst relative FID from the training shift alone:
  RAE 61.5%, FLUX.2 73.3%, SD 75.7%, FLUX.1 86.4%
- Logit-normal or plateau logit-normal beat shifted uniform in every
  latent. The optimal sampling shift is slightly above the optimal training
  shift
- Ranking flip: RAE loses to shifted FLUX.2 when RAE is unshifted, and wins
  when both are tuned
- REPA helps all four latents

## Limitations

- **One FID per configuration, one seed, ImageNet 256², DiT-XL.** Random
  (not class-balanced) class sampling, so the numbers are not comparable to
  RAE's paper
- **The grid tops out at α = 6.93**, which is where RAE's optimum lands.
  The √(m/n) agreement is partly a grid-edge effect
- **Table 2** (best parameters per step) is an interactive widget that did
  not render. The prose summary of it is what was read
- **The authors' own autoencoder**, and the FLUX.2 model results are human
  preference only
