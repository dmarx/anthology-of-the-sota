---
status: Active
title: 'Understanding over-squashing and bottlenecks on graphs via curvature'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
date: '2026-10-22'
published: '2021-11-29'
arxiv: '2111.14522'
first_author: 'Topping'
keywords:
- 'over-squashing'
- 'graph-curvature'
- 'balanced-forman-curvature'
- 'graph-rewiring'
- 'sdrf'
- 'cheeger-constant'
implementations: []
extends:
- LIT-tmpt6hyo
compared_against:
- LIT-tmpt6hyo
summary: >-
  Topping, Di Giovanni, Chamberlain, Dong, Bronstein (ICLR 2022),
  [ARXIV-2111.14522](https://arxiv.org/abs/2111.14522). The Jacobian of node i's features with respect to node
  s's input is bounded by the (r+1)-th power of the normalized adjacency.
  The paper defines Balanced Forman curvature, a combinatorial edge
  curvature that lower-bounds Ollivier curvature, and proves that a very
  negatively curved edge leaves many 2-hop neighbours with a small average
  Jacobian. SDRF rewires by adding edges around the most negative edge. On
  nine node-classification sets with a GCN, it beats no rewiring on all
  nine, by 0.3–6.7 points, while changing 0.2–33% of edges. DIGL or a
  fully adjacent last layer is ahead of it on five.
extended_by:
- LIT-tmpggqnq
---

# LIT-tmp0hkly: Understanding over-squashing and bottlenecks on graphs via curvature

Topping, Di Giovanni, Chamberlain, Dong, Bronstein, Oxford, Imperial
College and Twitter (ICLR 2022) — [ARXIV-2111.14522](https://arxiv.org/abs/2111.14522)

## Key takeaways

- **Sensitivity** (Lemma 1): for an MPNN whose message and update functions
  have bounded derivatives (α, β), |∂h_i^(r+1)/∂x_s| ≤ (αβ)^{r+1}·(Â^{r+1})_is
  for s at distance r + 1. On a binary tree that entry is 2^{-1}·3^{-r}
- **Balanced Forman curvature** (Definition 1): Ric(i, j) is computed from
  the degrees of i and j, the triangles on the edge, and the 4-cycles
  through it without diagonals. It is > −2: n/(n − 1) on the complete
  graph K_n, zero on grids and 4/(r + 1) − 2 on the tree T_r (Table 1).
  Negative means the edge is a bridge between the two neighbourhoods
- **Relation to Ollivier curvature** (Theorem 2): κ(i, j) ≥ Ric(i, j) on
  unweighted graphs, where κ is Ollivier curvature in the Lin–Lu–Yau form
  (the limit of the α-lazy curvature as the idleness α → 1, divided by
  1 − α). Ric costs O(|E|·d_max²) against O(|E|·d_max³) for κ
- **Negative curvature causes the bottleneck** (Theorem 4): if
  Ric(i, j) ≤ −2 + δ with δ small relative to the degrees, there is a set
  Q of more than 1/δ two-hop neighbours of i whose average Jacobian with
  respect to i is below (αβ)²·δ^{1/4}. It is a statement about two hops
- **Diffusion rewiring is limited** (Theorem 6): rewiring with the
  personalized-PageRank kernel, as DIGL does, leaves the Cheeger constant
  of a set S within a factor (1 − α)/α · d_avg/d_min of the old one. On two
  cliques joined by one edge, the bound is O(n^{-2})
- **SDRF** (Algorithm 1): repeatedly add the edge near the most negatively
  curved edge that most raises its curvature, sampled by softmax at
  temperature τ, and remove the most positively curved edge above C⁺
- **Experiments** (Table 2, GCN, hyperparameters tuned per dataset and
  preprocessing by random search over 100 splits, 95% bootstrap
  intervals): SDRF beats no rewiring on all nine datasets, most on the
  low-homophily ones. Actor goes from 23.84 to 28.42 and Squirrel from
  30.32 to 37.05. With undirected edges, Texas goes to 70.35 and
  Wisconsin to 61.55. Edges changed are 0.2–33% for SDRF and 73–8,331%
  added for DIGL (Table 3). The degree distribution's W1 to the original
  is 0.03–0.28 for SDRF and 11.8–831.9 for DIGL on the three shown

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). Read in its v4 (4 October 2026). The arXiv comment
says v2 corrected Corollary 3, and nothing more about later versions.

**It extends Alon and Yahav** ([LIT-tmpt6hyo](LIT-tmpt6hyo.md)): it takes their
over-squashing and bottleneck from intuition to a Jacobian bound, and
locates the bottleneck at negatively curved edges. It is also
`compared_against` them, running their fully adjacent last layer (+FA) as
a baseline. +FA is the best entry on Cornell (58.29) and Pubmed (79.48),
is slightly ahead of plain SDRF on Texas, and is within half a point of
it on Wisconsin, Chameleon and Squirrel. It loses 1.8 points to no
rewiring on Citeseer.

**Not Ollivier–Ricci, and not Ni et al.'s flow.** [LIT-766](LIT-766.md) computes
Ollivier–Ricci curvature with idleness α = ½ on weighted graphs and runs a
Ricci flow on edge weights that stretches negatively curved edges until
surgery cuts them. Balanced Forman curvature is a different, combinatorial
quantity, defined on unweighted graphs. Its tie to Ollivier curvature is
Theorem 2's one-sided bound against the Lin–Lu–Yau form. SDRF also runs
the other way: it adds edges to support a negatively curved edge and
homogenize curvature. The paper names Ni et al. as the contrast, where
"it becomes increasingly expensive to propagate messages across
negatively curved edges".

**Where the headline stops.** Theorem 4 covers two-hop propagation, and
the experiments are node classification, which Alon and Yahav call
short-range. No experiment isolates over-squashing on a long-range task.
The WebKB sets have 135–184 nodes, and plain SDRF trails DIGL or +FA on
Cornell, Texas, Cora, Citeseer and Pubmed. The Jacobian figure (Appendix F.3)
shows both DIGL and SDRF raising two-hop sensitivity on Cornell. Di
Giovanni et al. ([LIT-tmpggqnq](LIT-tmpggqnq.md)) extend the account past two hops. The
account is [THEORY-tmpk02h3](../theory.d/THEORY-tmpk02h3.md).

Read — [NOTE-tmp9fulo](../notes.d/NOTE-tmp9fulo.md).
