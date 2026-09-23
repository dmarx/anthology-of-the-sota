---
number: 331
status: 'Read'
formerly:
- NOTE-tmpqkikb
paper: 'LIT-612'
title: 'Levy & Goldberg: SGNS as implicit PMI factorization'
version: 1
date: '2026-09-23'
summary: >-
  SGNS's objective is optimized at w·c = PMI(w, c) − log k, a weighted
  factorization of the shifted PMI matrix. Shifted PPMI nearly attains that
  optimum and SVD over it matches SGNS on similarity, while SGNS keeps an
  edge on syntactic analogies. Read in full.
---

# NOTE-331: Levy & Goldberg: SGNS as implicit PMI factorization

## Contribution

A closed form for what skip-gram with negative sampling is fitting. Before
it, word2vec's objective was known to push co-occurring pairs together, but
not what quantity its dot products converge to. After it, SGNS is a weighted
factorization of a matrix the count-based literature had used for decades.

## Key insight

**Negative sampling is PMI with a prior.** The positive term counts how often
a pair occurs. The negative term counts how often it would occur by chance,
k times over. Balancing the two gives the log ratio of observed to expected
co-occurrence, which is PMI, minus log k.

## Assumptions

- Each dot product w·c is free to take any value. This needs d large enough
  for exact reconstruction
- Negatives drawn from the unigram distribution, not the smoothed one
  word2vec uses
- Bag-of-words window contexts

## Main results

- **Eq. 6–7**: at the optimum, w·c = PMI(w, c) − log k
- **Eq. 8**: NCE gives w·c = log P(w|c) − log k
- **§3.2**: with limited d, the loss weights pair (w, c) by #(w,c) and by
  k·#(w)#(c)/|D|, so frequent pairs are fitted more closely

## Key results

- Deviation from the optimal objective (Table 1): SPPMI ~0.0001%. SGNS
  6–39%, falling with d. SVD 24–26% at k = 1, 95% at k = 5, 266% at k = 15
- Tasks at d = 1000 (Table 2): similarity, SVD/SPPMI ≥ SGNS by small
  margins. Mixed analogies, SPPMI 0.655 against SGNS 0.619. Syntactic
  analogies, SGNS 0.627 against 0.466

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | SGNS's optimum is shifted PMI | strong | derivation, under unconstrained dimensions |
| C2 | SGNS is a weighted factorization | strong | follows from the per-pair objective |
| C3 | shifted PPMI nearly attains SGNS's optimal objective | moderate | sampled estimate of the objective, Table 1 |
| C4 | SGNS wins syntactic analogies because of its weighting | weak | conjecture, one dataset |

## Limitations

- The optimum is not what SGNS reaches at practical dimensions
- The 0.75 noise smoothing is set aside
- Small evaluation: four datasets, one corpus, one window size

## Recommendations

- **R1** — represent words with shifted PPMI, or with symmetric SVD over it.
  *Left in the reading* ([ADR-041](../decisions.d/ADR-041.md)). [LIT-607](../literature.d/LIT-607.md) finds the shift task-dependent for
  PPMI and harmful for SVD.
