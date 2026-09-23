---
number: 89
status: Proposed
formerly:
- THEORY-tmp472k3
promote_when: >-
  A test of the mechanism, not only of analogy accuracy. For example, show
  that word-vector differences predict log co-occurrence ratios
  quantitatively across word pairs, or that analogy success on a relation
  tracks how well its co-occurrence ratios are captured. Both sources derive
  the account from their objectives and show it only by examples and
  benchmark scores.
title: 'Word vectors trained on co-occurrence behave linearly because they encode log co-occurrence statistics: differences carry log ratios, which gives analogies, and sums carry products of context distributions, which gives composition'
version: 1
tags:
- representation-and-encoding
- signal-structure
- concept-geometry
date: '2026-09-23'
source:
- LIT-602
- LIT-603
summary: >-
  Pennington et al. (2014), [LIT-602](../literature.d/LIT-602.md), and Mikolov et al. (2013),
  [LIT-603](../literature.d/LIT-603.md) — what distinguishes words is the ratio of how often they
  co-occur with probe words (ice and steam with solid versus gas). A model
  whose dot products fit log co-occurrence turns ratios into vector
  differences, so relations become offsets. The same log-linearity makes a
  sum of vectors act like a product of context distributions, an AND of
  their contexts. Derived from the objectives and illustrated. The mechanism
  is not measured.
---

# THEORY-089: Word vectors trained on co-occurrence behave linearly because they encode log co-occurrence statistics: differences carry log ratios, which gives analogies, and sums carry products of context distributions, which gives composition

## Source

Pennington et al. (2014), [LIT-602](../literature.d/LIT-602.md), read as [NOTE-327](../notes.d/NOTE-327.md), for the ratio
account. Mikolov et al. (2013), [LIT-603](../literature.d/LIT-603.md), read as [NOTE-326](../notes.d/NOTE-326.md), for
additive composition.

## The account

Co-occurrence probabilities are dominated by frequent words that go with
everything. Their ratios cancel that out and keep what discriminates. GloVe's
Table 1: P(solid|ice)/P(solid|steam) = 8.9 and P(gas|ice)/P(gas|steam) =
0.085, while water and fashion give about 1. If wᵢ·w̃ₖ ≈ log P(k|i), then
(wᵢ − wⱼ)·w̃ₖ ≈ log P(k|i)/P(k|j). A relation shared by many word pairs,
such as male to female or country to capital, shifts the same ratios in the
same way, so it becomes a common offset, and analogies can be solved by
arithmetic. Adding vectors adds log context probabilities, which multiplies
the distributions, so the sum picks out contexts both words share (Russian +
river → Volga River).

## What it explains

- Why analogy arithmetic works in both count-based (GloVe) and
  prediction-based (skip-gram) vectors: both fit the same statistics
- Why SVD on raw counts does poorly and on log counts much better (7.3%
  against 60.1% on analogies at 6B)
- Why element-wise addition composes meaning

## Where it is weak

- **A derivation from each model's objective, not a measurement.**
  Neither paper checks that vector differences match log ratios
- **Shown by analogy accuracy and hand-picked examples**
- **Word-level, static embeddings.** Whether anything like it holds for
  contextual representations is outside both sources
