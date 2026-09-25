---
number: 263
status: Active
formerly:
- SOTA-tmp4jpf3
consensus: emerging
consensus_note: >-
  Measured twice, concurrently, by two Google Brain groups in pixel space
  (simple diffusion and Chen 2023). SD3 measured the sampling-time value by
  human preference. SVD, LTX-Video and Open-Sora 2.0 adopt it and say why.
  HunyuanVideo shifts by step count instead, which is a different
  correction. `emerging` rather than `converged`, because the magnitude is
  tuned in every source and nobody agrees on it.
title: 'Shift the timestep schedule when the resolution changes, because more pixels need more noise'
version: 4
history:
- version: 4
  date: '2026-09-25'
  note: >-
    The zero-terminal-SNR section now names its origin. LIT-tmp6c6lg (Lin et
    al.) introduced the fix for a leaked channel mean at any resolution, and
    Emu Video added the resolution argument. The recommendation is
    unchanged.
- version: 2
  date: '2026-09-23'
  note: >-
    Appends `signal-structure`. A load-bearing part of this
    document is a property of the data: its mechanism is a property of
    images: the redundancy across neighbouring pixels survives the same
    noise at higher resolution.
- version: 3
  date: '2026-09-24'
  note: >-
    Promoted to Active. The first clause of promote_when, an ablation of
    what the shift is worth, was met 14 months before this practice was
    filed. Simple diffusion (ARXIV-2301.11093) Table 2 and Chen
    (ARXIV-2301.10972) Table 4 are controlled, and SD3's own Fig. 6 is a
    human-preference sweep the document had called qualitative.
    introduced_by moves from SD3 to the two 2023 papers, which SD3 cites
    for the log-SNR shift. The second clause, a report that says it
    shifted for this reason, was also met by LTX-Video and Open-Sora 2.0.
    It was not used, because per DP-005 it counts adoption.
tags:
- generative-modeling
- signal-structure
date: '2026-09-20'
source:
- LIT-660
- LIT-659
- LIT-449
introduced_by:
- LIT-660
- LIT-659
implementations:
- 'simple diffusion'
- 'Stable Diffusion 3'
- 'Stable Video Diffusion'
- 'LTX-Video'
- 'Open-Sora 2.0'
summary: >-
  Hoogeboom et al. (2023), [LIT-660](../literature.d/LIT-660.md), and Chen (2023), [LIT-659](../literature.d/LIT-659.md).
  A timestep is not a fixed amount of corruption. Destroying the signal in
  an image with more pixels takes more noise, so a schedule set at one
  resolution under-corrupts at a higher one. Shifting log-SNR down with
  resolution takes ImageNet 256 FID from 7.65 to 3.76 in pixel space. The
  direction is measured. The magnitude is tuned in every source.
---
<!-- inactive-ok-file: SOTA-346 — Proposed; cited for a latent-space datum on the shift's magnitude, not as settled -->


# SOTA-263: Shift the timestep schedule when the resolution changes, because more pixels need more noise

## Source

Hoogeboom, Heek and Salimans (2023), [LIT-660](../literature.d/LIT-660.md) — [ARXIV-2301.11093](https://arxiv.org/abs/2301.11093), and
Chen (2023), [LIT-659](../literature.d/LIT-659.md) — [ARXIV-2301.10972](https://arxiv.org/abs/2301.10972). They are concurrent, and each
cites the other.

Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — [ARXIV-2403.03206](https://arxiv.org/abs/2403.03206). SD3 derives the shift
again for rectified flow, measures the sampling-time value by human
preference, and notes that its shift is "similar to (Hoogeboom et al.,
2023)".

## The correction

A noise schedule is usually treated as a property of the model: chosen once,
carried across runs. But what a timestep *does* depends on how much signal
there is to destroy, and an image with more pixels has more. Add the same
noise to a 256×256 image and a 1024×1024 one and the second is less
corrupted, because the redundancy across neighbouring pixels survives.

So a timestep `t` at one resolution corresponds to a *different* timestep at
another if the two are to corrupt equivalently, and the correspondence can be
written down from the pixel count. The usual pipeline — pretrain at low
resolution, finetune at high — carries the schedule across unchanged, which
means the high-resolution stage trains against a schedule that under-corrupts
throughout. The same error occurs without a second stage. The cosine
schedule was designed at 32 and 64, and using it to train at 256 from
scratch is where the error was first measured.

The direction of the error is predictable, which is what makes this a
practice rather than an observation: higher resolution wants more noise at
the same nominal timestep.

## Why this is easy to miss

Nothing breaks. The model trains, the loss falls, and the samples are
plausible — the failure is that the high-resolution stage spends its budget
on a corruption range it was not supposed to be in. That is the same shape of
quiet failure the record records elsewhere for over-large batches
([SOTA-061](SOTA-061.md)) and for unadjusted preconditioning ([SOTA-188](SOTA-188.md)): the run
completes and is simply worse than it should have been, and the deficit gets
attributed to data or to scale.

## Relation to the schedule material the record holds

[THEORY-027](../theory.d/THEORY-027.md) says the continuous-time bound is indifferent to the
schedule's *shape* given its endpoints. This practice is not in tension with
that: a resolution shift changes which corruption level a given `t` produces,
which is a statement about the map from time to signal-to-noise, and the
endpoints move with it. What the invariance licenses is exactly this kind of
reparameterization — if the shape were part of the model, shifting it would
be a modelling change rather than a correction.

## What it is worth

**Simple diffusion, Table 2.** Pixel-space ImageNet, where only the
reference resolution of the cosine schedule changes:

| resolution | unshifted (FID train / eval) | best shift | shifted (train / eval) |
|---|---|---|---|
| 128 | 2.96 / 3.38 | to 32 | 2.26 / 2.88 |
| 256 | 7.65 / 6.87 | to 32 | 3.76 / 3.71 |

The shift halves FID at 256, and the gain grows with resolution,
which is the direction the argument predicts.

**Chen, Table 4.** The same shift written as input scaling, x0 → b·x0.
At 256 with a 1−t schedule, b = 1 gives 7.21 and b = 0.4 gives 3.52. The
best b falls from about 1.0 at 64 to 0.6 at 128 and 0.4 at 256.

**SD3, Fig. 6.** A human-preference sweep of the shift at sampling time, on
a model trained at 1024². It shows "a strong preference for samples with
shifts greater than 1.5 but less drastic differences among the higher
shift values".

## The direction is measured; the magnitude is not derived

Every source derives a shift from the pixel count, and none uses the
derived value:

- **SD3.** The derivation gives α = √(m/n), which is 4 for 256² → 1024².
  SD3 uses 3.0, chosen by preference, and the preference is flat above
  1.5.
- **Simple diffusion.** The reference resolution is picked empirically.
  Shift-to-32 and shift-to-64 differ by 0.18 FID at 256, and the authors
  recommend 64 "because it performed slightly better in early
  iterations".
- **Chen.** The optimum is found by sweeping b, and the sweep is not
  monotone between neighbouring values.
- **FLUX.2's latent-space sweep** ([LIT-572](../literature.d/LIT-572.md)) applies the same √(m/n)
  argument to latent channels. SD's best training shift is 1, and FLUX.2
  prefers 4.63 against a predicted 2.82. That is [SOTA-346](SOTA-346.md)'s territory, and
  it shows the same pattern.

So the practice is to shift in the predicted direction and then tune the
amount. The formula is a starting point, not an answer.

## Conditions

- **Where it is measured.** The controlled measurements are pixel-space
  class-conditional ImageNet, trained from scratch at each resolution. SD3
  is the latent case, and only sampling-time. Nobody has reported the
  pretrain-at-256, finetune-at-1024 path with and without the shift, which
  is the situation this document was written about. The mechanism is the
  same, and the measurement is adjacent.
- **Guidance interacts with it.** Simple diffusion's shifted schedule
  "can only tolerate little guidance" (Table 9). For text-to-image it
  interpolates between two shifts instead.
- **What counts as equivalent corruption is a modelling choice.** All
  three sources match signal destroyed per pixel, with slightly different
  arguments (pooling, redundancy, a constant image). A different notion of
  equivalence would give a different map.
- **Video adds duration.** Open-Sora 2.0 scales the shift with T×H×W, and
  LTX-Video with token count. Both extend the argument to time without
  testing it.

## Relation to zero terminal SNR

The fix comes from Lin et al. ([LIT-tmp6c6lg](../literature.d/LIT-tmp6c6lg.md)), and their reason is not
resolution. It is the per-channel mean that leaks through Stable Diffusion's
terminal SNR (`√ᾱ_T = 0.068`) at 512px. Emu Video ([LIT-635](../literature.d/LIT-635.md)) adds the
resolution argument, "the residual signal is higher for high resolution video
frames", for the same fix. It rescales the
schedule so the final step is pure noise, and its controlled comparison at
512px wins 96.8% on quality against the standard schedule. That fixes the
endpoint. This practice moves the whole curve. The two are compatible, and
nobody has compared them.

## Known implementations

- simple diffusion, Chen (2023) with RIN, Stable Diffusion 3
- Stable Video Diffusion, which raises P_mean from −1.2 through 0 to 1.0 as
  resolution rises, LTX-Video, and Open-Sora 2.0 (adoption, per [DP-005](../../docs/design-principles.md#dp-5))
