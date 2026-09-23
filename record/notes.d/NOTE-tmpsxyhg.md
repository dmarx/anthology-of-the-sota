---
status: Read
paper: LIT-tmpkhqrt
title: 'Pitfalls of GNN evaluation'
version: 1
date: '2026-09-23'
summary: >-
  With one shared training and tuning protocol over 100 splits × 20 seeds,
  GCN ranks first among four GNNs, and the single Planetoid split reorders
  models. Read in full.
---

# NOTE-tmpsxyhg: Pitfalls of GNN evaluation

## Contribution

A controlled re-evaluation of popular GNNs and four new node-classification
datasets. A benchmark framework came with it.

## Key insight

**A fixed test split plus model-specific training recipes measures
overfitting to that split and the quality of the recipe.** It does not
measure the architecture.

## Key results

- Average rank: GCN 2.3, MoNet 2.7, GraphSAGE-mean 2.7, GAT 3.6. The four
  baselines rank 7.4–8.8
- Planetoid split: GAT wins Cora and Citeseer. Another split of the same
  sizes: GCN wins both
- GAT collapses below 40% in 138 of 2,000 runs on Amazon Photo

## Limitations

- **Hyperparameters were selected on Cora and Citeseer only**, then reused
- **Two-layer models, transductive node classification**, with small label
  budgets
- **A workshop paper**, and newer architectures are not covered
