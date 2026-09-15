---
status: 'Active'
title: 'Coordination of groups of mobile autonomous agents using nearest neighbor rules'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
published: '2003-06-01'
doi: '10.1109/TAC.2003.812781'
first_author: 'Jadbabaie'
keywords:
- 'consensus'
- 'switching-topology'
- 'nearest-neighbour'
- 'spanning-tree'
implementations: []
summary: >-
  Jadbabaie et al. (2003), [DOI:10.1109/TAC.2003.812781.](https://doi.org/10.1109/TAC.2003.812781.) Nearest-neighbour
  averaging reaches consensus provided the union of the interaction graphs
  over each bounded window is connected — the switching-topology result the
  gossip literature builds on.
---
# LIT-tmpcaxue: Coordination of groups of mobile autonomous agents using nearest neighbor rules

Jadbabaie et al. (2003) — [DOI:10.1109/TAC.2003.812781](https://doi.org/10.1109/TAC.2003.812781)

## Key takeaways

This paper provides the first rigorous theoretical justification for the
empirical flocking behavior observed in Vicsek et al. (1995). It formalizes
the nearest-neighbor heading update rule as a linear time-varying consensus
protocol and proves that a sufficient condition for global heading alignment
is that the union of communication graphs over any time window of fixed
length T contains a directed spanning tree. This union-spanning-tree
condition is the foundational sufficient condition for consensus over
deterministic switching networks, and became the template for nearly all
subsequent consensus and gossip convergence results.

- **Theorem 2 (Main consensus theorem — directed case).** Consider the
  heading update θ_i(t+1) = (1/(|N_i(t)|+1)) * [θ_i(t) + Σ_{j∈N_i(t)}
  θ_j(t)]. If there exists T > 0 such that for every integer k ≥ 0, the
  union of directed graphs G(kT) ∪ G(kT+1) ∪ ··· ∪ G(kT+T-1) has a directed
  spanning tree rooted at some (possibly different) node, then all headings
  converge to a common value: θ_i(t) → θ* as t → ∞.
  *Holds when:* T is the window length (fixed); the spanning tree root can
  vary across windows. No assumption on the speed of convergence — only
  asymptotic consensus is proven.
- **Corollary (Undirected case).** For symmetric nearest-neighbor rules
  (undirected graphs), consensus holds if the union graph over any T-length
  window is connected (spanning tree condition reduces to connectivity).
  Consensus value is not necessarily the average of initial headings unless
  the graph is doubly stochastic at every step.
  *Holds when:* Undirected graphs; T fixed; symmetric neighborhood.
- **Vicsek model connection (informal).** Vicsek's empirical model (agents
  align heading to average of neighbors within radius r, plus noise)
  exhibits consensus empirically. Jadbabaie et al. show the noiseless
  version satisfies their union-spanning-tree condition for reasonable
  densities, providing the theoretical explanation for the empirical
  observations.
  *Holds when:* Noiseless regime only; noisy version remains outside this
  theorem's scope.

## What the evidence does not cover

- Only sufficient condition — does not characterize all gossip schedules
  that achieve consensus.
- No convergence rate — proves only asymptotic consensus; spectral gap
  analysis requires additional work.
- Pure averaging consensus, not gradient optimization. Extension to SGD
  requires additional analysis.
- Noiseless model — the noisy Vicsek model (the original empirical
  motivation) is outside the theorem.
- Consensus value may not be the average of initial values unless graphs are
  doubly stochastic throughout.

## Standing in the anthology

Read — the reading is [NOTE-tmpnnrhg](../notes.d/NOTE-tmpnnrhg.md). Arrived in the imported batch, which
brought in the consensus, synchronization and flocking literature that the
decentralized-training results rest on.
