---
number: 38
status: 'Active'
title: 'ICL permits few-shot task adaptability'
version: 1
tags:
- adaptation-and-tuning
date: '2026-08-24'
published: '2020-05-01'
source:
- LIT-035
extends:
- SOTA-036
summary: >-
  Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).
---

# SOTA-038: ICL permits few-shot task adaptability

## Source

Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).

## What it replaced

Before [LIT-035](../literature.d/LIT-035.md) the standard route to a task was fine-tuning: a labelled
dataset per task, a gradient update, a separate set of weights to serve. This
practice is the observation that a large enough pretrained model reaches
useful performance on many tasks from a prompt alone — the task specified in
the input, no weights changed.

The consequence is operational rather than statistical, and it is why the
practice matters more than its accuracy numbers: one model serves every task,
adaptation costs a prompt rather than a training run, and a new task is
available immediately rather than after a labelling effort.

## Where it stops

Few-shot prompting is generally *worse* than fine-tuning on any single task
with enough labelled data — [LIT-035](../literature.d/LIT-035.md) says so, and the gap is largest where the
task is unlike anything in pretraining. It is a trade of peak accuracy for
breadth and immediacy.

The record's own line has moved past the dichotomy: parameter-efficient
tuning ([SOTA-033](SOTA-033.md)'s territory) recovers most of the fine-tuning gain at a
<!-- inactive-ok-block: SOTA-130 — Proposed, cited as the post-training line that reaches past prompting; its status is the point -->
fraction of the cost, and post-training with verifiable rewards ([SOTA-130](SOTA-130.md))
produces capabilities prompting does not reach at all. Few-shot prompting is
now the *baseline* you compare those against rather than the recommendation.

Kept Active because the claim is true and load-bearing: it is why the field
stopped building one model per task, which is an assumption almost everything
else in this record rests on.
