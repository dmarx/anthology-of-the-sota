---
number: 250
status: Active
formerly:
- SOTA-tmpkip7h
consensus: unreplicated
consensus_note: >-
  One lab. LIT-216 introduces it for images and LIT-215 carries the same
  construction to video at 1M+ hours and 1B parameters, but both are Meta AI
  and share authors, so this is one line rather than two groups agreeing.
  DP-005 keeps that separate from evidence: what is measured is real, what is
  missing is an independent replication.
title: 'Pretrain by predicting representations of masked regions, not their pixels'
version: 1
tags:
- vision-and-graphics
- representation-and-encoding
date: '2026-09-19'
source:
- LIT-216
introduced_by:
- LIT-216
implementations:
- I-JEPA
- V-JEPA 2
summary: >-
  Assran et al. (2023), [LIT-216](../literature.d/LIT-216.md) — [ARXIV-2301.08243](https://arxiv.org/abs/2301.08243). Predict the
  *representations* of masked target blocks from a context block, with a
  learned target-encoder, instead of reconstructing pixels. No hand-crafted
  augmentations, and a ViT-H/14 reaches strong downstream performance in under
  1200 GPU-hours — faster than a ViT-S/16 trained with iBOT.
---

# SOTA-250: Pretrain by predicting representations of masked regions, not their pixels

## Source

Assran et al. (2023), [LIT-216](../literature.d/LIT-216.md) — [ARXIV-2301.08243](https://arxiv.org/abs/2301.08243).

## The rule

Mask part of the image. Do **not** ask the model to reconstruct what was
there. Ask it to predict what a target-encoder's *output* would be for those
regions, given an encoding of the part you kept.

Three details are load-bearing and the paper names all three:

- **Mask the target-encoder's output, not its input.** Called out as crucial:
  computing targets from the full image and then selecting is what keeps the
  targets semantic.
- **Target blocks must be large enough to be semantic**, and the context
  block must be spatially distributed enough to be informative. This is the
  masking strategy, and it is the design choice that decides whether the
  representations come out semantic at all.
- **An exponential-moving-average target-encoder.** The asymmetry between
  context and target encoders is what prevents representation collapse — the
  standing failure mode of joint-embedding architectures.

## Why this over reconstructing pixels

A pixel objective spends capacity on detail that no downstream task wants —
texture, noise, exact colour. Predicting in representation space lets the
target-encoder decide what is worth predicting, which is the same argument
the record makes elsewhere for latent-space work.

**And it is cheaper, which is the measured part.** A ViT-H/14 on ImageNet:
16 A100s, under 72 hours, under 1200 GPU-hours total. That is faster than a
ViT-S/16 pretrained with iBOT and more efficient than a ViT-H/14 pretrained
with MAE — a larger model for less compute than a smaller one under the
competing objective.

## No hand-crafted augmentations

Worth stating separately because it is the other half of what this replaces.
The joint-embedding line before this depended on view augmentations — crops,
colour jitter, blur — chosen by hand and carrying an implicit claim about
which invariances matter. This needs none.

## Conditions

- **Vision Transformers.** The scaling claim is ViT-specific; nothing here is
  evidence for convolutional backbones
- **Images, then video.** [LIT-215](../literature.d/LIT-215.md) carries the same construction to over
  1 million hours of video at up to 1B parameters, reaching 77.3 on
  Something-Something v2 and 39.7 recall-at-5 on Epic-Kitchens-100
- **One lab.** See `consensus_note`. The construction is measured twice and
  replicated by nobody outside the group that proposed it

## What the record held before this

Nothing. Twenty-one `LIT` notes carry `vision-and-graphics` and until now
three practices did, all of them about geometry or scene representation
([SOTA-205](SOTA-205.md), [SOTA-236](SOTA-236.md), [SOTA-237](SOTA-237.md)). The record had no statement at all
about how to *pretrain* a visual encoder, which is upstream of all three.
Found by `#86`'s trunk detector, which reported `LIT-216`'s note saying so in
its own words.
