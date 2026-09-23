---
status: Read
paper: LIT-tmp55q30
title: 'word2vec (negative sampling, subsampling, phrases)'
version: 1
date: '2026-09-23'
summary: >-
  The tricks that made word2vec the standard: negative sampling with a
  unigram^(3/4) noise distribution, subsampling of frequent words, and
  data-driven phrase tokens, plus additive compositionality. The 3/4 exponent
  is asserted without numbers. Read in full.
---

# NOTE-tmpd9zqq: word2vec (negative sampling, subsampling, phrases)

## Contribution

A training recipe for skip-gram that is faster and better on rare words and
phrases. It remained the default for embedding training long after.

## Key insight

**Most co-occurrences are uninformative, so do not pay for them.**
Negative sampling avoids normalizing over the vocabulary. Subsampling
discards most occurrences of words that co-occur with everything. Both are
ways of spending the update budget on the informative part of the
distribution.

## Key results

- Subsampling, word analogies: NEG-5 38 → 14 minutes and 59 → 60%. HS 41 →
  21 minutes and 47 → 55%
- Subsampling, phrase analogies: NEG-15 27 → 42%, HS 19 → 47%
- Negative sampling beats hierarchical softmax on word analogies (61% for
  NEG-15 against 47% for HS, without subsampling)
- Best phrase model: 72% with 33B words, 66% with 6B

## Limitations

- **The unigram^(3/4) noise distribution has no reported numbers**, only
  "outperformed significantly … on every task we tried"
- **Subsampling's accuracy gain is uneven**: large for hierarchical softmax
  and phrases, and about zero for NEG-15 on words
- **Analogy accuracy is the only quantitative measure**, and
  compositionality is shown by examples
