---
status: Read
paper: 'LIT-tmp8wx7k'
title: 'Benchmarking GNNs'
version: 1
date: '2026-10-22'
summary: >-
  A budget-matched benchmark of message-passing and WL-style GNNs on twelve
  medium-scale datasets, four seeds each. Laplacian eigenvector positional
  encodings, with random sign flips, help message-passing GNNs most where
  nodes are anonymous. On small TU datasets a second seed reorders the
  models. The v5 (2022) text was read: main text and Appendices C–H in
  full, Appendix B's layer equations skimmed, I–J not read.
---

# NOTE-tmpjnifj: Benchmarking GNNs

## Contribution

A shared codebase and dataset collection where GNNs are compared at equal
parameter counts under one training schedule, and the positional-encoding
idea that came out of using it.

## Key insight

**Hold capacity and training fixed, and see which mechanism still wins.**
At 100k parameters and one schedule, the differences that survive point
at mechanisms: gating or attention on edges, and positional information
for nodes that the features cannot tell apart.

## Key results

- Table 13, GatedGCN with positional encodings: ZINC MAE 0.354 (none),
  0.319 (eigenvectors), 0.214 (random sign flips), 0.214 (absolute values),
  0.431 (fixed node order). CSL 10.0, 68.6, 99.8, 99.4, 10.5%
- Table 11, CYCLES with 200 training graphs: GatedGCN 50.0 → 95.1%, GIN
  70.6 → 86.7% with PE
- Table 14, TSP F1: isotropic GatedGCN 0.646, with edge gates 0.757, with
  explicit edge states 0.791, initialized from distances 0.808
- Table 5, COLLAB Hits@50: GraphSAGE (max) 51.6, GAT 51.5, GatedGCN 52.6,
  GIN 41.7, matrix factorization 44.2
- Table 16, TU datasets, two seeds with the same folds and
  hyperparameters: rankings change, and MLPs match GNNs on DD and PROTEINS

## Limitations

- **No per-model tuning.** One schedule for all, which can favor whichever
  model it suits
- **Four seeds**, and some mean differences are within a standard deviation
- **PE gains are uneven.** COLLAB is unchanged (52.6 → 52.8), and on
  GraphTheoryProp PE helps GatedGCN and leaves GIN level
- **GraphNorm**, proposed in an earlier version, is withdrawn in App. G as
  having "no concrete theoretical basis"
- **The paper changed across versions.** Results here are v5's
