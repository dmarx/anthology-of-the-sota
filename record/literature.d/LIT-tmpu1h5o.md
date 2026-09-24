---
status: Active
title: 'simple diffusion: End-to-end diffusion for high resolution images'
version: 1
tags:
- generative-modeling
- signal-structure
- model-architecture
date: '2026-09-24'
published: '2023-01-01'
arxiv: '2301.11093'
first_author: 'Hoogeboom'
keywords:
- 'shifted-noise-schedule'
- 'reference-resolution'
- 'log-snr-shift'
- 'multiscale-loss'
- 'u-vit'
- 'pixel-space-diffusion'
implementations:
- 'simple diffusion'
summary: >-
  Hoogeboom, Heek and Salimans, Google Brain (2023), [ARXIV-2301.11093](https://arxiv.org/abs/2301.11093).
  Trains single-stage pixel-space diffusion up to 512x512 with four
  changes. The first is to define the noise schedule at a reference
  resolution and shift its log-SNR by 2·log(ref/d) at resolution d. Table 2
  is the controlled measurement. On ImageNet 256 the unshifted cosine
  schedule gives FID 7.65 train / 6.87 eval, and the schedule shifted to 32
  gives 3.76 / 3.71. This is the origin, with the concurrent Chen (2023),
  of the resolution-dependent schedule shift SD3 later derives again.
---

# LIT-tmpu1h5o: simple diffusion: End-to-end diffusion for high resolution images

Hoogeboom, Heek and Salimans, Google Research, Brain Team (January 2023;
ICML 2023) — [ARXIV-2301.11093](https://arxiv.org/abs/2301.11093). Read at v2: the main text, Tables 2–9 and
Appendix C.

## Key takeaways

- **The argument (§3.1).** Average-pooling a d×d noised image by s×s
  halves the per-pixel noise at each halving step: the SNR at d/s is s²
  times the SNR at d. So a schedule designed at 32 or 64, like the cosine
  schedule, adds too little noise at high resolution. Global structure is
  fixed early, "a small time window to decide on the global structure".
- **The fix.** Choose a reference resolution. Define the schedule there,
  and multiply the SNR by (ref/d)², which is a log-SNR shift of
  2·log(ref/d) (eq. 5).
- **The measurement (Table 2, §5.1).** Same setup, and only the reference
  resolution varies:

  | resolution | schedule | FID train | FID eval |
  |---|---|---|---|
  | 128 | cosine, unshifted | 2.96 | 3.38 |
  | 128 | shifted to 64 | 2.41 | 3.03 |
  | 128 | shifted to 32 | 2.26 | 2.88 |
  | 256 | cosine, unshifted | 7.65 | 6.87 |
  | 256 | shifted to 128 | 5.05 | 4.74 |
  | 256 | shifted to 64 | 3.94 | 3.89 |
  | 256 | shifted to 32 | 3.76 | 3.71 |

  The gain grows with resolution, which is the direction the argument
  predicts. The authors recommend shifting to 64 because it "performed
  slightly better in early iterations".
- **Interpolated schedules for guidance.** A shifted schedule "can only
  tolerate little guidance" (Table 9). For text-to-image they interpolate
  in log-space between shift 32 and shift 256 (eq. 6).
- **The other three findings.** Scale the U-Net only at 16×16. Add dropout,
  but not at the highest-resolution maps. Downsample at the input. A
  multiscale loss helps at 512 (FID 4.85 → 4.30 train) and slightly hurts
  at 256 (Table 6).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The reference resolution is tuned, not derived.** The argument gives a
  shift for any reference. Which reference is best is found empirically
  (32 or 64), and the two differ by 0.18 FID at 256, one run each.
- **Single runs throughout.** The 7.65 → 3.76 gap is far outside
  [SOTA-307](../practices.d/SOTA-307.md)'s roughly 2% run-to-run floor. The 3.94 against 3.76 comparison
  is not.
- **Pixel space, trained from scratch at each resolution.** The schedule is
  set before training, not carried from a low-resolution stage. The
  mechanism is the same one [SOTA-263](../practices.d/SOTA-263.md) describes for finetuning, but the
  measurement is not on the pretrain-then-finetune path.

## Standing in the anthology

This is where the resolution-dependent schedule shift comes from, together
with Chen (2023), [LIT-tmpnbpgd](LIT-tmpnbpgd.md), which it names as "concurrent and
complementary". SD3 ([LIT-449](LIT-449.md)) derives the shift again from a
constant-image argument and states that it implies "a log-SNR shift ...
similar to (Hoogeboom et al., 2023)". [SOTA-263](../practices.d/SOTA-263.md) named SD3 as its origin and
said no ablation existed. Table 2 here is that ablation, published 14
months earlier.
