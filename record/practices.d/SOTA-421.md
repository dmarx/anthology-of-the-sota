---
number: 421
status: Proposed
formerly:
- SOTA-tmpg915d
consensus: emerging
consensus_note: >-
  Per-size tuning before fitting is done by Porian et al., Pearce and Song
  (LR per size) and DeepSeek LLM (not held). The warmup rule and the β₂
  point come from one source. Read as of 2026-09.
promote_when: >-
  A second group ablates warmup length and per-size tuning separately in a
  compute-optimal sweep, and reports the exponent shift from each. Or a
  scaling study fits constant-LR and per-budget-cosine exponents on the same
  grid above 1B and finds them equal. A study that tunes per size without
  reporting the untuned exponent would not count.
title: 'Before fitting a compute-optimal allocation law, tune learning rate, batch size and AdamW beta2 per model size and keep warmup short of the smallest run'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-690
introduced_by:
- LIT-690
implementations: []
summary: >-
  Porian et al. (NeurIPS 2024), [LIT-690](../literature.d/LIT-690.md). In a small-scale sweep that
  will be fitted for `N*(C)`, a warmup longer than the smallest models'
  optimal runs moves the exponent by 0.10. So does one batch size, learning
  rate and β₂ shared across sizes. Tune them per size, with β₂ above 0.95 at
  small batch, and cap warmup (the source uses warmup tokens = N, at most 20%
  of the budget). A constant learning rate is enough *to fit the exponent*,
  at about half the cost of a per-budget cosine.
---

<!-- inactive-ok-file: THEORY-108 SOTA-141 — Proposed; the account this protocol rests on,
     and the decay practice the final model should still follow -->

# SOTA-421: Before fitting a compute-optimal allocation law, tune learning rate, batch size and AdamW beta2 per model size and keep warmup short of the smallest run

## Source

Porian, Wortsman, Jitsev, Schmidt and Carmon (2024), [LIT-690](../literature.d/LIT-690.md).

## What to do

In a sweep meant to fit a compute-optimal allocation law:

- **Warmup**: keep it well short of the smallest model's compute-optimal token
  count. The source uses `min(N, 0.2·budget)` tokens.
- **Per-size tuning**: find learning rate and batch size for each size, and
  raise AdamW β₂ above 0.95 at small batches (the source's cut-off is 128
  sequences of 2048 tokens).
- **Schedule**: a constant learning rate after warmup is enough to recover the
  exponent. Running a cosine per (N, C) pair costs about twice as much and
  moved the exponent by 0.03.
- **Counting**: see [SOTA-413](SOTA-413.md).

## Why

At small scale, fixed warmup and fixed hyperparameters penalize some sizes
more than others. The penalty tilts the fitted slope toward parameters
(`THEORY-108`).

## Conditions

- **It matters below about 1B.** The source expects each factor to fade with
  scale.
- **"Warmup = N tokens" is confounded** with "about 5% of a 20:1 run". It was
  ablated at one size.
- **The β₂ grid stopped at 0.999.** A rule holding β₂'s half-life fixed in
  tokens ([LIT-444](../literature.d/LIT-444.md)) would go higher at small batch.
- **A constant learning rate is for fitting, not training.** The source's
  constant runs reach worse loss than cosine. Train the final model with a
  decay ([SOTA-140](SOTA-140.md), [SOTA-141](SOTA-141.md)).

## Known implementations

- The source's released code and checkpoints.
