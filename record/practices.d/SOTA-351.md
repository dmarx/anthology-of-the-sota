---
number: 351
status: Active
formerly:
- SOTA-tmpola8o
title: 'In a message-passing GNN for graph-level tasks, aggregate neighbours by sum with an MLP update, not by mean or max, when graph structure rather than node features carries the signal'
version: 1
tags:
- model-architecture
date: '2026-09-23'
source:
- LIT-580
introduced_by:
- LIT-580
consensus: unassessed
consensus_note: >-
  GIN and its edge-feature variant GINE are standard baselines, and the
  expressivity result is a proof. The empirical margin is large only on
  structure-dominated tasks. How far sum aggregation is the default in
  current practice has not been assessed here.
implementations: []
summary: >-
  Xu et al. (2019), [LIT-580](../literature.d/LIT-580.md) — mean and max aggregation cannot count
  neighbors, so graphs that differ only in counts look the same to them. On
  featureless Reddit graphs, mean-aggregation GNNs are at chance (50.0,
  20.0) and sum–MLP scores 92.4 and 57.5. With informative node features the
  choice matters much less, and results are mostly within noise. Use
  h = MLP((1 + ε)h + Σ neighbors) with ε = 0 and a sum readout.
---

# SOTA-351: In a message-passing GNN for graph-level tasks, aggregate neighbours by sum with an MLP update, not by mean or max, when graph structure rather than node features carries the signal

## Source

Xu et al. (2019), [LIT-580](../literature.d/LIT-580.md). Read as [NOTE-319](../notes.d/NOTE-319.md). The reason is
[THEORY-083](../theory.d/THEORY-083.md).

## The practice

- **Sum, then MLP.** `h_v ← MLP((1 + ε)·h_v + Σ_{u∈N(v)} h_u)`. Fix ε = 0
  (GIN-0), which fit as well as learned ε and generalized slightly better
- **Read out by summing** node states from every layer, and concatenate the
  per-layer readouts
- **Know when it matters.** Where the node features are weak or absent, and
  counts and structure are the signal, mean or max aggregation can fail
  outright. Where the features are informative, expect small differences,
  and choose by validation

## Conditions

- **Graph classification on small benchmarks**, with 10-fold CV
- **Bounded by 1-WL either way.** Tasks needing cycle counts or more need
  positional or structural encodings
