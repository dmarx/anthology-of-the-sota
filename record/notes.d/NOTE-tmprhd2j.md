---
status: Read
paper: 'LIT-tmpggqnq'
title: 'Over-squashing: width, depth and topology'
version: 1
date: '2026-10-22'
summary: >-
  Width raises sensitivity everywhere and does not target the starved
  pairs. Depth near the distance over-squashes, and depth far beyond it
  vanishes the gradients. Commute time bounds the obstruction from both
  sides, which is why rewiring that lowers effective resistance helps.
  Main text and experimental appendices read, proofs not checked.
---

# NOTE-tmprhd2j: Over-squashing: width, depth and topology

## Contribution

It extends the Jacobian account of over-squashing to arbitrary width,
depth past the distance, and global topology, and it gives one reason why
spatial, spectral and curvature rewiring all help.

## Key insight

**Over-squashing is a property of the pair of nodes, set by the graph,
and the model can only scale it.** Width and weight scale multiply every
sensitivity by the same factor. Depth turns the problem into vanishing
gradients. What separates a pair that communicates from one that does not
is how long a random walk takes to go between them and back.

## Key results

- Theorem 3.2: ‖∂h_v^(m)/∂h_u^(0)‖ ≤ (c_σwp)^m (S_{r,a}^m)_vu
- Theorem 4.1: decay like (2c_σwp/d_min)^r times the walk count between
  nodes at distance r, for depth r + k with 0 ≤ k < r
- For a GCN with depth equal to the distance r, the exact topology term is
  (3/2)^{-(r−1)} on CrossedRing, 2^{-(r−1)} on Ring and
  2^{-(r−2)}/(r√(r−2)) on CliquePath. Accuracy falls in the same order
- Theorem 4.2: gradients decay exponentially in m when c_σμ(c_r + c_a) < 1
- Theorem 5.5: the symmetric obstruction Õ^(m)(v, u) is bounded below by
  a multiple of τ(v, u)/2|E| and above by a multiple of it plus a term in
  1/h_Cheeg², up to errors that vanish with m
- Appendix F: with random weights and no training, signal travels further
  on graphs with lower total effective resistance, in PROTEINS, NCI1, PTC
  and ENZYMES

## Limitations

- **No benchmark result.** Every experiment is synthetic or untrained
- **Equal-weight aggregation only.** GAT and gated models are left out of
  the theory
- **In expectation, under Assumption 5.1**, which treats ReLU paths as
  equally likely to be active
- **Which rewiring to prefer is left open**, as the authors say
