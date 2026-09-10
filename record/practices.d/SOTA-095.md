---
number: 95
status: 'Active'
title: 'consider rewinding to earlier checkpoint and skipping a few batches to mitigate unusual loss spikes'
version: 1
tags:
- model-architecture
date: '2026-08-24'
source:
- LIT-069
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-095: consider rewinding to earlier checkpoint and skipping a few batches to mitigate unusual loss spikes

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

## Known implementations

- PaLM

## The response half of the monitoring cluster

[SOTA-069](SOTA-069.md), [SOTA-070](SOTA-070.md), [SOTA-098](SOTA-098.md) and [SOTA-099](SOTA-099.md) all detect. This is what to do,
and it is the only practice in either stability cluster that says so: on a
loss spike, restore the last checkpoint from before it and skip forward past
the batches that were being consumed when it happened.

The reasoning is that a spike is usually caused by *specific data* — a
pathological document, a bad shard — interacting with the current parameters,
rather than by a general instability. Rewinding alone would replay the same
batches into the same state and reproduce it; skipping alone would leave the
damage already done to the weights and the optimizer moments in place. Both
together are what makes the recovery reliable, and PaLM reports using it.

## What it depends on

Three things the record now says elsewhere, and the practice is worth reading
as the reason they matter. Checkpoints frequent enough that "the last one"
is close ([SOTA-054](SOTA-054.md)). Detection early enough to know which batches to skip —
the NaN case is [SOTA-072](SOTA-072.md), and by the time it reaches the loss the moments are
already poisoned. And a data loader whose position can be restored and
advanced, which [LIT-059](../literature.d/LIT-059.md) says most implementations get wrong and for which
this record still has no practice.

Its cost is honest and rarely stated: the skipped data is not seen, and
nobody checks afterwards whether what was skipped mattered.
