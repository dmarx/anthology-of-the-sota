---
number: 397
status: Proposed
formerly:
- SOTA-tmpjhzoa
promote_when: >-
  A second controlled comparison of reconstruction guidance against
  replacement for conditioning an unconditionally trained diffusion model
  on known frames or pixels, by another group or in another domain, with
  the model and guidance weight fixed. A comparison against a model trained
  with explicit conditioning would also bear on whether this practice is
  still worth using.
consensus: unreplicated
consensus_note: >-
  One controlled comparison, VDM (LIT-627, Table 6). The field has largely
  moved past the setting: current video models train conditioning in
  explicitly, with masked frames concatenated on channels (Wan LIT-619, Emu
  Video LIT-635, SVD LIT-625). So this is a practice for when retraining is
  not an option. Read as of 2026-09.
title: 'To condition an unconditionally trained diffusion model on known frames, use reconstruction guidance, not replacement'
version: 1
tags:
- generative-modeling
- inference-optimization
- vision-and-graphics
date: '2026-09-24'
source:
- LIT-627
introduced_by:
- LIT-627
implementations:
- 'Video Diffusion Models'
summary: >-
  Ho, Salimans et al. (2022), [LIT-627](../literature.d/LIT-627.md). Extending a video autoregressively
  from a model trained without conditioning, reconstruction guidance
  (steering each denoising step toward consistency with the known frames)
  gives FVD 136 against 451 for replacing the known frames' noisy latents
  (Table 6). The model and guidance weight are held fixed.
---

# SOTA-397: To condition an unconditionally trained diffusion model on known frames, use reconstruction guidance, not replacement

## Source

Ho, Salimans et al. (2022), [LIT-627](../literature.d/LIT-627.md) — Video Diffusion Models, §3.1 and Table 6.

## The claim

Given a diffusion model trained unconditionally on 16-frame clips, you can
extend a video by generating the next block conditioned on the frames you
already have. The obvious way is **replacement**: at each denoising step,
overwrite the known frames' part of the sample with a correctly noised copy
of the real frames, and let the model fill in the rest. That lets the known
frames influence the new ones only through the model's joint prediction.
The model is never told the new frames must agree with them.

**Use reconstruction guidance instead.** At each step, add a gradient term
that pushes the model's denoised estimate of the known frames toward the
real ones, and let that gradient flow into the unknown frames. VDM compares
the two with the model and guidance weight fixed, generating 64×64×64 video
by extending 16-frame blocks (Table 6):

| Guidance weight | Method | FVD | FID-avg | IS-avg |
|---|---|---|---|---|
| 2.0 | reconstruction guidance | 136.22 | 13.77 | 10.30 |
| 2.0 | replacement | 451.45 | 25.95 | 7.00 |
| 5.0 | reconstruction guidance | 133.92 | 13.59 | 10.31 |
| 5.0 | replacement | 456.24 | 26.05 | 7.04 |

First-frame FID and IS are the same for both, as they should be, since both
methods generate the first block identically. The difference is entirely in
coherence across blocks. With replacement, "frames from different blocks
throughout the generated videos appear to be uncorrelated samples" (§4.3.3).

## Conditions

- **This is for models you cannot retrain.** Current video models build
  conditioning into training. Wan ([LIT-619](../literature.d/LIT-619.md)) concatenates a masked
  conditioning latent on channels, as do Emu Video and SVD. A model trained
  that way needs neither method. This practice applies when all you have is
  an unconditional model.
- **One comparison, one domain, one model size.** The small text-to-video
  model at 16×64×64. The paper also uses the method for spatial
  super-resolution conditioning, shown qualitatively.
- **It costs a gradient per step.** Reconstruction guidance needs a backward
  pass through the model at every sampling step, which replacement does not.
  The paper does not report the cost.
