---
status: Active
title: 'DiLoCo: Distributed Low-Communication Training of Language Models'
version: 1
tags:
- distributed-optimization
date: '2026-09-07'
published: '2023-11-01'
arxiv: '2311.08105'
first_author: 'Douillard'
keywords:
- 'distributed-training'
- 'communication-efficiency'
- 'federated-averaging'
- 'outer-optimizer'
- 'fault-tolerance'
summary: >-
  Douillard et al. (2023), [ARXIV-2311.08105](https://arxiv.org/abs/2311.08105). Training on islands of badly
  connected devices instead of one tightly coupled cluster: many inner AdamW
  steps per worker, Nesterov momentum as the outer optimizer over the
  resulting deltas, synchronised rarely. On C4 with 8 workers it matches fully
  synchronous training while communicating 500× less, and tolerates workers
  appearing and disappearing mid-run.
corrected_by:
- LIT-tmpwmo68
---

# LIT-tmp84crn: DiLoCo: Distributed Low-Communication Training of Language Models

Douillard et al. (2023) — [ARXIV-2311.08105](https://arxiv.org/abs/2311.08105)

## Key takeaways

**The constraint it attacks is co-location, not bandwidth.** Standard
distributed training exchanges gradients every step, so every accelerator has
to sit behind a low-latency high-bandwidth link — which means one cluster, and
a big one. DiLoCo's premise is that several small clusters are easier to
obtain than one large one, and the algorithm is what makes that arrangement
trainable rather than a compromise.

**The shape is federated averaging with the constants pushed hard.** A large
number of inner steps per worker, AdamW as the inner optimizer, and — the
part that is not standard federated averaging — **Nesterov momentum as the
outer optimizer** applied to the accumulated worker deltas. The outer momentum
is what recovers the quality that infrequent synchronisation would otherwise
cost.

**500× less communication at matched quality**, on C4 with 8 workers, against
fully synchronous optimization. Robust to workers holding differently
distributed data, and robust to resources disappearing and reappearing during
the run — which is a property of the algorithm rather than a checkpointing
trick.

## Standing in the anthology

**It fills a hole in the oldest part of the registry.** The record's
distributed material — pipeline parallelism, the ZeRO stages, allreduce
tuning, sharding factors — is entirely inherited from the pre-migration
corpus and assumes exactly the thing DiLoCo relaxes: that all the devices are
in one place and talk every step. Nothing in the record contemplates training
across poorly connected islands.

That gap is worth naming rather than quietly filling, because it changes what
several existing practices are advice *about*. The allreduce and buffer-size
recommendations are tuning within a synchronous regime; DiLoCo is a different
regime, and their advice neither applies nor conflicts.

**Not filed as a practice here.** The record has no frontier report training
this way, and the result is at 8 workers on C4 rather than at the scale its
own motivation describes. Its successor ([LIT-tmpwmo68](LIT-tmpwmo68.md)) takes the bandwidth
argument further and is where the practical case is made; a practice, if one
is filed, should rest on both.
