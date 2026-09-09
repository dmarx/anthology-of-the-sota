---
number: 35
status: 'Active'
title: 'use gradient clipping'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2012-11-01'
source:
- LIT-037
summary: >-
  Pascanu et al. (2012), [LIT-037](../literature.d/LIT-037.md) — [ARXIV-1211.5063](https://arxiv.org/abs/1211.5063).
---

# SOTA-035: use gradient clipping

## Source

Pascanu et al. (2012), [LIT-037](../literature.d/LIT-037.md) — [ARXIV-1211.5063](https://arxiv.org/abs/1211.5063).

## What clipping actually protects

Rescaling the gradient when its global norm exceeds a threshold bounds the
size of a single step. It does not make training stable in general — it makes
the run survive *individual* anomalous batches, which is a narrower and more
useful claim: one pathological sequence cannot take a step large enough to
leave the basin the run is in and destroy hours of progress.

That is why it is close to universal in large runs despite being crude. The
expected cost is near zero when the threshold is above the typical norm, and
the avoided cost is a rewind ([SOTA-095](SOTA-095.md)) or a dead run.

## The parameter, and its failure mode

The threshold. Set above the typical norm it clips rarely and costs nothing;
set below, it clips constantly and quietly changes the optimisation — every
step is then rescaled, so the effective learning rate is set by the threshold
rather than by the schedule, and the run trains slowly for a reason that looks
like a bad learning rate.

Monitoring the *clip rate* is what distinguishes those, and it is the signal a
fixed threshold needs, because gradient norms fall by orders of magnitude over
a run and a threshold chosen at the start eventually clips nothing. [SOTA-071](SOTA-071.md)'s
adaptive answer to that has its own failure, recorded there: a threshold that
tracks the norms rises with an excursion it exists to catch.
