---
status: Active
title: 'Scaling Laws for Precision'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2024-11-01'
arxiv: '2411.04330'
first_author: 'Kumar'
keywords:
- 'quantization'
- 'scaling-laws'
- 'low-precision'
- 'effective-parameters'
- 'post-training-quantization'
summary: >-
  Kumar et al. (2024), [ARXIV-2411.04330](https://arxiv.org/abs/2411.04330). Training in low precision
  reduces a model's effective parameter count, and post-training quantization
  degrades *more* the longer a model was trained — so past some point extra
  pretraining data is actively harmful.
---

# LIT-tmpyeabk: Scaling Laws for Precision

Kumar et al. (2024) — [ARXIV-2411.04330](https://arxiv.org/abs/2411.04330)

## Key takeaways

- Standard scaling laws are silent about numerical precision, which is
  strange given that precision decides both training cost and serving cost.
  This fits precision-aware laws for both.
- The training-side idea: **low precision reduces the model's effective
  parameter count**, which makes the extra loss from training in low
  precision predictable rather than empirical, and lets the law price parts
  of a model held at different precisions.
- The inference-side result is the counter-intuitive one: degradation from
  post-training quantization **increases with how much data the model was
  trained on**, to the point where additional pretraining data becomes
  actively harmful if the model will be quantized afterwards. More training
  makes a model less robust to being compressed.
- Both are unified into a single functional form covering pre- and
  post-training quantization, fit on over 465 pretraining runs and validated
  up to 1.7B parameters and 26B tokens.
- A practical suggestion falls out: training *larger* models in *lower*
  precision may be compute-optimal.

## Standing in the anthology

Filed because two models the record holds ship precision decisions this
paper's framework is about, and neither note explains why they are choices
rather than implementation details: [LIT-139](LIT-139.md)'s DeepSeek-V4 does FP4
quantization-aware training on the expert weights and the indexer's
query-key path, and Kimi K3 releases in MXFP4.

The inference result is the one a reader should carry: if a model is going to
be quantized for serving, the pretraining budget and the quantization plan
are not independent decisions, and the usual instinct — train on more data,
it can only help — is wrong past a point this paper can locate. Its own
limit is scale; the fits stop at 1.7B and 26B tokens, far below everything
that ships FP4 today.
