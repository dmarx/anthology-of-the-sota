---
status: Active
title: 'Bootstrap a large annotation set with the model you are training, staging the automation as it improves'
version: 1
tags:
- data-pipeline
consensus: emerging
date: '2026-09-08'
source:
- LIT-096
implementations:
- SA-1B
---

# SOTA-tmp3vux6: Bootstrap a large annotation set with the model you are training, staging the automation as it improves

## Source

Kirillov et al. (2023), [LIT-096](../literature.d/LIT-096.md) — [ARXIV-2304.02643](https://arxiv.org/abs/2304.02643), ICCV 2023.

The dataset and the model are built together, in three stages, and the
staging is the practice:

- **Assisted-manual.** Annotators label with the model in the loop; the model
  is weak, so it mostly speeds up a human.
- **Semi-automatic.** The model proposes the confident cases; annotators are
  directed only at what it missed, which is where their time is worth most.
- **Fully automatic.** The model annotates unaided, and humans move to
  quality control on samples.

Retraining at each stage is what makes it work: the model that produced stage
*n*'s labels is trained on stage *n−1*'s, so the annotation cost per unit
falls as the model improves on data it helped create. The reported outcome is
about 1.1B masks over 11M images — a corpus no fully-manual budget reaches.

**The transferable claim is not about segmentation.** It is that when
annotation is the binding constraint, the right structure is a staged loop
rather than a one-shot labelling contract, and the thing that decides where
humans are pointed is the current model's own uncertainty. That is a
`data-pipeline` decision, and the record's other entries in that topic — the
perplexity filter in [SOTA-101](SOTA-101.md), the mixing-ratio practices — are the same kind
of claim at a different altitude.

## Conditions

It assumes the task has a cheap, checkable output. A mask is verifiable at a
glance; a long-form judgement is not, so the quality-control stage that makes
the automatic phase safe does not transfer for free.

It also assumes a model good enough at stage one to beat a bare human
workflow. The loop compounds, so it also compounds a bad start: errors the
early model makes enter the training data for the model that makes the next
round of them, and the paper's human quality control is what bounds that
rather than anything structural.

Marked `emerging`: model-in-the-loop annotation is now common practice across
several labs, but the explicit three-stage escalation with retraining between
stages is much less widely reported than the general idea.

## Known implementations

- SA-1B; the pattern recurs in most large open annotation efforts since
