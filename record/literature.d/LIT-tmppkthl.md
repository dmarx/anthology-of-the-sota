---
status: Active
title: 'Understanding the Disharmony between Dropout and Batch Normalization by Variance Shift'
version: 1
tags:
- model-stability
date: '2026-09-18'
published: '2018-01-01'
arxiv: '1801.05134'
first_author: 'Li'
keywords:
- 'dropout'
- 'batch-normalization'
- 'variance-shift'
- 'regularization'
- 'train-test-mismatch'
implementations: []
summary: >-
  Li et al. (2018), [ARXIV-1801.05134](https://arxiv.org/abs/1801.05134), CVPR 2019. Answers why stacking
  dropout and batch normalization usually hurts. Dropout changes a unit's
  variance between train and test; batch normalization carries statistics
  accumulated over training and does not follow. The mismatch — "variance
  shift" — makes inference numerically unstable. Verified on PreResNet,
  ResNeXt, DenseNet and Wide ResNet over CIFAR10/100, with two fixes: put
  dropout after every BN layer, or use a dropout variant less sensitive to
  variance. Also explains why a small rate and a wide layer both help.
---

# LIT-tmppkthl: Understanding the Disharmony between Dropout and Batch Normalization by Variance Shift

Li et al. (2018) — [ARXIV-1801.05134](https://arxiv.org/abs/1801.05134), CVPR 2019

## Key takeaways

- **The question is one practitioners had answered empirically and nobody had
  explained.** Dropout and batch normalization are each strong regularizers
  and combining them usually *lowers* accuracy. This paper gives the
  mechanism.

- **The mechanism is a train/test mismatch that batch norm cannot see.**
  Dropout shifts the variance of a unit when the network moves from training
  to inference — that is inherent to the method, which is why the weight
  scaling at test time exists at all. Batch normalization, meanwhile, uses
  variance statistics **accumulated across the whole of training** and applies
  them unchanged at test time. The two disagree, the disagreement compounds
  through the network, and inference becomes numerically unstable.

- **The direction matters: dropout *before* BN is the harmful order.** That is
  the arrangement in which BN inherits a variance that dropout has already
  perturbed.

- **Verified across four modern architectures** — PreResNet, ResNeXt,
  DenseNet, Wide ResNet — on CIFAR10 and CIFAR100, by measuring the ratio
  between the moving variance BN stores and the real variance at inference,
  layer by layer, at drop rates 0.0 through 0.7.

- **Two fixes, both tested.** Apply dropout **after all BN layers**; or modify
  dropout to a form less sensitive to variance — Gaussian and uniform variants
  in place of Bernoulli. Most of the variants worked and some improved on the
  baseline.

- **Two conditions that fall out of the same analysis and explain the field's
  folklore.** A **small drop rate** (0.1) keeps the shift curves close to the
  no-dropout baseline, and performance with it. And a **wide layer** tolerates
  more: Wide ResNet, with a much larger channel dimension `d`, stays close to
  baseline even at rates of 0.3 and 0.5, and beats it — because the larger `d`
  keeps the variance from exploding while dropout's benefit survives.

## Standing in the anthology

**This is the answer to a question [SOTA-240](../practices.d/SOTA-240.md)
raises and cannot settle.** That practice records that dropout's benefit
depends on whether a model can memorize what it is shown, and notes that the
record has not established why modern recipes turn dropout off. For
convolutional architectures specifically, this is a large part of the answer,
and it is not about the data regime at all: dropout stopped being used in
convnets because batch normalization arrived and the two interact badly.

It is also the only paper in the record whose subject is an **interaction
between two practices** rather than a practice. That shape is one the `SOTA`
scheme can express and had no instance of.
