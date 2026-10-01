---
number: 6
status: 'Active'
title: 'Consider alternatives like LayerNorm for transformers'
version: 1
tags:
- model-stability
date: '2026-08-24'
source:
- LIT-002
introduced_by:
- LIT-002
compared_against:
- SOTA-004
summary: >-
  Ioffe et al. (2015), [LIT-002](../literature.d/LIT-002.md) — [ARXIV-1502.03167](https://arxiv.org/abs/1502.03167).
explained_by:
- THEORY-003
---

# SOTA-006: Consider alternatives like LayerNorm for transformers

## Source

Ioffe et al. (2015), [LIT-002](../literature.d/LIT-002.md) — [ARXIV-1502.03167](https://arxiv.org/abs/1502.03167).

## Why the alternative wins for sequence models

Batch normalization normalises each feature across the batch, which makes an
example's representation depend on the other examples in its batch and
requires running statistics at inference ([SOTA-005](SOTA-005.md)). Both are awkward for
sequence models and one is close to fatal: sequences vary in length, so the
set of examples contributing to a position's statistics varies with the batch's
padding, and at inference with batch size one there is nothing to normalise
across.

Both properties are stated in [LIT-002](../literature.d/LIT-002.md) itself, which is what this practice can
take from it: Ioffe and Szegedy note that BN "does not independently process
the activation in each training example" but depends on "the other examples in
the mini-batch", and they need population statistics to make inference
deterministic. The paper was about convolutional image classifiers; it lists
recurrent networks only as future work, and it does not propose LayerNorm,
which came later.

LayerNorm normalises across the feature dimension of a single example. No
cross-example dependence, no running statistics, no train/eval divergence, and
nothing that changes when the batch does.

The practice this one sets itself against is [SOTA-004](SOTA-004.md), BatchNorm placed after
the linear map and before the activation in convolutional networks. The
comparison is argued rather than measured in the record: no source here trains
the same transformer under both. And the two do not trade like for like. Moving
to LayerNorm does not carry [SOTA-004](SOTA-004.md)'s placement rule along; the placement
question becomes whether normalisation sits inside or outside the residual
branch.

## Where this has gone since

Further than the title says, which is worth recording. RMSNorm drops the
mean-centring and the bias and keeps only the scaling by root-mean-square,
on the finding that the centring contributes little — cheaper, and now the
common choice in large language models.

The placement question also moved: [SOTA-032](SOTA-032.md)'s pre-norm arrangement, rather
than the post-norm original, is what makes deep transformers trainable
without a warmup schedule tuned to depth ([SOTA-100](SOTA-100.md)).

So "consider alternatives like LayerNorm for transformers" understates a
settled outcome. Transformers do not use BatchNorm; the live question in this
area is which normalisation and where, not whether to consider one.
