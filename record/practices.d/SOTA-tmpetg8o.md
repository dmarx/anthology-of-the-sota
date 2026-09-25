---
status: Proposed
consensus: emerging
consensus_note: >-
  Two groups report the defect: Lin et al. (2023, arXiv 2305.08891), which
  the record does not yet hold, and LIT-tmpy1bpi, which measures its cost with
  everything else fixed. Adoption of trailing spacing as a library default was
  not checked and is not asserted here. Read as of 2026-09.
promote_when: >-
  Lin et al. is filed and its own leading-against-trailing comparison is read
  next to this one. This is a correctness fix with a single-variable
  measurement, so a second reading of the originating paper is what stands
  between it and Active. A benchmark gain from a model that changed other
  things along with the spacing would not count.
title: 'When sampling a diffusion model in few steps, start at t = T: use trailing, not leading, timestep spacing'
version: 1
tags:
- generative-modeling
- inference-optimization
- vision-and-graphics
date: '2026-09-25'
source:
- LIT-tmpy1bpi
introduced_by:
- LIT-tmpy1bpi
implementations:
- 'diffusers (timestep_spacing="trailing")'
summary: >-
  Martin Garcia et al. (WACV 2025), [LIT-tmpy1bpi](../literature.d/LIT-tmpy1bpi.md). DDIM's "leading" spacing
  never visits the final timestep. So at one step, a pure-noise input is
  labelled with a timestep that claims an almost clean sample. With the same
  weights and only the spacing changed, Marigold's single-step depth goes
  from noise to NYUv2 AbsRel 5.7. The mismatch vanishes as the step count
  approaches T, which is why it goes unnoticed at 50 steps.
---

# SOTA-tmpetg8o: When sampling a diffusion model in few steps, start at t = T: use trailing, not leading, timestep spacing

## Source

Martin Garcia et al. (2024; WACV 2025), [LIT-tmpy1bpi](../literature.d/LIT-tmpy1bpi.md), applying
the trailing setting Lin et al. (2023, arXiv 2305.08891) proposed. That
paper is not yet held, and it is the practice's origin.

## What to do

Choose inference timesteps so the first network call gets the timestep that
matches the pure-noise input it is given: `[T, …]`, not `[…, 1]`. With `T =
1000` and `k` steps, trailing gives `[1000, 1000 − T/k, …]` and leading gives
`[…, 1]`, missing `T` entirely. In diffusers this is
`timestep_spacing="trailing"`.

## Why

The network is trained on pairs of noise level and timestep. Leading spacing
at small `k` breaks that pairing at the first step, where the input is pure
noise and the timestep says otherwise. For one step, "the model receives a
timestep encoding that indicates an almost perfect depth map whereas the
actual input is pure noise". The error is largest when every step counts
and when the first prediction is expected to be nearly final, which is the
case for single-step inference and strongly conditioned models.

## Conditions

- **It matters at few steps and fades toward T.** "In the limit of k → T
  inference steps, both strategies converge."
- **For unconditional or text-to-image generation the gain is reported as
  slight.** That characterization is the source's, of Lin et al. For
  image-conditional prediction it is the difference between output and
  noise.
- **It is not zero-terminal-SNR rescaling.** Lin et al. propose both, and they
  are separate fixes. This practice is the spacing alone.
  [SOTA-263](SOTA-263.md)'s zero-terminal-SNR discussion is about the other one.

## Known implementations

- diffusers exposes the setting. Which pipelines default to it was not
  checked.
