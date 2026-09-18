---
status: Active
title: "Dropout shifts a unit's variance between train and test, and batch normalization's stored statistics do not follow"
version: 1
tags:
- model-stability
date: '2026-09-18'
source:
- LIT-tmppkthl
explains:
- SOTA-tmpjjsir
summary: >-
  Li et al. (2018), [LIT-tmppkthl](../literature.d/LIT-tmppkthl.md) — dropout necessarily changes a unit's
  variance between training and inference, which is why it needs a test-time
  correction at all. Batch normalization applies variance statistics
  accumulated over the whole of training, and those do not move. Stack them in
  that order and inference runs on a variance neither layer agrees about; the
  error compounds with depth. Verified layer by layer on four architectures
  over CIFAR10/100, and the same analysis predicts the two conditions that
  rescue the combination — a small rate and a wide layer.
---

# THEORY-tmpr6ead: Dropout shifts a unit's variance between train and test, and batch normalization's stored statistics do not follow

## Source

Li et al. (2018), [LIT-tmppkthl](../literature.d/LIT-tmppkthl.md) —
[ARXIV-1801.05134](https://arxiv.org/abs/1801.05134), CVPR 2019.

## What was actually shown

**The shift is not a defect of dropout; it is dropout.** Training passes
activations through a randomly thinned network, inference passes them through
the whole one. The variance of a unit differs between those two regimes by
construction — the weight scaling at test time
([THEORY-016](THEORY-016.md)) exists precisely to correct the *mean*. Nothing
corrects the variance, and nothing needs to, as long as the next layer does
not depend on it.

**Batch normalization depends on it, and cannot see the change.** BN
normalizes by variance statistics accumulated across the entire training run
and applies them, frozen, at inference. So the statistic BN uses was estimated
under dropout's training-time variance and is applied to dropout's test-time
variance. The two disagree, BN rescales by the wrong amount, and the resulting
numerical instability compounds through the network into worse predictions.

**Measured rather than argued.** The paper tracks, layer by layer, the ratio
between BN's stored moving variance and the real variance at inference, across
PreResNet, ResNeXt, DenseNet and Wide ResNet on CIFAR10 and CIFAR100, at drop
rates from 0.0 to 0.7. The shift curves separate from the no-dropout baseline
in exactly the way the derivation predicts, and the accuracy drop tracks the
separation.

**The account predicts its own escape routes, which is the strongest thing
here.** Two conditions should reduce the shift, and both do:

- **A small rate.** At 0.1 the shift curves sit near the no-dropout baseline
  and the accuracy does too.
- **A wide layer.** Wide ResNet, with a much larger channel dimension,
  tolerates rates of 0.3 and 0.5 while staying near baseline — and *beats*
  baseline, because the width keeps the variance from exploding while
  dropout's regularization survives.

That second one is the load-bearing prediction. An account that only said
"these two interfere" would not say that widening the layer should rescue the
combination, and it does.

**And the fixes follow from the mechanism rather than from search.** Put
dropout after every BN layer, so BN never inherits a perturbed variance; or
replace Bernoulli dropout with a variant whose variance behaviour is milder.
Most worked, some improved on the baseline.

## What this does not say

**It is about batch normalization specifically, not normalization in general.**
The mechanism requires a layer that *stores* training-time statistics and
reuses them at inference. Layer normalization computes its statistics from the
current activations at both train and test time, so it has nothing to go stale
— and the transformers the practice registry mostly advises on use layer norm
or RMSNorm. Nobody in this line tested that, and extending the result to them
is not licensed here.

**Vision, and CIFAR.** Four convolutional architectures, two small image
datasets. The claim is mechanical enough to travel, and it has not been shown
to.

**It does not explain why large language models set dropout to zero.**
[SOTA-240](../practices.d/SOTA-240.md) leaves that open and it stays open:
this explains why dropout left *convolutional* architectures, which is a
different question with a different answer, and conflating the two would
answer `SOTA-240`'s question with evidence about somebody else's.
