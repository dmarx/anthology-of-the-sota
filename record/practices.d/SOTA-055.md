---
number: 55
status: 'Active'
title: 'Save optimizer state every N epochs (N ~ sqrt(total_epochs))'
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

# SOTA-055: Save optimizer state every N epochs (N ~ sqrt(total_epochs))

## Source

Mohan et al. (2021), [LIT-059](../literature.d/LIT-059.md) — https://www.usenix.org/conference/fast21/presentation/mohan.

## The source argues against this practice

This is the strongest case in the cluster and it goes the other way. [LIT-059](../literature.d/LIT-059.md)
opens on the observation that checkpointing "had been epoch-granular and
hand-tuned", and both halves are named as the problem:

- **Epoch granularity** is too coarse. CheckFreq's contribution is to make
  checkpointing *iteration*-granular, because an epoch on a large corpus is
  hours and a failure inside one loses all of it.
- **A hand-tuned interval** is a guess. The frequency is derived from online
  profiling and adapted at runtime against an overhead bound.

"Every N epochs, N ~ sqrt(total_epochs)" is a hand-tuned interval at epoch
granularity. It is precisely the practice the cited paper exists to replace,
and no reading of [LIT-059](../literature.d/LIT-059.md) supports it.

Nor is the formula the paper's, or anyone's that the record can point to.
Where it came from is not recoverable from the document.

## What this needs

Not a body. Either a source that argues for a closed-form epoch interval, or
retirement — and if it is retired, the successor is the mechanism in
[SOTA-054](SOTA-054.md)'s discussion rather than a different constant. Left `Active` and
flagged rather than retired here, because changing a practice's status is a
claim about the world and belongs in its own contribution, not in a pass
that was supposed to be writing bodies.

This is the finding the worklist in [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) anticipated: a practice whose source
does not support it, discovered by trying to write down why it holds.
