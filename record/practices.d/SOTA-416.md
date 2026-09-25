---
number: 416
status: Active
formerly:
- SOTA-tmpetg8o
consensus: emerging
consensus_note: >-
  Two groups report the defect. LIT-689 (Lin et al.) diagnoses it and
  shows it on one same-seed image, and LIT-687 measures its cost with
  everything else fixed. Marigold's own authors (LIT-691) measured the
  leading arm without knowing it: about 34% NYUv2 AbsRel at one step. It is
  not the library default. diffusers' DDIMScheduler still defaults to
  leading (checked 2026-09-25), and adopters opt in per checkpoint (Marigold
  v1-1). Read as of 2026-09.
promote_when: >-
  Lin et al. is filed and its own leading-against-trailing comparison is read
  next to this one. This is a correctness fix with a single-variable
  measurement, so a second reading of the originating paper is what stands
  between it and Active. A benchmark gain from a model that changed other
  things along with the spacing would not count.
title: 'When sampling a diffusion model in few steps, start at t = T: use trailing, not leading, timestep spacing'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Active, as its promote_when set out: Lin et al. is filed and was read
    next to LIT-687, and found no contradiction. It adds an independent
    diagnosis and a same-seed single-variable comparison, though not a
    second number. Marigold's own step curve supplies the leading arm's cost
    on the same weights. The reading also corrected three things. Lin
    credits the trailing discretization to DPM-Solver rather than proposing
    it. "Slight" was LIT-687's word, not Lin's. And nothing in either paper
    tests unconditional generation.
tags:
- generative-modeling
- inference-optimization
- vision-and-graphics
date: '2026-09-25'
source:
- LIT-687
- LIT-689
# LIT-687 is the numeric single-variable measurement. LIT-689 states the
# rule ("sample steps should always include the last timestep") and names
# the three spacings; it credits the trailing discretization itself to
# DPM-Solver (LIT-076), which was not checked (ADR-030).
introduced_by:
- LIT-689
implementations:
- 'diffusers (timestep_spacing="trailing")'
summary: >-
  Martin Garcia et al. (WACV 2025), [LIT-687](../literature.d/LIT-687.md). DDIM's "leading" spacing
  never visits the final timestep. So at one step, a pure-noise input is
  labelled with a timestep that claims an almost clean sample. With the same
  weights and only the spacing changed, Marigold's single-step depth goes
  from noise to NYUv2 AbsRel 5.7. The mismatch vanishes as the step count
  approaches T, which is why it goes unnoticed at 50 steps.
---

# SOTA-416: When sampling a diffusion model in few steps, start at t = T: use trailing, not leading, timestep spacing

## Source

Martin Garcia et al. (2024; WACV 2025), [LIT-687](../literature.d/LIT-687.md), measuring the
rule Lin et al. (2023; WACV 2024), [LIT-689](../literature.d/LIT-689.md), stated: "sample steps
should always include the last timestep t = T". Lin et al. named the leading,
linspace and trailing spacings. They credit the trailing discretization itself
to DPM-Solver ([LIT-076](../literature.d/LIT-076.md)), which this record has not checked.

What it costs, measured before anyone knew: Marigold's authors report about
34% NYUv2 AbsRel at one step ([LIT-691](../literature.d/LIT-691.md), Fig. 7) on weights that
reach 5.7 at one step once the spacing is trailing.

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
  inference steps, both strategies converge." That describes the timestep
  list. On a zero-terminal-SNR model, Lin et al.'s one same-seed image shows
  leading still changing the composition at 25 steps, because the single
  pure-noise timestep is exactly the one leading skips. That is one image,
  so it is a hedge, not a claim.
- **For text-to-image generation [LIT-687](../literature.d/LIT-687.md) calls the gain "slight".** That is
  its characterization of Lin et al. Lin never measures spacing alone.
  Nothing in either paper tests unconditional generation. For
  image-conditional prediction it is the difference between output and
  noise.
- **It is not zero-terminal-SNR rescaling.** Lin et al. propose both, and they
  are separate fixes. This practice is the spacing alone.
  [SOTA-263](SOTA-263.md)'s zero-terminal-SNR discussion is about the other one.

## Known implementations

- diffusers exposes the setting, and its DDIM default is still `leading`.
  Marigold's v1-1 configuration opts in (adoption, `DP-005`).
