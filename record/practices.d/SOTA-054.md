---
number: 54
status: 'Active'
title: 'Derive the checkpoint interval from online profiling and adapt it at runtime against an overhead bound'
version: 2
history:
- version: 1
  note: >-
    Titled "Checkpoint frequency should increase with training time" — a
    heuristic standing in for a mechanism, and not what LIT-059 recommends.
    That paper's contribution is to stop choosing the interval by hand at all.
- version: 2
# inactive-ok-block: SOTA-055 — Rejected, named in the history entry as the practice retired instead of restated
  note: >-
    Restated as what the source actually says. The subject is unchanged; the
    rule it states is now the source's rather than a paraphrase of it.
    SOTA-055, which proposed a closed-form epoch interval, is retired rather
    than restated, because it had no defensible reading left.
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-059
corrects:
- SOTA-055
summary: >-
  Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.
compared_against:
- SOTA-189
---

# SOTA-054: Derive the checkpoint interval from online profiling and adapt it at runtime against an overhead bound

## Source

Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.

## What this is instead of

Checkpointing had been epoch-granular and hand-tuned, which makes the interval
a guess in both directions: too rare and a failure costs hours of
recomputation, too frequent and the write dominates. [LIT-059](../literature.d/LIT-059.md)'s contribution is
to stop choosing it. CheckFreq profiles the run online, works at *iteration*
granularity rather than epoch, and tunes the interval at runtime so that
checkpointing overhead stays inside a stated bound as conditions change —
**within 3.5%**, while recovery falls from hours to seconds.

The title this practice carried until now — "checkpoint frequency should
increase with training time" — was a heuristic standing in for that mechanism,
and it was not what the cited paper says. There is a defensible intuition
behind it, since the value at risk grows as a run proceeds, but the paper's
answer is to let the profiler and the overhead bound settle the interval
<!-- inactive-ok: SOTA-055 — Rejected, named as the practice retired for the same reason this one was restated -->
rather than any schedule. Restated to match its source; [SOTA-055](SOTA-055.md), which
proposed a closed-form epoch interval, is retired for the same reason.

## Conditions and cost

The mechanism needs a loader that can measure its own write cost and change
the interval, which is a property of the training framework rather than of
the model. Without one, the fallback is a fixed interval chosen from a
measured write time and an accepted overhead — the same calculation, done once
by hand.

It also depends on [SOTA-056](SOTA-056.md): the overhead bound is only reachable because the
persist is pipelined against compute, so a system checkpointing synchronously
cannot hit it at any interval worth having.

What the paper adds that this record still has no practice for: **resuming
must restore the data loader's state**, or an epoch stops seeing each item
exactly once. [LIT-059](../literature.d/LIT-059.md) says most implementations get that wrong.
