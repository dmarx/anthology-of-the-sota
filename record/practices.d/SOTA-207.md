---
number: 207
status: Active
formerly:
- SOTA-tmpt7rzg
consensus: converged
consensus_note: >-
  DDIM inversion is the standard entry point for diffusion image editing and
  for interpolation, and it exists only because the sampler is deterministic.
  The record holds no work recovering a usable latent from a stochastic
  sampler.
title: 'Use the deterministic sampler when the noise input has to mean something'
version: 1
tags:
- generative-modeling
date: '2026-09-10'
source:
- LIT-038
summary: >-
  Song et al. (2020), [LIT-038](../literature.d/LIT-038.md). A stochastic sampler injects fresh noise at
  every step, so nothing about the starting point survives to the output.
  Setting the family's stochasticity to zero makes the initial noise a latent
  code you can interpolate in and invert to.
---

# SOTA-207: Use the deterministic sampler when the noise input has to mean something

## Source

Song et al. (2020), [LIT-038](../literature.d/LIT-038.md) — DDIM.

## The claim

The sampler family [LIT-038](../literature.d/LIT-038.md) derives is parameterised by how much noise it
injects at each step. At zero, the generative process is a deterministic map
from the initial noise to the sample, and two capabilities appear that a
stochastic sampler structurally cannot have:

- **The initial noise determines high-level image content regardless of how
  many steps you take.** It therefore behaves as a latent code, and
  interpolating in it produces semantically meaningful interpolation.
- **Samples can be encoded back to their latent and reconstructed** with very
  low error.

DDPM cannot do either, and the reason is not a tuning gap: its sampling adds
fresh noise at every step, so the trajectory does not carry the starting point
forward.

## When this applies

Reach for it when the *latent* is part of the product — editing, inversion,
interpolation, or anything that needs the same input to give the same output.

It is not a blanket recommendation to sample deterministically. [LIT-075](../literature.d/LIT-075.md) finds
that the useful amount of stochasticity depends on how good the model is: noise
injected during sampling corrects accumulated error, and a weaker model
benefits from it. Determinism buys invertibility and costs that correction.

## Conditions

- 2020, images, DDPM-scale models.
- Deterministic trajectories accumulate error at the low signal-to-noise end.
  [LIT-038](../literature.d/LIT-038.md) does not examine this; [LIT-067](../literature.d/LIT-067.md) is where it has to be fixed.
- Determinism here is a property of the sampler, not of the parametrization.
  It composes with [SOTA-188](SOTA-188.md) and [SOTA-195](SOTA-195.md) rather than competing with them.
