---
status: Active
title: 'Use Muon with decoupled weight decay and AdamW-matched update RMS in place of AdamW'
version: 1
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source: LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Stable at nearly the same optimal LR as AdamW, better evaluations; used for every Falcon-H1-Tiny model.
---

# SOTA-121: Use Muon with decoupled weight decay and AdamW-matched update RMS in place of AdamW

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

Muon as modified in [ARXIV-2502.16982](https://arxiv.org/abs/2502.16982): weight decay applied to the
orthogonalised update, and the update's RMS rescaled to match what AdamW
would produce, so that the learning rate and weight decay tuned for AdamW
carry over. Under that recipe the authors saw stable training at nearly the
same optimal learning rate as AdamW and better downstream evaluations, and
adopted it for every model in the series, at 90M and 0.6B.

Conditions: the comparison here is at tiny scale with a µP-parameterised
hybrid Mamba/attention model. The RMS matching is what makes the AdamW
hyperparameters transferable; without it the learning rate has to be
re-tuned. Muon applies to matrix parameters — embeddings, norms and other
vectors keep an Adam-style update.

## Known implementations

- Falcon-H1-Tiny (all released checkpoints)
