---
status: Active
title: 'Compare GNN architectures over many random data splits and seeds, with one shared training and hyperparameter-selection procedure for every model, never on a single fixed split'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-23'
source:
- LIT-tmpkhqrt
introduced_by:
- LIT-tmpkhqrt
consensus: unassessed
consensus_note: >-
  The finding recurs in later GNN re-evaluations, including LIT-tmp4yk7i for
  graph transformers. Many node-classification papers still report the
  Planetoid split. How common multi-split reporting has become has not been
  assessed here.
implementations:
- gnn-benchmark
summary: >-
  Shchur et al. (2018), [LIT-tmpkhqrt](../literature.d/LIT-tmpkhqrt.md) — on the Planetoid split GAT beats GCN.
  On another random split of the same size GCN wins, and averaged over 100
  splits × 20 seeds with identical training and tuning, GCN ranks first of
  four GNNs. A single split selects the model that overfits it, and
  per-model recipes measure the recipe. Report mean and spread over many
  splits and seeds, with the same tuning budget for every model.
---

# SOTA-tmpdjto5: Compare GNN architectures over many random data splits and seeds, with one shared training and hyperparameter-selection procedure for every model, never on a single fixed split

## Source

Shchur et al. (2018), [LIT-tmpkhqrt](../literature.d/LIT-tmpkhqrt.md). Read as [NOTE-tmpsxyhg](../notes.d/NOTE-tmpsxyhg.md).

## The practice

- **Many splits, many seeds.** The source used 100 random splits with the
  same label budget, and 20 initializations each. Report the mean and the
  distribution, not the best run
- **One protocol for everyone:** the same optimizer, early stopping,
  initialization, batching and hyperparameter search, under a matched
  parameter budget
- **Look at the distribution, not just the mean.** GAT's average on Amazon
  was driven by rare collapsed runs, which is a stability result, not an
  accuracy one
- **Include non-graph baselines** (MLP, logistic regression, label
  propagation), so the value of the graph is measured

## Conditions

- **Transductive node classification with few labels.** Benchmarks with
  official splits (OGB) fix the split for comparability. Multiple seeds and
  a shared protocol still apply there
- **Select hyperparameters per dataset if you can.** The source selected
  on two datasets and reused the result
