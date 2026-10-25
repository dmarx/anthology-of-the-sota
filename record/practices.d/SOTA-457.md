---
number: 457
status: Proposed
formerly:
- SOTA-tmpzd1sw
promote_when: >-
  An ablation by a group other than OGB's or Gilmer et al.'s that adds
  only the virtual node to otherwise fixed message-passing models, on
  several graph-level datasets with multiple seeds, and finds gains
  outside the seed spread on most of them. A leaderboard entry that adds a
  virtual node alongside other changes does not settle it, and neither
  does a result from a model that already has global attention.
title: 'In a message-passing GNN for graph-level prediction, try a virtual node connected to every node, and keep it only if validation favors it'
version: 1
tags:
- graphs-and-networks
- model-architecture
date: '2026-10-22'
source:
- LIT-808
- LIT-829
# Gilmer et al. described the "master node" first, as a long-range
# mechanism. OGB, which credits them, ran the controlled with/without
# comparison on most datasets, so it is the primary source.
introduced_by:
- LIT-829
consensus: unassessed
consensus_note: >-
  Two groups, at Google and at Stanford, report gains, and OGB's baselines
  ship with the option. Neither is independent of the other, since OGB
  cites the MPNN paper for the idea. How often later graph-level models
  keep a virtual node, or replace it with attention, has not been assessed
  here.
implementations:
- ogb
summary: >-
  Hu et al. (2020), [LIT-808](../literature.d/LIT-808.md), and Gilmer et al. (2017), [LIT-829](../literature.d/LIT-829.md) —
  a node joined to every other node gives each message-passing step a
  global channel. In OGB's baselines it lifts GIN from 22.66 to 27.03 AP on
  ogbg-molpcba and leaves GIN comparable or better on 9 of 10 further
  MoleculeNet sets, but leaves GCN level on ogbg-molhiv. In the MPNN paper
  a master node cuts QM9 error by about a quarter without geometry. Treat
  it as a cheap option to validate, not a default.
---

<!-- inactive-ok-file: SOTA-455 — a Proposed sibling practice, named as an alternative not compared -->

# SOTA-457: In a message-passing GNN for graph-level prediction, try a virtual node connected to every node, and keep it only if validation favors it

## Source

Hu et al. (2020), [LIT-808](../literature.d/LIT-808.md). Read as [NOTE-419](../notes.d/NOTE-419.md). Gilmer et al.
(2017), [LIT-829](../literature.d/LIT-829.md). Read as [NOTE-384](../notes.d/NOTE-384.md).

## The practice

Gilmer et al. introduced the mechanism in [LIT-829](../literature.d/LIT-829.md) as a latent "master
node" joined to every atom by a special edge type, a global scratch space
read and written at every step. Trained on QM9 without spatial
information, GG-NN's average error ratio over 13 targets fell from 3.47 to
2.62 with it, and every target improved. Virtual edges between all
unbonded pairs gave 2.90 and a set2set readout 2.57, so the gain is from
long-range communication, not from this mechanism alone. Those runs used a
partial-charge input that is a DFT output.

OGB ([LIT-808](../literature.d/LIT-808.md)) ran the with/without comparison across its
graph-level baselines, ten seeds each. With the additional molecular
features, GIN moves from 75.58 to 77.07 ROC-AUC on ogbg-molhiv and from
22.66 to 27.03 AP on ogbg-molpcba, and GCN from 20.20 to 24.24 on
molpcba but from 76.06 to 75.99 on molhiv. On ogbg-ppa GIN goes from
68.92 to 70.37%, and on ogbg-code2 GCN from 15.07 to 15.95 F1. Across ten
further MoleculeNet sets, the virtual node leaves GIN comparable or better
on 9, with clintox the exception.

- **Add one node with its own embedding, joined to every node**, and run
  message passing over the augmented graph. It costs one node and |V|
  edges per graph
- **Validate it per dataset.** The gains range from about 4 AP points to
  none, and GIN's 1.5-point gain on molhiv is about one standard deviation
  of its seeds
- **Prefer it when the target is a global property** and the graphs are
  sparse and tree-like with long diameters, as molecules and code ASTs
  are, where a few message-passing steps cannot reach across the graph

## Conditions

- **Graph-level prediction.** Both sources test it only on whole-graph
  targets
- **Message-passing models without global attention.** Graph transformers
  already provide the global channel. The comparison to them is not made
  here
- **Not independent evidence.** OGB credits the MPNN paper, and both
  sources report the gain from their own baselines
- **A neighbouring remedy.** [SOTA-455](SOTA-455.md) makes the last layer fully
  adjacent, another way of giving every node a one-hop path to every other.
  Neither source compares the two
