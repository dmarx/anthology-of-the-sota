---
status: Active
title: 'Skip-gram with negative sampling implicitly factorizes the word-context PMI matrix shifted by log k, weighting frequent pairs more heavily'
version: 1
tags:
- representation-and-encoding
- signal-structure
date: '2026-09-23'
source:
- LIT-tmppsaaa
summary: >-
  Levy and Goldberg (2014), [LIT-tmppsaaa](../literature.d/LIT-tmppsaaa.md) — setting the derivative of SGNS's
  per-pair objective to zero gives w·c = PMI(w, c) − log k, with k the number
  of negatives. So word2vec's skip-gram is a factorization of the matrix
  count-based methods use, shifted by a constant, with each pair's error
  weighted by how often it occurs. NCE gives log P(w|c) − log k the same way.
  Exact at the optimum with unconstrained dimensions. At practical
  dimensions it describes the target, not the result.
extended_by:
- THEORY-089
- THEORY-092
---

# THEORY-tmpismnk: Skip-gram with negative sampling implicitly factorizes the word-context PMI matrix shifted by log k, weighting frequent pairs more heavily

## Source

Levy and Goldberg (2014), [LIT-tmppsaaa](../literature.d/LIT-tmppsaaa.md), read as [NOTE-tmpqkikb](../notes.d/NOTE-tmpqkikb.md).

## The account

SGNS scores each observed pair (w, c) by log σ(w·c) and each of k sampled
negatives by log σ(−w·c). Summed over the corpus, a pair's contribution is
#(w,c)·log σ(w·c) + k·#(w)#(c)/|D|·log σ(−w·c). The first term pulls the dot
product up in proportion to how often the pair occurs. The second pushes it
down in proportion to how often it would occur by chance. The balance point
is

    w·c = log( #(w,c)·|D| / (#(w)·#(c)) ) − log k = PMI(w, c) − log k.

So the dot products SGNS learns are trying to equal PMI, shifted down by
log k. When the dimension is too small to hit every target, the error on
each pair is weighted by its counts, so frequent pairs are fitted better
than rare ones. Changing the noise distribution to count^α changes the PMI's
denominator the same way.

## Why `Active`

It is a derivation, and it holds exactly under its stated assumption:
dot products free to take any value. It is the standard account of what
word2vec fits, and later work ([LIT-607](../literature.d/LIT-607.md)) uses it to transfer SGNS's settings
to count methods, with results that behave as the account predicts.

## What it explains

- **Why count and prediction methods converge once tuned alike** ([LIT-607](../literature.d/LIT-607.md)).
  They fit the same statistic, and the differences are in weighting and
  settings.
- **Why the number of negatives acts like a prior.** It shifts every target
  by log k, which is why the same shift can be applied to PPMI.
- **Why SVD degrades as k grows.** The shifted positive matrix gets more
  zeros, and SVD's unweighted L2 loss cannot tell unobserved cells from
  observed ones (§5.1, a hypothesis in the source).

## Where it is weak

- **The optimum is not what training reaches.** At d = 100–1000, SGNS is
  6–39% off the optimal objective. The account describes what SGNS aims at.
  What it actually encodes is a weighted low-rank approximation of that
  target.
- **word2vec's default uses a smoothed noise distribution**, so the
  factorized matrix uses count^0.75 in place of P(c). The source sets this
  aside.
- **Why the weighting helps analogies is conjecture.**
