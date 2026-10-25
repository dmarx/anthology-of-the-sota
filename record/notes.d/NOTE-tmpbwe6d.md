---
status: Read
paper: LIT-tmpgtmmr
title: 'NetMF'
version: 1
date: '2026-10-22'
summary: >-
  DeepWalk and LINE with negative sampling factorize closed-form matrices of
  random-walk transition powers, by Levy and Goldberg's argument applied to a
  walk corpus in the long-walk limit. Factorizing that matrix directly beats
  DeepWalk on three of four networks with few labels. Read in full,
  including the appendix proofs.
---

# NOTE-tmpbwe6d: NetMF

## Contribution

Closed forms for the matrices that DeepWalk, LINE and PTE implicitly
factorize, and a partial one for node2vec. It connects the DeepWalk matrix
to the normalized Laplacian's spectrum, and gives an explicit SVD-based
algorithm, NetMF, that computes the embedding without sampling walks.

## Key insight

**A random-walk corpus is a sampling estimate of a matrix you can write
down.** As walks lengthen, the fraction of (w, c) pairs at distance r
converges to (d_w / vol(G))·(P^r)_wc. Feed that into SGNS's shifted-PMI
optimum and DeepWalk's target is log(vol(G)/T · Σ P^r D⁻¹) − log b. Averaging
the first T powers is a low-pass filter on the graph's spectrum, so a larger
window keeps fewer, larger eigen-directions.

## Key results

- LINE(2nd) factorizes log(vol(G)·D⁻¹AD⁻¹) − log b (Eq. 4); DeepWalk
  factorizes the T-step generalization (Theorem 2.3); LINE is DeepWalk with
  T = 1 (Corollary 2.4)
- Convergence is in probability as walk length L → ∞, by a law of large
  numbers for the correlated walk (Theorem 2.1, appendix)
- NetMF (T = 10) against DeepWalk, Micro-F1 at 10% labeled: BlogCatalog
  38.36 against 29.32, PPI 18.16 against 12.05, Wikipedia 46.21 against
  36.08; Flickr at 1%: 29.95 against 26.21 (Table 3)
- NetMF (T = 1) loses to LINE on Flickr, by 1.31 Micro-F1 and 2.88
  Macro-F1, and on Wikipedia Macro-F1 (Table 3)

## Limitations

- **The assumptions are the SGNS ones plus a limit.** Dot products free (so
  enough dimensions), noise ∝ degree, walks infinitely long and started from
  the stationary distribution of a connected, non-bipartite, undirected
  graph. Practical DeepWalk has short walks, d = 128 and, as shipped,
  hierarchical softmax
- **NetMF factorizes max(M, 1)**, a truncation borrowed from shifted PPMI,
  not M itself, and the large-T version uses a top-h eigen-approximation
- **The DeepWalk baseline is weaker than DeepWalk's own reported numbers**
  on the same datasets (29.32 against 36.00 on BlogCatalog at 10%), with no
  explanation; no spreads are reported
- **node2vec's result is stated without proof** and without a matrix form
- **Dense |V|×|V| matrices**, so the explicit method does not scale the way
  the sampled ones do
