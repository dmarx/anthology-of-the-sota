---
status: Active
title: 'A large trained ViT repurposes redundant patch tokens as scratch space for global information, which is what its feature-map artifacts are'
version: 1
tags:
- representation-and-encoding
- model-architecture
date: '2026-09-24'
source:
- LIT-tmpic7xb
explains:
- SOTA-tmpnogfc
summary: >-
  Darcet et al. (2023), [LIT-tmpic7xb](../literature.d/LIT-tmpic7xb.md). The high-norm tokens that spoil ViT
  feature maps are not damage: they sit on patches redundant with their
  neighbours, they have discarded their own local content, and they carry
  global information instead. The model found spare capacity and used it. The
  account's own prediction — give the model dedicated slots and the artifacts
  should move there — was tested and holds.
---

<!-- inactive-ok-file: THEORY-tmp3s87v — Proposed, named in a section whose whole point is that these
     two accounts should NOT be read as corroborating each other: different
     modality, quantity, cause and remedy, and no comparison anyone ran
     (ADR-011). Its status is not load-bearing here. -->
# THEORY-tmpjr84g: A large trained ViT repurposes redundant patch tokens as scratch space for global information, which is what its feature-map artifacts are

## Source

Darcet, Oquab, Mairal and Bojanowski (2023), `LIT-tmpic7xb`.

## The claim

> large, sufficiently trained models learn to recognize redundant tokens, and
> to use them as places to store, process and retrieve global information

A ViT has no scratch space. Every position in its sequence is a patch of the
image and is expected to carry that patch's representation out the other end.
But a transformer accumulates global state as it goes, and needs somewhere to
put it.

On this account the model solves that by noticing which patches it can afford
to lose — the ones whose content is already present in their neighbours — and
overwriting them. The high-norm tokens people see as artifacts in attention
and feature maps are that overwriting, seen from outside.

## What it explains, and each piece is measured

- **Why the artifacts sit on background.** High-norm tokens have high cosine
  similarity to their four neighbours *at the patch embedding*, before any
  attention. The model is selecting redundancy, not creating it.
- **Why they are useless locally.** Linear probes: position top-1 22.8 against
  41.7 for normal tokens, pixel-reconstruction L2 25.23 against 18.38. The
  local content is gone because it was overwritten.
- **Why they are valuable globally.** One high-norm patch token taken at
  random as the entire image representation classifies substantially better
  than one normal token.
- **Why only large models, and only late.** Around layer 15 of 40, after a
  third of training, and only at ViT-Large and above. Small models have no
  spare capacity to find, and the strategy has to be learned.

## Why it is `Active`

**The account made a prediction and the prediction was tested.** If the
artifacts exist because the model needs scratch space, then supplying dedicated
scratch space should relocate them — and appending register tokens removes the
high-norm patch tokens **entirely**, in supervised (DeiT-III), image-text
(OpenCLIP) and self-supervised (DINOv2) training alike. Downstream performance
does not degrade and dense prediction improves.

That is a successful intervention derived from the hypothesis rather than a
correlation consistent with it, which is the strongest form of evidence a
mechanistic account of this kind can have, and it is why the status is
`Active` on one paper.

**The measurements point the same way from four independent directions** —
input-space similarity, two local probes, a global probe, and three sweeps over
depth, training time and model size.

## What it does not settle

**"Redundant" is operationalised as similarity to four neighbours**, which is
a proxy for what the model can afford to lose and not a measurement of it.

**It does not say the strategy is optimal or unique.** The model found *a*
place to put global state; nothing here shows it is the best available or that
a model given registers uses them the same way. The paper's own qualitative
analysis of what the registers learn is exploratory.

**One case the remedy does not help.** OpenCLIP object discovery is slightly
*worse* with registers. The account offers no explanation and the paper puts
its analysis in an appendix, so there is at least one behaviour the
scratch-space reading does not cover.

**The gap to DINO is not closed.** DINOv2+registers reaches 55.4 corloc on VOC
2007 where the original DINO reaches 61.9. If artifacts were the whole
difference the gap should have gone, and it did not — so something else about
DINOv2 also costs object discovery, and this account does not name it.

## Where it sits

The record holds one other account of activation outliers in a trained network:
`THEORY-tmp3s87v`, which says the outlier feature dimensions that break INT8
quantization in language models track pre-training optimization choices rather
than scale. Both accounts start from a phenomenon that correlates with size and
both conclude the correlation is not the explanation.

They are not the same claim and should not be read as corroborating each other.
Different modality, different quantity — feature dimensions across a whole
model against token positions within a sequence — different cause, and
different remedies: one changes a hyperparameter before training, the other
changes the architecture. What the pair supports is a question rather than a
conclusion: **when an activation pathology appears above a size threshold, what
else changed at the same time?**
