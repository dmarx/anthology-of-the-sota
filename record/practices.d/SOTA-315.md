---
number: 315
status: Active
formerly:
- SOTA-tmpony2u
consensus: unreplicated
consensus_note: >-
  One group, and an unusually broad study for one: 196 tabular datasets across
  three model families with 30 hyperparameter configurations each, plus a
  vision benchmark run ten times per dataset. Breadth is not independence, and
  the group proposing the criterion is the group measuring it. Nobody else has
  reported the separation or the remedy, and the field's default is still to
  stop on raw validation loss.
title: 'Early-stop and tune on validation loss after temperature scaling, then calibrate post hoc, instead of stopping on raw validation loss'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-21'
source:
- LIT-514
introduced_by:
- LIT-514
implementations: []
summary: >-
  Berta et al. (2025), [LIT-514](../literature.d/LIT-514.md) — a proper loss is calibration
  error plus refinement error, and the two bottom out at different epochs, so
  the validation-loss minimum is optimal for neither. Fit a temperature on the
  validation set each time you would have read the loss, read the loss after
  it, and stop there; then keep the temperature. Measured across **196**
  classification datasets and a vision benchmark with ten runs per dataset.
explained_by:
- THEORY-060
---

<!-- inactive-ok-file: THEORY-060 — Proposed, filed in this same
     contribution. This practice declares `explained_by:` on it, so the
     citation is the relation itself; the practice stands without the account
     and the account is the weaker of the two, which is why their statuses
     differ. -->

# SOTA-315: Early-stop and tune on validation loss after temperature scaling, then calibrate post hoc, instead of stopping on raw validation loss

## Source

Berta, Holzmüller, Jordan and Bach (2025), [LIT-514](../literature.d/LIT-514.md) — read as
[NOTE-259](../notes.d/NOTE-259.md). The account of why is [THEORY-060](../theory.d/THEORY-060.md).

## When this applies

You train a classifier iteratively, you pick an epoch or a hyperparameter
configuration by validation loss, and the probabilities it outputs are used
for something — a threshold, a ranking, a downstream expected-value
calculation, an abstention rule. It applies to gradient-boosted trees as much
as to networks: anything with an iteration count to stop.

## Do this

**Fit a temperature on the validation set, then read the loss.** Temperature
scaling rescales the logits by a single scalar. It does not change the
ordering of predictions and therefore does not change accuracy or refinement;
it changes only confidence. So the validation loss measured *after* fitting it
is an estimate of the refinement term alone, with the calibration term removed
rather than traded against.

**Stop and tune on that number.** Select the epoch, and the hyperparameter
configuration, by post-temperature-scaling validation loss. This is the whole
change, and it is a change to a line in a training loop.

**Then keep the temperature.** The selected model is deliberately one that has
not been penalised for being over-confident, so it will be. Calibrating it
afterwards is the second half of the instruction, not an optional extra.

**Use a fast temperature fit, because you are now doing it every epoch.**
The source gives one: the loss is convex in the inverse temperature, so its
derivative is increasing, and bisection on the derivative is both faster and
better than the line searches in common use. Measured against implementations
from Guo et al., TorchUncertainty and AutoGluon, it reaches lower test loss in
less time. Released as `probmetrics`.

**If fitting a temperature every epoch is too much, stop on Brier score
instead.** The source's own suggestion: Brier is also a proper loss and is
less sensitive than log-loss to sharp swings in calibration error, so it is a
usable proxy for practitioners who want the effect without the fit.

## What it buys

On the vision benchmark, in order, each step improving on the last: stopping
on validation loss; then applying temperature scaling to that model; then
stopping on TS-refinement instead. Stopping on validation **accuracy** — the
other obvious refinement proxy — is less consistent than TS-refinement.

On tabular data with at least 10K samples, temperature scaling helps on most
datasets and so does stopping on TS-refinement, while stopping on accuracy
often gives poor log-loss even after calibration. Stopping on TS-refinement
also frequently gives **better accuracy and AUC** than stopping on log-loss,
which is the part a reader who does not care about probabilities should
notice.

## Why `Active` on one group

Because the reason is close to arithmetic and the instruction is nearly free.
The decomposition is an identity, not a finding; what the paper adds is that
the two terms do not co-minimize, measured across 196 datasets and three model
families and separately in vision with ten runs per dataset. Against that, the
cost is one scalar fit per validation pass and a line changed in a loop.

The `consensus` is `unreplicated` because breadth is not independence: the
group that proposes the criterion is the group that measured it.

## Conditions

**It does less on small or easy datasets.** The source says so: results are
"more noisy and unclear" there, and the headline tabular figure is restricted
to datasets with at least 10K samples. A small validation set also makes the
temperature fit itself noisy, which cuts the same way.

**The size of the effect depends on the recipe.** The learning-rate schedule
and regularization strength change how calibration error moves during
training, and therefore how far apart the two minima are. This practice
predicts the direction, not the magnitude.

**It assumes temperature scaling is the right calibrator.** The estimate of
refinement is only as good as the calibration family removed from the loss.
Where a single temperature cannot fix the miscalibration — strong class
imbalance, distribution shift between validation and test — the number being
stopped on is not the refinement error.

**Do not read this as "calibration does not matter".** The practice separates
the two terms so each can be handled with the tool that suits it; it does not
rank them. Which one matters is a property of what the probabilities are for.

**Not the same as stopping on accuracy.** Accuracy is the intuitive
refinement proxy and the source measures it as a baseline: it is less
consistent on vision and often gives poor log-loss even after calibration on
tabular data.

## Known implementations

- `probmetrics` (github.com/dholzmueller/probmetrics) — the estimator and the
  bisection temperature fit, usable with any architecture.
- `RefineThenCalibrate-Vision` (github.com/eugeneberta/RefineThenCalibrate-Vision)
  — the vision benchmark.
