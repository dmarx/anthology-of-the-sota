---
number: 346
status: Proposed
formerly:
- SOTA-tmprnub7
promote_when: >-
  An independent comparison of latent spaces for diffusion or flow models,
  with more than one seed per configuration, that tunes the training
  timestep shift per latent and shows the ranking or the gap between latents
  changing materially relative to a shared schedule. The source is one
  lab's report, single runs, on ImageNet 256² with DiT-XL.
title: 'Retune the training timestep shift for each autoencoder latent space, and never rank latent spaces for generation under one shared schedule'
version: 1
tags:
- generative-modeling
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-572
introduced_by:
- LIT-572
consensus: unassessed
consensus_note: >-
  Papers proposing new latent spaces (RAE, semantic VAEs) do tune their
  shift, and often compare against baselines run at defaults. How common
  per-latent tuning of baselines is has not been assessed here.
implementations: []
summary: >-
  Black Forest Labs (2025), [LIT-572](../literature.d/LIT-572.md) — four autoencoders, 30 timestep
  configurations each. The training shift alone moves FID by 61–86%. An RAE
  latent that wins when both are tuned loses to a tuned FLUX.2 latent when
  left unshifted. When you swap the autoencoder under a diffusion or flow
  model, sweep the shift again, using a logit-normal training distribution.
  When you compare autoencoders, compare each at its own optimum.
---

# SOTA-346: Retune the training timestep shift for each autoencoder latent space, and never rank latent spaces for generation under one shared schedule

## Source

Black Forest Labs (2025), [LIT-572](../literature.d/LIT-572.md). Read as [NOTE-311](../notes.d/NOTE-311.md).

## The practice

- **Changing the autoencoder changes the noise schedule you need.** The
  shift that suits a 16-channel SD latent is not the one that suits a
  128- or 768-channel latent. In the report the best training shift
  ranged from α = 1 (SD) to at least 6.93 (RAE), and choosing it badly cost
  61–86% relative FID
- **Sweep the training shift first, then the sampling shift.** The
  sampling shift mattered less (4.5–38.7%), and its optimum sat slightly
  above the training shift's
- **Use a logit-normal training distribution** (as in [SOTA-266](SOTA-266.md)). It, or its
  plateau variant, beat shifted-uniform sampling in every latent
- **When comparing latent spaces, tune each.** Otherwise the comparison
  measures fit to the schedule. The report's ranking of RAE against FLUX.2
  reverses between untuned and tuned

## Conditions

- **Single runs on ImageNet 256² with a DiT-XL.** Text-to-image at scale is
  not tested
- **The report's √(m/n) rule for predicting the shift is not established by
  its own data** (see [LIT-572](../literature.d/LIT-572.md)). Sweep it rather than computing it. The
  resolution form of the same argument is [SOTA-263](SOTA-263.md)
