---
status: Skimmed
paper: 'LIT-tmpo8g4p'
title: 'GSN'
version: 1
date: '2026-10-22'
summary: >-
  Substructure counts as node or edge features make message passing
  strictly more expressive than 1-WL at linear training cost. Training
  error follows how uniquely the counts identify nodes and test error does
  not; rings generalize on molecules. Main text read in full; the
  appendices with the proofs and hyperparameters were not.
---

# NOTE-tmpy4wqs: GSN

## Contribution

A way past 1-WL that keeps message passing local and linear in edges:
precompute, for each node or edge, how often it occupies each orbit of a
few small chosen subgraphs, and give those counts to the message function.

## Key insight

**Counts are identifiers that repeat across graphs.** Unique random IDs
make a GNN universal but do not generalize, because nothing about them
recurs. Substructure counts are permutation invariant and recur, so they
trade some uniqueness for generalization. Which counts to use is an
inductive bias, and the paper chooses it from domain knowledge.

## Key results

- Strictly more expressive than 1-WL for any counted graph other than a
  star or, under induced counting, a single node or edge (Theorem 3.1).
  Edge counts are at least as expressive as node counts (Theorem 3.3)
- Strongly regular graphs up to 35 nodes: cycle or path counts up to size
  6 separate every same-size pair, with random weights (Figure 4)
- ZINC: 0.140 MAE, 0.115 with edge features, against 0.254 and 0.209 for the
  base MPNN (Table 2). A 500k-parameter version reaches 0.101
- TUD (Table 1) and OGB-MOLHIV (Table 3): at or near the best reported,
  mostly within one standard deviation
- Training error tracks the disambiguation score; test error does not
  (Figure 5)
- DeepSets on the same counts, without message passing, ties GSN on three
  small TUD datasets (Table 4)

## Limitations

- **Generalization is not covered by the theory,** which the paper states
- **Substructure family and size are tuned per dataset,** on the
  validation set for ZINC and OGB and with GIN's best-epoch protocol for
  TUD
- **Worst-case counting cost is O(n^k).** Figure 3 shows it is far lower
  on sparse molecular graphs
- **Not read:** the appendix proofs and dataset details
