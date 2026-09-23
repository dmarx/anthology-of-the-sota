---
number: 327
status: Read
formerly:
- NOTE-tmpw8lop
paper: LIT-602
title: 'GloVe'
version: 1
date: '2026-09-23'
summary: >-
  Derives a word-embedding objective from the claim that meaning lives in
  ratios of co-occurrence probabilities. It fits log co-occurrence counts by
  weighted least squares and beats default-configured word2vec on analogies.
  Read in full.
---

# NOTE-327: GloVe

## Contribution

A count-based embedding method with a stated reason for its form. It also
argues that count-based and prediction-based methods probe the same
statistics and differ mainly in how efficiently they use them.

## Key insight

**Ratios, not probabilities.** Whether "solid" tells you more about ice or
steam is the ratio of its co-occurrence probabilities with each. Asking
vector differences to encode log ratios fixes the model up to a bias term.

## Key results

- Word analogy: 75.0% (42B tokens), 71.7% (6B), against skip-gram 69.1% and
  CBOW 65.7% on the same 6B
- SVD on log counts reaches 60.1% at 6B and falls to 49.2% at 42B, which the
  authors read as evidence the weighting matters
- Word similarity: best or near-best on five sets. NER features are
  competitive (Table 4)
- α = 3/4 is modestly better than linear weighting, and x_max matters
  weakly

## Limitations

- **word2vec at defaults.** Time is proxied by negative samples, a choice the
  authors acknowledge should be relaxed
- **Small margins** on the headline comparison (2.6 points)
- **The ratio argument motivates the model. It is not tested as a
  mechanism**
