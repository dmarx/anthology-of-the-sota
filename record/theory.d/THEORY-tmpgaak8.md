---
status: Active
title: 'Skip-gram node embeddings with negative sampling implicitly factorize a closed-form matrix: DeepWalk the log of the degree-normalized average of the first T random-walk transition powers, shifted by log b, and LINE the same with T = 1'
version: 1
tags:
- graphs-and-networks
- representation-learning
- representation-and-encoding
- analysis-and-evaluation
date: '2026-10-22'
source:
- LIT-tmpgtmmr
extends:
- THEORY-093
explains: []
summary: >-
  Qiu et al. (2018), [LIT-tmpgtmmr](../literature.d/LIT-tmpgtmmr.md) — apply Levy and Goldberg's SGNS optimum
  ([THEORY-093](THEORY-093.md)) to a random-walk corpus. As walks lengthen, pair counts
  converge to stationary-weighted transition powers, so DeepWalk's target is
  log(vol(G)/T · Σ_{r=1..T} (D⁻¹A)^r D⁻¹) − log b and LINE's is the T = 1
  case. A derivation, exact under free dot products, noise ∝ degree and
  infinitely long walks. It names the target, not what a 128-dimensional
  embedding trained on finite walks reaches.
---

# THEORY-tmpgaak8: Skip-gram node embeddings with negative sampling implicitly factorize a closed-form matrix: DeepWalk the log of the degree-normalized average of the first T random-walk transition powers, shifted by log b, and LINE the same with T = 1

## Source

Qiu et al. (2018), [LIT-tmpgtmmr](../literature.d/LIT-tmpgtmmr.md), read as [NOTE-tmpbwe6d](../notes.d/NOTE-tmpbwe6d.md).

## The account

Levy and Goldberg ([LIT-612](../literature.d/LIT-612.md)) showed that skip-gram with b negatives, when
each dot product is free, is optimized at w·c = log(#(w,c)·|D| /
(#(w)·#(c))) − log b ([THEORY-093](THEORY-093.md)). That is a statement about whatever corpus
produced the counts. Qiu et al. supply the corpus side for graphs, in
[LIT-tmpgtmmr](../literature.d/LIT-tmpgtmmr.md). In a walk on a connected, undirected, non-bipartite graph,
the fraction of pairs at distance r that are (w, c) converges in probability,
as the walk length grows, to (d_w / vol(G))·(P^r)_wc with P = D⁻¹A
(Theorem 2.1, by a law of large numbers for correlated draws). Averaging
over r = 1..T and both directions and substituting gives DeepWalk's target
(Theorem 2.3):

    log( vol(G)/T · Σ_{r=1..T} P^r D⁻¹ ) − log b

LINE(2nd) is derived directly in the same paper: its optimum is
log(vol(G)·D⁻¹AD⁻¹) − log b, which is the T = 1 case (Corollary 2.4).

The matrix inside the log has a spectral reading. With
D^(−1/2)AD^(−1/2) = UΛUᵀ, it is D^(−1/2)·U·((1/T)Σ Λ^r)·Uᵀ·D^(−1/2), so each
eigenvalue λ passes through f(λ) = (1/T)Σ λ^r. That filter keeps large
positive eigenvalues and shrinks negative and small ones, more strongly as T
grows (§3.1, Figure 1). A wider window therefore targets a lower-rank,
smoother matrix.

## Why `Active`

It is a derivation and it holds under its stated conditions, as [THEORY-093](THEORY-093.md)
does for words. The paper also tested a consequence that could have failed:
if the closed form is what DeepWalk approximates by sampling, computing it
and taking an SVD should do at least as well. NetMF (T = 10) did, on
BlogCatalog, PPI and Flickr with few labels (Table 3), and tied on Wikipedia
Macro-F1. That test is weaker than the derivation, for the reasons under
*Where it is weak*, and the account does not rest on it.

## What it explains

- **Why LINE and DeepWalk behave like relatives.** LINE is the window-1
  member of the same family. LINE's paper ([LIT-tmpkyvvg](../literature.d/LIT-tmpkyvvg.md)) described DeepWalk
  as also capturing second-order proximity, and found LINE(2nd) behind
  DeepWalk on its sparsest graphs, where one step reaches few contexts and
  a window of 10 reaches many
- **Why the window size acts like a smoothing knob.** The filter view says
  larger T emphasizes the top of the spectrum. The paper shows this on
  Cora's eigenvalues; it does not test what it does downstream beyond
  comparing T = 1 with T = 10
- **Why count-style and sampling-style graph embeddings can be compared at
  all.** As with words ([LIT-607](../literature.d/LIT-607.md)), they fit the same statistic and differ in
  weighting, truncation and rank

## Where it is weak

- **The target is not what training reaches.** The derivation lets every
  dot product take any value. At d = 128 the embedding is some weighted
  low-rank approximation of the matrix, as [THEORY-093](THEORY-093.md) says of words, and
  which one depends on the sampler
- **Infinite walks and stationary starts.** DeepWalk uses walks of length 40
  to 80 started uniformly; the paper's remark covers the start, not finite
  length
- **Noise ∝ degree.** LINE used degree^(3/4), and DeepWalk as published used
  hierarchical softmax, not negative sampling. The paper says the 3/4 case
  is similar without deriving it
- **node2vec is not covered in usable form.** The paper gives a closed form
  in the second-order walk's stationary distribution and transition tensor,
  without proof and without a matrix expression
- **The empirical check has a baseline problem.** The DeepWalk numbers NetMF
  beats are lower than DeepWalk's own on the same datasets ([LIT-tmpp6g0g](../literature.d/LIT-tmpp6g0g.md):
  36.00 against 29.32 Micro-F1 on BlogCatalog at 10%), and NetMF itself
  factorizes max(M, 1), not M
