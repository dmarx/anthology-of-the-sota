---
status: Active
title: 'Graph Attention Networks'
version: 1
tags:
- graphs-and-networks
- model-architecture
- attention-techniques
date: '2026-10-22'
published: '2017-10-30'
arxiv: '1710.10903'
first_author: 'Veličković'
keywords:
- 'gat'
- 'graph-attention'
- 'masked-self-attention'
- 'multi-head-attention'
- 'node-classification'
implementations: []
compared_against:
- LIT-582
- LIT-tmp77hqw
summary: >-
  Veličković, Cucurull, Casanova, Romero, Liò, Bengio (ICLR 2018),
  [ARXIV-1710.10903](https://arxiv.org/abs/1710.10903). Each node attends over its first-order neighbors with
  softmax-normalized, multi-head attention scores, so neighbors get
  learned weights instead of fixed degree-based ones. Over 100 runs on the
  Planetoid split it scores 83.0% on Cora and 72.5% on Citeseer against
  81.4% and 70.9% for a 64-unit GCN, and ties on Pubmed. On unseen PPI
  graphs it reaches micro-F1 0.973, against 0.934 for the same model with
  constant attention.
---

# LIT-tmpislka: Graph Attention Networks

Veličković, Cucurull, Casanova, Romero, Liò, Bengio, Cambridge, UAB and
Mila (ICLR 2018) — [ARXIV-1710.10903](https://arxiv.org/abs/1710.10903)

## Key takeaways

- **The layer** (Eqs. 1–4): eᵢⱼ = LeakyReLU(aᵀ[Whᵢ ‖ Whⱼ]), normalized by a
  softmax over j ∈ N(i) including i, and hᵢ′ = σ(Σⱼ αᵢⱼ Whⱼ). Cost is
  O(|V|FF′ + |E|F′) per head, on par with GCN, with no eigendecomposition
- **Multi-head** (Eqs. 5–6): K heads are concatenated in hidden layers and
  averaged in the output layer, "to stabilize the learning process"
- **Transductive** (Table 2, mean ± sd over 100 runs, Planetoid split):
  Cora 83.0 ± 0.7, Citeseer 72.5 ± 0.7, Pubmed 79.0 ± 0.3. The authors'
  own GCN-64 run gets 81.4 ± 0.5, 70.9 ± 0.5 and 79.0 ± 0.3
- **Inductive** (Table 3, 10 runs, two unseen PPI test graphs): GAT 0.973 ±
  0.002 micro-F1, Const-GAT (same architecture, all neighbors weighted
  equally) 0.934 ± 0.006, the best GraphSAGE they could build 0.768
- **Heavy regularization on the citation graphs**: dropout 0.6 on inputs
  and on the attention coefficients, and L2 of 0.0005. The architecture was
  tuned on Cora and reused for Citeseer

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

It is `compared_against` GCN ([LIT-582](LIT-582.md)): the authors re-ran GCN with 64
hidden units over 100 runs and report GAT 1.6 points ahead on Cora (83.0
against 81.4), 1.6 ahead on Citeseer and level on Pubmed, all on the single
Planetoid split. It is also `compared_against` GraphSAGE ([LIT-tmp77hqw](LIT-tmp77hqw.md))
on PPI, where it beats the published GraphSAGE results (best 0.612) and a
three-layer GraphSAGE-LSTM the authors enlarged themselves (0.768).

**Which comparison isolates attention.** Only the Const-GAT row does:
same architecture, same training, constant weights, and it gives 0.973
against 0.934. The 20.5% margin over GraphSAGE also changes the full
versus sampled neighborhood, the depth, the width and the skip
connections at once. The Cora and Citeseer margins rest on one split, and
under 100 random splits with a shared protocol GAT ranks fourth of four
GNNs, mostly because 138 of 2,000 runs collapse on Amazon Photo
([LIT-581](LIT-581.md)). In the parameter-matched benchmark filed alongside this note
([LIT-tmp8wx7k](LIT-tmp8wx7k.md)), the authors report anisotropic aggregation, GAT among
it, ahead of isotropic aggregation on most datasets at 100k parameters.
GAT itself trails vanilla GCN on ZINC there (MAE 0.475 against 0.459).

Read — [NOTE-tmpvdswa](../notes.d/NOTE-tmpvdswa.md).
