---
number: 2
status: 'Active'
title: 'Common hyperparameters: β₁=0.9, β₂=0.999, ε=1e-8'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2014-12-01'
source:
- LIT-001
summary: >-
  Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).
---

# SOTA-002: Common hyperparameters: β₁=0.9, β₂=0.999, ε=1e-8

## Source

Kingma et al. (2014), [LIT-001](../literature.d/LIT-001.md) — [ARXIV-1412.6980](https://arxiv.org/abs/1412.6980).

## What the three numbers do

β₁ = 0.9 is the decay on the first moment: the update follows an exponential
average of roughly the last ten gradients, which smooths the direction without
lagging far behind it. β₂ = 0.999 is the decay on the second moment, averaging
over roughly the last thousand — deliberately much slower, because the
per-parameter scale it estimates should not swing with a few noisy batches.

ε = 10⁻⁸ is a floor on the denominator, and it is the one whose default is
most often wrong. It sets the largest step a parameter with a tiny gradient
can take, so under mixed precision — where the second moment is small and
noisy — a larger ε (10⁻⁶ is common) is what stops rare parameters taking
enormous steps. That interaction is why [SOTA-015](SOTA-015.md) keeps the moments in FP32.

## Where these stop being right

β₂ = 0.999 is a long memory relative to a short fine-tuning run: a few hundred
steps never fill the average, and the bias correction is doing most of the work
throughout. Lowering it is common in that regime.

At the other end, very large batch training often lowers β₂ as well, because
the gradient is already averaged over many samples and the extra temporal
smoothing mostly adds staleness.

These are defaults from [LIT-001](../literature.d/LIT-001.md)'s experiments on problems much smaller than
what the record otherwise concerns itself with. They have held remarkably
well, which is a fact worth stating, and it is not the same as their having
been re-derived at scale.
