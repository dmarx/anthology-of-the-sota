---
status: Active
title: 'MaskGIT: Masked Generative Image Transformer'
version: 1
tags:
- generative-modeling
- representation-and-encoding
- inference-optimization
date: '2026-09-21'
published: '2022-02-08'
arxiv: '2202.04200'
first_author: 'Chang'
keywords:
- 'non-autoregressive-decoding'
- 'masked-prediction'
- 'cosine-mask-schedule'
- 'parallel-decoding'
- 'image-synthesis'
extends:
- LIT-tmpb17dj
implementations: []
summary: >-
  Chang, Zhang, Jiang, Liu and Freeman (2022), [ARXIV-2202.04200](https://arxiv.org/abs/2202.04200). Keeps
  VQGAN's tokenizer and replaces its raster-order autoregressive prior with a
  bidirectional masked transformer decoded in parallel: predict every token,
  keep the most confident, re-predict the rest. **8 steps instead of 256**, up
  to 64× faster, and better — ImageNet `256×256` FID **6.18 vs 15.78**, IS
  **182.1 vs 78.3**. The mask schedule matters and the concave family wins;
  cosine is best in every experiment.
compared_against:
- LIT-494
---

# LIT-tmpig8jj: MaskGIT: Masked Generative Image Transformer

Chang, Zhang, Jiang, Liu and Freeman (2022) —
[ARXIV-2202.04200](https://arxiv.org/abs/2202.04200).

## Key takeaways

- **Raster order was never justified, and dropping it wins on both axes.**
  MaskGIT's own framing is that treating an image as a line-by-line sequence
  is "neither optimal nor efficient". Bidirectional attention plus
  confidence-ranked parallel decoding beats the sequential model on quality
  *and* takes 8 steps instead of 256.
- **The mask schedule is a real hyperparameter with a stated shape
  requirement.** `γ(r)` must be continuous on `[0,1]`, monotonically
  decreasing, with `γ(0) → 1` and `γ(1) → 0`. Concave schedules (cosine,
  square, cubic, exponential) implement less-to-more information flow — few
  confident predictions early, many forced late — and convex ones (square
  root, logarithmic) the reverse. Cosine wins in all their experiments.
- **BERT's fixed 15% is explicitly wrong here** and the paper says why: a
  decoder generating from scratch starts at 100% masked, so a constant ratio
  cannot cover the decoding trajectory.
- **The tokenizer is untouched.** This is a prior-and-decoding paper; every
  number it reports rides on a VQGAN tokenizer. That is why it appears as a
  generation baseline in later tokenizer papers rather than as a tokenizer
  one.

## Standing in the anthology

Filed as the branch of the trunk that changes what you do *with* the tokens,
against [LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md) which changes how many of them there are and
keeps the order. Both are descendants of [LIT-tmpb17dj](../literature.d/LIT-tmpb17dj.md) and they
disagree about the most basic question in the line — whether visual tokens
should be generated left to right — with MaskGIT winning on speed by two
orders of magnitude and LlamaGen later winning on FID while keeping raster
order.

The record holds it at reading depth `Skimmed` equivalent: no `NOTE` is filed,
because this contribution's purpose was the tokenizer trunk and MaskGIT's
tokenizer is somebody else's. Its decoding contribution deserves a reading of
its own and has not had one.
