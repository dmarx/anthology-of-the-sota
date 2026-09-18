---
status: Active
consensus: converged
consensus_note: >-
  One group produced the explanation and the measurements; the *behaviour* is
  near-universal and predates the explanation. Modern convolutional
  architectures do not stack dropout before batch normalization, and the
  ordering in every reference implementation reflects it. What this record has
  assessed is that the field's arrangement matches what LIT-tmppkthl derives,
  not that the field arrived at it by reading this paper — which is exactly
  the case the `converged` blurb admits, adopters who did not choose
  deliberately.
title: 'Do not place dropout before a batch-normalization layer'
version: 1
tags:
- model-stability
date: '2026-09-18'
source:
- LIT-tmppkthl
introduced_by:
- LIT-tmppkthl
implementations: []
summary: >-
  Li et al. (2018), [LIT-tmppkthl](../literature.d/LIT-tmppkthl.md) — dropout changes a unit's variance between
  train and test; batch normalization applies statistics accumulated over
  training and does not follow, so the combination runs inference on a
  variance neither layer agrees about. Put dropout after every BN layer
  instead. If it has to go before one, the same analysis says what makes it
  survivable: a small rate, or a wide layer — Wide ResNet beats its baseline at
  0.3 and 0.5 where narrower networks do not.
explained_by:
- THEORY-tmpr6ead
---

# SOTA-tmpjjsir: Do not place dropout before a batch-normalization layer

## Source

Li et al. (2018), [LIT-tmppkthl](../literature.d/LIT-tmppkthl.md) —
[ARXIV-1801.05134](https://arxiv.org/abs/1801.05134), CVPR 2019.

The mechanism is [THEORY-tmpr6ead](../theory.d/THEORY-tmpr6ead.md), and it is
worth having because it makes this a rule with conditions rather than a
superstition: dropout necessarily shifts a unit's variance between train and
test, batch normalization applies frozen training-time statistics, and in that
order BN rescales by a number estimated under the wrong regime.

## What to do instead

**Put dropout after all the BN layers.** That is the paper's first fix and the
one requiring no change to dropout itself. BN then never inherits a variance
that dropout has perturbed.

**Or make dropout less variance-sensitive.** Gaussian and uniform variants in
place of Bernoulli were tested and most worked, some improving on the
baseline.

## If it has to go before one, two things make it survivable

Both fall out of the same analysis, which is why they are here rather than in
a tuning guide:

- **A small rate.** At 0.1 the variance-shift curves sit near the no-dropout
  baseline, and so does the accuracy.
- **A wide layer.** Wide ResNet tolerates 0.3 and even 0.5 while staying near
  baseline, and beats it — a larger channel dimension keeps the variance from
  exploding while dropout's regularization survives. Narrower architectures at
  the same rates do not.

## What this does not claim

**Batch normalization specifically.** The mechanism needs a layer that stores
training-time statistics and reuses them at inference. Layer normalization and
RMSNorm compute theirs from the current activations at both train and test, so
there is nothing to go stale — and that is what the transformers this registry
mostly advises on use. **This practice does not transfer to them**, and nobody
in this line tested whether some analogous effect exists.

**Convolutional, and CIFAR.** PreResNet, ResNeXt, DenseNet and Wide ResNet on
CIFAR10/100. The derivation is general; the evidence is not.

**It is not the reason large language models set dropout to zero.** That is
[SOTA-240](SOTA-240.md)'s open question and this does not answer it. What this
answers is why dropout left *convolutional* architectures, which happened for
an architectural reason rather than a data-regime one — a distinction worth
keeping, because the two stories are easy to merge and only one of them is
evidenced.

## Known implementations

- The ordering is near-universal in modern convolutional code; the record has
  not traced specific ones to this paper.
