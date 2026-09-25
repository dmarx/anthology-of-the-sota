---
status: Proposed
consensus: converged
consensus_note: >-
  Awkward corner, stated deliberately: `Proposed` + `converged`. SWA is in
  PyTorch's own `torch.optim.swa_utils`, in timm, and appears across this
  record as a baseline other methods improve on — not doing it is not what
  needs justifying, but doing it is unremarkable. What keeps the *status*
  `Proposed` is that all of the evidence this record holds is 2018
  convolutional vision against an SGD baseline, and the record has looked at no
  measurement of it on a transformer. `ADR-015` is the decision that lets these
  two disagree. Read as of 2026-09.
promote_when: >-
  The averaging measured on a transformer trained with a modern optimizer —
  AdamW or a spectral update — against a properly tuned decayed-learning-rate
  baseline rather than against constant-LR SGD. Another convolutional
  replication is not it, and neither is a model report listing SWA among its
  ingredients without an ablation: this record has enough of the latter already
  and they are why the consensus above reads `converged` while this line does
  not.
title: 'Average the weights along the tail of training under a cyclical or high constant learning rate, then re-estimate the normalization statistics'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-09-25'
source:
- LIT-tmpq75ig
introduced_by:
- LIT-tmpq75ig
implementations:
- 'PyTorch (torch.optim.swa_utils)'
- SWA
summary: >-
  Izmailov et al. (2018), [LIT-tmpq75ig](../literature.d/LIT-tmpq75ig.md). Hold the learning rate high — cyclical or
  constant — over the last stretch of training and keep a running average of the
  weights, then ship the average. From pretrained torchvision checkpoints, ten
  further epochs gives ImageNet top-1 **76.15 → 76.97** on ResNet-50 and
  **78.31 → 78.94** on ResNet-152, at one model's inference cost. With batch
  normalization, the running statistics must be recomputed with one pass over
  the data or the averaged model is broken rather than merely worse.
---

# SOTA-tmp9l3pq: Average the weights along the tail of training under a cyclical or high constant learning rate, then re-estimate the normalization statistics

<!-- inactive-ok-file: SOTA-217 — Proposed, and cited to say that this practice avoids the problem that one exists for, because a
     shared trajectory has no permutation to undo. -->

## Source

Izmailov, Podoprikhin, Garipov, Vetrov and Wilson (2018), [LIT-tmpq75ig](../literature.d/LIT-tmpq75ig.md) —
[ARXIV-1803.05407](https://arxiv.org/abs/1803.05407).

## What to do

Three parts, and the third is the one people skip.

1. **Do not decay the learning rate to zero.** Over the stretch of training you
   intend to average, hold it high — either constant or cyclical. The averaging
   is what replaces the decay.
2. **Keep a running average of the weights** over that stretch, and ship the
   average rather than the last iterate. Inference cost is one model.
3. **Recompute the normalization statistics.** A batch-normalized network stores
   running means and variances that belong to the weights that were visited, not
   to their average. One additional pass over the training data with the averaged
   weights fixes it. Omitting this does not cost a fraction of a point; it
   produces a model that does not work.

## What it buys

ImageNet top-1, starting from pretrained torchvision checkpoints and running the
averaging for further epochs under one cyclical schedule shared across
architectures, mean over three runs:

| | baseline | 5 epochs | 10 epochs |
| --- | --- | --- | --- |
| ResNet-50 | 76.15 | 76.83 ± 0.01 | **76.97 ± 0.05** |
| ResNet-152 | 78.31 | 78.82 ± 0.01 | **78.94 ± 0.07** |

Better than **+1.3%** on CIFAR-100 and better than **+0.4%** on CIFAR-10 across
Preactivation ResNet-164, VGG-16 and Wide ResNet-28-10. The paper's framing is
that this "approximates Fast Geometric Ensembling with a single model" — an
ensemble's generalization without an ensemble's inference cost.

## Conditions

**The extra epochs are real compute.** +0.8 on ImageNet for ten epochs of
averaging is a good trade at the end of a long run and a poor one if those
epochs would otherwise have gone into training. The comparison the paper makes
is against a converged SGD baseline, not against spending the same compute
elsewhere.

**Convolutional vision in 2018, against SGD.** Every number here is a
convolutional architecture and the baseline is SGD with a decayed learning rate.
The `promote_when` asks for a transformer and a modern optimizer because that is
what the record does not have, and because a decayed-LR AdamW baseline is a
harder thing to beat than the one measured here.

**`Proposed` while the consensus reads `converged`.** This is the `ADR-015`
corner used deliberately: the technique ships in PyTorch and appears throughout
this record as a baseline, and the record has still never seen it measured in the
setting its readers train in. Adoption is not evidence — `DP-005` — and here the
adoption is real and the evidence is old.

**Related but distinct from interpolating two endpoints.** [SOTA-tmp7f0us](SOTA-tmp7f0us.md)
averages a zero-shot and a fine-tuned model; this averages points along one
trajectory. Both avoid the permutation problem [SOTA-217](SOTA-217.md) exists for, for the same
reason — a shared trajectory — and they are different operations with different
evidence.

**What it is evidence for, and what it is not.** The paper argues the averaged
solution is *flatter* and that this explains the gain. [SOTA-012](SOTA-012.md) is where this
record keeps the flatness correlation and its hedges; nothing in this practice
depends on that account being right.

## Known implementations

- **PyTorch**, as `torch.optim.swa_utils`, including an `update_bn` helper for
  step 3.
- **SWA**, the authors' release.
