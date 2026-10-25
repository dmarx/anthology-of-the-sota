---
number: 400
status: Read
formerly:
- NOTE-tmpeq1tm
paper: 'LIT-810'
title: 'Random node initialization'
version: 1
date: '2026-10-22'
summary: >-
  Random initial node features make message passing universal in
  probability, by an existence proof whose construction is enormous. On a
  purpose-built synthetic dataset a GCN with them reaches 96.6–98.0%
  against 50%, slowly and with careful tuning. Read in full, including the
  proof and dataset construction.
---

# NOTE-400: Random node initialization

## Contribution

A universality theorem for message-passing GNNs with random initial
features, and two synthetic datasets, EXP and CEXP, whose pairs are
indistinguishable by 1-WL and distinguishable by 2-WL.

## Key insight

**Random values individualize the nodes, and an individualized graph is
something a message-passing network can recognize.** Any one sample breaks
invariance. The distribution of outputs does not, because the noise is
i.i.d.

## Key results

- **Theorem 1:** for all ε, δ > 0 an MPNN with RNI (ε, δ)-approximates any
  invariant function on graphs of at most n nodes. Embedding dimension of
  order n²/δ suffices to individualize. One random dimension suffices in
  principle
- **EXP** (Table 1): GCN-RNI 96.6–98.0%, 1-GCN 50%, PPGN 50%, 1-2-3-GCN-L
  50%, 3-GCN 99.7%
- **CEXP** (Figure 2): partial randomization (12.5–87.5% of dimensions)
  beats full randomization, which stays under 60% on the 1-WL-distinguishable
  half
- **Convergence:** about 10 epochs for 3-GCN, over 100 for GCN-RNI, with
  fold-to-fold variance high until about epoch 200

## Limitations

- **Synthetic data only,** built by the authors
- **The construction is "prohibitively large"** in the authors' words, and
  the theorem says nothing about learning it from finite data
- **Sensitive to learning rate, activation and noise distribution,** by the
  authors' report
- **The EXP label is decided by a fixed core pair,** so the task is
  structure detection, not satisfiability in general
