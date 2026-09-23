---
number: 196
status: Active
formerly:
- SOTA-tmpkh4j4
consensus: emerging
consensus_note: >-
  Two clean measurements of the conflict, in settings where both metrics
  mattered, and the earlier one is the larger. The practice is
  uncontroversial once stated and is still not stated often. Revised
  2026-09-23 when `LIT-588` was filed; the note previously said one
  measurement, which was true of the record and not of the literature.
title: 'Report zero-shot and in-distribution performance separately; one hyperparameter can move them in opposite directions'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Second source added. CLIP had made the same measurement a year earlier
    and larger, and the record did not hold it — the consensus note said
    one measurement and meant one the record had read.
tags:
- analysis-and-evaluation
date: '2026-09-10'
source:
- LIT-072
- LIT-588
introduced_by:
- LIT-072
implementations: []
---

# SOTA-196: Report zero-shot and in-distribution performance separately; one hyperparameter can move them in opposite directions

## Source

Minderer et al. (2022), [LIT-072](../literature.d/LIT-072.md) — OWL-ViT, open-vocabulary detection from a
contrastively pretrained image-text model.

## The claim

Tuning a single hyperparameter can **improve one metric while destroying the
other**, and a paper reporting one number has made a choice it did not disclose.

The instance is exact. Fine-tuning a two-encoder model, the text encoder's
learning rate is swept. `AP_rare^LVIS` measures zero-shot transfer;
`AP^OI` measures in-distribution performance. Using the same learning rate for
both encoders "results in a big drop in `AP_rare^LVIS`" — **and increases
`AP^OI`**. The paper states the conclusion plainly:

> the optimal recipe for zero-shot transfer does not necessarily maximize
> in-distribution performance

One sweep, two measures, opposite gradients.

## Why it is not obvious

The two metrics are usually treated as measuring more and less of the same
thing — a better model should be better at both — so a single headline number
feels like a summary rather than a selection. Here they are in tension because
the hyperparameter controls **how much of the pretrained model is preserved**,
and preservation is what generalisation is made of and what in-distribution
fitting spends.

Any hyperparameter with that character — a fine-tuning rate, a regularisation
weight, a KL-to-reference coefficient — will have the same property. The failure
is silent: nothing in the training loop reports it.

## The same conflict, a year earlier and larger

`LIT-588` measures it on CLIP, and the numbers are bigger. Fitting a
supervised linear classifier on ImageNet features raises ImageNet accuracy by
**9.2%** — which the authors put at "roughly 3 years of improvement in SOTA"
— and produces **no improvement in average accuracy across seven natural
distribution shifts**. It is not a wash made of noise, either: the gain
concentrates on ImageNetV2, the one shift dataset built to follow ImageNet's
own construction, while accuracy *falls* 4.7% on ImageNet-R, 3.8% on
ObjectNet, 2.8% on ImageNet Sketch and 1.9% on ImageNet-A.

CLIP also supplies the continuum `LIT-072` does not. Sweeping 0-, 1-, 2-,
4-… 128-shot and fully supervised classifiers on the same features, effective
robustness decays monotonically as shots are added, and zero-shot CLIP is
more robust than a few-shot model with *equal* ImageNet accuracy. So the
trade is not a property of one hyperparameter's setting — it is a property of
how much distribution-specific supervision the model has seen at all.

The authors state plainly that they do not know why, listing it as an open
question. That is worth preserving: the practice this document states is
about reporting, and it does not need the mechanism.

## Conditions

Two measurements, both in vision, in 2021 and 2022. The generalisation — that this happens
whenever a hyperparameter trades preservation against fitting — is the shape of
the argument rather than something `LIT-072` establishes.

The practical form is weaker and safe: **when a model is expected to do
something it was not fine-tuned for, measure that separately and report it
beside the in-distribution number.**

## Known implementations

- `LIT-072`'s Table 3 is the sweep
