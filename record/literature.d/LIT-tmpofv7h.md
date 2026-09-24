---
status: Active
title: 'Patch n'' Pack: NaViT, a Vision Transformer for any Aspect Ratio and Resolution'
version: 1
tags:
- vision-and-graphics
- training-optimization
- representation-and-encoding
- model-architecture
date: '2026-09-24'
published: '2023-07-01'
arxiv: '2307.06304'
first_author: 'Dehghani'
extends:
- LIT-587
keywords:
- 'patch-n-pack'
- 'sequence-packing'
- 'native-aspect-ratio'
- 'variable-resolution-training'
- 'factorized-position-embeddings'
- 'continuous-token-dropping'
implementations:
- 'NaViT'
summary: >-
  Dehghani, Mustafa et al., Google DeepMind (2023), [ARXIV-2307.06304](https://arxiv.org/abs/2307.06304).
  Packs patches from several images into each fixed-length sequence, with
  per-example attention masks and pooling. A ViT can then take any aspect
  ratio and a sampled resolution per image. It leads ViT at each of 12
  compute-matched budgets, and matches the best ViT with 4x less compute.
  The paper attributes the gain chiefly to seeing about 5x more images, not
  to aspect ratio. The one test that isolates aspect ratio is a linear
  probe on fairness attributes.
---
<!-- inactive-ok-file: SOTA-251, SOTA-tmpao7ji — Proposed practices this paper bears on; named as what it informs, not as settled advice -->


# LIT-tmpofv7h: Patch n' Pack: NaViT, a Vision Transformer for any Aspect Ratio and Resolution

Dehghani, Mustafa, Djolonga, Heek et al., Google DeepMind (2023) —
[ARXIV-2307.06304](https://arxiv.org/abs/2307.06304). Read at v1 in full, appendices included.

## Key takeaways

- **The mechanism.** Patches from several images share one sequence.
  Self-attention and pooling are masked so each example sees only itself,
  and padded examples are masked from the loss (§2.1, Fig. 2). Greedy
  packing leaves under 2% padding tokens (§2.3, App. A.3). Position is
  encoded by separate x and y embeddings, summed.
- **What was trained.** ViT pretrains at 224x224 square. NaViT samples a
  side length r ~ U(64, 256) per image and resizes to r² pixels, keeping
  aspect ratio (App. A.1). So "native resolution" means native aspect
  ratio at a sampled area. The authors chose sampling over true native
  size for control over throughput and packing.
- **Compute-matched pretraining.** On JFT-4B, NaViT matches the
  top-performing ViT with 4x less compute (§1, Fig. 1). Each of 12 ViT
  runs (three sizes, four budgets) has a matching NaViT run. At the
  largest L/16 budget, NaViT sees 1.9×10¹⁰ images to ViT's 4.0×10⁹
  (Table 2).
- **Variable against fixed resolution, at equal FLOPs** (§3.2, Fig. 5).
  Both arms keep native aspect ratio. Sampling R ~ U(64, R_max) "matches or
  outperforms" training at R_max alone, even when evaluated at R_max. This
  is the cleanest single-variable result in the paper.
- **How to sample** (Fig. 7). Sampling side length beats sampling area,
  and a truncated normal biased toward low resolution does best (64.3%
  zero-shot ImageNet in the contrastive setup). Both choices raise
  throughput by favouring short sequences.
- **Token dropping.** Per-image drop rates beat a constant rate (Fig. 9a).
  Lowering the drop rate over training beats a fixed one (Fig. 8: 76.5%
  against 75.8%), and raising it hurts (72.2%).
- **Factorized position embeddings extrapolate.** They beat both ViT's 1D
  embeddings and Pix2Struct's learned 2D table, which "struggles to
  generalize to higher resolution" (§3.4, Fig. 10).
- **Downstream.** On LVIS with OWL-ViT, AP goes from 23.3 to 28.3 and
  rare-class AP from 17.2 to 24.3 (Table 1). On ADE20k, NaViT at R384
  beats ViT at R512 (Fig. 13). ImageNet-A improves most, for example 60.4
  to 68.9 at the largest L/16 budget (Table 5).
- **Inference.** Resizing to 256 tokens keeps accuracy within 0.3% of
  native, and 128 tokens costs about 1% (App. C, Fig. 18a). Dropping
  random tokens at inference is much worse than resizing (Fig. 17b).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The headline comparison changes several things at once.** Against
  compute-matched ViT, NaViT differs in aspect ratio, sampled resolution,
  token dropping and the number of images seen. The paper names the last
  as "the chief contributor" (§3.1). Its base architecture also adds
  QK-norm, no biases and attention pooling (§3). The text does not say
  whether the ViT baselines carry the same changes.
- **Aspect ratio is isolated only in a fairness probe.** Fig. 12 (right)
  and Fig. 21 (bottom) resize crops to the same area, as squares or at
  native ratio, and train linear annotators on NaViT features. Native wins
  on FairFace and CelebA attributes (p = 0.02). That test concerns input to
  a frozen probe, not pretraining.
- **The detection and segmentation wins compare two backbones.** In each
  transfer, ViT and NaViT differ in pretraining as well as input format.
  On ADE20k, ViT also gets random square crops while NaViT gets
  aspect-preserving resizes.
- **The out-of-distribution gap depends on preprocessing.** With ViT's
  aspect-preserving centre crop, ObjectNet is roughly tied (57.7 against
  57.9 at the largest L/16 budget). With a plain square resize, the gap is
  39.8 against 48.8 (Table 5). So much of the out-of-distribution gain
  comes from ViT's square resize distorting extreme-aspect images.
- **The Kinetics claim has no NaViT number.** "Competitive performance
  with ViViT-L (80.4%)" in about 6x fewer epochs is stated without
  NaViT's own accuracy (§3.6).
- **Calibration text and table disagree slightly.** The text gives the
  interval (0.045, 0.047). Table 4 has 0.048 at 384 tokens.

## Standing in the anthology

This is the source the record lacked for training on native aspect
ratio. Sora ([LIT-652](LIT-652.md)) cites it as reference 18 and describes the same
design for video, without a measurement. It supports a narrower claim than
"native size beats crops". The package of packing, sampled resolution and
preserved aspect ratio beats square fixed-resolution pretraining at matched
compute, mostly by raising throughput. Variable resolution beats fixed on
its own. Aspect ratio on its own is barely tested. [SOTA-tmpao7ji](../practices.d/SOTA-tmpao7ji.md) records
the practice at that width.

It also offers an alternative to [SOTA-251](../practices.d/SOTA-251.md), which holds resolution low and
raises it only in the decay phase. NaViT mixes resolutions throughout and
names the staged approach's irreversibility as its downside (§4). Neither
paper compares the two.
