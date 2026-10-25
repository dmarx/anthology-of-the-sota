---
number: 83
status: Active
formerly:
- THEORY-tmplxq36
title: 'A message-passing GNN can distinguish no more graphs than the 1-WL test, and reaches that limit only if its neighbor aggregation is injective on multisets, as a sum followed by an MLP is and a mean or max is not'
version: 1
tags:
- graphs-and-networks
- model-architecture
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-580
- LIT-840
summary: >-
  Xu et al. (2019), [LIT-580](../literature.d/LIT-580.md) — each message-passing layer refines node
  labels as one 1-WL iteration can at best, so 1-WL bounds what the network
  separates. Injective aggregation reaches the bound. Sums of an MLP over a
  multiset are injective. Means lose counts and maxes lose multiplicities.
  It is a theorem, and it explains the paper's training-fit ordering and the
  collapse of mean aggregators to chance on featureless graphs. Morris et al.
  (2019), LIT-840, proved the same bound independently.
---

<!-- inactive-ok-file: SOTA-452 — Proposed, named as where the encodings that leave this account are recommended -->

# THEORY-083: A message-passing GNN can distinguish no more graphs than the 1-WL test, and reaches that limit only if its neighbor aggregation is injective on multisets, as a sum followed by an MLP is and a mean or max is not

## Source

Xu et al. (2019), [LIT-580](../literature.d/LIT-580.md). Read as [NOTE-319](../notes.d/NOTE-319.md).
Morris et al. (2019), [LIT-840](../literature.d/LIT-840.md). Read as [NOTE-396](../notes.d/NOTE-396.md).

## The account

A message-passing layer maps each node's own state and the multiset of its
neighbors' states to a new state. If two nodes get the same 1-WL color
after k rounds, no k-layer GNN can tell them apart, because each layer sees
no more than a WL refinement does. The bound is achieved when every step is
injective. Sum with an MLP is (Lemma 5, Corollary 6). Mean is not: two
neighborhoods with the same feature proportions collide. Max is not either:
the multiplicities vanish.

The bound and the injectivity argument are [LIT-580](../literature.d/LIT-580.md)'s, which also put them to
a test: training accuracy ranks sum–MLP above sum with one layer above the
mean and max variants (Figure 4), and on REDDIT-BINARY and MULTI-5K with no
node features GIN-0 reaches 92.4 and 57.5 while the mean variants sit at
chance, 50.0 and 20.0. Those are fold-averaged validation accuracies, as
GIN's §6 says. Errica et al. ([LIT-838](../literature.d/LIT-838.md)) score held-out folds and get
87.0 and 53.8 for GIN. The mean variants' chance-level scores are a
failure to separate the graphs at all, which is what this account
predicts, and no protocol would lift them.

Morris et al. proved the bound independently, three days later, in
[LIT-840](../literature.d/LIT-840.md). Their Theorem 1 shows that 1-WL refines the coloring of any
message-passing GNN, for every choice of aggregate and merge functions and
weights. That is the first half of this account, reached by a separate
induction. Their matching result (Theorem 2) is narrower than the second
half here. For a given labeled graph, weights exist under which a linear sum
layer reproduces 1-WL. They say nothing about mean or max, so the
injectivity argument that separates the aggregators rests on [LIT-580](../literature.d/LIT-580.md) alone.

## What it explains

- Why sum–MLP GNNs fit training sets that mean and max variants underfit
- Why mean-aggregation GNNs are at chance on featureless Reddit graphs,
  where every neighborhood has the same proportions
- Why adding node degree as a feature partly rescues mean aggregation

## Where it stops

- **Distinguishability, not generalization.** With informative features,
  aggregator choice matters little in the paper's own tables. Later work
  that goes past 1-WL shows the same gap from the other side. In
  Bouritsas et al. ([LIT-835](../literature.d/LIT-835.md), Figure 5), training error on ZINC follows
  how uniquely the added substructure counts identify nodes, and test error
  does not. With a GCN encoder on OGB-MOLHIV, Bevilacqua et al.
  ([LIT-813](../literature.d/LIT-813.md), Table 5) raise training AUC to as much as 99.5, while test
  AUC ranges from 73.8 to 76.5 around the base model's 76.1. More
  separating power buys fit first
- **1-WL is itself limited.** It cannot count triangles or cycles, gives
  every node of a triangle-plus-square the same color ([LIT-840](../literature.d/LIT-840.md)), and
  cannot tell some regular graphs apart
- **The bound is on message passing over the raw graph with deterministic
  inputs.** Change the input or the unit of computation and it no longer
  applies. Each of the following is outside this account:
  - messages between k-element node sets ([LIT-840](../literature.d/LIT-840.md))
  - substructure counts as features ([LIT-835](../literature.d/LIT-835.md))
  - bags of subgraphs ([LIT-813](../literature.d/LIT-813.md))
  - random-walk or sign-invariant spectral encodings ([LIT-833](../literature.d/LIT-833.md),
    [LIT-818](../literature.d/LIT-818.md); see [SOTA-452](../practices.d/SOTA-452.md))
  - random node features ([LIT-810](../literature.d/LIT-810.md)), which reach universality only in
    probability, by an impractically large construction
