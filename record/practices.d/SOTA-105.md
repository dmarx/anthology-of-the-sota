---
number: 105
status: 'Active'
title: 'PagedAttention to accelerate batch inference for LLM sampling'
version: 1
tags:
- inference-optimization
date: '2026-08-24'
source:
- LIT-112
summary: >-
  Kwon et al. (2023), [LIT-112](../literature.d/LIT-112.md) — [ARXIV-2309.06180](https://arxiv.org/abs/2309.06180).
extended_by:
- SOTA-113
---

# SOTA-105: PagedAttention to accelerate batch inference for LLM sampling

## Source

Kwon et al. (2023), [LIT-112](../literature.d/LIT-112.md) — [ARXIV-2309.06180](https://arxiv.org/abs/2309.06180).

## The fragmentation problem, and the borrowed idea

Serving batches many requests whose KV caches grow at different rates and
finish at different times. Allocating each a contiguous block sized for the
maximum length wastes most of it — the request that stops after 200 tokens
still holds an allocation for 4,096 — and the free space left behind is
scattered in pieces too small to reuse.

PagedAttention borrows the operating system's answer: the cache is stored in
fixed-size blocks, and a request's blocks need not be contiguous, with an
indirection table mapping logical positions to physical blocks. Internal
fragmentation is bounded by one block, external fragmentation disappears, and
the memory that is freed is immediately usable by anyone.

## What the recovered memory is spent on

More concurrent requests, which is the whole point: throughput at a given
latency is set by how many sequences fit in memory at once, so recovering the
waste converts almost directly into batch size ([SOTA-113](SOTA-113.md)).

Two capabilities fall out of the indirection rather than being added: blocks
can be **shared** between requests with a common prefix — a system prompt
materialised once, not once per request — and copy-on-write makes parallel
sampling from one prompt nearly free.

## Condition

This is an inference practice, and the record should be explicit that it does
not transfer to training: there is no KV cache to fragment in a training step,
and the memory pressure there is activations and optimizer state, which the
practices around [SOTA-028](SOTA-028.md) address instead.
