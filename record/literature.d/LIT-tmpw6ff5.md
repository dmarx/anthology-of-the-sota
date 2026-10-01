---
status: Active
title: 'Community Detection on Networks with Ricci Flow'
version: 1
tags:
- graphs-and-networks
date: '2026-10-01'
published: '2019-07-09'
arxiv: '1907.03993'
first_author: 'Ni'
keywords:
- 'community detection'
- 'graph clustering'
- 'discrete Ricci curvature'
- 'discrete Ricci flow'
implementations:
- 'saibalmars/GraphRicciCurvature'
summary: >-
  Ni et al. (2019), [ARXIV-1907.03993](https://arxiv.org/abs/1907.03993) (Scientific Reports). Ollivier–Ricci
  curvature on a graph comes from optimal transport between the
  neighbourhoods of an edge's endpoints. Edges between communities come out
  negatively curved and edges inside them positively curved. A discrete
  Ricci flow stretches negative edges and shrinks positive ones, and
  thresholding the resulting weights ("surgery") separates the
  communities. On a 500-node, two-block SBM, ARI goes from nearly 100% at
  p_inter/p_intra = 0.5 to nearly 0% at 0.55. On LFR graphs it is the most
  stable of the methods compared.
---

# LIT-tmpw6ff5: Community Detection on Networks with Ricci Flow

Ni et al. (2019) — [ARXIV-1907.03993](https://arxiv.org/abs/1907.03993)

## Key takeaways

- **Method.** Each node carries a probability measure on itself and its
  neighbours. It has two parameters, α (mass kept at the node) and p (how
  sharply far neighbours are discounted by edge weight). The experiments
  mostly use α = ½ and p = 2. The curvature of edge xy is
  κ = 1 − W(m_x, m_y)/d(x, y), with W the Wasserstein distance. The flow
  updates every weight at once, w ← d − κ·d, and recomputes shortest
  paths. After the flow (50 iterations in the evaluation, with surgery every
  5), edges heavier than a cutoff are removed.
- **Synthetic graphs (Fig. 5, ARI averaged over 10 graphs).**
  - On a two-community SBM with 500 nodes, accuracy is nearly perfect up
    to p_inter/p_intra = 0.5 and collapses to near zero by 0.55. Most
    baselines also do well below 0.5; label propagation and Infomap are
    the exceptions.
  - On LFR graphs, Ricci flow and Spinglass beat Fast Greedy, label
    propagation, Infomap and edge betweenness. Ricci flow is nearly
    perfect for most mixing values μ, where Spinglass reaches about 95%.
  - On one LFR graph with 30 communities, any final cutoff between 1 and
    0.47 recovers all 30 exactly, with ARI 1.0 (Fig. 6a).
- **Real graphs.** On Karate, college football, Polbooks and Polblogs, the
  paper reports results that are competitive or better (Fig. 5c). Without
  labels, it suggests choosing the cutoff where modularity first plateaus.
  Varying the cutoff also exposes hierarchical communities (Fig. 7).
- **Theory.** Theorem 4.1 proves the flow separates communities on a
  symmetric family G(a, b) (b+1 cliques of size a+1 joined at one vertex
  each) when a > b ≥ 2. It does so for α = 0, p = 0, which is not the
  setting the experiments use.
- **Not ablated.** The iteration count and cutoff are per-network choices
  that the authors compare to the surgery timing in Hamilton–Perelman.
  There is no sensitivity analysis over α and p. Forman curvature was tried
  and is reported only as "less satisfying".

## Standing in the anthology

Filed under `graphs-and-networks`. The paper is a graph algorithm, and
nothing in it is learned. The record's graph-model documents are [LIT-580](LIT-580.md)
(GIN, *How Powerful are Graph Neural Networks?*), [SOTA-351](../practices.d/SOTA-351.md) (sum aggregation
in message-passing GNNs, drawn from it) and [LIT-581](LIT-581.md) (pitfalls of GNN
evaluation). None of them uses curvature, so this paper neither supports
nor contests them.

Its likely bearing is on work the record does not yet hold. Discrete Ricci
curvature, including the Ollivier form computed by this paper's
GraphRicciCurvature package, became a tool for diagnosing over-squashing in
message passing and for rewiring graphs to relieve it. None of that work is
filed yet. Until it is, this note is a seed for that thread, not evidence
for anything held.

[LIT-581](LIT-581.md) bears on how to read the comparison. Its point is that results on a
few fixed graphs and splits can reorder under a shared protocol. The same
caution applies here: the real-graph comparison rests on four small graphs,
and the cutoff is tuned per network.

The paper is also held in the companion record:
[nucleation's note](https://github.com/dmarx/nucleation/blob/main/record/literature.d/LIT-004.md),
which has a full reading, including the supplementary theory.

Unread — no NOTE.
