---
number: 184
status: Active
formerly:
- SOTA-tmpsb4lw
title: 'Adapt a pretrained model by training a low-rank update to each weight matrix, not the matrix itself'
version: 2
history:
- version: 2
  date: '2026-09-17'
  note: >-
    Gained the placement condition it was silent about. The recommendation is
    unchanged; what is new is that WHICH matrices carry an adapter is a
    decision this practice never named, and a later paper measures it as the
    one that decides whether the method reaches full fine-tuning at scale.
tags:
- adaptation-and-tuning
consensus: universal
date: '2026-09-08'
source:
- LIT-046
introduced_by:
- LIT-046
summary: >-
  Hu et al. (2021), [LIT-046](../literature.d/LIT-046.md) — [ARXIV-2106.09685](https://arxiv.org/abs/2106.09685). Freeze the pretrained weights
  and learn a rank-r product BA beside each one, so the trainable parameter
  count and the optimizer state fall by orders of magnitude and the adapter
  folds back into the weight at inference.
compared_against:
- SOTA-329
extended_by:
- SOTA-tmppbzba
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

## Which matrices, which this practice did not say

"Each weight matrix" is the title, and the paper's experiments adapt the
attention query and value projections. Those are not the same instruction,
and the gap between them became the default: query/value is what the tooling
ships and what most published fine-tunes use.

[SOTA-231](SOTA-231.md) is the measurement of that gap. On large base models,
query/value alone does not replicate full fine-tuning; the number of adapted
matrices is what closes it, and the rank — the hyperparameter people actually
search — is flat across the sweep. Read the two together: this practice is
why to use a low-rank update, that one is where to put it.

## Known implementations

- effectively every open-weight fine-tune published since 2022, and the
  default path in the major PEFT libraries
