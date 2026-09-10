---
number: 189
status: Proposed
formerly:
- SOTA-tmp3q7to
consensus: unassessed
title: "Set the checkpoint interval from the job's measured time-to-failure, which shrinks as the job grows"
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
source:
- LIT-222
compared_against:
- SOTA-054
promote_when: >-
  A second operator publishes a failure rate measured the same way, or the
  record acquires a source for the classical optimal-interval result the two
  inputs imply. One fleet's constant is not yet an industry figure, and the
  recommendation currently rests on a self-published benchmark.
summary: >-
  CoreWeave (2025), [LIT-222](../literature.d/LIT-222.md). Expected work lost to a failure is half the
  inter-checkpoint interval, and mean time to failure falls linearly with GPU
  count — so the interval belongs to the job's size and the cluster's failure
  rate, not to the write cost alone.
---

# SOTA-189: Set the checkpoint interval from the job's measured time-to-failure, which shrinks as the job grows

## Source

CoreWeave (2025), [LIT-222](../literature.d/LIT-222.md) — a benchmark report that fits a
right-censored exponential survival model to real job durations and
interruptions.

## The two facts that decide the interval

**Expected loss is half the interval.** From the report: "assuming a failure
can occur randomly anywhere in the inter-checkpoint interval, the expected
badput for any job is half the inter-checkpoint interval." So doubling the
cadence halves the work at risk, and the benefit of checkpointing more often
is linear and knowable rather than a matter of taste.

**Failure rate scales with the job.** Synchronous data-parallel training is
all-or-nothing, so a job's mean time to failure is the per-GPU rate divided by
its GPU count. The measured per-GPU rate is 3,748.25 days per failure, giving
**3.66 days at 1,024 GPUs** — and, on the same model, under a day at 4,096 and
a few hours at 16,384.

That second fact is the recommendation. An interval that is right for a
256-GPU job is four times too long for the same work at 1,024 GPUs, and the
run will not tell you: it simply loses more each time, and the loss is charged
to "infrastructure flakiness" rather than to a setting nobody revisited.

## What this is an alternative to

[SOTA-054](SOTA-054.md) derives the interval from the *write cost*, adapting it to hold
checkpointing overhead inside a bound. That is the cost side. This is the risk
side, and the two are the halves of one trade — checkpoint often enough that
expected loss is small, rarely enough that the writing is not the job.

Neither source combines them. The classical answer given both is an interval
of about √(2 · checkpoint cost · MTTF); the record holds no source for that
result, which is worth stating rather than deriving here.

The practical reading, with both practices in hand: take the write cost from
profiling as [SOTA-054](SOTA-054.md) says, take MTTF from the fleet's own failure data as
this one says, and expect the answer to move when the job is resized — which
is the part neither the checkpointing literature nor most operators do.

## What to discount

A vendor's benchmark of its own platform, with baselines it selected. [DP-005](../../docs/design-principles.md#dp-5)
applies: the uplift figures are marketing and the ratios are not independent
evidence.

The method and the shape survive that. A censored survival fit is the right
way to estimate a failure rate from a fleet where most jobs do not fail, and
MTTF falling linearly in job size is structural. The constant is one fleet's
and should be re-measured, which is exactly what makes this a practice about
*measuring* rather than a practice about 3.66 days.
