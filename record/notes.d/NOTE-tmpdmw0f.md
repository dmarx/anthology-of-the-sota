---
status: Read
paper: LIT-tmpp6g0g
title: 'DeepWalk'
version: 1
date: '2026-10-22'
summary: >-
  Skip-gram over truncated random walks gives node features that beat
  spectral and modularity features for multi-label classification when few
  nodes are labeled, and lose their lead on BlogCatalog as labels grow. Read
  in full.
---

# NOTE-tmpdmw0f: DeepWalk

## Contribution

The first transfer of word2vec's skip-gram to graphs: random walks as
sentences, vertices as words. It made node embedding an online, parallel,
local computation, where the spectral methods it replaced needed an
eigendecomposition of the whole graph.

## Key insight

**A short random walk is a sample of a node's neighborhood, and skip-gram
turns co-occurrence in samples into geometry.** Nodes that appear in each
other's walks often end up with similar vectors. The paper motivates the
transfer by a shared power law in frequencies, which is an analogy, not a
derivation; the derivation came later from NetMF.

## Key results

- BlogCatalog Micro-F1: 36.00 at 10% labeled against 31.06 for spectral
  clustering; spectral is ahead from 70% labeled (Table 2)
- Flickr at 1% labeled: 32.4 against 27.43; YouTube at 1%: 37.95 against
  26.79 for wvRN (Tables 3–4)
- About 30 walks per node give most of the benefit (Figure 5)
- 8 asynchronous workers give a near-linear speedup with no accuracy loss
  (Figure 4)

## Limitations

- **Baseline numbers are copied** from earlier papers, at d = 500 against
  DeepWalk's 128, and no spreads are given across the 10 splits
- **Hierarchical softmax, not negative sampling.** Later analyses
  ([LIT-tmpgtmmr](../literature.d/LIT-tmpgtmmr.md)) treat the negative-sampling variant
- **Only node classification** on three social networks, with a linear
  probe; link prediction is mentioned as an application, not tested
- **The power-law argument is illustrative.** Nothing tests whether it is
  why the method works
