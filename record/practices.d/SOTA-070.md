---
number: 70
status: 'Active'
title: 'Track gradient norm ratios between layers'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2022-10-01'
source:
- LIT-054
summary: >-
  Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).
compared_against:
- SOTA-099
---

# SOTA-070: Track gradient norm ratios between layers

## Source

Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).

## What a ratio catches that a global norm does not

A single global gradient norm goes up when anything goes wrong, which makes
it a good trigger and a poor diagnostic. The ratio between layers localises
it: an early layer whose gradient norm is orders of magnitude below the late
layers' is a vanishing-signal problem, and one layer spiking alone is usually
a specific numerical event — an attention logit overflow, a dead
normalisation — rather than a training-wide instability.

That distinction is what decides the response. A global spike is answered by
clipping ([SOTA-071](SOTA-071.md)) or by rewinding ([SOTA-095](SOTA-095.md)); a single-layer anomaly is
answered by looking at that layer.

## Cost

Per-layer norms are a reduction per parameter tensor per step. On a sharded
job that means a collective, or an approximation from the local shard, and at
every step it is not free — which is why the usual arrangement is a full pass
periodically and the global norm continuously.

The other cost is attention. Four monitoring practices in this cluster
produce four dashboards, and a signal nobody has a rehearsed response to is a
signal nobody reads.
