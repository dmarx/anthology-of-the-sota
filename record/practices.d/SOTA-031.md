---
number: 31
status: 'Active'
title: 'Keep micro-batch size per GPU as large as memory allows'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2019-10-01'
source:
- LIT-027
summary: >-
  Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).
---

# SOTA-031: Keep micro-batch size per GPU as large as memory allows

## Source

Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).

## What the micro-batch is trading against

Per-GPU batch is the lever that decides how much of each step is arithmetic
and how much is overhead. A larger micro-batch amortises kernel launches,
optimizer work and — under [SOTA-028](SOTA-028.md)'s line — the collectives, over more
tokens, so throughput rises until memory runs out. Gradient accumulation then
supplies whatever global batch the training recipe calls for, which is why
[LIT-027](../literature.d/LIT-027.md) states the two together: micro-batch from memory, accumulation steps
from the target global batch.

Under ZeRO-3 ([SOTA-030](SOTA-030.md)) it does more than amortise: parameters are gathered
per layer whatever the micro-batch, so a small one pays that cost over fewer
tokens.

## Where "as large as memory allows" stops being right

The rule is about the *micro*-batch, and it is only safe because accumulation
holds the global batch fixed. Where the global batch is allowed to grow with
it, the recommendation collides with the critical-batch-size argument —
[SOTA-092](SOTA-092.md) and [SOTA-093](SOTA-093.md) are the two halves of that, and past some size the
extra tokens per step stop buying proportionate progress.

The other limit is activation memory: filling memory with activations to the
last megabyte leaves nothing for fragmentation or a longer sequence, and the
run dies at an inconvenient step count rather than at step one.
