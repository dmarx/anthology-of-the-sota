---
status: 'Active'
title: 'A Necessary and Sufficient Condition for Consensus Over Random Networks'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '2008-03-01'
doi: '10.1109/TAC.2008.917743'
first_author: 'Tahbaz-Salehi'
keywords:
- 'consensus'
- 'random-networks'
- 'ergodicity'
- 'spectral-gap'
implementations: []
summary: >-
  Tahbaz-Salehi and Jadbabaie (2008), [DOI:10.1109/TAC.2008.917743.](https://doi.org/10.1109/TAC.2008.917743.) Consensus
  over random networks holds if and only if the expected topology has a
  spanning tree — the condition is on the average graph, not on each round.
---
# LIT-tmpp5h8k: A Necessary and Sufficient Condition for Consensus Over Random Networks

Tahbaz-Salehi and Jadbabaie (2008) — [DOI:10.1109/TAC.2008.917743](https://doi.org/10.1109/TAC.2008.917743)

## Key takeaways

This paper provides the first necessary AND sufficient condition for almost-
sure asymptotic consensus in discrete-time linear systems x(k) = W(k)x(k-1)
where W(k) are IID random weight (mixing) matrices. The condition is:
E[W(k)] has exactly one eigenvalue of unit modulus (equal to 1),
equivalently, the expected weighted directed graph of E[W] has a directed
spanning tree. Prior work (Jadbabaie et al. 2003) had only sufficient
conditions for deterministic switching networks; this paper gives a tight
characterization for the IID random case. The proof reduces consensus to the
ergodicity of infinite matrix products using probabilistic arguments,
bypassing Lyapunov methods.

- **Main Theorem (Theorem 1 / TAC 2008).** The system x(k) = W(k)x(k-1)
  achieves almost sure asymptotic consensus (i.e., x(k) → c·1 a.s. for some
  random scalar c) if and only if E[W(k)] has exactly one eigenvalue with
  unit modulus (λ = 1 with multiplicity 1, all other eigenvalues satisfy |λ|
  < 1).
  *Holds when:* W(k) IID, row-stochastic, nonneg entries. No assumptions on
  individual realizations.
- **Graph-theoretic equivalent (Corollary).** Under the same IID row-
  stochastic setup, almost sure consensus holds iff the expected weighted
  directed graph G(E[W]) contains a directed spanning tree (i.e., there
  exists a root node with directed paths to all other nodes in G(E[W])).
  *Holds when:* Directly verifiable from the topology distribution without
  eigenvalue computation.
- **Ergodicity reduction (Lemma).** For IID row-stochastic matrices, weak
  ergodicity of the infinite matrix product {W(k)·W(k-1)···W(1)} implies
  strong ergodicity. That is, if the product converges in the sense that any
  two rows become equal almost surely, all rows converge to the same limit
  vector almost surely.
  *Holds when:* IID assumption is critical; the IID structure makes
  weak→strong ergodicity automatic.
- **Convergence to average (Special case).** If the matrices W(k) are doubly
  stochastic (columns also sum to 1) almost surely, consensus converges to
  the average: c = (1/n) * sum_i x_i(0) almost surely.
  *Holds when:* Doubly stochastic means the uniform distribution is
  invariant — no drift in the mixing.

## What the evidence does not cover

- Assumes IID random matrices. For non-IID (adversarially chosen,
  correlated, or Markovian) topologies, the result does not hold — only
  sufficient conditions are available (Jadbabaie et al. 2003 union spanning
  tree, or joint spectral radius < 1).
- Establishes existence of consensus but does not give an explicit finite-
  time convergence rate. The spectral gap of E[W] controls the rate but the
  exact bound requires additional analysis (see Olshevsky & Tsitsiklis 2011
  for quantitative bounds).
- The model is purely averaging/linear consensus (no gradient, no loss
  function). The application to SGD/gossip training requires additional
  analysis of the gradient noise and optimization error layered on top of
  the consensus dynamics.
- Does not cover Byzantine failures: adversarial nodes that inject arbitrary
  W(k) values can violate the IID assumption and break the theorem's
  guarantees.
- The main theorem is for average consensus (single scalar convergence
  value). For weighted averages or optimization objectives, additional
  conditions on W(k) structure are needed.

## Standing in the anthology

Read — the reading is [NOTE-tmpd9dec](../notes.d/NOTE-tmpd9dec.md). Arrived in the imported batch, which
brought in the consensus, synchronization and flocking literature that the
decentralized-training results rest on.
