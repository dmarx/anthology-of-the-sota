---
number: 359
status: Active
formerly:
- SOTA-tmph2zob
consensus: converged
consensus_note: >-
  Every image-text foundation model this record has seen since is built this
  way. The `#290` pass read `open_clip`'s pretrained table directly: SigLIP,
  SigLIP 2, DFN, MetaCLIP and Perception Encoder are all contrastive
  image-text models, and the variation between them is the loss's shape or
  the data filter, never a return to predicting the caption's words. The
  objective converged; the efficiency argument behind it is rarely restated.
  Read as of 2026-09.
title: 'Supervise vision from the caption, and match image to caption rather than predicting its words'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    `training-optimization` added and `extends: SOTA-360` declared. The
    tag is true of the document on its own terms — this practice's entire
    justification is a training-efficiency measurement, 3x and 4x in rate of
    transfer per unit compute — and someone browsing that topic would be
    right to expect it. It is written here rather than left implicit because
    the relation is what prompted the re-reading (`ADR-049`).
tags:
- multimodal-learning
- data-pipeline
- vision-and-graphics
- training-optimization
extends:
- SOTA-360
date: '2026-09-23'
source:
- LIT-588
introduced_by:
- LIT-588
implementations: []
extended_by:
- SOTA-tmpgxyyv
---

# SOTA-359: Supervise vision from the caption, and match image to caption rather than predicting its words

## Source

Radford et al. (2021), [LIT-588](../literature.d/LIT-588.md) — [ARXIV-2103.00020](https://arxiv.org/abs/2103.00020).

## The claim

Two decisions, and the second is the one people skip.

**Take the supervision from the text that already accompanies the image.**
A caption is not a label, and that is the point: it needs no annotation
protocol, it scales to whatever the internet has, and it leaves the
representation attached to language, so the label set becomes a runtime
argument rather than an architectural commitment.

**Then do not try to reproduce that text.** Train the image and text
encoders to identify *which* caption goes with which image within the batch —
maximise cosine similarity on the `N` true pairs, minimise it on the `N²−N`
false ones, symmetric cross-entropy, learned temperature. Predicting the
caption's actual words is a far harder task than the supervision requires.

## The efficiency argument, which is the whole justification

The paper reports the ladder rather than asserting the endpoint, and each
rung is measured as the rate of zero-shot transfer to ImageNet:

- A 63M-parameter transformer predicting the caption — already twice the
  compute of its ResNet-50 image encoder — learns **3× slower** than a
  baseline predicting a bag-of-words encoding of the same text.
- Swapping that predictive objective for the contrastive one, from the same
  bag-of-words starting point, gives a **further 4×**.

So the claim is not that contrastive learning produces a better
representation in the abstract. It is that the exact-words target is an
expensive way to buy supervision that the matching target buys cheaply, and
at fixed compute that difference is the result.

## What is deliberately absent

The simplifications matter as much as the objective, because copying the
method without them is copying a different one:

- **A linear projection into the joint space, not a non-linear head.** The
  authors report no efficiency difference and speculate the non-linear head
  is co-adapted with image-only self-supervised methods.
- **A random square crop is the only augmentation.**
- **Nothing is initialised from pre-trained weights** — not the image
  encoder from ImageNet, not the text encoder from a language model.
- **The temperature is learned, and clipped.** Init at the equivalent of
  0.07, logit scale capped at 100, which the paper says was *necessary* to
  prevent training instability. This is the one line most likely to be
  dropped and most likely to be missed when training diverges.

## Conditions

- **It buys supervision cheaply; it does not buy data efficiency.** 400M
  pairs, batch 32,768, 32 epochs — 12.8B images seen. The paper is explicit
  that it compensates for deep learning's data inefficiency rather than
  addressing it.
- **The batch is the negative set, so batch size is not a throughput knob
  here** — it sets the difficulty of the task.
- **What you get out is competitive with a linear probe on ResNet-50
  features**, on average, which the paper notes is well below the state of
  the art. Use it for the flexibility and the robustness ([SOTA-196](SOTA-196.md)), not
  because it is the accurate option.
- **Coverage is the failure mode, not capacity.** CLIP scores 88% on MNIST,
  worse than logistic regression on raw pixels, because near-nothing like
  MNIST is in the pre-training data. "Train on enough that everything is
  in-distribution" is an assumption, and a checkable one.

## Known implementations

- `mlfoundations/open_clip` — the open reproduction, whose pretrained roster
  is entirely models of this form.
