---
number: 82
status: 'Active'
title: 'Optimize memory layout for hardware'
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

# SOTA-082: Optimize memory layout for hardware

## Source

Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).

## Layout is a real decision, and it is usually made by default

The same tensor can be laid out several ways — NCHW or NHWC, row- or
column-major, blocked into tiles matching a vector width — and the right
choice depends on what reads it. A convolution kernel tuned for one layout
runs badly on the other, and a graph that mixes producers and consumers with
different preferences pays for a transpose between them.

Frameworks pick a default, and the default is usually the one that suited the
hardware the framework grew up on. [LIT-063](../literature.d/LIT-063.md)'s related finding in [LIT-066](../literature.d/LIT-066.md)'s
words is that existing implementations use suboptimal layouts — a statement
about defaults, not about missing features, which is why the fix is available
to anyone willing to measure.

## What the practice actually asks of a reader

Not to hand-pick layouts. To let the compiler choose them, and to know that
the choice is being made — because the visible symptom of a bad one is a
transpose or a copy appearing in the profile between two operations that
should have been adjacent.

The cost of getting it right is that layout is a global decision: optimising
one operator's layout can force conversions around it that cost more than the
operator saved. That is why it belongs to a graph-level optimiser rather than
to a per-kernel choice, and why "optimize memory layout for hardware" is
better read as a property to check than as a task to do.
