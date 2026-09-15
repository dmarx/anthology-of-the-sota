---
status: 'Active'
title: '''Neural-gas'' network for vector quantization and its application to time-series prediction'
version: 1
tags:
- representation-and-encoding
date: '2026-09-15'
published: '1993-07-01'
doi: '10.1109/72.238311'
first_author: 'Martinetz'
keywords:
- 'neural-gas'
- 'vector-quantization'
- 'competitive-learning'
- 'time-series'
implementations: []
summary: >-
  Martinetz et al. (1993), [DOI:10.1109/72.238311.](https://doi.org/10.1109/72.238311.) Neural gas: adapt units by
  the rank of their distance to the input rather than by a fixed lattice
  neighbourhood, so no topology need be assumed.
---
# LIT-tmpxjc6m: 'Neural-gas' network for vector quantization and its application to time-series prediction

Martinetz et al. (1993) — [DOI:10.1109/72.238311](https://doi.org/10.1109/72.238311)

## Key takeaways

Introduced the Neural Gas algorithm: an unsupervised competitive learning
method for vector quantization that adapts reference vectors by ranking all
neurons by distance to each input and applying exponentially decaying
updates by rank, with no fixed grid topology. Proved convergence and showed
superiority over k-means and LVQ on time-series prediction benchmarks.

- **Convergence theorem.** Neural gas converges to a local minimum of the
  expected distortion E[||x - w_{s(x)}||^2] under standard stochastic
  approximation conditions on the learning rate schedule
  *Holds when:* Requires epsilon(t) -> 0, sum epsilon(t) = inf, sum
  epsilon(t)^2 < inf; lambda(t) -> 0

## Standing in the anthology

Read — the reading is [NOTE-tmpincwd](../notes.d/NOTE-tmpincwd.md). Arrived in the imported batch, which
brought in the competitive-learning and vector-quantization line.
