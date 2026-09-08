---
# inactive-ok-file: SOTA-144 — Proposed, and named throughout on purpose: it
# is the sibling extension of the same parent, and the fact that it was filed
# while this one was not is the reason this document exists.
status: Proposed
promote_when: >-
  An independent group training under u-µP and reporting either the
  hyperparameter decoupling or the FP8 result — that the sweep collapsed to
  one dimension, or that training held in FP8 without loss scaling. A result
  reaching low-precision stability by another route is not it: the claim here
  is that this parametrization gives it for free, and another mechanism
  achieving it says the property is reachable, not that this route works.
consensus: unreplicated
consensus_note: >-
  One paper from one collaboration (Graphcore and Cerebras), with no
  production report in the record trained under it — the same profile as
  SOTA-144, the other one-group extension of the same practice.
title: 'Combine µP with unit scaling so the hyperparameters decouple and FP8 needs no loss scaling'
version: 1
tags:
- training-optimization
date: '2026-09-08'
published: '2024-07-01'
source:
- LIT-149
extends:
- SOTA-143
implementations: []
summary: >-
  Blake et al. (2024), [LIT-149](../literature.d/LIT-149.md) — µP makes activation scale independent of
  model size; unit scaling makes activations, weights and gradients start at
  a scale of one. Together the model is size-independent *and* well-scaled
  from the first step, the hyperparameters become close to independent so a
  one-dimensional sweep replaces a joint search, and FP8 works without
  loss-scaling tricks.
---

# SOTA-tmp24dx3: Combine µP with unit scaling so the hyperparameters decouple and FP8 needs no loss scaling

## Source

Blake et al., Graphcore and Cerebras (2024; ICLR 2025), [LIT-149](../literature.d/LIT-149.md) —
[ARXIV-2407.17465](https://arxiv.org/abs/2407.17465).

[SOTA-143](SOTA-143.md) gets the transfer: under µP the optimal learning rate stops moving
with width, so you tune small and transfer. What it does not get is the
*scale* the tensors start at — µP makes activation scale independent of model
size without saying what that size-independent scale should be.

Unit Scaling answers that: activations, weights and gradients all begin
training at a scale of one. Combined, the model is size-independent **and**
well-scaled from the first step, and two things follow that neither gives
alone.

## What the combination buys

- **The sweep collapses.** The hyperparameters become close to independent,
  so a one-dimensional sweep replaces a joint search — a learning-rate sweep
  alone gets near the optimum. That is a cost reduction on top of the cost
  reduction [SOTA-143](SOTA-143.md) already claims.
- **FP8 without loss-scaling tricks**, because nothing starts far from the
  representable range. Low-precision stability falls out of the
  parametrization rather than being bolted on.
- u-µP models reach lower loss than comparable µP models.

## Conditions, and why this is Proposed

One paper, one collaboration, and nothing in the record trains under it.

Worth being explicit about the shape, because it is the reason this is filed
at all: **[SOTA-144](SOTA-144.md) is the other one-group extension of [SOTA-143](SOTA-143.md)** — CompleteP,
which extends the transfer across depth — and it carries the same evidence
profile, the same status and the same consensus value. Filing one and not the
other left the µP material with a fork where only one branch existed as a
document. The two are siblings, not rivals: one extends the transfer across
depth, this one improves what the transfer costs and what it survives.

## Known implementations

- None in the record.
