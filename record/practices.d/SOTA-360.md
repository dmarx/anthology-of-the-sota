---
number: 360
status: Active
formerly:
- SOTA-tmp6lc4c
consensus: universal
consensus_note: >-
  Not doing it is what needs justifying, and the record can now show the
  descendants rather than assert the popularity. `SOTA-359` (CLIP) is this
  recommendation for image-text, `LIT-216` (I-JEPA) and `SOTA-250` are it for
  masked image regions, and the `#304` audit lists SimCLR, MoCo, BYOL, DINO,
  SigLIP and the text-embedding line as further instances the record has yet
  to file. A pretraining objective that reconstructs the observation is now
  the one that argues for itself. Read as of 2026-09.
title: 'Score a density ratio against sampled negatives instead of reconstructing the target'
version: 1
tags:
- representation-and-encoding
- training-optimization
date: '2026-09-23'
source:
- LIT-589
introduced_by:
- LIT-589
implementations: []
explained_by:
- THEORY-085
extended_by:
- SOTA-359
---

# SOTA-360: Score a density ratio against sampled negatives instead of reconstructing the target

## Source

Oord et al. (2018), [LIT-589](../literature.d/LIT-589.md) — [ARXIV-1807.03748](https://arxiv.org/abs/1807.03748).

## The claim

When you want a representation rather than a reconstruction, do not train a
model to produce the target. Train a **score** that says how much more likely
the true target is than a sampled one, and optimise it by making the true
target win a classification against `N−1` negatives.

Concretely: learn `f(x, c) ∝ p(x|c) / p(x)`, which need not be normalised —
a bilinear form on two encoder outputs is enough — and minimise the
categorical cross-entropy of identifying the positive among `N` candidates.

## Why, in the paper's own terms

The reason is a budget argument and it carries a number. A generative loss on
`p(x|c)` has to account for every detail of the observation, while the thing
you want is small: *"images may contain thousands of bits of information
while the high-level latent variables such as the class label contain much
less (10 bits for 1,024 categories)"*. Reconstruction spends model capacity
in proportion to the data's entropy; the density ratio spends it in
proportion to what the context and the target share.

That is why the recommendation transfers across modalities with the mechanism
unchanged. The same objective, with a deliberately plain encoder, gives a
**48.7%** ImageNet linear probe (+9 absolute over the best prior pretext
task), **64.6%** LibriSpeech phone classification against 39.7 for MFCCs,
skip-thought-level sentence representations without a word-level decoder, and
an improvement on 4 of 5 DeepMind Lab tasks as an auxiliary loss.

## What the negatives are for, and what they are not for

This is the part most often inverted, so state it twice:

- **The estimator's optimum does not depend on `N`.** The paper proves the
  optimal `f` is the density ratio regardless of how many negatives you drew.
- **The mutual-information bound does depend on `N`, and is capped by it.**
  `I ≥ log N − L`, which tightens with `N` and can never certify more than
  `log N` — [THEORY-085](../theory.d/THEORY-085.md).

So "more negatives is better" is a claim about the *certificate*, not about
the *objective*, and it saturates. Scaling the batch because a paper said
negatives help is a reason to check which of the two sentences you are acting
on.

## Conditions

- **You need a proposal distribution you can sample from, and its quality is
  the method.** Negatives drawn from the wrong distribution make the
  classification easy, and an easy classification teaches nothing. In the
  descendants this is where nearly all the engineering went — the augmentation
  policy, the memory queue, the in-batch pairing.
- **The batch is the negative set in the common implementation**, so batch
  size stops being purely a throughput knob and becomes part of the loss.
- **A density ratio gives you no sample and no likelihood.** If the
  downstream requirement is generation or a calibrated probability, this
  trades away the thing you need.
- **What to predict is still yours to choose.** This paper predicts several
  steps ahead in latent space to force slow features; CLIP pairs an image
  with its caption; I-JEPA pairs a masked region with its context. The
  recommendation constrains the *loss*, not the pretext task.

## Known implementations

-
