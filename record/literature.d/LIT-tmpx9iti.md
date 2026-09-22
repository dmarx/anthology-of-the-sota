---
status: Active
title: 'Complexity-Guided Component-wise Initialization for Language Model Pretraining'
version: 1
tags:
- model-stability
- analysis-and-evaluation
- training-optimization
date: '2026-09-22'
published: '2026-07-10'
arxiv: '2607.09204'
first_author: 'Garbers'
keywords:
- 'weight initialization'
- 'effective rank entropy'
- 'layerwise diagnostics'
- 'spectral patterns'
- 'GPT-2'
implementations: []
summary: >-
  Garbers and Oh (2026), [ARXIV-2607.09204](https://arxiv.org/abs/2607.09204) — eleven
  GPT-2-style checkpoints differing in size, language, tokenizer and corpus
  share a depth profile: effective-rank entropy **falls** in the last few
  blocks, most sharply in the residual-writing matrices `W_O` and `W_down`,
  whose Frobenius norms rise almost linearly with depth. Initializing to
  imitate that profile changes the spectra and does **not** improve
  results. Read as [NOTE-tmpptsb7](../notes.d/NOTE-tmpptsb7.md).
---
<!-- inactive-ok-file: THEORY-059 — Proposed, named as the open question this
     paper supplies breadth for; the Standing section says what it measures,
     not that the account is settled. -->

# LIT-tmpx9iti: Complexity-Guided Component-wise Initialization for Language Model Pretraining

Garbers and Oh (2026) —
[ARXIV-2607.09204](https://arxiv.org/abs/2607.09204). Read as
[NOTE-tmpptsb7](../notes.d/NOTE-tmpptsb7.md).

## Key takeaways

- **Spectral concentration has a shared depth profile.** Across eleven
  checkpoints — English, Russian, Vietnamese, Chinese, Portuguese, Japanese,
  Turkish, plus poem and story models — effective-rank entropy drops in the
  final few blocks after per-model normalization.
- **It is strongest where the model writes to the residual stream.** `W_O`
  and `W_down` show the sharpest entropy drop, and their Frobenius norms grow
  almost linearly with depth: more total weight mass, carried by fewer
  directions.
- **The instrument is the right one for a magnitude claim.** Entropy
  effective rank, `exp(−Σ pᵢ log pᵢ)` on the trace-normalized spectrum,
  measures how many directions carry substantial mass — which is what a
  low-rank branch removes.
- **Imitating the profile at initialization does not work.** Initializers
  matched to pretrained component-wise magnitudes and singular-value shapes
  visibly change the structural spectra and produce no performance advantage;
  reusing the actual weights stays competitive.

## Standing in the anthology

**It is the breadth datapoint for [THEORY-059](../theory.d/THEORY-059.md)'s question.** The
other measurements in this cluster are deep on one or two model families.
This one holds the architecture fixed and varies size, language, tokenizer
and corpus, which is what tells you the spectral profile is a property of
trained transformers rather than of one recipe or one language.

**The negative half is worth as much as the positive half.** A recurring
spectral profile that cannot be transplanted is evidence that the profile is
a *consequence* of training rather than a configuration that causes good
training — which is the distinction [DP-005](../../docs/design-principles.md#dp-5) exists to keep the record
honest about, and the authors draw it themselves.
