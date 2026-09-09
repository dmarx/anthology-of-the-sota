---
number: 19
status: 'Active'
title: 'Choose pipeline chunks based on memory vs. compute trade-off'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2018-11-01'
source:
- LIT-016
summary: >-
  Huang et al. (2018), [LIT-016](../literature.d/LIT-016.md) — [ARXIV-1811.06965](https://arxiv.org/abs/1811.06965).
---

# SOTA-019: Choose pipeline chunks based on memory vs. compute trade-off

## Source

Huang et al. (2018), [LIT-016](../literature.d/LIT-016.md) — [ARXIV-1811.06965](https://arxiv.org/abs/1811.06965).

## The two ends of the dial

The chunk count is the *m* in [SOTA-017](SOTA-017.md)'s bubble formula, and it trades the
two costs against each other directly. Raising it shrinks the bubble as
(*k*−1)/(*m*+*k*−1) and raises activation memory roughly linearly, because
each in-flight micro-batch's activations are live until its backward pass.
Lowering it does the reverse.

There is a third cost the title does not mention and that decides the answer
more often than either: below some size a micro-batch stops filling the GPU.
Matrix multiplies at small batch are latency-bound rather than
bandwidth-bound, so cutting the batch into more chunks eventually makes each
stage slower, and the bubble you removed comes back as arithmetic
inefficiency.

## So the practical rule

Increase chunks until either memory runs out or per-stage throughput starts
falling, and take the last value before whichever comes first. Which one
binds tells you something: memory-bound means the model wants recomputation
or more stages, throughput-bound means the pipeline has more stages than the
batch can feed and the parallelism should be spent elsewhere.

The schedule matters as much as the count. GPipe's fill-drain schedule holds
all *m* micro-batches' activations at the peak; the interleaved
one-forward-one-backward schedules that followed hold far fewer for the same
bubble, which changes the memory half of this trade without touching the
time half.
