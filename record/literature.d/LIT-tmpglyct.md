---
status: Active
title: 'SVDQuant: Absorbing Outliers by Low-Rank Components for 4-Bit Diffusion Models'
version: 1
tags:
- numerics-and-precision
- inference-optimization
- systems-optimization
date: '2026-09-21'
published: '2024-11-07'
arxiv: '2411.05007'
first_author: 'Li'
keywords:
- 'post-training quantization'
- 'low-rank decomposition'
- 'outliers'
- 'diffusion models'
- 'kernel fusion'
implementations: []
summary: >-
  Li et al. (2024), [ARXIV-2411.05007](https://arxiv.org/abs/2411.05007) — 4-bit weights **and**
  activations for diffusion transformers. Shift outliers from activations into
  the weights by smoothing, peel the dominant singular values into a 16-bit
  rank-32 branch, quantize only the residual. Two propositions bound the
  output error by the *magnitudes* rather than only the rounding errors, which
  is why shrinking the residual works. Naïvely the extra branch costs **57%**
  latency; fused, the system reaches **3.0×** over a W4A16 baseline and
  **3.5×** memory reduction on 12B FLUX.1. Read as [NOTE-tmpujtdw](../notes.d/NOTE-tmpujtdw.md).
---

<!-- inactive-ok-file: THEORY-tmpo44nu — Proposed, filed in this same
     contribution. Named as the second document this paper contributes; a
     Standing section saying what a source yields is not leaning on it. -->

# LIT-tmpglyct: SVDQuant: Absorbing Outliers by Low-Rank Components for 4-Bit Diffusion Models

Li, Lin, Zhang, Cai, Li, Guo, Xie, Meng, Zhu and Han (2024) —
[ARXIV-2411.05007](https://arxiv.org/abs/2411.05007), read as [NOTE-tmpujtdw](../notes.d/NOTE-tmpujtdw.md).

## Standing

**Held for a mechanism the record's quantization cluster does not have.**
[SOTA-185](../practices.d/SOTA-185.md) compensates rounding error into columns not yet quantized;
[SOTA-163](../practices.d/SOTA-163.md) shrinks the scale's blast radius with block scaling;
[SOTA-230](../practices.d/SOTA-230.md) keeps adapters in 16 bits beside a 4-bit base. None of them
*removes* the outliers before quantizing, and none applies a low-rank
correction to the weight matrix itself.

**Its contribution to the record is two documents.** [SOTA-tmp0iki2](../practices.d/SOTA-tmp0iki2.md) takes
the recommendation; [THEORY-tmpo44nu](../theory.d/THEORY-tmpo44nu.md) takes the spectral argument
underneath it, which is proved rather than measured and is the part that
travels.

**The systems half is not optional and the paper says so.** A rank-32 branch
run naïvely adds **57%** latency from 16-bit reads and writes around the
projections. The claim only survives with the fusion, which is why the
practice states both halves as one instruction.
