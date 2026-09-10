---
status: Active
consensus: emerging
consensus_note: >-
  Widely done in practice as a heuristic — discriminative fine-tuning, layer-wise
  rates, freezing an encoder — and rarely stated as a decision with a measured
  optimum.
title: 'Give each pretrained component its own learning rate when fine-tuning a composite model'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-10'
source:
- LIT-072
implementations:
- OWL-ViT
---

# SOTA-tmpwf9e5: Give each pretrained component its own learning rate when fine-tuning a composite model

## Source

Minderer et al. (2022), [LIT-072](../literature.d/LIT-072.md) — OWL-ViT, fine-tuning a contrastively
pretrained image-text model for open-vocabulary detection.

## The claim

A model assembled from separately pretrained parts should not be fine-tuned at
one learning rate. Each part carries different knowledge, is being asked for a
different amount of change, and has a different amount to lose.

The measurement: using the same rate for the image and text encoders is "clearly
sub-optimal", and the text encoder needs a rate roughly **100× lower**. The
authors' explanation is that this

> may help to prevent catastrophic forgetting of the wide knowledge the model
> acquired during the contrastive pre-training stage

## The optimum is interior

**Freezing the text encoder entirely — learning rate 0 — also does not work
well.** So this is not "fine-tune the new part and freeze the old one", which is
the usual binary. The response is non-monotone with a maximum somewhere in the
middle, and both corners are wrong.

That is what makes it a decision rather than a default: a single shared rate is
one corner, freezing is the other, and the answer is neither.

## The metric conflict comes with it

The same sweep moves `AP^OI` — in-distribution performance — in the **opposite**
direction: the shared-rate setting that collapses zero-shot transfer improves
it. So the component learning rate is a dial between preservation and fitting,
and picking it requires knowing which you want. See [SOTA-tmpkh4j4](SOTA-tmpkh4j4.md), which is
that finding on its own.

## Relation to the other ways of protecting a pretrained part

The record now carries three instruments for the same goal, at different price
points:

- **This** — turn the learning rate down on what you do not want to move.
  Costs one hyperparameter per component.
- **[SOTA-tmptrepp](SOTA-tmptrepp.md)** — regularize against the pre-fine-tuning model's own
  samples. Costs a loss term and a sampling pass.
- **[SOTA-184](SOTA-184.md)** — do not touch the weights at all; train a low-rank update.

None has been compared against the others.

## Conditions

One measurement, vision-language, 2022. The 100× factor is specific to this
model pair and is not derived — nothing here says how to choose the ratio, only
that it is large and that both corners fail.

The explanation (catastrophic forgetting) is offered by the authors and not
isolated.

## Known implementations

- OWL-ViT, Table 3
