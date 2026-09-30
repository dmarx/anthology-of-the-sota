---
number: 271
status: Proposed
formerly:
- SOTA-tmp121r8
promote_when: >-
  A controlled run reporting what a second modality buys at matched token
  budget — the same language model trained with and without image data, on
  language evaluations — from anybody. Or a stated conversion ratio: how many
  words an image is worth for language pretraining, which is the number that
  turns this from a direction into a recipe. What would not move it: another
  multimodal model outperforming a unimodal one, which confounds the extra
  data with the extra capability and is already common.
consensus: unreplicated
consensus_note: >-
  The vision direction is standard — many vision models are finetuned from
  pretrained language models. The direction this practice is about is the
  other one, and the record has a single cited instance of it being measured.
title: 'Train on a second modality even when the target is single-modality'
version: 1
tags:
- multimodal-learning
- data-pipeline
- representation-and-encoding
date: '2026-09-20'
source:
- LIT-458
introduced_by:
- LIT-458
implementations: []
summary: >-
  Huh et al. (2024), [LIT-458](../literature.d/LIT-458.md) — if representations converge on a
  modality-agnostic model of what generated the data, then data from any
  modality helps find it. The vision direction is already common practice;
  the language direction is not, and the paper cites a case where adding
  image data improved text performance.
explained_by:
- THEORY-036
---

# SOTA-271: Train on a second modality even when the target is single-modality
<!-- inactive-ok-file: THEORY-036 — Proposed, and filed in this same contribution as this practice's account; its Proposed status is why this one is too -->

## Source

Huh et al. (2024), [LIT-458](../literature.d/LIT-458.md) — [ARXIV-2405.07987](https://arxiv.org/abs/2405.07987).

## The asymmetry is the recommendation

One direction is already standard: many vision models are finetuned from
pretrained language models, and nobody finds this strange.

**The other direction is the claim.** If there is a modality-agnostic
representation that both image and text data are projections of, then image
data should help a language model find it — and the paper cites a case where
training on images improved performance on text.

That asymmetry in current practice is itself weak evidence for the
recommendation: the field adopted the direction that was convenient, not the
direction an argument picked out.

## Why it should work, and how much that is worth

[THEORY-036](../theory.d/THEORY-036.md) is the account: representations converge on a model of the
joint distribution that generated the observations, so any projection of that
distribution is evidence about it.

**That account is `Proposed` and its proof holds only for bijective
observations**, which real data are not. So this practice inherits a
conditional: the more informative each modality's observations are of the
shared underlying structure, the more the argument applies. The paper's own
caption-density result is the measurement of that — denser captions align
better — and it is also the reason to expect the benefit to be largest for
rich, descriptive cross-modal data and smallest for sparse labels.

## What is missing to make this a recipe

**The conversion ratio.** The paper says there should be one — a pixel worth
some number of words for training a language model, a word worth some number
of pixels for vision — and does not estimate it. Without it, "include image
data" does not say how much, and at a fixed token budget every image token is
a text token not spent.

That is the gap `promote_when:` names, and it is the difference between a
direction and an instruction.

## Conditions, and why this is `Proposed`

**The evidence is cited, not run here.** The paper's own contribution is the
convergence measurement; the language-improved-by-images instance is somebody
else's report, quoted.

**The theory's boundary is this practice's boundary.** Where modalities carry
genuinely different information they cannot converge to the same
representation — language can state a belief about free speech and an image
cannot — and the benefit is capped by the mutual information between the
signals and by model capacity.

**The claim is about general representations**, not narrow tasks. A model
being trained for one well-specified job has no obvious reason to spend
budget on another modality.

**And the expected benefit may be sample efficiency rather than ceiling.**
The paper suggests the primary advantage of cross-modal data could simply be
that it gets you there faster, which is a different and smaller claim than
"the final model is better", and the two are not distinguished by anything
measured.

## Known implementations

- None in the record. Every pretraining report it holds trains a language
  model on text.
