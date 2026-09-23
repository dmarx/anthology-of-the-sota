---
status: Proposed
promote_when: >-
  A reported comparison, from anyone, of negative-sampling noise
  distributions (uniform, unigram and unigram^α for several α) at matched
  compute, showing α near 3/4 is better by a stated margin, on more than one
  task. The source asserts the result without numbers.
title: 'When training with sampled negatives, draw them from the unigram distribution raised to the 3/4 power, not from the unigram or uniform distribution'
version: 1
tags:
- training-optimization
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmp55q30
introduced_by:
- LIT-tmp55q30
consensus: unassessed
consensus_note: >-
  The 3/4 exponent is a fixture of embedding, recommendation and retrieval
  code. That is adoption (DP-005). GloVe independently found 3/4 best for a
  different job, weighting co-occurrence counts, which is suggestive and not
  the same evidence.
implementations:
- word2vec
summary: >-
  Mikolov et al. (2013), [LIT-tmp55q30](../literature.d/LIT-tmp55q30.md) — sample negatives in proportion to
  count^(3/4). That flattens the Zipfian head so frequent words are not
  nearly the only negatives, while keeping rare words rare. The authors report it
  "outperformed significantly the unigram and the uniform distributions …
  on every task we tried", but give no numbers.
---

# SOTA-tmpuwmrz: When training with sampled negatives, draw them from the unigram distribution raised to the 3/4 power, not from the unigram or uniform distribution

## Source

Mikolov et al. (2013), [LIT-tmp55q30](../literature.d/LIT-tmp55q30.md). Read as [NOTE-tmpd9zqq](../notes.d/NOTE-tmpd9zqq.md).

## The practice

- **Noise distribution Pₙ(w) ∝ count(w)^{3/4}**, for negative sampling or
  NCE
- **Use k = 5–20 negatives for small data and 2–5 for large**, in the
  authors' experience

## Conditions

- **No measurements in the source.** Proposed until one is filed
- **Word-level skip-gram.** Other tasks and item distributions may want a
  different exponent
