---
status: Proposed
promote_when: >-
  The audit run by somebody other than the authors, catching a
  badly-generalizing model that was *not* produced adversarially — an
  ordinarily overfit checkpoint, or a model whose training data nobody
  controlled — with a false-positive rate against clean models reported. A
  repeat on a poisoned/clean pair is not it: that is the demonstration this
  practice already rests on.
consensus: unreplicated
consensus_note: >-
  One paper, two authors, one poisoned/clean pair. The estimator improves on
  prior work (Huang et al.) and agrees with it on direction; nobody outside
  has run it, and its accuracy against a known ground truth has not been
  established by anyone including its authors.
title: 'To find a model that generalizes badly where its outputs look fine, measure how much of parameter space behaves the way it does'
version: 1
tags:
- analysis-and-evaluation
- model-stability
date: '2026-09-21'
source:
- LIT-tmpk8scf
introduced_by:
- LIT-tmpk8scf
implementations: []
explained_by:
- THEORY-tmp8wi2a
---

<!-- inactive-ok-file: THEORY-tmp8wi2a — Proposed, and the account this practice
     declares as its explanation. Both rest on one source whose estimator the
     source itself does not claim to have validated -->

# SOTA-tmpczmhy: To find a model that generalizes badly where its outputs look fine, measure how much of parameter space behaves the way it does

## Source

Scherlis and Belrose (2025), [LIT-tmpk8scf](../literature.d/LIT-tmpk8scf.md) — read as
[NOTE-tmpw2aa7](../notes.d/NOTE-tmpw2aa7.md). A 4810-parameter MLP, a 3.4M-parameter ConvNeXt on
CIFAR-10, and Pythia 31M.

## The problem it addresses

A model can have low training loss, behave indistinguishably from a good model
on the data you have, and still generalize badly — because something was
wrong with what it was trained on, or because it overfit in a way your
evaluation set does not reach. Behavioural testing on that data cannot see it,
by construction.

## The claim

Estimate the **local volume** of the trained weights: the measure, under the
model's own initialization distribution, of the region of parameter space
whose behaviour stays within a small KL budget of the model's, on held-out
inputs. `−log` of that number is a description length
([THEORY-tmp8wi2a](../theory.d/THEORY-tmp8wi2a.md)), and the badly-generalizing model has the
shorter region and the longer description.

The demonstration is the point. A ConvNeXt trained with an added term making
it fail on a held-out poison set — while keeping training loss low — has a
**measurably smaller** local volume than its clean twin, and this is detected
**on clean held-out data**, where the two models behave alike, in a small
number of forward passes. The poison set is not needed and neither are labels.

## How

Sample directions from the anchor, binary-search the radius at which KL
crosses the cutoff, and aggregate into a log-volume estimate by importance
sampling. Precondition with **Adam's second moment**, or K-FAC, or HesScale —
all three work and work similarly, and the second moment is already sitting in
your optimizer state.

Do **not** reach for the full Hessian of the KL. The Fisher matrix is the
theoretically natural choice and it performs no better than no preconditioning
at all. The authors report this as surprising and cannot explain it, which is
itself worth knowing before you spend time on it.

## Conditions

**Measure a converged model, not a run in progress.** This is the sharpest
practical caveat and it comes from the source's own figure: the poisoned
ConvNeXt has the *larger* local volume for most of training, crossing below
the clean model only around 30,000 steps — where validation and poison losses
diverge. A reading taken mid-training would have pointed the wrong way.

**The evidence is one adversarially-produced pair.** Poisoning induces bad
generalization on purpose. Whether ordinary overfitting shrinks volume the
same way is not shown, and the crossing above is a reason not to assume it.

**The estimator's accuracy is unknown**, and the source says so: "it is still
unclear how close our estimates are to the ground truth". The aggregate sits
close to the largest individual sample, so treat it as a lower bound of
unestablished tightness. Comparisons between two models measured the same way
are on firmer ground than any single number.

**Know the two numerical failure modes.** At high KL cutoffs the Adam
preconditioner starts returning *smaller* estimates than no preconditioning —
raise its damping hyperparameter. At very low cutoffs the radius-finding
binary search can fail in floating point and the volume appears to collapse;
the source confirmed one such collapse was an artefact, not a finding.

**Scale.** 4810 parameters, 3.4M, and 31M for the language model. Nothing here
runs at the sizes this record's practices are mostly argued at, and the cost
of the estimator at those sizes is not reported.

## What this is not for

It is not a replacement for a validation set — it is for the case where the
validation set cannot see the problem. And it is not evidence about optimizer
choice: the source offers an argument that adaptive optimizers generalize
worse because they undo the architecture's volume bias, and measures nothing
about it. [SOTA-001](SOTA-001.md) is untouched.
