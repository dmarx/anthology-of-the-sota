---
number: 56
status: 'Active'
title: 'Use async I/O for checkpoint writing'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2021-02-01'
source:
- LIT-059
summary: >-
  Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.
---

# SOTA-056: Use async I/O for checkpoint writing

## Source

Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.

## Why the write can be hidden almost entirely

A checkpoint is a serialisation of state that the next iterations are about
to overwrite, so the only part that must be synchronous is the snapshot
itself. CheckFreq splits it in two: a fast snapshot into a separate buffer
while compute is paused, then the persist to storage pipelined against
ongoing iterations. The expensive half overlaps with training rather than
blocking it.

That is what makes frequent checkpointing affordable at all. [LIT-059](../literature.d/LIT-059.md) reports
runtime overhead bounded within 3.5% while recovery falls from hours to
seconds — and it is the overhead bound, not the write speed, that changes
what interval is reasonable to choose.

## Cost and condition

The snapshot buffer is extra memory, roughly the size of the state being
copied, held at the moment the run is already at its memory ceiling. And the
pipelining is only safe if the persist finishes before the next snapshot
starts; when storage cannot keep up, the asynchrony turns into a queue and
the overhead reappears as a stall, which is what the adaptive rate tuning in
[SOTA-054](SOTA-054.md)'s source exists to prevent.

Asynchrony also has a correctness edge: a checkpoint that is written while
training continues must be a consistent cut, or resuming from it silently
restarts from a state the run never actually occupied.
