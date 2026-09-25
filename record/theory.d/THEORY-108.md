---
number: 108
status: Proposed
formerly:
- THEORY-tmp9y82q
title: "Kaplan's and Chinchilla's compute-optimal exponents differ because of how small-scale runs were counted, warmed up and tuned, not because of the learning-rate decay"
version: 1
tags:
- training-optimization
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-690
- LIT-688
explains:
- SOTA-096
- SOTA-413
promote_when: >-
  A second group reproduces Kaplan's raw exponent and removes the factors in
  a different order, or factorially, and finds the same three account for the
  gap with decay a minor term. Or a reproduction in Kaplan's own architecture
  and data (GPT-2-style, 1024 context, WebText2-like) recovers the
  attribution. Another study reaching a ≈ 0.5 with every correction applied at
  once would not settle it, because that shows the endpoint and not the
  decomposition.
summary: >-
  Porian et al. (NeurIPS 2024), [LIT-690](../literature.d/LIT-690.md), reproduce Kaplan's `a ≈ 0.84–0.86`
  from 5M to 901M on two datasets, then remove it in steps. Counting the
  output head's FLOPs takes 0.13 off. A warmup short enough for small models
  takes 0.10. Tuning batch, learning rate and β₂ per size, at a constant
  learning rate, takes another 0.10, landing on 0.497. Matching the cosine
  decay to each run, Chinchilla's proposed cause, moves it 0.03. Pearce and
  Song ([LIT-688](../literature.d/LIT-688.md)) independently find counting matters and a constant rate
  suffices, at 0.8–4.6M.
---

# THEORY-108: Kaplan's and Chinchilla's compute-optimal exponents differ because of how small-scale runs were counted, warmed up and tuned, not because of the learning-rate decay

## Source

Porian et al. (2024), [LIT-690](../literature.d/LIT-690.md), primary. Pearce and Song (2024),
[LIT-688](../literature.d/LIT-688.md), corroborating on counting and on decay.

## The account

At small scale, three things make a compute-optimal sweep favour
parameters over tokens:

1. **Uncounted head FLOPs.** Excluding the output layer under-counts compute by
   up to 90% at the smallest sizes, and by less and less as models grow. The
   under-count is size-dependent, so it tilts the fitted slope.
2. **A warmup longer than a small model's optimal run.** With 1.57B warmup
   tokens, small models are "forced" to train longer than is optimal to escape
   it. That pushes their optimal token counts up at small compute and flattens
   the growth of `D*`, which steepens `N*`.
3. **Hyperparameters fixed across sizes.** One batch size and learning rate,
   and β₂ = 0.95 at small batch, suit some sizes worse than others.

Each moves the exponent by about 0.1, and together they account for the gap
from about 0.84 to 0.5. The learning-rate *decay* moves it by 0.03.

## What it explains

- **[SOTA-096](../practices.d/SOTA-096.md)**: why 20:1, equal proportion, replaced
  Kaplan's parameter-heavy allocation. The earlier exponent was a small-scale
  measurement artefact, not a different law.
- **[SOTA-413](../practices.d/SOTA-413.md)**: why counting the head is a correction and
  not a convention. The under-count is size-dependent.

## Where it stops

- **The sources disagree on the shares.** Pearce and Song attribute "much of"
  the gap to counting, against the adjusted 0.73. Porian finds counting is
  about 38% of the gap to the raw 0.88, and explains the difference by the
  warmup factor Pearce and Song did not model.
- **Order matters in principle.** The attribution is sequential. One
  reordering (tuning first, 0.835 → 0.717) is roughly additive. No factorial
  design was run.
- **The reproduction is Kaplan-like, not Kaplan's.** Llama-style, context 2048,
  different data and tokenizer.
- **It does not say decay is irrelevant to loss.** Decay matters, increasingly
  with scale. It barely moves the fitted *allocation*.
- **The warmup factor has one source.** That is the main reason this is
  `Proposed`.
