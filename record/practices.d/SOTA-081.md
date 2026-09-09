---
number: 81
status: 'Active'
title: 'Use operator fusion for small operations'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
published: '2018-02-01'
source:
- LIT-063
summary: >-
  Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).
---

# SOTA-081: Use operator fusion for small operations

## Source

Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).

## Fusion at the graph level

A chain of small elementwise operations — a bias add, an activation, a
dropout mask, a residual add — each reads its input from memory and writes
its output back, and each of those tensors is used once, immediately. The
arithmetic is negligible; the traffic is the cost. Fusing the chain into one
kernel keeps the intermediates in registers and turns *n* round trips into
one.

This is the graph-level half of what [LIT-063](../literature.d/LIT-063.md) automates, and it is the same
principle as [SOTA-114](SOTA-114.md)'s fused attention and [SOTA-088](SOTA-088.md)'s kernel fusion — the
record holds it three times because three sources arrived at it, which is
worth knowing rather than deduplicating.

## Condition, and what the compiler changes about it

It pays where the operations are memory-bound and adjacent in the graph. It
does nothing for a matmul, which is already compute-bound, and it cannot
cross a boundary where a tensor is genuinely needed later — a residual whose
input is used again downstream has to be materialised.

TVM's contribution is that this stops being a hand-written kernel per
combination. The point of the paper is *portability of performance*: vendor
libraries cover a narrow set of targets, and a compiler that generates the
fused kernel covers whatever the target is. That is the argument [SOTA-083](SOTA-083.md) sits
awkwardly against.
