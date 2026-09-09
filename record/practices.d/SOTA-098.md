---
number: 98
status: 'Active'
title: 'Monitor validation loss for unexpected spikes during training'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2022-04-01'
source:
- LIT-069
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
---

# SOTA-098: Monitor validation loss for unexpected spikes during training

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

## What validation adds over the training loss

A training-loss spike can be one bad batch; a validation-loss spike is the
model. The two together separate a transient from damage — the case that
matters is the spike that does not recover, where training loss returns to
trend and validation does not, which says the weights took a step the run has
not undone.

That distinction is what makes this worth a separate practice from [SOTA-069](SOTA-069.md)
rather than a duplicate of it, and it is why the response in [SOTA-095](SOTA-095.md) keys
off the checkpoint rather than off the next few steps.

## Cost, and the sampling problem

Validation is a forward pass over held-out data at some interval, so the
signal is only as timely as the interval. Too rare and the spike is found
thousands of steps later, when "the last checkpoint before it" is far back;
too frequent and it is a real fraction of the run.

The failure this creates is specific: an interval chosen for reporting — once
per epoch, say, because that is what the dashboard wants — is almost always
too coarse for detection. Two different consumers of the same number, and the
one nobody configures for is the one that would have caught the problem.
