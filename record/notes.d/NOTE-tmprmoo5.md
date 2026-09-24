---
status: Skimmed
paper: LIT-tmpbr2sl
title: 'Wan'
version: 1
date: '2026-09-24'
summary: >-
  An open recipe for a 14B text-to-video DiT. Most of its evidence is
  engineering measurement: VAE throughput, parallelism overhead, inference
  speedups. Its three modelling ablations are small, judged mostly by
  training loss, and one of them shows the rejected option doing marginally
  better on FID.
---

# NOTE-tmprmoo5: Wan

**This note is `Skimmed`, not `Read`.** It covers the full core report
(§1–4: data, VAE, DiT, training, systems, inference, ablations), the
image-to-video application (§5.1) and the limitations (§6). It does not cover
the other applications in §5.2–5.7: editing, text-to-image, personalization,
camera control, real-time streaming and audio. It also leaves out the
benchmark tables in §4.6–4.7.1 beyond their headlines. Under [ADR-025](../decisions.d/ADR-025.md) that
is not enough to source a practice from, and this note has no claims table.

## Contribution

A complete, reproducible training stack for a frontier-competitive open video
generator. It covers curation, a causal video VAE, the DiT, the
resolution curriculum, 2D context parallelism and an image-to-video
extension, with weights at 1.3B and 14B.

## Key insight

**At video sequence lengths, the systems constraint shapes the training
recipe.** Attention takes up to 95% of step time at 1M tokens. Memory grows
linearly, so a 14B DiT needs about 8 TB of activations at batch 1. The report
gives both the low-resolution image pre-training and the choice of context
parallelism over tensor parallelism as consequences of that constraint. It
does not give a quality argument for either.

## Key results

- **Wan-VAE**: 4×8×8 compression into 16 channels, 127M parameters, and
  2.5× faster reconstruction than HunyuanVideo's VAE on the same hardware
  (Fig. 7, 720×720, 25 frames, 200 videos). The PSNR figures are shown only
  as a plot.
- **2D context parallelism**: communication overhead at 256K tokens on 16
  GPUs goes from over 10% (Ulysses) to under 1%.
- **Inference**: the diffusion cache gives 1.62×, the FP8 GEMMs 1.13× on
  the DiT, and the 8-bit FlashAttention above 1.27×. Native FA3-FP8 attention
  visibly degraded video. The fix is INT8 for QKᵀ, FP8 for PV, and FP32
  accumulation across blocks, because FP8 WGMMA's 14-bit accumulator
  overflows on long sequences.
- **Shared adaLN** (1.3B, text-to-image, 200k steps, training loss): at a
  matched 1.5B, spending the parameters on depth (35 shared layers) beats
  spending them on per-block adaLN.
- **Text encoder** (Table 6, FID): umT5 43.01, Qwen-VL-7B last layer 43.72,
  second-last layer 42.91.
- **VAE and VAE-D** (Table 5, FID at 10k and 15k steps): 42.60 against
  44.21, then 40.55 against 41.16. The text's "100,000 and 150,000 steps"
  disagrees with the table's labels.
- **Image-to-video human preference** (Table 7): win-rate gaps are
  10.8–81.6% overall. On matching it is −4.2% against CN-TopA.

## Limitations

- **"Scaling laws" appears only in the abstract.** No curve in data or
  model size appears in the sections read.
- **The ablations are small and indirect.** All run on 1.3B text-to-image,
  and none runs on video. Two are judged by training loss, which does not
  compare generation quality across text encoders.
- **The synthetic-contamination claim has no experiment.** The report says
  under 10% generated images "significantly degrade" the model, and does not
  show it.
- **The comparisons can't be reproduced.** Commercial opponents are
  anonymized, and Wan-Bench is the authors' own.
- **The curriculum is not ablated.** Image-first pre-training is justified by
  throughput and gradient-variance spikes. Neither is shown.

## Open questions

- Does image-first, resolution-progressive pre-training help quality, or
  only throughput?
- How much of the image-to-video quality comes from the SigLIP
  first-frame-similarity filter? The report says only that training was
  unstable without it.
