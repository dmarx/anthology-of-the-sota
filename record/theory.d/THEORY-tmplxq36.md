---
status: Active
title: 'A message-passing GNN can distinguish no more graphs than the 1-WL test, and reaches that limit only if its neighbor aggregation is injective on multisets, as a sum followed by an MLP is and a mean or max is not'
version: 1
tags:
- model-architecture
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmp95aa1
summary: >-
  Xu et al. (2019), [LIT-tmp95aa1](../literature.d/LIT-tmp95aa1.md) — each message-passing layer refines node
  labels as one 1-WL iteration can at best, so 1-WL bounds what the network
  separates. Injective aggregation reaches the bound. Sums of an MLP over a
  multiset are injective. Means lose counts and maxes lose multiplicities.
  It is a theorem, and it explains the paper's training-fit ordering and the
  collapse of mean aggregators to chance on featureless graphs.
---

# THEORY-tmplxq36: A message-passing GNN can distinguish no more graphs than the 1-WL test, and reaches that limit only if its neighbor aggregation is injective on multisets, as a sum followed by an MLP is and a mean or max is not

## Source

Xu et al. (2019), [LIT-tmp95aa1](../literature.d/LIT-tmp95aa1.md). Read as [NOTE-tmpvkwpe](../notes.d/NOTE-tmpvkwpe.md).

## The account

A message-passing layer maps each node's own state and the multiset of its
neighbors' states to a new state. If two nodes get the same 1-WL color
after k rounds, no k-layer GNN can tell them apart, because each layer sees
no more than a WL refinement does. The bound is achieved when every step is
injective. Sum with an MLP is (Lemma 5, Corollary 6). Mean is not: two
neighborhoods with the same feature proportions collide. Max is not either:
the multiplicities vanish.

## What it explains

- Why sum–MLP GNNs fit training sets that mean and max variants underfit
- Why mean-aggregation GNNs are at chance on featureless Reddit graphs,
  where every neighborhood has the same proportions
- Why adding node degree as a feature partly rescues mean aggregation

## Where it stops

- **Distinguishability, not generalization.** With informative features,
  aggregator choice matters little in the paper's own tables
- **1-WL is itself limited.** It cannot count cycles or tell some regular
  graphs apart. Positional encodings and higher-order GNNs address that,
  outside this account
