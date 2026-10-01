---
number: 92
status: 'Active'
title: 'smaller batch sizes are more sample efficient (i.e., better loss as a function of tokens seen) earlier in training'
version: 1
tags:
# Retagged from the report of unbound lineage. `training-optimization` names
# batch size in its blurb. It carried `model-architecture` because its source
# is a model report, which is where it was found rather than what it is about.
- training-optimization
date: '2026-08-24'
source:
# LIT-017 added in the correction pass: PaLM states this and cites it, and
# McCandlish et al. are who measured it (noise scale rising through
# training, their Fig. 5).
- LIT-069
- LIT-017
introduced_by:
# Was LIT-069. PaLM credits the observation to Smith et al. (2018) and
# McCandlish et al. (2018). Smith et al. (arXiv 1711.00489) recommend
# growing the batch as a substitute for learning-rate decay, an annealing
# argument that says nothing about sample efficiency or gradient estimates,
# so it is not filed as the origin. McCandlish et al. state this in words.
- LIT-017
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-092: smaller batch sizes are more sample efficient (i.e., better loss as a function of tokens seen) earlier in training

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

McCandlish et al. (2018), [LIT-017](../literature.d/LIT-017.md) — [ARXIV-1812.06162](https://arxiv.org/abs/1812.06162).

## Known implementations

- PaLM

## The observation, and the shape of it

Early in training the gradient is dominated by signal that almost any sample
carries, so a small batch already points in nearly the right direction and a
large one spends most of its samples confirming what the first few said. Loss
per token seen therefore falls faster at small batch.

[LIT-069](../literature.d/LIT-069.md) states this rather than measuring it. It is half of PaLM's given
reason for growing the batch during training — for the 540B model, 512
sequences (1M tokens) until step 50k, 1024 until step 115k, then 2048 (4M
tokens) to the end at step 255k — and the paper credits the observation to
Smith et al. (2018) and McCandlish et al. (2018), not to an experiment of its
own.

Of those two, the statement is McCandlish et al.'s, [LIT-017](../literature.d/LIT-017.md), and this record
names it as the origin. Across eight tasks they found the critical batch
size rising by an order of magnitude or more over a run, with the gradient
noise scale tracking it, and their line-search experiment on SVHN puts it in nearly PaLM's words: "Early in
training, smaller batches are sufficient to make optimal progress, while
larger batches are required later in training." Below the noise scale a
sample is nearly as useful in a small batch as a large one, so the small batch
reaches a given loss on fewer examples. Smith et al. (arXiv 1711.00489) also
grow the batch during training, but as a stand-in for learning-rate decay —
an annealing argument about the scale of SGD's noise, not a claim about
tokens per unit of loss — so they are not the origin of this one.
McCandlish et al. cite earlier adaptive-sampling work in optimisation that
uses the noise scale implicitly; the record has not read it, and a reader who
finds the claim there in a form that matches can move this field.

The effect is real and it is transient: it is a statement about the
signal-to-noise ratio of the gradient, which changes as the model gets
better. [SOTA-093](SOTA-093.md) is the other end of the same curve.

## What it does not license

Two things, and both are ways this practice gets misread.

It is about tokens seen, not wall-clock. A batch small enough to leave the
accelerator underutilised finishes fewer tokens per second, and the sample
efficiency it buys is paid back with interest in time — which is [SOTA-094](SOTA-094.md),
PaLM's other reason for its ramp: larger batches use the accelerator better.

And it is not an argument for a small *global* batch throughout. The practice
it implies is a batch-size *ramp*, which is what large training runs actually
do and what the record does not currently have as a practice: start small
while the gradient is informative, grow as it stops being.
