---
status: Active
title: 'The Platonic Representation Hypothesis'
version: 1
tags:
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-20'
published: '2024-05-01'
arxiv: '2405.07987'
first_author: 'Huh'
keywords:
- 'representational-convergence'
- 'multimodal'
- 'alignment'
- 'scaling'
implementations: []
summary: >-
  Huh et al. (2024), [ARXIV-2405.07987](https://arxiv.org/abs/2405.07987). Representations are converging:
  across architectures, objectives and modalities, and more so as models get
  larger. The conjecture is that they are converging on a statistical model
  of whatever generated the data. The mathematical argument holds only for
  bijective observations, which the authors say plainly and test at the
  boundary.
---

# LIT-tmpglvdv: The Platonic Representation Hypothesis
<!-- inactive-ok-file: THEORY-tmpwwu1v — Proposed, and filed in this same contribution from this note -->

## Key takeaways

- **The observation first, the conjecture second.** Vision and language
  models measure distance between datapoints in increasingly similar ways as
  they get larger — and the similarity spans architectures, training
  objectives, and modality. That part is measured.
- **The conjecture**: there is an endpoint, and it is a representation of the
  joint distribution over events in the world that generate the observations.
  Images and text are two projections of one underlying thing; the models are
  recovering it.
- **Three pressures are offered** for why convergence happens — task
  pressure, data pressure, and the simplicity bias of larger models — each
  argued rather than isolated.
- **Convergence extends to weights**, for models of the same architecture:
  same basin up to permutation, which is why separately trained models can be
  merged at all.
- **The proof is for an idealised world.** The mathematical argument assumes
  *bijective* observation functions, so the information in each projection
  equals the information in the world. Lossy or stochastic observations break
  it, and the authors say so.
- **They test the boundary rather than assert past it.** Varying caption
  density on the same images: denser captions — closer to bijective — align
  better with the visual representation. That is the hypothesis's own
  predicted failure direction, measured.

## Standing in the anthology

**The `representation-and-encoding` topic held fourteen notes and every one
of them was about tokenisation or positional encoding** — subword units,
RoPE, ALiBi, context extension, the inner lexicon. Nothing about what a
representation *is* or what it converges to. This is the first document on
the other half of the topic's own name.

It sources [THEORY-tmpwwu1v](../theory.d/THEORY-tmpwwu1v.md) and one practice. The practice is the part most
likely to be skipped: if there is a modality-agnostic representation, then
**to train the best language model you should also train on images** — and
the paper cites a case where that was measured, not merely predicted.

**What the record still does not hold is the antecedent.** Both this and
[LIT-tmpnglrb](LIT-tmpnglrb.md) build on the Linear Representation Hypothesis — that features
and concepts are directions in embedding space — and the record has no
document for it, nor for steering vectors, nor for concept geometry. That is
a trunk, found the way the trunks keep being found lately: not by a complaint
in the record, but by two arriving papers both standing on something absent.

## What it is careful about, and the record should be too

The counterexamples section is the strongest part of the paper and the
easiest to lose in summary. Different modalities carry different information
— language can state "I believe in the freedom of speech" and an image
cannot — so two models with access to genuinely different information cannot
converge to the same representation. The authors propose the nuanced form
themselves: convergence up to a cap set by the mutual information between the
signals and by each model's capacity.

And convergence is not universal even now: robotics has no standardised
representation of world state, which they attribute to a hardware-driven data
bottleneck rather than to anything about the hypothesis.
