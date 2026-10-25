---
number: 416
status: Read
formerly:
- NOTE-tmpvdswa
paper: 'LIT-826'
title: 'GAT'
version: 1
date: '2026-10-22'
summary: >-
  Masked multi-head self-attention over first-order neighbors beats GCN by
  about 1.5 points on Cora and Citeseer on the single Planetoid split. On
  unseen PPI graphs, learned attention beats the same model with constant
  weights, 0.973 against 0.934 micro-F1, which is the paper's one clean
  ablation of attention. Read in full.
---

# NOTE-416: GAT

## Contribution

A graph layer that weights each neighbor by a learned, feature-dependent
score, computed locally per edge. It needs neither the Laplacian's
eigenbasis nor the whole graph up front, so the same layer serves
transductive and inductive tasks and directed graphs.

## Key insight

**Let the features decide how much each neighbor counts.** GCN fixes the
weights by degree and GraphSAGE samples neighbors uniformly. GAT learns a
softmax over the full neighborhood, so the aggregation is anisotropic at
GCN's cost.

## Key results

- Cora / Citeseer / Pubmed, mean ± sd over 100 runs (Table 2): GAT 83.0 ±
  0.7 / 72.5 ± 0.7 / 79.0 ± 0.3, GCN-64 re-run 81.4 ± 0.5 / 70.9 ± 0.5 /
  79.0 ± 0.3, MLP 55.1 / 46.5 / 71.4. Other baselines are copied from
  earlier papers
- PPI micro-F1, 10 runs (Table 3): GAT 0.973 ± 0.002, Const-GAT 0.934 ±
  0.006, enlarged GraphSAGE-LSTM 0.768, published GraphSAGE best 0.612
- Pubmed, with 60 training labels, needed 8 output heads and stronger L2
  of 0.001

## Limitations

- **One split.** Every citation-graph number uses the Planetoid split, and
  the margins over GCN are 1–2 standard deviations
- **Attention is ablated only on PPI.** On the citation graphs, the
  comparison is to GCN, which also differs in hidden size, dropout on the
  coefficients and the number of heads
- **The PPI gap over GraphSAGE is mostly not attention.** Const-GAT
  already reaches 0.934 against 0.768, through full neighborhoods, a larger
  model and skip connections
- **Interpretation of the attention weights is left to future work**,
  despite being listed as a benefit
