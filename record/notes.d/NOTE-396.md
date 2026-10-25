---
number: 396
status: Read
formerly:
- NOTE-tmpc8k29
paper: 'LIT-840'
title: 'k-GNN'
version: 1
date: '2026-10-22'
summary: >-
  An independent proof that message passing is bounded by 1-WL and can match
  it, and k-GNNs that pass messages between node sets. QM9 gains are large
  on four energy targets and small elsewhere; TUD gains come without
  deviations. Read in full, proofs included.
---

# NOTE-396: k-GNN

## Contribution

The 1-WL bound on message-passing GNNs, proved at the same time as and
independently of GIN, with a constructive proof that a linear sum layer
can match 1-WL. A higher-order architecture, k-GNN, that follows a
set-based k-WL, and a hierarchical version that stacks 1-, 2- and 3-GNNs.

## Key insight

**A GNN layer is a WL refinement step with learned hashing.** Whatever the
aggregator, two nodes with the same color and the same multiset of
neighbor colors get the same output, so the network cannot outrun the
test. To see more structure, pass messages between tuples or sets of
nodes, which is what k-WL does.

## Key results

- **Theorem 1:** 1-WL refines the coloring of any 1-GNN, for every choice
  of aggregate and merge functions and weights. The proof is a short
  induction
- **Theorem 2:** for a given labeled graph there are weights making
  `sgn(A F W − J)` reproduce 1-WL, given one-hot or linearly independent
  label encodings. The width needed is at most 2n. Corollary 16 replaces
  sgn with two ReLU layers, so 2t layers simulate t rounds
- **Propositions 3 and 4:** the same two results for k-GNNs against the
  set-based k-WL, by running 1-WL on the graph of k-sets
- **QM9** (Table 2): 1-2-3-GNN vs 1-GNN, MAE gain 4.0% (µ), 65.3% (α),
  none (HOMO), 1.4% (LUMO), 6.1% (gap), 37.0% (R²), 85.5% (ZPVE),
  98.5% / 94.9% / 98.1% / 97.6% (U0, U, H, G), 65.0% (Cv)
- **TUD** (Table 1): 1-2-3-GNN vs 1-GNN, PROTEINS 75.5 vs 72.2, IMDB-B
  74.2 vs 71.2, IMDB-M 49.5 vs 47.7, PTC-FM 62.8 vs 59.3, NCI1 76.2 vs 74.3,
  MUTAG 86.1 vs 82.2, PTC-MR 60.9 vs 59.0. Untrained aggregation weights
  give 70.7 on PROTEINS against 72.2 trained, and 58.6 against 74.3 on NCI1

## Limitations

- **The matching weights are per graph.** Theorem 2 builds weights for one
  labeled graph, not one set of weights for a dataset
- **The experiments use local k-GNNs,** which drop the global neighborhood
  the k-WL equivalence relies on, so the tested models are not covered by
  Proposition 4
- **No variance on TUD,** and a claimed parameter-matched 1-GNN control is
  described but not shown
- **The QM9 baseline** uses bond distances only
