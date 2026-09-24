---
status: Active
title: 'On the Importance of Noise Scheduling for Diffusion Models'
version: 1
tags:
- generative-modeling
- signal-structure
date: '2026-09-24'
published: '2023-01-01'
arxiv: '2301.10972'
first_author: 'Chen'
keywords:
- 'noise-schedule'
- 'input-scaling'
- 'resolution-dependent-schedule'
- 'pixel-space-diffusion'
- 'rin'
summary: >-
  Chen, Google Brain (2023), [ARXIV-2301.10972](https://arxiv.org/abs/2301.10972). Higher-resolution images are
  less corrupted by the same per-pixel noise, so the best schedule moves
  with resolution. It sweeps schedule functions (Table 3) and an input
  scaling factor b, with x_t = sqrt(γ)·b·x0 + sqrt(1−γ)·ε (Table 4), on
  ImageNet 64, 128 and 256 with RIN. The best b falls as resolution rises.
  At 256 with a 1−t schedule, b = 1 gives FID 7.21 and b = 0.4 gives 3.52.
  This is concurrent with simple diffusion and is the second origin of the
  resolution-dependent shift.
---

# LIT-tmpnbpgd: On the Importance of Noise Scheduling for Diffusion Models

Ting Chen, Google Research, Brain Team (January 2023) — [ARXIV-2301.10972](https://arxiv.org/abs/2301.10972).
Read at v4 in full.

## Key takeaways

- **The observation (§1, Fig. 2).** At the same noise level, "higher
  resolution natural images tend to exhibit higher degree of redundancy in
  (nearby) pixels, therefore less information is destroyed". An optimal
  schedule at low resolution "may lead to under training of certain noise
  levels" at high resolution.
- **Two knobs.** Strategy 1 changes the schedule function: cosine, sigmoid
  and linear, each with its own parameters. Strategy 2 scales the input by
  b, which shifts log-SNR by 2·log b uniformly in t (§2.2, Fig. 5). This is
  the same shift simple diffusion derives from pooling.
- **Schedule functions (Table 3).** No function is best at every
  resolution. The best at 64 is 2.03 (a sigmoid), at 128 3.91 (a different
  sigmoid) and at 256 4.28 (a third). "It is difficult to find the optimal
  schedule".
- **Input scaling (Table 4).** The best b falls with resolution:
  - With 1−t: about 1.0 at 64 (FID 2.04), 0.6 at 128 (3.50) and 0.4 at
    256 (3.52, against 7.21 at b = 1).
  - With cosine(0.2, 1, 1) at 256: 12.3 at b = 1 and 3.7 at b = 0.3.
  - Tuning b beats the best schedule function alone (4.28 → 3.52 at 256).
- **Headline.** The compound strategy with RIN reaches single-stage
  pixel-space generation up to 1024×1024 (Table 5).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **Table 4 is not monotone.** At 256 with cosine, b = 0.7 gives 7.93 and
  b = 0.8 gives 4.52. With 1−t at 128, b = 0.4 gives 6.89 and b = 0.3 gives
  5.25. These are single runs, and the swings between neighbouring values
  are as large as some of the gains. The trend across resolutions is clear.
  Individual optima are not.
- **Reduced settings.** The paper uses "smaller models as well as shorter
  overall training steps (except for >256 resolutions) to conserve
  compute" (§3.1). Hyperparameters are not "thoroughly" tuned for high
  resolutions (§3.4).
- **Pixel space only, with one architecture (RIN).**

## Standing in the anthology

This is a concurrent origin of the resolution-dependent shift, with simple
diffusion ([LIT-tmpu1h5o](LIT-tmpu1h5o.md)). Each cites the other as concurrent. Its input
scaling is the same log-SNR shift written as a data transform, so the two
papers measure one intervention two ways. Both are in [SOTA-263](../practices.d/SOTA-263.md)'s
`introduced_by`, which previously named SD3.
