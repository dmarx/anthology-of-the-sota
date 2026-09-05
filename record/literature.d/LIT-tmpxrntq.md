---
status: Active
title: 'EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test'
version: 1
tags:
- inference-optimization
date: '2026-09-05'
published: '2025-03-01'
arxiv: '2503.01840'
first_author: 'Li'
keywords:
- 'speculative-decoding'
- 'draft-model'
- 'feature-fusion'
- 'inference-acceleration'
- 'scaling'
implementations:
- EAGLE-3
summary: >-
  Li et al. (2025), [ARXIV-2503.01840](https://arxiv.org/abs/2503.01840). Drop feature prediction for direct
  token prediction and fuse multi-layer features, so the draft model finally
  benefits from more training data: up to 6.5× speedup.
---

# LIT-tmpxrntq: EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test

Li et al. (2025) — [ARXIV-2503.01840](https://arxiv.org/abs/2503.01840)

## Key takeaways

- The observation that motivates it is a negative one, and a good example of
  a scaling law failing usefully: the community's default move is to scale up
  training data, and **EAGLE barely improves when you do**. The draft model
  was not data-limited; it was limited by what it was asked to predict.
- The constraint was feature prediction. EAGLE-3 **abandons predicting the
  target model's features in favour of predicting tokens directly**, and
  replaces reliance on top-layer features with multi-layer feature fusion via
  a technique the authors call *training-time test*.
- With that constraint removed the draft model scales with data as expected.
  Up to **6.5× speedup**, about 1.4× better than EAGLE-2, and a 1.38×
  throughput improvement in SGLang at batch size 64.
- Evaluated on chat and reasoning models across five tasks.

## Standing in the anthology

Filed because three frontier models in the record fine-tune their
multi-token-prediction head into a draft model of exactly this shape:
[LIT-131](LIT-131.md) says so explicitly — the MTP layer mirrors a backbone block, EAGLE-3's
draft is a single decoder layer of matching structure, so the pretrained
head becomes the draft with the target frozen. [LIT-135](LIT-135.md) and [LIT-139](LIT-139.md) ship the
same arrangement.

So the pair [LIT-tmp52sif](LIT-tmp52sif.md) and this note explain a design that had been
appearing in the record fully formed: train n heads for sample efficiency,
then spend them at inference. Neither paper proposes that combination; the
model reports discovered it.
