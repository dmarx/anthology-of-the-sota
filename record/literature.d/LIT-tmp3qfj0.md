---
status: Active
title: 'Open Graph Benchmark: Datasets for Machine Learning on Graphs'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
- data-pipeline
- biomolecular-modeling
date: '2026-10-22'
published: '2020-05-02'
arxiv: '2005.00687'
first_author: 'Hu'
keywords:
- 'ogb'
- 'benchmark'
- 'realistic-splits'
- 'scaffold-split'
- 'out-of-distribution'
- 'virtual-node'
implementations:
- ogb
summary: >-
  Hu, Fey, Zitnik, Dong, Ren, Liu, Catasta, Leskovec (NeurIPS 2020),
  [ARXIV-2005.00687](https://arxiv.org/abs/2005.00687). Fifteen node, link and graph datasets, from 4k to 111M
  nodes, each with an application-driven split (time, species, scaffold,
  protein target, project) and a fixed evaluator. On every dataset where
  the authors also ran a random split of the same proportions, the same
  model scores higher on it: 88.2 against 78.5% on ogbn-products, 82.7
  against 77.1 ROC-AUC on ogbg-molhiv, 92.9 against 70.4% on ogbg-ppa.
---

# LIT-tmp3qfj0: Open Graph Benchmark: Datasets for Machine Learning on Graphs

Hu, Fey, Zitnik, Dong, Ren, Liu, Catasta, Leskovec, Stanford, TU Dortmund,
Harvard and Microsoft Research (NeurIPS 2020) — [ARXIV-2005.00687](https://arxiv.org/abs/2005.00687)

## Key takeaways

- **The complaint** (§1–2): Cora, Citeseer and Pubmed have 2,700–20,000
  nodes, and, citing Zou et al., 42% of Cora's nodes leak label
  information through their features. PPI, Reddit and Amazon2M train on
  83%, 65% and 90% of nodes. TU graph sets mostly hold under 1,000 graphs, and protocols vary between
  papers
- **Splits by application** (Table 2): sales rank for products, species for
  proteins, publication year for arXiv, MAG and collaboration, protein
  target for drug interactions, molecular scaffold for MoleculeNet sets,
  GitHub project for code
- **Random against realistic, same model and ratio**: ogbn-products
  GraphSAGE 88.20 against 78.50%, ogbn-proteins GraphSAGE 87.83 against
  77.68 ROC-AUC, ogbn-arxiv GCN 73.54 against 71.74%, ogbl-ddi GraphSAGE
  80.88 against 53.90 Hits@20, ogbg-molhiv GIN 82.73 against 77.07,
  ogbg-molpcba 34.40 against 27.03 AP, ogbg-moltox21 86.03 against 77.57,
  ogbg-ppa 92.91 against 70.37%, ogbg-code2 21.64 against 15.95 F1. On the
  random splits the train–test gap nearly vanishes, about 1 point on
  products and 0.27 on proteins
- **Baselines** (Tables 4–18): 10 seeds each, mean and unbiased sd of the
  run with the best validation score. On ogbn-proteins only GraphSAGE beats
  an MLP. On ogbl-ppa, and on ogbl-collab when validation edges are not
  used at test time, GNNs lose to node2vec or matrix factorization, which
  the authors attribute to missing positional information
- **Virtual node and features** (Tables 15–17, Appendix A): GIN with a
  virtual node is best on ogbg-ppa (70.37), and with the additional atom
  and bond features as well on molhiv (77.07) and molpcba (27.03). On the
  10 further MoleculeNet sets, the virtual node leaves GIN comparable or
  better on 9, and so do the features

## Standing in the anthology

<!-- inactive-ok-block: SOTA-tmpzd1sw — Proposed, and named as the practice this paper sources, not relied on -->
**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It sources [SOTA-tmp2qn9u](../practices.d/SOTA-tmp2qn9u.md), on evaluating under
application-driven splits, and is the main evidence in [SOTA-tmpzd1sw](../practices.d/SOTA-tmpzd1sw.md), on
virtual nodes.

**It fixes the split, which [SOTA-350](../practices.d/SOTA-350.md) already allows for.** OGB answers
[LIT-581](LIT-581.md)'s split-sensitivity problem by making one realistic split
official and asking for many seeds, not by averaging over random splits.
Its baselines are lightly tuned, with fixed width and depth and dropout
chosen from {0, 0.5}, so they are reference points, not a ranking of
architectures.

**The hedge on "realistic".** That a time or scaffold split is the
deployment distribution is argued per dataset, not measured. What the
paper measures is that random splits score higher for the same model and
proportions, every time it checks. A virtual node is the MPNN paper's
master node ([LIT-tmpk1b2y](LIT-tmpk1b2y.md)).

Read — [NOTE-tmpxapd8](../notes.d/NOTE-tmpxapd8.md).
