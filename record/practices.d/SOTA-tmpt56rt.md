---
status: Active
title: 'When learning embeddings from co-occurrence, subsample very frequent tokens, discarding each occurrence with probability 1 − √(t/f) with t around 10⁻⁵'
version: 1
tags:
- data-pipeline
- representation-and-encoding
- signal-structure
date: '2026-09-23'
source:
- LIT-tmp55q30
introduced_by:
- LIT-tmp55q30
consensus: unreplicated
consensus_note: >-
  One paper's measurement, from the authors of the method. It became part of
  the standard word2vec and embedding-training recipe. That is adoption, not
  evidence (DP-005), and independent ablations have not been filed here.
implementations:
- word2vec
summary: >-
  Mikolov et al. (2013), [LIT-tmp55q30](../literature.d/LIT-tmp55q30.md) — in a Zipfian corpus, the few most
  frequent words co-occur with everything and dominate the updates while
  teaching little. Discard each occurrence of word w with probability
  1 − √(t/f(w)). This cut skip-gram training time by 2–3× and raised
  accuracy, only slightly for words (59 → 60% at NEG-5) but a lot for
  phrases (27 → 42% at NEG-15, 19 → 47% with hierarchical softmax).
---

# SOTA-tmpt56rt: When learning embeddings from co-occurrence, subsample very frequent tokens, discarding each occurrence with probability 1 − √(t/f) with t around 10⁻⁵

## Source

Mikolov et al. (2013), [LIT-tmp55q30](../literature.d/LIT-tmp55q30.md). Read as [NOTE-tmpd9zqq](../notes.d/NOTE-tmpd9zqq.md).

## The practice

- **Discard each occurrence of token w with probability 1 − √(t/f(w))**,
  where f is its relative frequency. Tokens rarer than t are never
  discarded, and the frequency ranking is preserved
- **Start at t ≈ 10⁻⁵** for corpora of billions of words
- **Expect speed first and accuracy second.** The run time fell by 2–3×.
  Accuracy gains are largest for rare items and phrases

## Conditions

- **Word2vec-style co-occurrence training.** The rationale, that frequent
  tokens co-occur with everything, is a property of text (heavy-tailed word
  frequencies). It transfers to other embedding methods with the same
  structure, but that is not tested here
- **Gains on word analogies were small or zero with enough negatives**
  (NEG-15: 61 → 61%)
