---
status: Active
title: 'On Over-Squashing in Message Passing Neural Networks: The Impact of Width, Depth, and Topology'
version: 1
tags:
- graphs-and-networks
- analysis-and-evaluation
- model-architecture
date: '2026-10-22'
published: '2023-02-06'
arxiv: '2302.02941'
first_author: 'Di Giovanni'
keywords:
- 'over-squashing'
- 'commute-time'
- 'effective-resistance'
- 'vanishing-gradients'
- 'graph-rewiring'
- 'jacobian-sensitivity'
implementations: []
extends:
- LIT-tmp0hkly
summary: >-
  Di Giovanni, Giusti, Barbero, Luise, Liò, Bronstein (ICML 2023),
  [ARXIV-2302.02941](https://arxiv.org/abs/2302.02941). A theory paper. The sensitivity of node v to node u
  after m layers is at most (c_σ·w·p)^m times the (v, u) entry of the m-th
  power of the message-passing matrix. Width p and weight scale can raise
  the bound, but for the whole network at once. With depth near the
  distance, over-squashing hits distant, badly connected nodes. With much
  more depth, gradients vanish. Averaged over layers, the obstruction
  between two nodes is bounded above and below by their commute time, under
  an assumption that every path is active with equal probability. The
  experiments are synthetic.
---

# LIT-tmpggqnq: On Over-Squashing in Message Passing Neural Networks: The Impact of Width, Depth, and Topology

Di Giovanni, Giusti, Barbero, Luise, Liò, Bronstein, Cambridge, Sapienza,
Oxford and Microsoft Research (ICML 2023) — [ARXIV-2302.02941](https://arxiv.org/abs/2302.02941)

## Key takeaways

- **Width** (Theorem 3.2): for h^(t+1) = σ(c_r W_r h_v + c_a W_a Σ A_vu h_u),
  ‖∂h_v^(m)/∂h_u^(0)‖ ≤ (c_σ·w·p)^m·(S^m)_vu with S = c_r I + c_a A. A
  wider network or larger weights raise the bound, but uniformly, so
  nearby nodes stay exponentially more sensitive than distant ones. On
  graph-transfer tasks a GCN reaches further as the hidden size grows from
  1 to 64 (Figure 2)
- **Depth near distance** (Theorem 4.1): for nodes at distance r and depth
  r + k, the bound is C_k·γ_{r+k}(v, u)·(2c_σwp/d_min)^r, with γ the
  number of walks between them. If 2c_σwp < d_min it decays exponentially
  in r. GIN, SAGE, GCN and GAT all fall to chance soonest on CliquePath,
  then Ring, then CrossedRing (Figure 3), at equal distance
- **Much more depth** (Theorem 4.2): with spectral norms bounded by μ,
  gradients with respect to a layer-k weight decay like
  (c_σμ(c_r + c_a))^{m−k}. This covers models with residual terms. The
  authors conjecture, without proof, a distance beyond which no depth helps
- **Topology** (Theorems 5.3 and 5.5): averaged over layers, the
  obstruction to v receiving from u is at least proportional to the access
  time t(u, v). The symmetric obstruction is bounded above and below by
  terms in the commute time τ(v, u) = 2|E|·Res(v, u), up to errors that
  vanish with m. Both hold in expectation, under Assumption 5.1 that every
  path in the computation graph is active with the same probability
- **What follows** (§5.3): adding edges lowers total effective resistance
  (Rayleigh monotonicity), which accounts for spatial rewiring. A larger
  Cheeger constant lowers the bound (Corollary 5.6), which accounts for
  spectral rewiring and for expander graphs. Bounded effective resistance
  bounds resistance curvature, and under some assumptions Ollivier
  curvature, from below, which recovers Topping et al.'s curvature result

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22).

**It extends Topping et al.** ([LIT-tmp0hkly](LIT-tmp0hkly.md)) and is built as an answer to
it: their Jacobian bound becomes a bound for any width, for depth beyond
the distance, and for topology beyond two hops. Their curvature result is
recovered as a consequence of bounded effective resistance. Two of the
authors overlap. It also makes formal Alon and Yahav's ([LIT-tmpt6hyo](LIT-tmpt6hyo.md))
observation that doubling the width barely helped on QM9.

**Where it stops.** The paper says that it does not tell which rewiring is
preferable, and that its analysis covers MPNNs that weigh each edge the
same up to degree normalization. Attention and gating are excluded, though
GAT also fails the graph-transfer tasks. The commute-time theorems hold in
expectation over an assumption about ReLU paths. The experiments are
synthetic: graph transfer (5,000 training graphs, depth equal to distance)
and untrained signal propagation on four TU datasets (Appendix F). Nothing
here measures a benchmark gain. The account is [THEORY-tmpk02h3](../theory.d/THEORY-tmpk02h3.md).

Read — [NOTE-tmprhd2j](../notes.d/NOTE-tmprhd2j.md).
