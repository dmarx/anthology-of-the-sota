---
number: 398
status: Proposed
formerly:
- SOTA-tmpao7ji
consensus: unreplicated
consensus_note: >-
  One group, one paper, a large compute-matched sweep. The package clearly
  wins, but its parts are not separated. Throughput, which the paper
  credits with most of the gain, is not what the practice's name promises.
  Sora and SD3 train on native aspect ratios. Per DP-005 that is adoption,
  and neither reports a controlled comparison.
title: 'Pretrain a vision transformer on packed, aspect-preserved images at sampled resolutions, not on fixed square crops'
version: 1
tags:
- vision-and-graphics
- training-optimization
- representation-and-encoding
date: '2026-09-24'
promote_when: >-
  An independent compute-matched comparison reproduces the package's gain.
  Or a controlled run isolates aspect ratio in pretraining: square resize
  against aspect-preserved resize, at the same area, resolution
  distribution and images seen. A generative model counts if its metric is
  quantitative. Another report that adopts native aspect ratios does not
  count, and neither does a qualitative square-crop comparison like Sora's.
source:
- LIT-657
introduced_by:
- LIT-657
implementations:
- 'NaViT'
summary: >-
  Dehghani et al. (2023), [LIT-657](../literature.d/LIT-657.md). Do not resize or crop images to one
  square resolution. Keep each image's aspect ratio and sample its
  resolution per example, favouring small side lengths. Pack the patches
  into fixed-length sequences with per-example attention masks. At matched
  compute this beats square fixed-resolution ViT pretraining, and matches
  the best ViT with 4x less compute. Most of the gain is throughput.
---
<!-- inactive-ok-file: SOTA-251, SOTA-152 — Proposed neighbours this practice is set against; named to place it, not to rest on them -->


# SOTA-398: Pretrain a vision transformer on packed, aspect-preserved images at sampled resolutions, not on fixed square crops

## Source

Dehghani, Mustafa et al. (2023), [LIT-657](../literature.d/LIT-657.md) — [ARXIV-2307.06304](https://arxiv.org/abs/2307.06304).

## The recipe

- **Keep aspect ratio.** Resize each image to a target area without
  squashing or cropping it square.
- **Sample the area per image.** NaViT samples side length r ~ U(64, 256)
  and resizes to r² pixels (App. A.1). Sampling side length beats sampling
  area, and a distribution biased toward small sizes does best (Fig. 7).
- **Pack.** Put several images' patches into one fixed-length sequence.
  Mask attention and pooling per example, and mask padded examples out of
  the loss. Greedy packing leaves under 2% padding.
- **Use factorized x/y position embeddings.** They extrapolate to unseen
  resolutions better than learned 1D or 2D tables (Fig. 10).

## What the evidence supports, part by part

| Part | Evidence | Isolated? |
|---|---|---|
| The whole package | Leads ViT at each of 12 compute-matched budgets. Matches the best ViT with 4x less compute (Fig. 1) | No: aspect ratio, resolution, token dropping and images seen all change together |
| Variable resolution | U(64, R_max) matches or beats fixed R_max at equal FLOPs, with aspect ratio preserved in both (Fig. 5) | Yes |
| Aspect ratio | Native beats square resize at equal area in a linear fairness probe, p = 0.02 (Fig. 12 right) | Only at probe time, not in pretraining |
| Throughput | About 5x more images seen at the same compute (Table 2) | The paper names this "the chief contributor" |

So the recommendation holds as a package. Its title names aspect ratio
because that is what the package lets you keep, but aspect ratio is not
shown to be what makes it win.

## Conditions

- **ViT encoders trained for classification or contrastive learning.**
  JFT-4B and WebLI, B/32 to L/16, one lab. No generative model is
  measured. Sora ([LIT-652](../literature.d/LIT-652.md)) and SDXL ([LIT-566](../literature.d/LIT-566.md), crop conditioning) argue for
  the generative case with example images only.
- **Evaluation has to match.** Much of the out-of-distribution gain
  appears when the square baseline is evaluated by square resize (Table
  5). With an aspect-preserving crop, ObjectNet is roughly tied.
- **Packing costs attention.** The overhead from attending over longer
  packed sequences shrinks as the model gets wider (Fig. 4). Per-example
  masks also require an attention kernel that supports them.
- **Example-level losses need care.** Pooled, contrastive losses must
  handle a variable number of examples per sequence. NaViT uses a chunked
  contrastive loss for this (§2.3).

## Relation to the record

This is an alternative to [SOTA-251](SOTA-251.md), which holds resolution low and raises
it only in the decay phase. NaViT mixes resolutions throughout training.
It argues that a staged increase cannot be reversed, while a mixed-trained
model can be run at any resolution afterwards. The record holds no
comparison of the two.

[SOTA-152](SOTA-152.md) recommends best-fit document packing for language models. This
practice applies the same idea to images, with per-example masks that
[SOTA-152](SOTA-152.md)'s setting does not need in the same form.
