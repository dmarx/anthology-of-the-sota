---
number: 184
status: Active
formerly:
- SOTA-tmpsb4lw
title: 'Adapt a pretrained model by training a low-rank update to each weight matrix, not the matrix itself'
version: 1
tags:
- adaptation-and-tuning
consensus: universal
date: '2026-09-08'
source:
- LIT-046
summary: >-
  Hu et al. (2021), [LIT-046](../literature.d/LIT-046.md) — [ARXIV-2106.09685](https://arxiv.org/abs/2106.09685). Freeze the pretrained weights
  and learn a rank-r product BA beside each one, so the trainable parameter
  count and the optimizer state fall by orders of magnitude and the adapter
  folds back into the weight at inference.
---

# SOTA-184: Adapt a pretrained model by training a low-rank update to each weight matrix, not the matrix itself

## Source

Hu et al. (2021), [LIT-046](../literature.d/LIT-046.md) — [ARXIV-2106.09685](https://arxiv.org/abs/2106.09685).

## The method

Freeze W. Learn a low-rank product BA of the same shape, initialized so it
starts at zero, and train that instead. The argument is that the *update* a
fine-tune applies has low intrinsic rank even when the weight does not — so
representing it in full is spending memory on a degree of freedom the task
does not use.

What it buys, on the paper's own GPT-3 175B numbers: about 10,000× fewer
trainable parameters and roughly 3× less GPU memory, because the optimizer
state scales with the trainable count rather than the model. Quality is
on-par with or better than full fine-tuning across RoBERTa, DeBERTa, GPT-2
and GPT-3.

## Why it won rather than merely worked

`BA` is the same shape
as `W`, so it can be added into the weight after training and the served
model has no adapter, no extra layer, and no extra latency. Adapter methods
that insert modules pay at every forward pass; this one does not. That is
also what makes many adapters over one base model cheap to hold — the
alternative to swapping in a full fine-tune per task.

## Conditions

The saving is in optimizer state and gradient
memory, not in the forward activations, so it shrinks the fine-tuning bill
rather than the serving bill. And rank is a real hyperparameter — the paper's
tasks do well at small `r`, but a task that genuinely needs a high-rank
update will report the ceiling rather than announce it.

## Known implementations

- effectively every open-weight fine-tune published since 2022, and the
  default path in the major PEFT libraries
