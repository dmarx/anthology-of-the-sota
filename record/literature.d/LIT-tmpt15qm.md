---
status: 'Active'
title: 'A Growing Neural Gas Network Learns Topologies'
version: 1
tags:
- representation-and-encoding
date: '2026-09-15'
published: '1994-12-01'
url: 'https://proceedings.neurips.cc/paper_files/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html'
first_author: 'Fritzke'
keywords:
- 'growing-neural-gas'
- 'topology-learning'
- 'vector-quantization'
- 'incremental-networks'
implementations: []
summary: >-
  Fritzke (1994), [A Growing Neural Gas Network Learns Topologies](https://pro
  ceedings.neurips.cc/paper_files/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c00
  67e7-Abstract.html). Growing neural gas: insert units where the accumulated
  error is largest, so the network finds its own size and topology without an
  annealing schedule.
---
# LIT-tmpt15qm: A Growing Neural Gas Network Learns Topologies

Fritzke (1994) — [A Growing Neural Gas Network Learns Topologies](https://proceedings.neurips.cc/paper_files/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html)

## Key takeaways

Introduces the Growing Neural Gas (GNG) algorithm, an incremental
unsupervised network that learns the topology of a data distribution by
combining competitive Hebbian learning with periodic insertion of new units
at locations of high accumulated quantization error. Unlike Martinetz &
Schulten's neural gas, GNG uses only constant parameters (no annealing) and
network size need not be specified in advance.

- **Informal (no formal theorem).** Edges produced by competitive Hebbian
  learning form a subgraph of the Delaunay triangulation (the 'induced
  Delaunay triangulation') which optimally preserves topology of P(xi)
  *Holds when:* Result attributed to Martinetz (1993); GNG tracks this graph
  as units move.
- **Empirical demonstration.** GNG adapts to distributions of varying
  intrinsic dimensionality and clustered distributions, producing center
  distributions comparable to NG with 100 units
  *Holds when:* Demonstrated with lambda=100, eps_b=0.2, eps_n=0.006,
  alpha=0.5, a_max=50, d=0.995

## What the evidence does not cover

- No formal convergence or consistency theorems
- Assumes stationary input distribution; behavior under drift is not
  analyzed
- Requires choosing 6 hyperparameters (lambda, eps_b, eps_n, alpha, d,
  a_max) and a stopping criterion
- Empirical evaluation is limited to 2D toy distributions
- Edge aging threshold a_max effectively reintroduces a time-scale parameter
  despite the 'no annealing' claim

## Standing in the anthology

Read — the reading is [NOTE-tmpkjsbu](../notes.d/NOTE-tmpkjsbu.md). Arrived in the imported batch, which
brought in the competitive-learning and vector-quantization line.
