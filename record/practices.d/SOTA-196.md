---
number: 196
status: Active
formerly:
- SOTA-tmpkh4j4
consensus: emerging
consensus_note: >-
  One clean measurement of the conflict, in a setting where both metrics
  mattered. The practice is uncontroversial once stated and is not stated often.
title: 'Report zero-shot and in-distribution performance separately; one hyperparameter can move them in opposite directions'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-10'
source:
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

## Conditions

One measurement, in vision, in 2022. The generalisation — that this happens
whenever a hyperparameter trades preservation against fitting — is the shape of
the argument rather than something `LIT-072` establishes.

The practical form is weaker and safe: **when a model is expected to do
something it was not fine-tuned for, measure that separately and report it
beside the in-distribution number.**

## Known implementations

- `LIT-072`'s Table 3 is the sweep
