---
number: 30
status: 'Active'
title: 'Use ZeRO-3 only when other strategies insufficient'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-027
extends:
- SOTA-029
summary: >-
  Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).
extended_by:
- SOTA-116
---

# SOTA-030: Use ZeRO-3 only when other strategies insufficient

## Source

Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).

## Why this stage is the one with a condition on it

Partitioning the parameters as well takes the per-rank cost to 16Ψ/N — a
reduction that is linear in the number of ranks, with no floor. That is the
stage that puts a model on a cluster that could not otherwise hold it.

It is also the first stage that is not free. The parameters have to be
gathered before each layer's forward and again for its backward, and
[LIT-027](../literature.d/LIT-027.md) reports the total communication volume rising to **about 1.5× that
of standard data parallelism**. Stages 1 and 2 leave it unchanged; this one
does not, and on a slow interconnect that shows up directly in step time.

## So the ordering is a real recommendation, not caution

Take the stages that cost nothing first. Reach for stage 3 when the model,
its activations and its state genuinely do not fit at stage 2 — or when
trading step time for a larger micro-batch is the better bargain, which is a
measurement rather than a rule.

The comparison to make is against the alternatives for the same problem:
tensor and pipeline parallelism also make a too-large model fit, at the cost
of a partitioning the model code has to know about. ZeRO-3's appeal is that
it leaves the model code alone.
