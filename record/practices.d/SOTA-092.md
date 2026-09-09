---
number: 92
status: 'Active'
title: 'smaller batch sizes are more sample efficient (i.e., better loss as a function of tokens seen) earlier in training'
version: 1
tags:
- model-architecture
date: '2026-08-24'
published: '2022-04-01'
source:
- LIT-069
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-092: smaller batch sizes are more sample efficient (i.e., better loss as a function of tokens seen) earlier in training

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

## Known implementations

- PaLM

## The observation, and the shape of it

Early in training the gradient is dominated by signal that almost any sample
carries, so a small batch already points in nearly the right direction and a
large one spends most of its samples confirming what the first few said. Loss
per token seen therefore falls faster at small batch.

The effect is real and it is transient: it is a statement about the
signal-to-noise ratio of the gradient, which changes as the model gets
better. [SOTA-093](SOTA-093.md) is the other end of the same curve.

## What it does not license

Two things, and both are ways this practice gets misread.

It is about tokens seen, not wall-clock. A batch small enough to leave the
accelerator underutilised finishes fewer tokens per second, and the sample
efficiency it buys is paid back with interest in time — which is [SOTA-094](SOTA-094.md),
the third of PaLM's three observations and the one that decides what
actually gets run.

And it is not an argument for a small *global* batch throughout. The practice
it implies is a batch-size *ramp*, which is what large training runs actually
do and what the record does not currently have as a practice: start small
while the gradient is informative, grow as it stops being.
