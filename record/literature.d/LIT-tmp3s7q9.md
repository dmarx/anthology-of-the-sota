---
status: Active
title: 'node2vec: Scalable Feature Learning for Networks'
version: 1
tags:
- graphs-and-networks
- representation-learning
- representation-and-encoding
date: '2026-10-22'
published: '2016-07-03'
arxiv: '1607.00653'
first_author: 'Grover'
keywords:
- 'node2vec'
- 'biased-random-walks'
- 'homophily'
- 'structural-equivalence'
- 'link-prediction'
- 'node-embedding'
implementations: []
extends:
- LIT-tmpp6g0g
compared_against:
- LIT-tmpp6g0g
- LIT-tmpkyvvg
summary: >-
  Grover and Leskovec (KDD 2016), [ARXIV-1607.00653](https://arxiv.org/abs/1607.00653). DeepWalk with a
  second-order biased walk: a return parameter p and an in-out parameter q
  move the walk between BFS-like and DFS-like exploration, and p = q = 1 is
  DeepWalk. With p and q picked by grid search on 10% of the labels, Macro-F1
  at 50% labeled is 0.2581 against DeepWalk's 0.2110 on BlogCatalog and
  0.1552 against 0.1274 on Wikipedia, and 0.1791 against 0.1768 on PPI. For
  link prediction, a Hadamard product of node vectors beats the common
  neighbor heuristics, and DeepWalk ties it on Facebook at 0.9680 AUC.
---

# LIT-tmp3s7q9: node2vec: Scalable Feature Learning for Networks

Grover and Leskovec, Stanford University (KDD 2016) — [ARXIV-1607.00653](https://arxiv.org/abs/1607.00653)

## Key takeaways

- **The walk** (§3.2): having just stepped t → v, the unnormalized
  probability of stepping to x is w_vx/p if x = t, w_vx if x is a neighbor
  of t, and w_vx/q otherwise. High q keeps the walk local (BFS-like, which
  the authors tie to structural equivalence); low q pushes it outward
  (DFS-like, tied to homophily). Transition probabilities are precomputed
  and sampled by alias tables, at O(a²|V|) memory for average degree a
- **The comparison is at an equal sample budget** (§4.2): DeepWalk is
  switched to negative sampling, LINE is run for k epochs, and all use
  d = 128, r = 10 walks of l = 80, context k = 10. p and q are chosen by
  10-fold cross-validation on 10% labeled data over {0.25, 0.5, 1, 2, 4}²
- **Node classification** (Table 2, Macro-F1, 50% labeled): BlogCatalog
  0.2581 (DeepWalk 0.2110, LINE 0.0784, spectral 0.0405), PPI 0.1791
  (0.1768, 0.1447, 0.0681), Wikipedia POS 0.1552 (0.1274, 0.1164, 0.0395).
  The best p, q were (0.25, 0.25), (4, 1) and (4, 0.5). Figure 4 gives the
  largest gain over DeepWalk as 26.7% on BlogCatalog at 70% labeled
- **Link prediction** (Table 4, AUC, Hadamard operator): Facebook 0.9680
  (DeepWalk 0.9680), PPI 0.7719 (0.7441), arXiv 0.9366 (0.9340). The best
  heuristic, Adamic-Adar, scores 0.8289, 0.7126 and 0.8315. With the
  Weighted-L1 and L2 operators LINE beats node2vec on PPI and arXiv
- **Robustness and scale** (Figures 5–6): Macro-F1 falls roughly linearly
  as edges are removed or added at random on BlogCatalog. One million nodes
  embed in under four hours

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

**It `extends` DeepWalk ([LIT-tmpp6g0g](LIT-tmpp6g0g.md))**, whose uniform walk is the setting
p = q = 1, and is `compared_against` both DeepWalk and LINE ([LIT-tmpkyvvg](LIT-tmpkyvvg.md)),
re-run at the same number of samples. Its BlogCatalog gain over DeepWalk is
real at that budget. On PPI the selected walk is "virtually
indistinguishable" from DeepWalk's, in the authors' words, and the gain is
1.3%. LINE does far worse here than in its own paper; the authors put that
down to LINE not reusing samples, which the equal-budget rule penalizes.

**What the headline does not say.** node2vec gets a 25-point grid over p and
q selected on labels, and DeepWalk is one point in that grid with no search
of its own. That is the method's claim, that the search is worth having, but
it also means part of the gain is a tuning budget, the confound [SOTA-350](../practices.d/SOTA-350.md)
names for GNNs. There are no spreads in the tables, only a statement that
results are significant at p < 0.01 over 10 seeds.

**NetMF covers it only partly.** Qiu et al. ([LIT-tmpgtmmr](LIT-tmpgtmmr.md)) give a closed
form for what node2vec factorizes, in terms of the stationary distribution
and transition tensor of the second-order walk, but leave its matrix form
open, so [THEORY-tmpgaak8](../theory.d/THEORY-tmpgaak8.md) states the account for DeepWalk and LINE only.

Read — [NOTE-tmpx964a](../notes.d/NOTE-tmpx964a.md).
