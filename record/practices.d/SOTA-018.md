---
number: 18
status: 'Active'
title: 'Balance pipeline stages to minimize bubble overhead'
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

# SOTA-018: Balance pipeline stages to minimize bubble overhead

## Source

Huang et al. (2018), [LIT-016](../literature.d/LIT-016.md) — [ARXIV-1811.06965](https://arxiv.org/abs/1811.06965).

## Why balance matters more here than elsewhere

A pipeline runs at the speed of its slowest stage, and every other stage
waits. Unlike data parallelism, where an imbalance costs the difference, an
imbalance here costs that difference *on every micro-batch and every stage*
— so a single stage 20% slower than the rest makes the whole pipeline 20%
slower regardless of how well the others are tuned.

That is what makes automatic partitioning part of GPipe rather than an
afterthought: the split has to equalise time, and layer count is a poor proxy
for it. Attention and MLP blocks differ in cost, embeddings and the output
head are large and cheap or small and expensive depending on vocabulary, and
the first and last stages carry the embedding tables.

## The other axis, easy to miss

Balancing *memory* matters as much as balancing time, and the two conflict.
Earlier stages hold activations for more in-flight micro-batches than later
ones — stage 1 is holding *k* of them when stage *k* is holding one — so an
even split by compute leaves the early stages under memory pressure. The
usual answer is to give earlier stages fewer layers, which unbalances the
time deliberately to balance the memory.
