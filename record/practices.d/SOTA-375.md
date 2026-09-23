---
number: 375
status: Proposed
formerly:
- SOTA-tmpuwmrz
promote_when: >-
  A reported comparison, from anyone, of negative-sampling noise
  distributions (uniform, unigram and unigram^α for several α) at matched
  compute, showing α near 3/4 is better by a stated margin, on more than one
  task. The source asserts the result without numbers.
title: 'When training with sampled negatives, draw them from the unigram distribution raised to the 3/4 power, not from the unigram or uniform distribution'
version: 2
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Gains its first measurement, LIT-607 (smoothing against none: SGNS
    0 to +1.4, PPMI up to +9.2), and consensus `unreplicated` for it. Still
    Proposed: only two exponents are compared.
tags:
- training-optimization
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-603
- LIT-607
introduced_by:
- LIT-603
consensus: unreplicated
consensus_note: >-
  The 3/4 exponent is a fixture of embedding, recommendation and retrieval
  code. That is adoption (DP-005). The one controlled measurement is
  LIT-607, a second group, against α = 1 only. GloVe independently found
  3/4 best for a different job, weighting co-occurrence counts, which is
  suggestive and not the same evidence.
implementations:
- word2vec
summary: >-
  Mikolov et al. (2013), [LIT-603](../literature.d/LIT-603.md) — sample negatives in proportion to
  count^(3/4). That flattens the Zipfian head so frequent words are not
  nearly the only negatives, while keeping rare words rare. The authors report it
  "outperformed significantly the unigram and the uniform distributions …
  on every task we tried", but give no numbers.
explained_by:
- THEORY-092
---

# SOTA-375: When training with sampled negatives, draw them from the unigram distribution raised to the 3/4 power, not from the unigram or uniform distribution

## Source

Mikolov et al. (2013), [LIT-603](../literature.d/LIT-603.md). Read as [NOTE-326](../notes.d/NOTE-326.md).

## The practice

- **Noise distribution Pₙ(w) ∝ count(w)^{3/4}**, for negative sampling or
  NCE
- **Use k = 5–20 negatives for small data and 2–5 for large**, in the
  authors' experience

## Evidence

- **Mikolov et al. give none.** "Significantly" better "on every task we
  tried", with no table.
- **Levy, Goldberg and Dagan measure it** ([LIT-607](../literature.d/LIT-607.md), Table 8d), as
  context-distribution smoothing against α = 1, over 8 similarity and
  analogy datasets. SGNS gains 0 to +1.4 points and never loses. PPMI gains
  up to +9.2 and SVD up to +2.2. The authors call it the one setting that can
  be applied blindly. [THEORY-092](../theory.d/THEORY-092.md) is their account of why.

## Why still `Proposed`

`promote_when` asks for several exponents and the uniform distribution at
matched compute. The measurement compares two values, 0.75 and 1. It
establishes that smoothing helps, and helps SGNS only a little. It does not
establish that 3/4 is the right exponent.

## Conditions

- **The gain for skip-gram itself is small.** Most of the measured benefit
  goes to count-based PMI methods
- **Word-level skip-gram.** Other tasks and item distributions may want a
  different exponent

<!-- inactive-ok-file: THEORY-092 — Proposed, filed in this same contribution as this practice's account -->
