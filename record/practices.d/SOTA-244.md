---
number: 244
status: Proposed
formerly:
- SOTA-tmp8yskz
promote_when: >-
  An early-checkpoint importance score defined and validated for next-token
  prediction — per-token loss, or whatever replaces the error vector — with
  the pruning it licenses reported against training on the full corpus. A
  frontier training report saying it scored its corpus from a short probe run
  rather than a full one would also move it. What would not move it: another
  classification-scale result, or a score that needs a fully trained model,
  which is the cost this is trying not to pay.
title: 'Score example importance a few epochs into training, averaged over several initializations'
version: 1
consensus: unassessed
consensus_note: >-
  Widely cited and, in this record, followed up on by exactly one paper
  (LIT-399, which uses EL2N as one of ten benchmarked metrics). No
  training report here says how it scored its data, or whether it scored it,
  so there is no adoption to read either way.
tags:
- data-pipeline
date: '2026-09-17'
source:
- LIT-397
introduced_by:
- LIT-397
implementations: []
summary: >-
  Paul et al. (2021), [LIT-397](../literature.d/LIT-397.md) — the importance ranking is available from a
  single early checkpoint, not only from a finished run. EL2N at epoch 20,
  averaged over ten initializations, prunes half of CIFAR-10 with accuracy
  slightly up, and the ranking transfers to other architectures.
---

# SOTA-244: Score example importance a few epochs into training, averaged over several initializations

## Source

Paul et al. (2021), [LIT-397](../literature.d/LIT-397.md) — [ARXIV-2107.07075](https://arxiv.org/abs/2107.07075).

## What this replaces

Example-importance scores used to be trajectory statistics: forgetting events
counted over a whole run, area under the margin integrated over training. They
work, and they cost the training run you were pruning in order to avoid. On
ResNet18/CIFAR-10 forgetting scores only stabilise around epoch 75 of 200.

Two scores computed from **local information at a single early checkpoint**
do the same job:

- **GraNd** — the expected loss-gradient norm of an example, which up to a
  constant bounds the change in loss on other examples caused by removing it.
  That bound is what makes it a measure of importance rather than of
  difficulty.
- **EL2N** — the norm of the error vector, the predicted class probabilities
  minus the one-hot label. It approximates GraNd once per-logit gradients are
  roughly orthogonal, which the paper argues holds after a few epochs, and it
  turns out to be the **stronger** pruning signal of the two as well as the
  cheaper.

At epoch 20 this prunes 50% of CIFAR-10 with test accuracy slightly improved,
and 25% of CIFAR-100 for about a point. (The abstract says that second figure
is free; the conclusion says it costs a point. Quote the conclusion.)

## Average over initializations, not over time

This is the half of the recommendation most easily dropped, and the ablation
says it is load-bearing: scores from a **single** network perform materially
worse. The paper's protocol averages over ten independently initialized
networks.

The reason is worth holding onto beyond this method. **The quantity being
estimated is a property of the example, and one training trajectory is one
noisy sample of it.** The earlier literature reduced that noise by integrating
over time within a run, which is expensive and confounds the example with when
the run happened to reach it. Averaging over initializations is the cheaper
estimator of the same thing.

## The ranking is a property of the dataset

EL2N computed on a ResNet18 prunes as well for a ResNet50 as ResNet50's own
scores do, and scores computed incidentally during hyperparameter search are
reusable. So the scoring cost is paid once per corpus rather than once per
model, which is most of the cost argument.

## Conditions

**The score is defined for supervised classification.** "The error vector" is
predicted class probabilities minus a one-hot label. Next-token prediction has
no such object at the example level, and the paper offers no substitute. This
is the binding limitation and the reason for `Proposed`; per-token loss is the
obvious candidate and nothing here tests it.

**Several independent runs must be affordable**, at least for a few epochs.
Cheap at CIFAR scale; not obviously cheap anywhere this record's practices
operate.

<!-- inactive-ok-block: SOTA-243 — Proposed, and cited only to say where the upper-cutoff
     correction was filed. The pointer is right whatever that practice's status becomes. -->
**The highest scorers are the mislabelled ones.** Keeping only the top of the
ranking is not optimal even on clean data, and the exclusion widens with label
corruption. That correction is filed with the practice it corrects,
[SOTA-243](SOTA-243.md).

**Do not extend this to scoring at initialization.** An earlier version of
this paper reported striking results for pruning before any training, and
withdrew them after later work identified a framework bug. The surviving claim
is about early training, and the distinction is exactly the sort that gets
lost in a summary.
