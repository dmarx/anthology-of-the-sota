---
number: 18
status: 'Active'
title: 'Balance pipeline stages to minimize bubble overhead'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Gained the bubble expression on reading the source for #114. The
    paper's analysis assumes evenly balanced partitions explicitly,
    which is what makes balance a precondition rather than an
    optimisation. The recommendation is unchanged.
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

## What "minimize bubble overhead" means quantitatively

The bubble is `O((K − 1)/(M + K − 1))` for `K` partitions over `M`
micro-batches, and [LIT-016](../literature.d/LIT-016.md) states that its Figure 2(c) analysis **assumes
partitions are evenly balanced**.

That assumption is the reason balance is a precondition and not a tuning
opportunity. The formula describes the idle time from filling and draining a
pipeline whose stages take equal time; with unequal stages there is a second,
larger source of idling — every stage waits on the slowest — and the paper's
expression no longer describes the loss. Balancing does not *minimise* the
bubble so much as make the bubble the only thing left to minimise.

## The other axis, easy to miss

Balancing *memory* matters as much as balancing time, and the two conflict.
Earlier stages hold activations for more in-flight micro-batches than later
ones — stage 1 is holding *k* of them when stage *k* is holding one — so an
even split by compute leaves the early stages under memory pressure. The
usual answer is to give earlier stages fewer layers, which unbalances the
time deliberately to balance the memory.
