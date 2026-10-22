---
status: Active
title: 'Deep Graph Infomax'
version: 1
tags:
- graphs-and-networks
- representation-learning
- representation-and-encoding
date: '2026-10-22'
published: '2018-09-27'
arxiv: '1809.10341'
first_author: 'Veličković'
keywords:
- 'dgi'
- 'mutual-information'
- 'contrastive-learning'
- 'self-supervised'
- 'gcn'
- 'node-classification'
implementations: []
compared_against:
- LIT-tmpp6g0g
- LIT-582
summary: >-
  Veličković, Fedus, Hamilton, Liò, Bengio, Hjelm (ICLR 2019),
  [ARXIV-1809.10341](https://arxiv.org/abs/1809.10341). Train a GNN encoder without labels by having a bilinear
  discriminator tell each node's embedding paired with the graph's mean
  summary from embeddings of a corrupted graph, made by shuffling node
  features across positions. A linear probe on the embeddings reaches 82.3%
  on Cora against 81.5% reported for supervised GCN. A randomly initialized
  encoder of the same shape is almost as good on the inductive tasks: 0.933
  against 0.940 micro-F1 on Reddit, 0.626 against 0.638 on PPI.
---

# LIT-tmp2xwx2: Deep Graph Infomax

Veličković, Fedus, Hamilton, Liò, Bengio, Hjelm, Cambridge, Mila, Google
Brain, McGill and Microsoft Research (ICLR 2019) — [ARXIV-1809.10341](https://arxiv.org/abs/1809.10341)

## Key takeaways

- **The objective** (§3.2, Eq. 1): binary cross-entropy for a discriminator
  D(h_i, s) = σ(h_iᵀWs), positives being node embeddings of the real graph
  with its summary s = σ(mean h_i), negatives being node embeddings of a
  corrupted graph with the same summary. The authors relate it to the
  Jensen-Shannon estimate of mutual information, following Deep InfoMax
- **The corruption** (§4.2): keep the adjacency matrix and shuffle the rows
  of the feature matrix, so each node is placed somewhere else in the same
  graph. On PPI, where over 40% of nodes have all-zero features, a different
  training graph is the negative instead
- **Theory** (§3.3): for finite input sets with an injective readout,
  minimizing the discriminator's error maximizes MI between input and
  summary (Theorem 1) and between a node's neighborhood and its embedding
  (Theorem 2). The authors call this "some intuition"
- **Transductive** (Table 2, accuracy over 50 runs, one-layer GCN encoder of
  width 512): Cora 82.3 ± 0.6, Citeseer 71.8 ± 0.7, Pubmed 76.8 ± 0.6. The
  supervised GCN figures, copied from Kipf and Welling, are 81.5, 70.3 and
  79.0. DeepWalk with features concatenated: 70.7, 51.4, 74.3
- **Inductive** (Table 2, micro-F1): Reddit 0.940 ± 0.001 against 0.908 for
  the best unsupervised GraphSAGE; PPI 0.638 ± 0.002 against 0.502. The
  supervised state of the art on PPI is 0.969
- **Random-Init** (Table 2): the same encoder with random weights and a
  linear probe scores 69.3, 61.9 and 69.6 transductively, and 0.933 on
  Reddit and 0.626 on PPI
- **Other corruptions** (Appendix C, Figures 7–8): flipping adjacency
  entries at rate ρ also works once ρ is large enough, and no better than
  feature shuffling

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

**It is `compared_against` DeepWalk ([LIT-tmpp6g0g](LIT-tmpp6g0g.md)) and GCN ([LIT-582](LIT-582.md)).**
DeepWalk's numbers, and GCN's, are taken from Kipf and Welling; DGI runs
only DeepWalk with features concatenated itself, and beats it by 11.6 points
on Cora and 20.4 on Citeseer. Against supervised GCN, DGI is 0.8 ahead on
Cora, 1.5 on Citeseer and 2.2 behind on Pubmed. Those are single figures on
the one fixed Planetoid split, which is the evaluation [LIT-581](LIT-581.md) shows
reorders GNNs ([SOTA-350](../practices.d/SOTA-350.md)).

**What the headline does not say.** "Competitive with supervised learning"
is true transductively. On the inductive tasks the unsupervised gain over
an untrained encoder is 0.007 micro-F1 on Reddit and 0.012 on PPI, and the
paper's own comparison point there is GraphSAGE's unsupervised random-walk
objective, which Random-Init already beats. The authors draw the right
conclusion, that the random-walk objectives may have been adding little,
but the abstract does not.

**Its contrastive design is close to CPC's** ([LIT-589](LIT-589.md)): the paper describes
its bilinear scoring function as similar to CPC's, and contrasts its
global-against-local objective with CPC's prediction between parts. GraphCL ([LIT-tmp1wiuo](LIT-tmp1wiuo.md)) later
contrasts augmented views of whole graphs instead of node against summary.

Read — [NOTE-tmpz3kcn](../notes.d/NOTE-tmpz3kcn.md).
