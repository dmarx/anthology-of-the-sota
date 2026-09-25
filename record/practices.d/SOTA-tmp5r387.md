---
status: Proposed
consensus: unreplicated
consensus_note: >-
  One model, one successful run after two failures, from one group. Looped
  and universal transformers have a longer literature, but this record holds
  none of it. The same authors' earlier LIT-tmpa75eq found no gain from
  recurrence at matched wall-clock on a small encoder. Read as of 2026-09.
promote_when: >-
  A recurrent-depth model is compared against a standard transformer at
  matched training FLOPs *and* matched inference FLOPs, on the same data, by
  any group. Or random-`r` sampling is ablated against a fixed `r` at 1B or
  more parameters. Another looped model that "improves with more iterations"
  would not count, because that is this paper's result, not its open question.
title: 'To let a model spend more compute at inference without more parameters, train a depth-recurrent core on a randomly sampled iteration count, re-injecting the input at every iteration'
version: 1
tags:
- model-architecture
- inference-optimization
- training-optimization
date: '2026-09-25'
source:
- LIT-tmpdiu35
introduced_by:
- LIT-tmpdiu35
implementations:
- 'Huginn-0125'
summary: >-
  Geiping et al. (NeurIPS 2025), [LIT-tmpdiu35](../literature.d/LIT-tmpdiu35.md). Put a small core block
  between a short prelude and coda. At each training step sample how many
  times to iterate it, from a heavy-tailed distribution with mean 32.
  Backpropagate through the last few iterations only. Feed the input
  embedding into every iteration, and start the state from noise. Trained
  this way, accuracy rises with iterations at test time and saturates per
  task. A model trained at fixed depth does not gain this. Nothing yet shows
  it beats a standard transformer of the same FLOPs.
---

# SOTA-tmp5r387: To let a model spend more compute at inference without more parameters, train a depth-recurrent core on a randomly sampled iteration count, re-injecting the input at every iteration

## Source

Geiping et al. (2025), [LIT-tmpdiu35](../literature.d/LIT-tmpdiu35.md).

## What to do

- **Shape**: a prelude of a few layers, a core block iterated `r` times, and a
  coda. The source uses `(2, 4, 2)`.
- **Input re-injection**: concatenate the prelude's output with the state at
  every iteration and project it back to width.
- **Random initial state**: `s₀` drawn from noise.
- **Random depth in training**: sample `r` per step from a log-normal Poisson
  with a heavy tail (mean 32 in the source). Backpropagate through only the
  last `k` iterations (`k = 8`). The prelude still gets gradient every step,
  through the re-injection.
- **At inference**, choose `r` per task, or exit per token when successive
  states stop changing.

## Why

The model is trained to improve its state for as long as it is iterated. So
extra test-time iterations are a direction it has learned to use, not an
extrapolation. Training at a single depth does not give this: the same
architecture run once through the core, or the recurrent model evaluated at
`r = 1`, is far below the recurrent model at `r = 32`.

## Conditions

- **Per parameter, not per FLOP.** The source shows accuracy per parameter.
  It has no standard transformer trained at matched compute. The same authors
  found, at small scale and equal wall-clock, that shared recurrent layers
  gave no gain over unshared ones ([LIT-tmpa75eq](../literature.d/LIT-tmpa75eq.md)).
  Use this where parameters or memory bind. Where FLOPs bind, the case is not
  made.
- **Training was fragile.** Two runs failed: one by representation collapse,
  one by the model learning to ignore its state. The one that worked used
  sandwich normalization and a much smaller learning rate. Expect to need
  similar measures, and do not assume the listed recipe elements are each
  necessary. None was ablated at scale.
- **One 3.5B model on code- and math-heavy data**, with a constant learning
  rate that was never decayed.

## Known implementations

- Huginn-0125, the source's released model.
