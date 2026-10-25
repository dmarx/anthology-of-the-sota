---
number: 402
status: Read
formerly:
- NOTE-tmpgkme7
paper: 'LIT-811'
title: 'Survey on oversmoothing'
version: 1
date: '2026-10-22'
summary: >-
  Over-smoothing defined as exponential decay of a node-similarity measure,
  with Dirichlet energy as the canonical one and Mean Average Distance ruled
  out. A deep GCN with a bias keeps its Dirichlet energy and still loses
  accuracy with depth, so avoiding over-smoothing is necessary and not
  sufficient. Read in full.
---

# NOTE-402: Survey on oversmoothing

## Contribution

A common definition for a phenomenon that had been measured several
inconsistent ways, and a demonstration that preventing it does not by
itself make deep GNNs work.

## Key insight

**Keeping the nodes apart is not the same as keeping them informative.**
A bias term is enough to stop the features collapsing to one value, and
the deep network is still no better. Over-smoothing is one way a deep GNN
fails, not the only one.

## Key results

- Definition 1: over-smoothing is μ(X^n) ≤ C₁e^{−C₂n} for a measure μ that
  vanishes exactly on constant features and is subadditive
- Dirichlet energy qualifies. MAD does not, since it is zero for any
  one-dimensional features of one sign
- GCN, GAT and GraphSAGE over-smooth exponentially on Texas, Cora and
  Cornell5, with random Gaussian inputs (Figure 1)
- DropEdge and Res-GCN still over-smooth. PairNorm, GCNII, GraphCON and
  G² do not (Figure 2)
- Trained on Cora: GCN with a bias holds Dirichlet energy near 1 and loses
  accuracy with depth like the plain GCN. PairNorm drops past 32 layers.
  G² holds accuracy to 128 layers (Figure 3)

## Limitations

- **Qualitative.** One measure, figures without tabulated numbers, and no
  stated tuning protocol for the methods compared
- **Figures 1–2 use random inputs**, and the text does not say whether
  those networks were trained
- **One trained dataset** for the necessary-not-sufficient result
- **The authors' own methods** (GraphCON, G²) are among those that come
  out best
