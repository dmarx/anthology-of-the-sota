---
status: Proposed
consensus: emerging
consensus_note: >-
  Emu Video ran the only controlled comparison. CogVideoX and Marigold v1-1's
  released configuration adopt the fix, which is adoption, not evidence
  (DP-005). Movie Gen found flow matching beat this recipe outright, and flow
  matching has zero terminal SNR by construction. Read as of 2026-09.
promote_when: >-
  A second controlled comparison of the schedule-plus-v-prediction change
  against the standard schedule, everything else fixed, on images or video.
  Ideally it reports an output-brightness statistic, since that is the failure
  the fix names. Another model that ships zero terminal SNR would not count,
  and neither would a result that bundles it with guidance rescale or
  spacing changes, as its source's own table does.
title: 'Rescale the noise schedule so the last timestep is pure noise, and train with v-prediction so the model can learn there'
version: 1
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
source:
- LIT-tmp6c6lg
- LIT-635
# LIT-tmp6c6lg introduces and argues the fix but measures it only bundled
# with three others. LIT-635 is the controlled comparison (96.8 / 88.3 at
# 512px video), which also switches to v-prediction in the same arm. That is
# why the practice pairs the two (ADR-030).
introduced_by:
- LIT-tmp6c6lg
compared_against:
- SOTA-266
implementations:
- 'diffusers (rescale_betas_zero_snr=True)'
summary: >-
  Lin et al. (WACV 2024), [LIT-tmp6c6lg](../literature.d/LIT-tmp6c6lg.md), with Emu Video's comparison, [LIT-635](../literature.d/LIT-635.md).
  Common VP schedules leave signal at `t = T`. Stable Diffusion's leaves
  `√ᾱ_T = 0.068`. The model learns to keep the leaked channel mean, and
  pure-noise inference then limits brightness. Rescale `√ᾱ_t` so it reaches 0
  at `T`. Then train with v-prediction, because at zero SNR ε-prediction is
  trivial and `v_T = x₀`. Sample in the `x₀` form, because converting v to ε
  at zero SNR divides by zero.
---

<!-- inactive-ok-file: SOTA-tmpzrrgi — Proposed; named as the companion fix the source motivates -->

# SOTA-tmpwowqa: Rescale the noise schedule so the last timestep is pure noise, and train with v-prediction so the model can learn there

## Source

Lin, Liu, Li and Yang (2023; WACV 2024), [LIT-tmp6c6lg](../literature.d/LIT-tmp6c6lg.md), with the controlled
comparison in Emu Video ([LIT-635](../literature.d/LIT-635.md)).

## What to do

1. Shift and scale `√ᾱ_t` linearly so that `√ᾱ_T = 0` and `√ᾱ_1` is unchanged.
   For a cosine schedule, drop the 0.999 clip on `β`.
2. Train with v-prediction ([SOTA-195](SOTA-195.md)). At zero SNR, ε-prediction
   "becomes a trivial task", and the v-target at `t = T` is the clean sample.
3. Sample from `t = T` ([SOTA-416](SOTA-416.md)), and write the sampler in the `x₀`
   form. Converting v to ε at `ᾱ_t = 0` is a division by zero.

## Why

The leaked signal at `t = T` is the lowest-frequency part of the image,
chiefly each channel's mean. The model learns to respect it, and at inference
it gets pure noise with zero mean, so outputs are pulled to medium
brightness. That account is the source's argument. No experiment isolates it,
and the source never measures brightness numerically.

## Evidence

Emu Video's controlled arm at 512px video wins 96.8% on quality and 88.3% on
faithfulness against "the standard noise schedule". That arm also switches ε
to v, which is why this practice pairs the two. Lin et al.'s only number,
COCO FID 22.96 → 21.66, bundles this fix with trailing spacing and guidance
rescale, so it is not cited for this practice alone.

## Conditions

- **VP schedules only.** "variance-exploding formulation cannot truly reach
  zero terminal SNR."
- **Flow matching gets this for free, and beat it.** Movie Gen compared flow
  matching against v-prediction diffusion with zero terminal SNR, everything
  else fixed, and flow matching won. See [SOTA-266](SOTA-266.md). This practice is
  for anyone staying on a VP diffusion model.
- **Compatible with [SOTA-263](SOTA-263.md)'s resolution shift.** That moves the whole
  curve, and this fixes the endpoint. Nobody has compared them.
- **Guidance may need rescaling afterwards.** The source reports that
  classifier-free guidance "becomes very sensitive" at zero terminal SNR. See
  `SOTA-tmpzrrgi`.

## Known implementations

- diffusers `rescale_betas_zero_snr`. It is adopted by CogVideoX and by
  Marigold's v1-1 configuration, which is adoption per `DP-005`.
