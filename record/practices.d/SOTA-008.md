---
number: 8
status: 'Active'
title: 'linear warmup of LR stabilizes early training with large batch size.'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2017-08-01'
source:
- LIT-009
summary: >-
  You et al. (2017), [LIT-009](../literature.d/LIT-009.md) — [ARXIV-1708.03888](https://arxiv.org/abs/1708.03888).
compared_against:
- SOTA-100
---

# SOTA-008: linear warmup of LR stabilizes early training with large batch size.

## Source

You et al. (2017), [LIT-009](../literature.d/LIT-009.md) — [ARXIV-1708.03888](https://arxiv.org/abs/1708.03888).

## What warmup is for at large batch

A large batch gives a low-variance gradient estimate, which is what makes a
large learning rate usable — but only once the parameters are somewhere the
estimate means something. At initialisation the loss surface is far from any
minimum and the early steps are large in a direction chosen mostly by the
initialisation, so the same rate that is stable later diverges immediately.

Ramping the rate linearly from near zero over the first steps buys the time
for the parameters to reach a region where the large rate is survivable. It is
the compensation that makes the large-batch regime work at all, which is why
it arrived with large-batch training rather than before it.

## Three reasons warmup persists, only one of which is this

Worth separating, because the record holds them in different places and they
scale differently:

- **Initialisation gradients**, which is [SOTA-100](SOTA-100.md)'s mechanism and depended on
  post-norm; pre-norm ([SOTA-032](SOTA-032.md)) largely removed it.
- **Adam's second moment**, which is estimated from a handful of samples in the
  first steps and is unreliable until the average fills — this one is about the
  optimizer, not the architecture, and does not scale with model size.
- **Reaching a schedule's peak**, which is bookkeeping: a schedule with a peak
  needs a ramp to it, and [SOTA-009](SOTA-009.md) is that schedule.

A practice that says "warmup stabilises early training" is true and does not
say which of the three it means. All three are real; only the second still
binds for a pre-norm model trained with Adam, which is every model in this
record.
