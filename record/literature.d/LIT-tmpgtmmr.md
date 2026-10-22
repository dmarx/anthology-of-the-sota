---
status: Active
title: 'Network Embedding as Matrix Factorization: Unifying DeepWalk, LINE, PTE, and node2vec'
version: 1
tags:
- graphs-and-networks
- representation-and-encoding
- analysis-and-evaluation
date: '2026-10-22'
published: '2017-10-09'
arxiv: '1710.02971'
first_author: 'Qiu'
keywords:
- 'netmf'
- 'implicit-matrix-factorization'
- 'skip-gram'
- 'graph-laplacian'
- 'random-walks'
- 'node-embedding'
implementations: []
extends:
- LIT-612
compared_against:
- LIT-tmpp6g0g
- LIT-tmpkyvvg
summary: >-
  Qiu, Dong, Ma, Li, Wang, Tang (WSDM 2018), [ARXIV-1710.02971](https://arxiv.org/abs/1710.02971). Carries Levy
  and Goldberg's SGNS result to graphs. As walks grow long, DeepWalk with
  negative sampling factorizes log(vol(G)/T · Σ_{r=1..T} (D⁻¹A)^r D⁻¹) −
  log b, and LINE is the case T = 1. Computing that matrix, truncating it at
  log 1 and taking an SVD (NetMF) beats DeepWalk on BlogCatalog, PPI and
  Flickr with few labels, by up to 50.71% relative Micro-F1 on PPI at 10%.
  It loses to LINE on Flickr and ties DeepWalk on Wikipedia Macro-F1.
---

# LIT-tmpgtmmr: Network Embedding as Matrix Factorization: Unifying DeepWalk, LINE, PTE, and node2vec

Qiu, Dong, Ma, Li, Wang, Tang, Tsinghua University and Microsoft Research
(WSDM 2018) — [ARXIV-1710.02971](https://arxiv.org/abs/1710.02971)

## Key takeaways

- **LINE** (§2.1, Eq. 4): with noise ∝ degree and dot products free, setting
  the per-pair gradient of LINE(2nd) to zero gives
  x_i·y_j = log(vol(G)·A_ij / (b·d_i·d_j)), so it factorizes
  log(vol(G)·D⁻¹AD⁻¹) − log b
- **DeepWalk** (§2.2, Theorems 2.1–2.3): co-occurrence counts in a walk
  converge in probability, as the walk length L → ∞, to stationary-weighted
  r-step transition probabilities. Plugging those into Levy and Goldberg's
  shifted PMI gives log(vol(G)/T · Σ_{r=1..T} P^r D⁻¹) − log b, with
  P = D⁻¹A and window T. LINE is the case T = 1 (Corollary 2.4), and PTE is
  a joint factorization of three such matrices
- **node2vec** (§2.3): a closed form in terms of the second-order walk's
  stationary distribution and transition tensor, stated without proof and
  without a matrix form
- **A spectral reading** (§3.1, Figure 1): the averaged powers act as a
  filter f(x) = (1/T)Σ x^r on the eigenvalues of D^(−1/2)AD^(−1/2), keeping
  large positive ones and suppressing the rest more strongly as T grows. On
  Cora the smallest eigenvalue −0.971 is filtered out
- **NetMF** (§3.2, Algorithms 3–4): form M, replace it with max(M, 1) as in
  shifted PPMI, take the log and an SVD. For large T, approximate M with the
  top-h eigenpairs (h = 256, or 16,384 on Flickr), with an error bound
  (Theorem 3.5)
- **Results** (Table 3, Micro/Macro-F1 %): NetMF (T = 10) against DeepWalk
  at 10% labeled: BlogCatalog 38.36/22.90 against 29.32/18.38, PPI
  18.16/14.32 against 12.05/10.29, Wikipedia 46.21/8.38 against 36.08/8.38.
  At 1% of Flickr, 29.95/13.50 against 26.21/12.43. NetMF (T = 1) against
  LINE(2nd) gains on BlogCatalog, PPI and Wikipedia Micro-F1 and loses on
  Flickr (23.87/6.44 against 25.18/9.32)

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

**It `extends` Levy and Goldberg ([LIT-612](LIT-612.md))**, whose shifted-PMI optimum for
SGNS ([THEORY-093](../theory.d/THEORY-093.md)) is the step every derivation here starts from, and which
the paper names as its tool. The new work is the graph-side half: showing
that a random-walk corpus's PMI converges to a closed form in A and D. So
the bearing of the word-embedding record is direct. Levy, Goldberg and
Dagan ([LIT-607](LIT-607.md)) found count methods match SGNS once the settings are
aligned; NetMF finds an explicit factorization matches or beats the
sampled one on three of four networks. It sources [THEORY-tmpgaak8](../theory.d/THEORY-tmpgaak8.md), which
`extends` [THEORY-093](../theory.d/THEORY-093.md).

**It is `compared_against` DeepWalk ([LIT-tmpp6g0g](LIT-tmpp6g0g.md)) and LINE
([LIT-tmpkyvvg](LIT-tmpkyvvg.md))**, in the multi-label protocol DeepWalk introduced, at
d = 128 for every method. It does not compare against node2vec, though it
uses node2vec's datasets.

**What the headline does not say.** "Up to 50%" is relative, on PPI at 10%
labeled, where the absolute Micro-F1 is 18.16 against 12.05. The DeepWalk
numbers here are well below DeepWalk's own (29.32 against 36.00 on
BlogCatalog at 10%, and 26.21 against 32.4 on Flickr at 1%), the paper does
not say why, and NetMF's Flickr result is below DeepWalk's self-reported
one. No spreads are reported. The derivation assumes negative sampling with
noise ∝ degree, where DeepWalk shipped with hierarchical softmax and LINE
used degree^(3/4), and the paper says a similar result holds for the
latter without deriving it.

Read — [NOTE-tmpbwe6d](../notes.d/NOTE-tmpbwe6d.md).
