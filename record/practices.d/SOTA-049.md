---
number: 49
status: 'Active'
title: 'Set buffer size to network bandwidth-delay product'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2020-11-01'
source:
- LIT-051
summary: >-
  Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.
---

# SOTA-049: Set buffer size to network bandwidth-delay product

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## What is wrong with this one

The bandwidth-delay product is the amount of data in flight on a link at
full rate, and it is the right sizing rule for a *TCP socket buffer* or a
congestion window. It is not the rule for a gradient fusion buffer, which is
what "buffer" means everywhere else in this cluster ([SOTA-048](SOTA-048.md)): that size is
a trade between amortising per-collective overhead and preserving the overlap
with the backward pass, and it has nothing to do with round-trip time.

Two different quantities have been collapsed into one sentence. Either
reading is defensible on its own; together they are a recommendation that
cannot be followed, because it does not say which buffer.

[LIT-051](../literature.d/LIT-051.md) supports neither. Its contribution is the unified communication
framework and the Summation Service split ([SOTA-047](SOTA-047.md)).

## What it needs

Splitting or retiring. If it means the fusion buffer, [SOTA-048](SOTA-048.md)'s body already
states the real trade and this adds nothing. If it means transport tuning,
that is a claim about the network stack rather than about training, and needs
a source that is about networks.
