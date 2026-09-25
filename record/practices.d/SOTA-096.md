---
number: 96
status: 'Active'
title: '`num_tokens ~ 20 * num_params`'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    LIT-690 (Porian et al.) added as a second source. It reproduces an
    allocation exponent of 0.497 from 5M to 901M on two datasets, and lands
    within 15% of Chinchilla's model size at Chinchilla's compute. It
    measures the equal-proportion exponent directly. It does not pin the
    ratio at 20: its optimal ratio ranges 14–16 on RefinedWeb and 11–22 on
    OpenWebText2. The recommendation is unchanged.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-068
# LIT-690 is an independent reproduction of the exponent (a ≈ 0.5), not
# of the ratio "20", which it measures as 11–22 depending on data (ADR-030).
- LIT-690
introduced_by:
- LIT-068
summary: >-
  Hoffmann et al. (2022), [LIT-068](../literature.d/LIT-068.md) — [ARXIV-2203.15556](https://arxiv.org/abs/2203.15556).
implementations:
- chinchilla
- llama2
explained_by:
- THEORY-108
---

# SOTA-096: `num_tokens ~ 20 * num_params`
<!-- inactive-ok-file: SOTA-097 — Superseded, and named here only to record where the mis-sourced batch claim went; the sentence is history -->

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
