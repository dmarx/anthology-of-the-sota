---
status: Active
title: 'Loss Landscape Degeneracy and Stagewise Development in Transformers'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
- model-architecture
date: '2026-09-22'
published: '2024-02-04'
arxiv: '2402.02364'
first_author: 'Hoogland'
keywords:
- 'local learning coefficient'
- 'developmental stages'
- 'induction heads'
- 'in-context learning'
- 'loss landscape degeneracy'
implementations: []
summary: >-
  Hoogland, Wang, Farrugia-Roberts, Carroll, Wei and Murfet (2024),
  [ARXIV-2402.02364](https://arxiv.org/abs/2402.02364), TMLR 2025 — the instrument applied. Tracking the LLC
  through training divides two transformers into five stages each, and the
  boundaries coincide with structural changes the loss curve does not show:
  bigrams, then n-grams, then previous-token heads, then the induction circuit.
  In the in-context regression transformer, in-context learning is **acquired
  in LR2 and then deteriorates** across LR3 and LR4 as the model specializes to
  its pre-training distribution. Read as [NOTE-tmpwex9g](../notes.d/NOTE-tmpwex9g.md).
---

# LIT-tmpgj3s9: Loss Landscape Degeneracy and Stagewise Development in Transformers

Hoogland, Wang, Farrugia-Roberts, Carroll, Wei and Murfet (2024) —
[ARXIV-2402.02364](https://arxiv.org/abs/2402.02364), TMLR 2025. Read as [NOTE-tmpwex9g](../notes.d/NOTE-tmpwex9g.md).

## Key takeaways

- **The method.** Estimate the LLC through training; take critical points of
  the LLC curve as stage boundaries; then ask, independently, whether anything
  structural or behavioural changes at those boundaries.
- **Two-layer attention-only language model**, five stages ending at
  `t = 900 / 6.5k / 8.5k / 17k / 50k`, with `Δλ̂ = +26.4 / +22.5 / −1.57 /
  +8.62 / +1.77`. LM1 learns bigram statistics; LM2 common n-grams; LM3 forms
  previous-token heads; LM4 completes the induction circuit of Olsson et al.
  No significant change was found for LM5, and the authors say so.
- **In-context linear regression transformer**, five stages ending at
  `t = 1k / 40k / 126k / 320k / 500k`, with `Δλ̂ = +21.4 / +149 / −12.3 /
  −44.1 / +3.56`. LR1 learns the optimal context-independent prediction
  (`x_k ↦ ŷ_k = 0`); LR2 acquires in-context learning; **LR3 and LR4 see it
  deteriorate** as the model specializes to the pre-training task distribution
  and becomes fragile off it, alongside layer-normalization weights collapsing
  to zero.
- **A single run recapitulates a depth ladder.** Before the induction circuit
  forms, the 2-layer model passes through the strategies Olsson et al. found in
  *fully-developed* models of increasing depth — 0-layer bigrams, 1-layer
  skip-trigrams.
- **The claimed advantage over progress measures.** Degeneracy is
  "setting-agnostic" and "unsupervised": it detects a change **without
  requiring a mechanistic understanding in advance**, which the progress
  measures of Nanda et al. and Barak et al. do require. Interpreting the change
  is still a separate job, which the paper says.
- **LLC decreases are observed and are not explained.** Saddle-to-saddle theory
  for deep linear networks predicts monotonically increasing complexity, and
  the transitions sketched in the paper's own §5 are increases. Decreasing the
  LLC at constant loss would also lower the free energy; "providing a full
  theoretical account of these stages is an open problem".

## Standing in the anthology

**`Active`, and it is a direct rival to `LIT-085`'s progress measures**, named
as such by its authors. `SOTA-200` records that `LIT-085`'s restricted and
excluded loss are computed by projecting onto five frequencies the network was
reverse-engineered to be using, and are meaningless without that
reverse-engineering. This is the same job done without that prerequisite.

**The LR3/LR4 result bears on the in-context-learning cluster filed the same
day.** That an ICL-objective transformer *loses* in-context ability with
further training, while its loss keeps falling, is a fact about the setting
[LIT-534](LIT-534.md) established and every mechanism paper measures in — and none of
those papers reports it.

**Two case studies, and the paper is explicit that they are two case studies.**
"We do not claim that the structural and behavioral developments we observed
in each setting are universal phenomena."
