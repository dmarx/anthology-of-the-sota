---
number: 10
status: 'Active'
title: 'skip connections promote training stability by smoothing out the loss landscape'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2017-12-01'
source:
- LIT-014
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).
---

# SOTA-010: skip connections promote training stability by smoothing out the loss landscape

## Source

Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).

## The strongest visual result in the paper

[LIT-014](../literature.d/LIT-014.md)'s most cited figure is a pair: the same deep network with and without
skip connections, plotted the same way. Without them the surface is chaotic —
non-convex, with visible barriers between nearby points. With them it is
smooth and close to convex over the region plotted.

That is a claim about *trainability* rather than about capacity: the residual
network is not more expressive, it is reachable. It explains why depth stopped
being the barrier it had been, and why the residual connection is the one
architectural element every model in this record shares.

## What follows, and what does not

It is why the practices around residual streams are about *what to do with*
them rather than whether to have them — where to normalise ([SOTA-032](SOTA-032.md)), how
strongly to initialise the branch ([SOTA-051](SOTA-051.md), [SOTA-060](SOTA-060.md)), how many streams to
<!-- inactive-ok-block: SOTA-136, SOTA-169 — Proposed, cited as the open questions about residual streams that this result underwrites -->
run ([SOTA-136](SOTA-136.md), [SOTA-169](SOTA-169.md)).

The visualisation is a two-dimensional slice through a very high-dimensional
surface, chosen by random filter-normalised directions. It is evidence about
the geometry, not a proof of it, and the paper is careful about this in a way
summaries of it usually are not. What survives is the qualitative contrast,
which is large and reproduces; the record should not read a slice as a
measurement.
