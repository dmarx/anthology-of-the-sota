---
number: 5
status: 'Active'
title: 'Use running statistics for inference'
version: 1
tags:
- inference-optimization
- model-stability
date: '2026-08-24'
source:
- LIT-002
introduced_by:
- LIT-002
summary: >-
  Ioffe et al. (2015), [LIT-002](../literature.d/LIT-002.md) — [ARXIV-1502.03167](https://arxiv.org/abs/1502.03167).
---

# SOTA-005: Use running statistics for inference

## Source

Ioffe et al. (2015), [LIT-002](../literature.d/LIT-002.md) — [ARXIV-1502.03167](https://arxiv.org/abs/1502.03167).

## Two different computations wearing one name

At training time batch normalization standardises using the statistics of the
current batch. At inference there may be no batch — or a batch of one, or a
batch whose composition is arbitrary — so using batch statistics would make a
prediction depend on the other examples it happened to be evaluated with.

The running estimates accumulated during training stand in for the population
statistics instead, which makes inference deterministic and per-example.

Both halves of that are [LIT-002](../literature.d/LIT-002.md)'s, which introduced the practice along with
the method. Ioffe and Szegedy say in §3.1 that mini-batch-dependent
normalisation "is neither necessary nor desirable during inference" because
the output should depend only on the input, and they replace the batch
statistics after training with population statistics: means and an unbiased
variance estimate (the m/(m−1) correction) averaged over training mini-batches,
with moving averages as the way to track them while training (Algorithm 2).
With the statistics fixed, BN at inference is just a linear transform that can
be folded into the learned scale and shift.

## The failure this prevents, and the one it causes

Getting it wrong is not subtle in one direction and very subtle in the other.
Forgetting to switch to evaluation mode gives predictions that change with
batch composition, which shows up as an unreproducible metric.

The subtle direction is that the running estimates are only as good as what
they averaged. A model fine-tuned on data whose distribution differs from
pretraining carries stale statistics unless they are updated, and a model
evaluated on a distribution the running averages never saw is normalising by
the wrong constants — with no error, just worse predictions. This is the
mechanism behind a familiar train/test gap that looks like overfitting and is
not. [LIT-002](../literature.d/LIT-002.md) anticipates the remedy without testing it: its conclusion lists as
future work whether a network could adapt to a new data distribution "perhaps
with just a recomputation of the population means and variances".

It is also the reason this whole family of practices is less relevant to
transformers: LayerNorm has no running statistics, computing over the feature
dimension of a single example, and the train/eval distinction disappears with
them ([SOTA-006](SOTA-006.md)).
