---
status: Proposed
promote_when: >-
  The method applied to a transformer — LayerNorm's gain and bias are the
  obvious substitute for BatchNorm's — with stochastic weight averaging as the
  baseline rather than plain SGD, by a group other than the authors. Another
  convolutional result against an SGD baseline is not it: the gain over plain
  SGD is established and the gain over SWA is the open question.
consensus: unreplicated
consensus_note: >-
  One paper, 2020, and nobody in the record has followed it. The surrounding
  family — Polyak averaging, stochastic weight averaging, snapshot ensembles,
  BatchEnsemble — is well established and several of its members appear here
  only as baselines, so the *area* is settled practice while this particular
  method is not.
title: 'Late in training, replicate a small subset of the weights, train the copies against shared base weights, and average the subset back into one model'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-09-21'
source:
- LIT-tmpledv1
introduced_by:
- LIT-tmpledv1
implementations: []
---

# SOTA-tmpw07d8: Late in training, replicate a small subset of the weights, train the copies against shared base weights, and average the subset back into one model

## Source

von Oswald, Kobayashi, Meulemans, Henning, Grewe and Sacramento (2020),
[LIT-tmpledv1](../literature.d/LIT-tmpledv1.md) — read as [NOTE-tmpdgwy1](../notes.d/NOTE-tmpdgwy1.md). CIFAR-10/100,
ImageNet fine-tuning, and an enwik8 LSTM, five seeds throughout.

## The claim

Pick a time `T₀` partway through training. From there, keep one shared set of
**base** weights and `K` copies of a small **late-phase** subset. On each
minibatch, update every copy's late-phase weights and accumulate the base
gradients across copies before taking one base step. At the end, **average the
late-phase copies into a single model** and throw the ensemble away.

Training costs slightly more; inference costs exactly what it did.

**Replicate BatchNorm's scale and shift**, plus the final classification
layer. That is the default, it is the best-performing variant, and it is a few
thousand parameters.

WRN 28-10 on CIFAR-100: 81.35 → **82.87** under SGD, 82.46 → **83.06** under
SWA, over five seeds. ImageNet fine-tuning for 20 epochs: ResNet-50 76.62 →
76.87, ResNet-152 78.37 → 78.77, at standard deviations of 0.01–0.06.

## Three things the source establishes about how to do it

**It has to be late.** Running the same procedure from initialization —
`T₀ = 0` — **fails to reach the base model** on both CIFAR-10 and CIFAR-100.
The copies must stay in one basin for the final average to mean anything, and
perturbing early gives the mode coverage that ordinary ensembles want and this
method cannot use.

**Replicate a small subset, not everything.** A late-phase *full* deep
ensemble — same schedule, all weights replicated — lands between the base
model and the low-dimensional version. Less is more here, and the source
attributes it to data efficiency: a few free parameters per copy can be
trained on the same data a single model needs.

**Do not reach for the general version.** Hypernetwork weight embeddings, the
most expressive variant, score 81.55 on CIFAR-100 against BatchNorm's 82.87 —
and under SWA they reach 82.01 against a base of **82.46**, which is worse
than not doing it.

## Conditions

**Compare against SWA, not against plain SGD, and expect the answer to depend
on the problem.** Stochastic weight averaging is simpler and already strong.
On CIFAR the two stack — late-phase adds 0.33 and 0.60 points on top of SWA.
On the enwik8 LSTM they mostly overlap: 1.626 BPC for base-plus-SWA against
1.615 for late-phase-plus-SWA, a gap of 0.011 where the no-SWA gap was 0.062.
Try SWA first.

**On the LSTM, half the gain is not the ensemble at all.** Adding the rank-1
multiplicative parameters with no replication and no averaging moves 1.695 →
1.663; late-phase takes it to 1.633. Part of what is being measured is a
parameterization change.

**A deep ensemble is still better, at `K` times the cost** — 96.91 against
96.81 on CIFAR-10, 84.09 against 83.06 on CIFAR-100. The source uses deep
ensembles as an upper baseline and says they are not directly comparable.

**BatchNorm is assumed by the variant that works.** On an architecture without
it you are choosing between the rank-1 and hypernetwork variants, and the
hypernetwork one is the one that failed.

**Vision, one small LSTM, and 2020.** WRN, PyramidNet, ResNet and DenseNet on
CIFAR and ImageNet; a 1.56M-parameter LSTM sized deliberately so it does not
overfit, trained with no regularization at all. Nothing at transformer scale,
and no follow-up in this record.

**`T₀` is tuned once and reused.** Set on CIFAR-100 and held fixed across the
CIFAR experiments. Given that `T₀ = 0` fails outright, the choice matters and
the source offers no rule for making it.

## What this opens rather than settles

The record holds nothing else on weight-space ensembling — no Polyak
averaging, no stochastic weight averaging, no snapshot ensembles, no model
soups — and several of those appear here only as baselines. This practice is
the entry point to that family, not a summary of it, and SWA in particular is
a stronger and simpler thing that the record should hold and does not.
