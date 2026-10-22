---
status: Read
paper: 'LIT-tmpivepp'
title: 'GNNs exponentially lose expressive power'
version: 1
date: '2026-10-22'
summary: >-
  A ReLU GCN's features approach the component-and-degree subspace at rate
  (sλ)^l. The condition sλ < 1 bites on dense graphs and barely at all on
  sparse citation graphs, which the experiments densify. Main text and the
  experimental appendix read, proofs skimmed.
---

# NOTE-tmp36ez0: GNNs exponentially lose expressive power

## Contribution

The over-smoothing limit proved for networks with weights and ReLU, with
an explicit rate that ties the weights' scale to the graph's spectrum.

## Key insight

**Over-smoothing is a race between the weights and the graph.** Each
propagation step shrinks the component of the features that varies within
a component by a factor of λ. The weights can stretch it back by up to s.
When sλ < 1 the graph wins and depth erases everything except
component membership and degree.

## Key results

- Theorem 1: d_M(f_l(X)) ≤ s_l·λ·d_M(X) under non-negativity and
  invariance assumptions on the subspace
- Theorem 2: for GCN, d_M(X^(l)) ≤ (sλ)^l·d_M(X^(0)), with λ the largest
  |1 − μ| over the augmented normalized Laplacian's nonzero eigenvalues μ
- Theorem 3: on dense Erdős–Rényi graphs the allowed s grows without bound
  in N, so most GCNs lose information
- §6.2: the bound is close to the observed distance when sλ is small and
  loose when it is large
- §6.3–6.4: on Noisy Cora, accuracy is higher with s outside the
  information-loss region. Accuracy correlates with the size of the
  component orthogonal to the subspace (R = 0.545, or 0.827 excluding
  one-layer models)

## Limitations

- **ReLU only.** The proof uses ReLU as a projection onto the non-negative
  cone
- **Node classification only.** No readout, so not graph classification
- **Sparse real graphs are barely covered**, and the authors say so: the
  threshold on Cora is 1.0036. The experiments add random edges
- **Weight scaling is tested on the noisy graphs, with 3 trials**, and
  results are given only as figures
- **Residual connections are not analysed**, and the authors flag 56-layer
  residual GCNs as a case their intuition does not cover
