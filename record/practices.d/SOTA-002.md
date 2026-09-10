---
number: 2
status: 'Active'
title: 'Common hyperparameters: β₁=0.9, β₂=0.999, ε=1e-8'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Records that MT-NLG 530B trained with beta_2 = 0.95 and why -- to
    reduce loss spikes, which is a stability argument rather than the
    batch-size one this practice already gave. 0.999 is Adam's default
    and not what large runs use, and the practice now says so.
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

## A published instance, with a different reason

MT-NLG 530B trained with **β₂ = 0.95**, and [LIT-065](../literature.d/LIT-065.md) says why: "we also reduced
β₂ from its standard value of 0.99 to reduce spikes in the training loss."

That is not the batch-size argument above. It is a **stability** argument, about
a parameter whose long-quiet second moment makes the next large gradient's step
enormous. Both may be true and they are different claims;
<!-- inactive-ok-block: SOTA-tmpbqbcf — Proposed, and named as the stability practice this section distinguishes itself from -->
[SOTA-tmpbqbcf](SOTA-tmpbqbcf.md) is the stability one.

The consequence for this practice: **0.999 is Adam's default and not what large
runs use.** The title records the defaults, which is what it is for, and a
reader should not take it as a recommendation at scale.

These are defaults from [LIT-001](../literature.d/LIT-001.md)'s experiments on problems much smaller than
what the record otherwise concerns itself with. They have held remarkably
well, which is a fact worth stating, and it is not the same as their having
been re-derived at scale.
