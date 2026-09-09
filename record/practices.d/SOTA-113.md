---
number: 113
status: 'Active'
title: 'Use continuous batching for inference'
version: 1
tags:
- inference-optimization
date: '2026-08-24'
published: '2023-09-01'
source:
- LIT-112
extends:
- SOTA-105
summary: >-
  Kwon et al. (2023), [LIT-112](../literature.d/LIT-112.md) — [ARXIV-2309.06180](https://arxiv.org/abs/2309.06180).
extended_by:
- SOTA-115
---

# SOTA-113: Use continuous batching for inference

## Source

Kwon et al. (2023), [LIT-112](../literature.d/LIT-112.md) — [ARXIV-2309.06180](https://arxiv.org/abs/2309.06180).

## Why static batching wastes most of a serving GPU

A static batch runs until every sequence in it finishes, so the whole batch is
held hostage by its longest generation while the finished slots sit idle
producing nothing. Generation lengths in real traffic differ by more than an
order of magnitude, so that idle fraction is large.

Continuous batching schedules at the *iteration* rather than the request:
a sequence that emits its stop token leaves at the end of that step and a
waiting request takes its slot immediately. The batch is refilled constantly
rather than drained and refilled.

## What it depends on, which is [SOTA-105](SOTA-105.md)

Admitting a new request mid-flight means finding memory for its KV cache
right now, in whatever is free. Under contiguous allocation there usually
isn't a suitable hole, which is why continuous batching and paged KV memory
arrived together and why the record holds them as a pair rather than as two
independent tricks.

## Cost

Latency variance. A request admitted into a busy batch shares bandwidth with
everything else in flight, so per-request latency depends on what else is
running — worse tail latency in exchange for much higher throughput. A serving
target expressed as a p99 rather than as a mean is the one that notices.

The scheduler also becomes a real component with its own policy: which waiting
request to admit, whether to preempt a long generation, how to avoid starving
large prompts. Those choices are invisible in the practice as stated and are
where serving systems actually differ.
