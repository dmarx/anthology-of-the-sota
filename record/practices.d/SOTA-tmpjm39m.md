---
status: Active
consensus: emerging
consensus_note: >-
  Two independent groups measured it on different architectures and datasets
  and got the same shape, and both credit it to a third line of work
  (ViT-VQGAN) the record does not yet hold. It is not `converged` because the
  interior optimum is at a different dimension in each — 8 for LlamaGen, 3 for
  GaussianToken — so the rule is "shrink it and check", not a number anyone
  can carry across models.
title: "Make the codebook's code vectors low-dimensional and the codebook large, and report utilization alongside reconstruction quality"
version: 1
tags:
- representation-and-encoding
- generative-modeling
date: '2026-09-21'
source:
- LIT-tmpflmiq
- LIT-494
introduced_by:
- LIT-tmpflmiq
implementations: []
summary: >-
  Sun et al. (2024), [LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md) — at codebook size 16384,
  dropping the code vector dimension from 256 to 8 takes utilization from
  **0.29% to 97%** and rFID from 9.21 to 2.19. A 256-dimensional codebook uses
  three codes in a thousand. [LIT-494](../literature.d/LIT-494.md) finds the same shape
  independently, on a different architecture and dataset, with the same stated
  mechanism — and in both the curve turns back up, so there is an interior
  optimum to find rather than a direction to follow forever.
---

# SOTA-tmpjm39m: Make the codebook's code vectors low-dimensional and the codebook large, and report utilization alongside reconstruction quality

## Source

Sun, Jiang, Chen, Zhang, Peng, Luo and Yuan (2024),
[LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md); corroborated by Dong et al. (2025),
[LIT-494](../literature.d/LIT-494.md).

## When this applies

You are training a vector-quantized autoencoder — an image tokenizer, an audio
one, any bottleneck that snaps a feature vector to its nearest entry in a
learned codebook. The lineage is [LIT-tmpxz6hg](../literature.d/LIT-tmpxz6hg.md) and
[LIT-tmpb17dj](../literature.d/LIT-tmpb17dj.md); the tunable parts are the codebook's two shapes.

## Do this

**Shrink the code vector dimension into single digits and grow the codebook.**
Nearest-neighbour matching in a high-dimensional space is the problem: in 256
dimensions almost every encoder output has the same nearest neighbour, the
rest of the codebook is never selected, and the effective vocabulary is a
handful of entries whatever `K` says.

| code dim | rFID | utilization |
|---|---|---|
| 256 | 9.21 | **0.29%** |
| 32 | 3.22 | 20.9% |
| **8** | **2.19** | **97.0%** |
| 4 | 9.88 | 82.0% |

*(LlamaGen, codebook size 16384, downsample 16, ImageNet 50k validation.)*

**Measure utilization, not just reconstruction.** It is the mechanism and it
is the diagnostic: a tokenizer that reconstructs acceptably at 20% utilization
is one whose codebook is mostly decoration, and enlarging `K` will not help
it. LlamaGen reports the percentage of codes used across a queue of 65,536
samples; any equivalent will do.

**`ℓ₂`-normalize the code vectors.** Carried from the same source, which in
turn credits ViT-VQGAN. It is reported as part of the same design and is not
separately ablated in either paper here.

**Then find the optimum rather than following the direction.** Both sources
turn back up:

- LlamaGen: dimension 4 scores 9.88 rFID, *worse than 256*, while still using
  82% of the codebook.
- GaussianToken: 16.34 at dimension 2, **12.94 at 3**, 13.89 at 4, 13.86 at 8.

The two optima are at different dimensions on different architectures, which
is why this practice says to sweep rather than naming a number.

**Codebook size is the weaker lever and also non-monotone.** LlamaGen:
4096 → 3.02 (100% used), 8192 → 2.91 (75%), **16384 → 2.19** (97%),
32768 → 2.26 (85%). GaussianToken's sweep moves rFID by 1.6 across a 32× range
of `K` and its utilization falls below 50% at 16,384. Size buys less than
dimension does, and past the point where utilization drops it buys nothing.

## Why `Active`

Because two groups with no overlap measured it on different architectures
(pure VQGAN versus a Gaussian-splatting quantizer), different datasets
(ImageNet versus CIFAR) and different metrics, and reported the same shape and
the same mechanism; and because both credit a third, earlier line for the
design, which is what a practice that has quietly become standard looks like.
The instruction is also cheap to follow and cheap to check.

## Conditions

**Both sources state the monotone half in their captions and leave the
reversal in the table.** LlamaGen's caption reads "Lower vector dimension
(from 256 to 8) improves both", bounded exactly to exclude dimension 4. Its
codebook-size caption is bounded the same way. GaussianToken, to its credit,
describes its own curve as rising then falling. Anyone taking the captions
rather than the tables gets "smaller is better", which is false at the end.

**The optimum is not transferable.** 8 and 3 on two models; nothing here
predicts where it sits on a third.

**The utilization metric is not standardized.** LlamaGen measures over a
65,536-sample queue and deliberately omits the entropy loss that MaskGIT and
the MAGVIT line use in codebook learning. Utilization numbers across papers
that differ on that term are not directly comparable.

**Two sources, and neither is the origin.** Both attribute the design to Yu
et al. (2021), which this record does not hold. The corroboration is real —
independent measurement — but it is two measurements of somebody else's
recommendation rather than two independent discoveries.
