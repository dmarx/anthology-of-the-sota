---
number: 96
status: 'Active'
title: '`num_tokens ~ 20 * num_params`'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2022-03-01'
source:
- LIT-068
summary: >-
  Hoffmann et al. (2022), [LIT-068](../literature.d/LIT-068.md) — [ARXIV-2203.15556](https://arxiv.org/abs/2203.15556).
implementations:
- chinchilla
- llama2
---

# SOTA-096: `num_tokens ~ 20 * num_params`

## Source

Hoffmann et al. (2022), [LIT-068](../literature.d/LIT-068.md) — [ARXIV-2203.15556](https://arxiv.org/abs/2203.15556).

## The finding

Given a fixed compute budget, previous practice ([LIT-028](../literature.d/LIT-028.md)) allocated it toward
model size and stopped well short of convergence. Fitting the loss surface
over 400 runs from 70M to 16B parameters and 5B to 500B tokens, Hoffmann et al.
found instead that **model size and training tokens should scale in equal
proportion**: double the compute, double both. The ratio that falls out is
about 20 tokens per parameter.

The demonstration was the point. Chinchilla at 70B, trained on 1.4T tokens,
outperformed Gopher at 280B trained on 300B tokens — a model four times
smaller, on the same compute, beating it across the board. Gopher, GPT-3,
Jurassic-1 and Megatron-Turing NLG were all substantially undertrained.

## What the ratio is and is not

It is the *compute-optimal* allocation: the split that minimises loss for a
fixed training budget. It is not the allocation that minimises the cost of
using the model, and the record's practice has diverged from it for that
reason. Inference cost scales with parameters and not with training tokens,
so a model that will serve many requests is worth training past 20:1 — every
frontier release in this record trains far beyond it, and none of them is
violating this finding. They are optimising a different objective.

The ratio also assumes the data is there to spend. Past the point where a
corpus must be repeated, the trade changes
<!-- inactive-ok: SOTA-124 — Proposed; named as the open question this law's regime assumes away -->
([SOTA-124](SOTA-124.md)'s question), and the
scaling law was fit in a regime where fresh tokens were assumed.

The batch-size claim that used to sit beside this one under the same citation
([SOTA-097](SOTA-097.md)) is Kaplan's, not Chinchilla's, and now says so.

## Known implementations

- chinchilla
- llama2
