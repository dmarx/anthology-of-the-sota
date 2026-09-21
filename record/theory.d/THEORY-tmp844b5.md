---
status: Proposed
promote_when: >-
  The separation reproduced by a group that is not proposing a remedy for it:
  calibration and refinement plotted against epoch, from a training run set up
  for some other purpose, showing the two minima at different places. The
  cheapest version is a single figure on any model with a validation set.
  What would NOT meet it: another early-stopping criterion that improves test
  loss. That is evidence about the remedy, and the remedy already has its own
  document.
title: 'Calibration error and refinement error have separate minimizers during training, so the loss minimum is optimal for neither'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-21'
source:
- LIT-tmpanahl
explains:
- SOTA-tmpony2u
summary: >-
  Berta et al. (2025), [LIT-tmpanahl](../literature.d/LIT-tmpanahl.md) — a proper loss is exactly
  calibration error plus refinement error, so minimizing it minimizes a sum
  whose two terms bottom out at different epochs. The proposed mechanism: as
  the training set becomes separable the model must grow confident to keep
  *training* calibration error small, and across a generalization gap that
  confidence does not transfer — while refinement is still improving.
---


# THEORY-tmp844b5: Calibration error and refinement error have separate minimizers during training, so the loss minimum is optimal for neither

## Source

Berta, Holzmüller, Jordan and Bach (2025), [LIT-tmpanahl](../literature.d/LIT-tmpanahl.md) — read as
[NOTE-tmp1et69](../notes.d/NOTE-tmp1et69.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-tmpony2u](../practices.d/SOTA-tmpony2u.md) | stop and tune on validation loss after temperature scaling, then calibrate | the raw validation loss is a sum of two terms with different minima, so its own minimum is a compromise point nobody chose and neither term is at its best there |

## The account

A proper loss decomposes — this part is classical, not new — into

    risk = calibration error + refinement error

where calibration error measures systematic over- or under-confidence and
refinement error measures how well the predictions separate the classes.
Minimizing the risk therefore minimizes a **sum**, and a sum is minimized
where the terms trade off, not where either is smallest.

The empirical claim is that they genuinely do trade off during training rather
than descending together. Plot both against epoch and the two minima sit at
different places, so the validation-loss minimizer carries non-zero
calibration error *and* is past or short of the best refinement.

**The proposed mechanism is about what fitting demands.** As the training set
becomes well separated, the model has to make very confident predictions to
keep *training* calibration error small — confidence is what a correct,
well-calibrated prediction on a separable training set looks like. Across a
train-test generalization gap that confidence does not transfer, so the model
is over-confident on held-out data while its refinement may still be
improving. The two objectives then pull in different directions for the rest
of training.

This also explains an observation the field already had and treated as a
standalone fact: that modern networks are poorly calibrated after training.
On this account that is not a defect of the architecture but the expected
endpoint of minimizing a sum in which one term is still being traded away.

**It is not an artifact of deep networks.** The paper analyses the same
phenomenon for high-dimensional logistic regression and finds the separation
there too, which is what makes it an account of proper-loss minimization
rather than of neural network training.

## Why `Proposed`

**One group, and the group proposing the remedy.** The separation is the
premise of their method, which does not make it wrong and does mean the record
has no measurement of it from anyone with no stake. That is what the
`promote_when` asks for, and it is close to free to supply.

**The mechanism is a "possible scenario" in the source's own words**, offered
as one explanation of the separation rather than as the demonstrated cause.
The logistic-regression analysis shows separation can arise in a simple
setting; it is not a demonstration that the separability-plus-generalization-
gap story is what drives it in a ResNet.

**The size of the separation is not invariant.** The paper states that the
learning-rate schedule and regularization strength change how calibration
error behaves over training, and with it how much the method buys. So the
existence of two minimizers is the claim; the distance between them is a
property of the recipe, and nothing here predicts it.

## What it does not say

**It does not say the loss decomposition is new.** The split is due to
Bröcker; what is new is the variational formulation that makes the terms cheap
to estimate, and the observation about their minimizers.

**It does not say refinement is the thing you care about.** Which term matters
depends on what the probabilities are for. A decision rule that thresholds at
one point cares about calibration near that point; a ranking cares about
refinement. The practice recommends separating them precisely so a reader can
choose, not because one dominates.

**It does not generalize to improper metrics.** The decomposition is a
property of proper losses. Early stopping on accuracy is a different object
and the source measures it separately, finding it often yields poor logloss
even after calibration.
