---
status: Active
title: 'DeepWalk: Online Learning of Social Representations'
version: 1
tags:
- graphs-and-networks
- representation-learning
- representation-and-encoding
date: '2026-10-22'
published: '2014-03-26'
arxiv: '1403.6652'
first_author: 'Perozzi'
keywords:
- 'deepwalk'
- 'random-walks'
- 'skip-gram'
- 'node-embedding'
- 'network-classification'
implementations: []
summary: >-
  Perozzi, Al-Rfou, Skiena (KDD 2014), [ARXIV-1403.6652](https://arxiv.org/abs/1403.6652). Treat truncated
  random walks on a graph as sentences and train skip-gram with hierarchical
  softmax on them; the word vectors are node embeddings. With one-vs-rest
  logistic regression on top, they beat spectral, modularity, EdgeCluster
  and wvRN features when few nodes are labeled: Micro-F1 32.4 against 27.43
  for the best baseline at 1% of Flickr, and 37.95 against 26.79 at 1% of
  YouTube. On BlogCatalog, spectral clustering is ahead from 70% labeled on.
compared_against:
- LIT-tmp2xwx2
- LIT-tmp3s7q9
- LIT-tmpgtmmr
- LIT-tmpkyvvg
extended_by:
- LIT-tmp3s7q9
---

# LIT-tmpp6g0g: DeepWalk: Online Learning of Social Representations

Perozzi, Al-Rfou, Skiena, Stony Brook University (KDD 2014) —
[ARXIV-1403.6652](https://arxiv.org/abs/1403.6652)

## Key takeaways

- **The method** (§4, Algorithms 1–2): start γ truncated random walks of
  length t from every vertex, slide a window of size w over each walk, and
  update a |V|×d embedding matrix with skip-gram, using hierarchical softmax
  over a Huffman tree. The walks are the corpus and the vertices are the
  vocabulary. The main tables use γ = 80, w = 10, d = 128
- **The motivating observation** (§3.2, Figure 2): vertex frequencies in
  short random walks on a scale-free graph follow a power law, as word
  frequencies do, so tools built for language should transfer
- **BlogCatalog** (Table 2, Micro-F1 %): 36.00 at 10% labeled against 31.06
  for spectral clustering. The lead narrows as labels increase, and spectral
  clustering is ahead from 70% (41.66 against 41.50) to 90% (42.62 against
  42.00). On Macro-F1, spectral clustering is ahead from 30% labeled on
- **Flickr and YouTube** (Tables 3–4): Micro-F1 at 1% labeled is 32.4 on
  Flickr, against 27.43 for spectral clustering, and 37.95 on YouTube,
  against 26.79 for wvRN and 23.90 for EdgeCluster. Spectral clustering and
  modularity could not run on YouTube's 1.1M nodes
- **Sensitivity** (Figure 5): most of the benefit comes by γ = 30 walks per
  node, and the best dimension depends on how many labels there are
- **Parallel and online** (§4.3, Figure 4): lock-free asynchronous SGD over
  up to 8 workers speeds training without loss of Micro-F1

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

**It is the first of the skip-gram node embeddings.** LINE ([LIT-tmpkyvvg](LIT-tmpkyvvg.md))
and node2vec ([LIT-tmp3s7q9](LIT-tmp3s7q9.md)) both compare against it, and node2vec contains
its walk as the setting p = q = 1. NetMF ([LIT-tmpgtmmr](LIT-tmpgtmmr.md)) shows that its
negative-sampling form factorizes a closed-form matrix built from powers of
the random-walk transition matrix, which [THEORY-tmpgaak8](../theory.d/THEORY-tmpgaak8.md) states. The
word-vector result that analysis builds on is Levy and Goldberg's ([LIT-612](LIT-612.md),
[THEORY-093](../theory.d/THEORY-093.md)).

**What the headline does not say.** "Up to 10% higher F1 when labeled data
is sparse" is the sparse end of the curves. The baselines' numbers are taken
from Tang and Liu's papers at d = 500, no spreads are reported across the 10
splits, and on BlogCatalog with most nodes labeled a spectral embedding is as
good or better. The baselines are unsupervised feature extractors and one
relational classifier; no GNN existed yet to compare against.

**Later papers report lower numbers for it.** NetMF gives DeepWalk 29.32
Micro-F1 on BlogCatalog with 10% labeled and 26.21 on Flickr with 1%, where
this paper reports 36.00 and 32.4 under what both describe as the same
protocol. Neither paper explains the gap.

**A baseline for a GNN-based unsupervised encoder.** Deep Graph Infomax
([LIT-tmp2xwx2](LIT-tmp2xwx2.md)) reruns DeepWalk with node features concatenated and beats
it by 11.6 points on Cora and 20.4 on Citeseer. DeepWalk embeds structure
alone, so much of that gap is the features a GCN encoder can use.

Read — [NOTE-tmpdmw0f](../notes.d/NOTE-tmpdmw0f.md).
