---
number: 115
status: 'Active'
title: 'Overlap prefill and decode compute'
version: 1
tags:
- inference-optimization
date: '2026-08-24'
source:
- LIT-103
# Chunked prefill is a decision inside the iteration-level scheduler that
# SOTA-113 introduced: it presumes that scheduler and adds what goes in each
# step.
extends:
- SOTA-113
summary: >-
  Agrawal et al. (2023), [LIT-103](../literature.d/LIT-103.md) — [ARXIV-2308.16369](https://arxiv.org/abs/2308.16369).
---

# SOTA-115: Overlap prefill and decode compute

## Source

Agrawal et al. (2023), [LIT-103](../literature.d/LIT-103.md) — [ARXIV-2308.16369](https://arxiv.org/abs/2308.16369).

## The asymmetry, which is the whole reason

Prefill processes an entire prompt at once and saturates the GPU even at small
batch. Decode emits one token per request per step and leaves the machine
mostly idle — it is memory-bandwidth bound, reading the weights and the KV
cache to produce a single token per sequence.

Run them in separate phases and each wastes what the other needs: a
decode-only batch under-uses compute, and a prefill blocks every decode
waiting behind it, which shows up directly as inter-token latency spikes for
users mid-generation.

[LIT-103](../literature.d/LIT-103.md)'s answer is to break prefills into chunks and pack decodes alongside
them in the same step, so every batch carries enough prefill work to fill the
compute the decodes leave idle.

## What it costs

Chunking a prefill makes that request's time-to-first-token worse: the prompt
is processed over several steps rather than one. So the practice trades
first-token latency for throughput and for steadier inter-token latency, which
is the right trade for most serving and the wrong one for a workload judged on
time-to-first-token alone.

It also needs the scheduler to be doing this deliberately — chunk size against
batch composition, per step — which is the same class of decision continuous
batching introduced ([SOTA-113](SOTA-113.md)) and the same reason serving systems differ from
each other more than their model code does.
