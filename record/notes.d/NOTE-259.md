---
number: 259
status: Read
formerly:
- NOTE-tmp1et69
paper: LIT-514
title: 'Refine, then calibrate: the validation-loss minimum is a compromise nobody chose'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist and filed because the record had no calibration
  document at all. A proper loss is calibration error plus refinement error;
  the two bottom out at different epochs, so stopping on validation loss lands
  between them. Fit a temperature before reading the loss and the compromise
  goes away. 196 tabular datasets, three model families, ten runs per vision
  dataset.
---

<!-- inactive-ok-file: THEORY-060 ADR-031 SOTA-102 — all three named
     rather than relied on. THEORY-060 is Proposed and filed in this same
     contribution as the account under this unit's practice, and this document
     says in as many words that it is the weaker of the two. ADR-031 is cited
     as the decision that splits practice from theory, which is what this unit
     is applying. SOTA-102 is Superseded and named ONLY as a false positive —
     the nearest thing a search for "calibration" returns, and about data
     mixing rather than probabilities, which is the point being made. -->

# NOTE-259: Refine, then calibrate: the validation-loss minimum is a compromise nobody chose

## Contribution

A proper loss decomposes, classically, into **calibration error** —
systematic over- or under-confidence — and **refinement error**, how well the
predictions separate the classes. The paper contributes a variational form of
that decomposition that makes both terms cheap to estimate, the observation
that they are not minimized at the same epoch, and the consequence: select the
epoch by validation loss *after* temperature scaling, then keep the
temperature.

## Key results

**The two minima are apart, and it is visible in one figure.** Calibration and
refinement plotted against epoch for a ResNet-18 on CIFAR-10 bottom out in
different places, so the validation-loss minimizer carries non-zero
calibration error and is not at the best refinement either.

**Why temperature scaling is the right instrument for the estimate.** It
rescales logits by a single scalar, so it cannot change the ordering of
predictions — accuracy and refinement are untouched and only confidence moves.
The validation loss after fitting it is therefore an estimate of refinement
alone. One parameter also means it barely overfits the validation set.

**The ordering of the four procedures**, on the vision benchmark, each better
than the last: stop on validation loss; apply temperature scaling to that
model; stop on TS-refinement instead; and — the comparison that matters —
stopping on validation **accuracy**, the other obvious refinement proxy, is
less consistent than TS-refinement.

**Scale.** 196 binary and multi-class tabular datasets from Ye et al.'s
benchmark, 1K–100K samples, on XGBoost, an MLP and RealMLP, with 60/20/20
splits and **30 random hyperparameter configurations** per split — about 40
hours of 32-core CPU and four RTX 3090s. Separately, CIFAR-scale vision with
ResNet-18 and a WRN, 300 epochs, **ten runs per dataset**, about 300 V100
hours. Both benchmarks' code is public.

**A side contribution that is a practice in itself.** Fitting a temperature
every epoch needs a fast fit. The loss is convex in the inverse temperature,
so its derivative is increasing and bisection finds the zero; the result is
both faster and lower-test-loss than the implementations in Guo et al.,
TorchUncertainty and AutoGluon. Released as `probmetrics`.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Calibration and refinement are not minimized at the same epoch | **strong** | measured across model families and datasets; analysed for high-dimensional logistic regression |
| C2 | Post-TS validation loss estimates refinement | strong | TS cannot change ordering, so it cannot change refinement; unbiasedness shown under stated assumptions on the logit distribution |
| C3 | Stopping on TS-refinement improves test loss | strong within this study | 196 datasets ×3 families; vision with ten runs |
| C4 | It also improves accuracy and AUC | moderate | "frequently", on tabular ≥10K |

## Limitations

**One group, and the group with the thesis.** The separation in C1 is the
premise of the method, and no independent party has plotted it. Breadth is not
independence — 196 datasets from one lab is one measurement.

**It thins out on small and easy datasets.** Said plainly in the source:
results there are "more noisy and unclear", and the headline tabular figure is
restricted to datasets with ≥10K samples. A small validation set also makes
the temperature fit noisy, which pushes the same way.

**The effect size is recipe-dependent and the paper says so.** Learning-rate
schedule and regularization strength change how calibration error moves during
training and therefore how far apart the minima are. The direction is the
claim; the magnitude is not.

**The refinement estimate inherits temperature scaling's limits.** It is the
loss with *one family* of calibrators removed. Where a single scalar cannot
fix the miscalibration — strong class imbalance, validation/test shift — the
quantity being stopped on is not refinement.

**Tabular and vision, not language.** No sequence models, no generative
models, and the decomposition is defined for classification.

## Bearing on the record

**It opens a subject the corpus did not have.** Grepping the practices for
calibration returns quantization scales, data-mixing temperature
([SOTA-102](../practices.d/SOTA-102.md), `Superseded`), and incidental uses of "confidence". Eighty
practices touch training and none asked whether the probabilities mean
anything. That absence is the reason this was worth a full unit rather than a
note.

**Two documents, on [ADR-031](../decisions.d/ADR-031.md)'s split.** [SOTA-315](../practices.d/SOTA-315.md) is the
instruction — stop on post-TS validation loss, then calibrate.
[THEORY-060](../theory.d/THEORY-060.md) is the claim underneath it, that the two terms have
separate minimizers, filed `Proposed` because the only measurement of it comes
from the party proposing the remedy.

**It is evidence for a practice this record already holds, from a new
direction.** [SOTA-196](../practices.d/SOTA-196.md) says report zero-shot and in-distribution
performance separately because one hyperparameter can move them in opposite
directions. This is the same shape one level down: two components of a single
loss, moved in opposite directions by one knob, and averaged into a number
that hides it. Two instances, different mechanisms, counted and not
generalized — [DP-009](../../docs/design-principles.md#dp-9).

## Open questions

- **Does the separation appear in language-model training?** The
  decomposition needs a classification loss, and next-token prediction is
  one. Whether calibration and refinement of the token distribution separate
  over pretraining is unasked here and would be a large finding either way.
- **Is temperature scaling enough on a shifted validation set?** The whole
  estimate rests on it, and the conditions under which one scalar suffices are
  assumed rather than tested.
- **What happens under a cosine schedule?** The source names the
  learning-rate schedule as something that changes the effect, and the
  schedules this record recommends elsewhere — [SOTA-140](../practices.d/SOTA-140.md)'s
  warmup-stable-decay among them — are not the step schedule it used.
