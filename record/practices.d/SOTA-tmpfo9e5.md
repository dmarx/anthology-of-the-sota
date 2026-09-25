---
status: Proposed
promote_when: >-
  A group other than the authors trains a CLIP-style model with and without
  image-patch masking on the same data and reports the pair at matched
  wall-clock or accelerator budget, with the masked arm's saving spent on batch
  or samples. A report that ships masked contrastive pretraining without the
  unmasked arm does not settle it, and neither does a same-epoch comparison —
  at equal epochs this paper's own ViT-B/16 result is a loss.
title: 'Drop half the image patches when training a CLIP-style model, spend the saving on more pairs and a larger batch, and unmask only for a short final tune'
version: 1
tags:
- multimodal-learning
- training-optimization
- systems-optimization
- vision-and-graphics
date: '2026-09-25'
source:
- LIT-tmparvj2
introduced_by:
- LIT-tmparvj2
extends:
- SOTA-359
- SOTA-372
implementations:
- 'facebookresearch/flip'
summary: >-
  Li et al. (2022), [LIT-tmparvj2](../literature.d/LIT-tmparvj2.md) — FLIP. Remove 50% of image patches and run
  the ViT on the rest, with CLIP's loss and nothing else. The saving buys a 2×
  larger batch at the same memory and 2× the samples per hour; ViT-L/16 on
  LAION-400M reaches its unmasked reproduction's accuracy more than 3× faster.
  The accuracy comes from what the saving buys: at equal batch, masking is
  parity.
---

# SOTA-tmpfo9e5: Drop half the image patches when training a CLIP-style model, spend the saving on more pairs and a larger batch, and unmask only for a short final tune

## Source

Li, Fan, Hu, Feichtenhofer and He (2022), [LIT-tmparvj2](../literature.d/LIT-tmparvj2.md) — [ARXIV-2212.00794](https://arxiv.org/abs/2212.00794);
read as [NOTE-tmpr24hg](../notes.d/NOTE-tmpr24hg.md).

## What to do

In contrastive image-text pretraining ([SOTA-359](SOTA-359.md)) with a ViT image encoder:

- **Randomly remove 50% of each image's patches** and run the encoder on the
  visible ones only — MAE's encoder design ([SOTA-372](SOTA-372.md)) without MAE's decoder or
  loss. 75% also works and is faster, at some accuracy.
- **Spend the saving.** Double the batch at the same memory, or train on
  more samples in the same time. This is not optional; it is where the gain
  comes from.
- **Do not add a reconstruction loss.** It bought nothing (−0.2 to −0.3).
- **Do not mask the text.** The text encoder is a few percent of the compute;
  masking it costs accuracy and saves almost nothing.
- **Evaluate on the whole image** with no adaptation — that already works —
  and, for the last point or so, **tune briefly with masking off** (a third of
  an epoch: +0.5 at 50%, +1.3 at 75%).

## Where the accuracy actually comes from

The abstract says masking "improves both accuracy and speed". Table 1 of the
same paper says which of those is masking's doing. ViT-L/16, LAION-400M,
6.4 epochs, zero-shot ImageNet:

| mask | batch | time | acc. |
|---|---|---|--:|
| 0% | 16k | 1.00× | 68.6 |
| 50% | **16k** | — | 68.5 |
| 50% | 32k | 0.50× | 69.6 |
| 50% | 64k | — | 70.4 |

At equal batch, masking is parity; the gain appears when the memory it frees
becomes batch. That is [SOTA-359](SOTA-359.md)'s own condition — in contrastive learning the
batch is the negative set — measured. So read this practice as *the cheapest
way to afford the batch*, and expect it to matter less where batch is not the
constraint.

## Conditions

- **The wall-clock claim is the strong one.** Fewer tokens through the image
  encoder is arithmetic; >3× faster to the reproduction's accuracy at ViT-L/16
  is measured. The accuracy claim at equal epochs is weaker: +1.5 to +1.9 at
  ViT-L, and **−0.2 at ViT-B/16** (68.0 vs 68.2).
- **The image encoder has to dominate the cost.** It does for ViT-L with a
  CLIP-sized text tower. With a cheaper image encoder or an expensive data
  pipeline the saving shrinks.
- **A ViT, or anything that can drop tokens.** A convolutional encoder does
  not get cheaper when half the image is blanked.
- **All evidence is on LAION.** The paper's own comparison against WIT-trained
  CLIP shows the data dominates several benchmarks — ImageNet-A by 20 points —
  and masking does not touch that gap.
- **Robustness gains are real within LAION and unexplained.** The authors
  hypothesize masking acts as a regularizer; nothing tests it.
- **Unknown under a sigmoid loss.** [SOTA-376](SOTA-376.md) removes the memory ceiling from
  the loss side and is least batch-sensitive above 16k; if FLIP's gain is the
  batch, it should shrink there. Nobody in this record has run the pair.

## Known implementations

- `facebookresearch/flip`, the reference implementation.
