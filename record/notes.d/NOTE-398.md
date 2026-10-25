---
number: 398
status: Read
formerly:
- NOTE-tmpdyx5w
paper: 'LIT-838'
title: 'A fair comparison of GNNs'
version: 1
date: '2026-10-22'
summary: >-
  Re-run under one protocol, five graph-classification GNNs fail to beat
  a graph-agnostic baseline on three of four chemical benchmarks, and
  published accuracies differ consistently from test accuracy. Hyperparameter
  selection must happen inside each training fold, never on the reported
  folds. Read in full, including the appendix.
---

# NOTE-398: A fair comparison of GNNs

## Contribution

A reproducible re-evaluation of DGCNN, DiffPool, ECC, GIN and GraphSAGE on
nine TU benchmarks, with code and splits released, and two
structure-agnostic baselines that measure whether the graph is used at
all.

## Key insight

**Model selection and model assessment are different estimates, and the
literature mixed them.** Reporting the CV score of the folds used to pick
hyperparameters is optimistic. A GNN that does not beat a model ignoring
the edges has not shown that it uses them.

## Key results

- Table 3: on D&D, PROTEINS and ENZYMES the baseline beats every GNN. On
  NCI1 every GNN beats it, by up to 10.2 points (GIN)
- Table 4: degree features lift the baseline by about 15 points on social
  datasets, to best on IMDB-MULTI and 0.4 behind GIN on IMDB-BINARY
- Figure 1: the paper's own validation accuracies are always at or above
  its test accuracies, and published numbers differ from its test numbers
  by a consistent gap
- Appendix A.3: adding degree reduces the median selected depth by about
  one layer for every model except GraphSAGE

## Limitations

- **Small TU datasets.** Standard deviations of 2–6 points leave most
  model-to-model differences unresolved
- **A 72-hour cap per training run** left ECC unevaluated on three social
  datasets
- **Implementations are re-written** in PyTorch Geometric, following each
  paper where paper and code disagree
- **The baselines are domain-specific**, and "the GNN does not use the
  structure" and "the task does not need it" are not separated
