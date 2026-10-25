---
number: 350
status: Active
formerly:
- SOTA-tmpdjto5
title: 'Compare GNN architectures over many random data splits and seeds, with one shared training and hyperparameter-selection procedure for every model, never on a single fixed split'
version: 2
history:
- version: 2
  date: '2026-10-22'
  note: >-
    Two sources added from the graph-coverage pass. LIT-tmprm7bo carries
    the practice to graph classification, with hyperparameters selected
    inside each training fold and a graph-agnostic baseline, and finds the
    baseline unbeaten on three of four chemical datasets. LIT-tmp8wx7k shows
    a second seed reordering models on fixed folds. The recommendation is
    unchanged, with one bullet added on keeping selection inside the
    training data, and consensus moves from unassessed to emerging.
tags:
- graphs-and-networks
- analysis-and-evaluation
- model-architecture
date: '2026-09-23'
source:
- LIT-581
- LIT-tmprm7bo
- LIT-tmp8wx7k
introduced_by:
- LIT-581
consensus: emerging
consensus_note: >-
  Three groups at different institutions now make it: Shchur et al. for
  node classification, Errica et al. for graph classification, following
  Shchur's advice, and Dwivedi et al. on TU datasets, citing Errica. They
  build on each other rather than replicating blind. LIT-579 repeats the
  finding for graph transformers. OGB (LIT-tmp3qfj0) builds multiple seeds and one
  evaluator into its leaderboard. Many node-classification papers still
  report the Planetoid split, and how common multi-split reporting has
  become has not been counted here.
implementations:
- gnn-benchmark
summary: >-
  Shchur et al. (2018), [LIT-581](../literature.d/LIT-581.md) — on the Planetoid split GAT beats GCN.
  On another random split of the same size GCN wins, and averaged over 100
  splits × 20 seeds with identical training and tuning, GCN ranks first of
  four GNNs. A single split selects the model that overfits it, and
  per-model recipes measure the recipe. Errica et al. (2020), LIT-tmprm7bo,
  find the same for graph classification, where a graph-agnostic baseline
  beats every GNN on three of four chemical datasets. Report mean and
  spread over many splits and seeds, with the same tuning budget for
  every model.
---

# SOTA-350: Compare GNN architectures over many random data splits and seeds, with one shared training and hyperparameter-selection procedure for every model, never on a single fixed split

## Source

Shchur et al. (2018), [LIT-581](../literature.d/LIT-581.md). Read as [NOTE-318](../notes.d/NOTE-318.md). Errica et al.
(2020), [LIT-tmprm7bo](../literature.d/LIT-tmprm7bo.md). Read as [NOTE-tmpdyx5w](../notes.d/NOTE-tmpdyx5w.md). Dwivedi et al. (2020),
[LIT-tmp8wx7k](../literature.d/LIT-tmp8wx7k.md). Read as [NOTE-tmpjnifj](../notes.d/NOTE-tmpjnifj.md).

## The practice

Shchur et al. made this recommendation in [LIT-581](../literature.d/LIT-581.md), from a re-evaluation of
four GNNs under one shared protocol. On the Planetoid split GAT wins Cora and
Citeseer. On another split of the same sizes GCN wins both, and over 100
splits × 20 seeds GCN has the best average rank (2.3, against 2.7 for MoNet
and GraphSAGE-mean and 3.6 for GAT), with the four non-graph baselines at
7.4–8.8. GAT fell below 40% in 138 of 2,000 runs on Amazon Photo, which is
the third bullet.

Errica et al. ([LIT-tmprm7bo](../literature.d/LIT-tmprm7bo.md)) found the same failure in graph
classification and ran the protocol at scale: more than 47,000 training
runs, five GNNs, nine datasets, stratified 10-fold CV with hyperparameters
selected on a holdout inside each training fold, three retrainings per
fold, and the same node features for every model. GIN's published
accuracies had been validation scores, and under the protocol its
featureless REDDIT-BINARY accuracy is 87.0 against the 92.4 it reported. A
structure-agnostic baseline beats every GNN on D&D, PROTEINS and ENZYMES
(78.4, 75.8 and 65.2% against at most 76.6, 73.7 and 59.6%), and every GNN
beats it on NCI1.

Dwivedi et al. ([LIT-tmp8wx7k](../literature.d/LIT-tmp8wx7k.md)) isolate the seed. On ENZYMES, DD and
PROTEINS they reran every model with the same 10 folds and the same
hyperparameters and only a new random seed, and the ranking changed. On
DD and PROTEINS an MLP matched the GNNs.

- **Many splits, many seeds.** The source used 100 random splits with the
  same label budget, and 20 initializations each. Report the mean and the
  distribution, not the best run
- **One protocol for everyone:** the same optimizer, early stopping,
  initialization, batching and hyperparameter search, under a matched
  parameter budget
- **Keep model selection inside the training data.** Choose
  hyperparameters on a holdout carved from each training fold, and report
  the test folds. A CV score over the folds used for selection is a
  validation score and is optimistic
- **Look at the distribution, not just the mean.** GAT's average on Amazon
  was driven by rare collapsed runs, which is a stability result, not an
  accuracy one
- **Include non-graph baselines** (MLP, logistic regression, label
  propagation, or a sum over node features then an MLP for graphs), so the
  value of the graph is measured. On small chemical TU datasets they win

## Conditions

- **Node and graph classification on small benchmarks**, where seed and
  split variance is of the same size as the differences between models.
  Benchmarks with official splits (OGB) fix the split for comparability,
  and [SOTA-tmp2qn9u](SOTA-tmp2qn9u.md) says which split to fix. Multiple seeds and a shared
  protocol still apply there
- **Select hyperparameters per dataset if you can.** The source selected
  on two datasets and reused the result
