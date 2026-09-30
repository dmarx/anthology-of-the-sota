---
number: 45
status: Proposed
formerly:
- THEORY-tmp8wi2a
promote_when: >-
  The volume/generalization relation shown on *ordinary* overfitting rather
  than deliberate poisoning — two models differing only in when training
  stopped, or in regularization, with the better-generalizing one measurably
  larger — and an accuracy check on the estimator against a case where the
  true measure is known. A further demonstration on an adversarially induced
  pair is not it.
title: 'How much of parameter space behaves like your trained network is a description length, and the better-generalizing network occupies more of it'
version: 1
tags:
- analysis-and-evaluation
- model-stability
date: '2026-09-21'
source:
- LIT-476
explains:
- SOTA-286
summary: >-
  Scherlis and Belrose (2025), [LIT-476](../literature.d/LIT-476.md) — measure the region
  around a trained network whose behaviour matches it, under the
  initialization distribution rather than Lebesgue. Negative log of that
  measure is, by the bits-back argument, a description length. A ConvNeXt
  trained to generalize badly occupies a smaller region, and local volume
  falls through training as the model's description grows.
---

<!-- inactive-ok-file: SOTA-286 — Proposed, and the practice this account
     explains; naming it in the `explains` table is the relation, not a claim
     that either is settled -->

# THEORY-045: How much of parameter space behaves like your trained network is a description length, and the better-generalizing network occupies more of it

## Source

Scherlis and Belrose (2025), [LIT-476](../literature.d/LIT-476.md) — read as
[NOTE-225](../notes.d/NOTE-225.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-286](../practices.d/SOTA-286.md) | estimate local volume on clean held-out data to catch a model that generalizes badly | reading a description length off the geometry, which is why it works where behavioural testing on the same data does not |

## The account

Take a trained network `w*` and ask which nearby weight vectors *behave* like
it — within a KL budget on held-out inputs, no labels involved. That region
has a measure. Measure it under the distribution the weights were initialized
from, not under Lebesgue, and you have the probability of drawing a
behaviourally-equivalent network at random.

Two choices make this more than a rescaling of flatness.

**The prior rather than Lebesgue.** Some real neighbourhoods have *infinite*
Lebesgue volume — the authors found this empirically — so the classical
quantity is not always defined. The initialization measure is finite by
construction and turns the number into a probability.

**Behaviour rather than loss.** A KL ball around the anchor is zero at the
anchor, needs no ground truth, and is a far stronger constraint than "loss
stays low", which is what makes the region compact enough to estimate. The
paper's image is a Tissot indicatrix: contours of equal functional similarity
in parameter space, whose size says how much the architecture stretches or
compresses the map from parameters to functions.

Then the bits-back argument does the rest. Treat the neighbourhood as an
ensemble, let the receiver hold the initialization distribution as a prior,
and `−log` of the local volume plus the data's code length **is** the
description length of model and data together. A network occupying more of
parameter space is a shorter description of the same data, and MDL says
shorter descriptions generalize.

That is the bridge. Volume is not a proxy for simplicity; under this framing
it is a measurement of it.

Two predictions follow, both made in the source before being tested: a
better-generalizing network should have the larger neighbourhood, and local
volume should fall through training as the network's description grows. Both
hold.

## What was found, including the part that complicates it

A ConvNeXt trained with an added term making it generalize badly while keeping
training loss low has a **smaller** local volume than its clean counterpart —
and this is visible on clean held-out data where the two models behave alike.
Local volume also falls through training, smoothly and roughly exponentially
for Pythia 31M after an early sharp drop.

But the poisoned model is **larger** for most of training, crossing below the
clean model only around 30,000 steps, which is also where validation and
poison losses separate. The reading offered is that early on the poison term
is simply making the network worse everywhere, so it learns less and its
description grows more slowly.

That is plausible and it is post hoc, and it narrows the claim: small volume
is a property of a badly-generalizing *converged* model, not of a
badly-generalizing *run*. A volume reading taken mid-training would have said
the opposite.

## Why `Proposed`

Three reasons, and the source states all of them.

**The estimator's accuracy against ground truth is unknown.** "It is still
unclear how close our estimates are to the ground truth." The aggregate sits
very close to the largest individual sample, which is the signature of a lower
bound whose tightness is unestablished — and one clean run produced a single
outlier sample that nearly reached the preconditioned estimate by itself.

**One adversarial pair carries the generalization result.** Poisoning induces
bad generalization deliberately. Whether ordinary overfitting behaves the same
way is not shown, and the crossing is a reason to doubt that it must.

**The hypothesis is left open by its own authors**: "broadly consistent with
the volume hypothesis", "more research is needed to confirm or refute any
specific version".

## What this does not say

**It does not explain why adaptive optimizers generalize worse**, although the
source proposes that they do because, as approximations of natural gradient
descent, they partly undo the architecture's nonuniform parameter-to-function
map and give up the overrepresentation of simple functions. That is an
argument in §3.3 with **no measurement anywhere in the paper**. It is the most
quotable idea in it, and [SOTA-001](../practices.d/SOTA-001.md) gains nothing from it.

**It does not settle the flatness question**, and it is not a restatement of
it. Volume under a prior and curvature at a point are different quantities,
and the source itself cites the known counterexamples to flat minima
generalizing better. [SOTA-012](../practices.d/SOTA-012.md) stands where it stood.

**It does not reach the scales the record argues at.** 4810 parameters, 3.4M,
and — for the language model — 31M.

**And one of its own components is unexplained.** The Fisher matrix, the
theoretically natural preconditioner for the estimator, performs no better
than none, while axis-aligned approximations of it do much better. The authors
report this as surprising and do not account for it. An estimator with an
unexplained component is a weaker instrument than one without.
