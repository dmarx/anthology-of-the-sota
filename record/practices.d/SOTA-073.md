---
number: 73
status: Rejected
status_note: >-
  states no signal, threshold or action, so there is nothing to do
  differently on reading it, and LIT-051 does not argue for it. The
  specific version worth having is in SOTA-048's body: the gap between
  achieved and peak bandwidth during the overlap window tells you the
  fusion buffer is sized wrong
title: 'Monitor network utilization during training'
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

# SOTA-073: Monitor network utilization during training

## Source

Jiang et al. (2020), [LIT-051](../literature.d/LIT-051.md) — https://www.usenix.org/conference/osdi20/presentation/jiang.

## Not a recommendation, and not from this paper

"Monitor network utilization during training" states no condition, no
threshold and no action — it is a category of good practice rather than
something a reader can do differently tomorrow. Compare [SOTA-045](SOTA-045.md), which says
what to measure, why the obvious measurement is wrong, and what technique
gets it right.

[LIT-051](../literature.d/LIT-051.md) does not argue for it. Its contribution is the unified
all-reduce/parameter-server framework and the Summation Service split
described under [SOTA-047](SOTA-047.md).

## What would make it a practice

A specific signal and what it tells you. The useful version in this area does
exist: the gap between achieved and peak interconnect bandwidth during the
overlap window tells you whether the fusion buffer is sized wrong
([SOTA-048](SOTA-048.md)), and a step time that is insensitive to batch size tells you the
job is communication-bound rather than compute-bound.

As written, this is a bullet. Flagged for restatement or retirement rather
than given a body arguing for something it does not say.
