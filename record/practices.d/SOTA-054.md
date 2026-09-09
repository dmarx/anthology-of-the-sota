---
number: 54
status: 'Active'
title: 'Checkpoint frequency should increase with training time'
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

# SOTA-054: Checkpoint frequency should increase with training time

## Source

Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.

## What the source says instead

[LIT-059](../literature.d/LIT-059.md)'s argument is that the interval should not be *chosen* at all. It
had been epoch-granular and hand-tuned, which makes it a guess in both
directions — too rare and a failure costs hours of recomputation, too
frequent and the write dominates — so CheckFreq derives the frequency from
systematic online profiling, at iteration granularity, and then tunes it at
runtime so that overhead stays inside a stated bound as conditions change.

Increasing frequency with training time is a reasonable-sounding rule, and it
is a rule of the kind the paper is arguing against. There is a defensible
version of it: the value at risk does grow as a run proceeds, since a failure
late costs more recomputation than one early. But that is an argument about
the *objective*, and CheckFreq's answer is to let the profiler and the
overhead bound settle the interval rather than any schedule.

## What to do with this practice

Read the title as a heuristic standing in for a mechanism the source
supplies. Where the mechanism is available — a loader that profiles and
adapts — it should be preferred, and this practice is at best its rough
approximation. Where it is not, an interval that tightens as the run
lengthens is better than a fixed one chosen once.

Flagged rather than retired: the recommendation is not wrong so much as
superseded by its own source, and deciding which of those it is affects
[SOTA-055](SOTA-055.md) in the same cluster.
