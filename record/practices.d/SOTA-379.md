---
number: 379
status: Active
formerly:
- SOTA-tmpl3rwi
consensus: unreplicated
consensus_note: >-
  One group's controlled study for word representations. The same lesson,
  retune the baselines under one procedure before crediting a method, is in
  the record for graph networks from other groups (SOTA-349, SOTA-350). This
  field-specific version has one source.
title: 'Before crediting a word-embedding method over count-based ones, give the baselines the same design choices and tune every method alike'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    `corrects` SOTA-380, the Baroni et al. recommendation it overturns,
    filed after it.
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-607
introduced_by:
- LIT-607
corrects:
- SOTA-380
implementations:
- hyperwords
summary: >-
  Levy, Goldberg and Dagan (2015), [LIT-607](../literature.d/LIT-607.md) — word2vec and GloVe ship
  with design choices (context smoothing, the negative-sample shift, dynamic
  windows, subsampling, adding context vectors) that count-based PPMI and SVD
  can use too. Port them and tune every method the same way before comparing.
  Done that way across 672 representations and 8 datasets, the
  prediction-over-count advantage disappears, SGNS beats GloVe on every task,
  and a single hyperparameter often matters more than the method.
---

# SOTA-379: Before crediting a word-embedding method over count-based ones, give the baselines the same design choices and tune every method alike

## Source

Levy, Goldberg and Dagan (2015), [LIT-607](../literature.d/LIT-607.md), read as [NOTE-329](../notes.d/NOTE-329.md).

## Do this

- **List the choices bundled with the method under test**, including those
  that appear only in its code: window weighting, subsampling, the negative
  shift log k, the 0.75 smoothing exponent, w + c, eigenvalue weighting and
  normalization.
- **Give each baseline every choice it can express.** PPMI takes shifted and
  smoothed PMI. SVD takes those and symmetric eigenvalue weighting. GloVe
  takes w + c.
- **Tune all methods over the same space, on held-out data.** In the source,
  2-fold cross-validation came within about 1 point of test-set tuning.
- **Report per task.** The winner changes from task to task.

## Why

Baroni et al. (2014, [LIT-608](../literature.d/LIT-608.md)) found prediction-based embeddings well
ahead, and recommended them ([SOTA-380](SOTA-380.md), now `Rejected`; this practice
`corrects` it). They had
compared word2vec with its recommended settings against vanilla PPMI and SVD,
with SVD at its worst setting. Equalizing the settings removes the
consistent gap. GloVe's win over word2vec reverses the same way. Tuning is
worth up to 15.7 points over vanilla, more than the gap between methods.

## Conditions

- **Similarity and analogy benchmarks on English Wikipedia.** Downstream
  tasks were not tested.
- **"The same space" means where applicable.** GloVe cannot express shifted
  PMI or smoothing, so identical treatment is not always possible. Say which
  choices each method was given.
- **Differences are reported without significance tests.** Treat gaps of a
  point or two as ties unless tested.

## Known implementations

- `hyperwords` (the authors' code)

<!-- inactive-ok-file: SOTA-380 — Rejected, and named as the retired recommendation; this citation records its retirement -->
