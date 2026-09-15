---
status: Proposed
promote_when: >-
  A robust aggregator adopted in a production or open large-scale training
  stack, or a measurement of what it costs on a job where workers are trusted.
  What would not satisfy this: another aggregator with better statistical
  rates — the rates are not what is missing.
consensus: unreplicated
consensus_note: >-
  The negative result is not in doubt and is nearly structural. What has no
  adoption evidence is the positive half: nothing in this record trains at
  scale with a robust aggregator, and the overhead of doing so is unmeasured
  here.
title: 'Aggregate worker gradients coordinate-wise by median when any worker may be faulty'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
source:
# LIT-tmp5ev5l is primary: it gives the aggregator that needs no estimate of
# the corruption fraction, which is the one a deployer can actually use.
- LIT-tmp5ev5l
# The paper that establishes the negative -- the mean has no robustness at any
# cluster size -- and the reason to want an aggregator at all.
- LIT-tmpth13v
introduced_by:
- LIT-tmpth13v
implementations: []
summary: >-
  Averaging has a breakdown point of zero: one worker returning an arbitrary
  vector can move the mean anywhere, and adding workers does not help, because
  it is the worker's magnitude and not its share of the population that does
  the moving. The coordinate-wise median is the robust aggregator that needs
  no estimate of how many workers are faulty; the trimmed mean has better
  rates and needs one.
---

# SOTA-tmptssew: Aggregate worker gradients coordinate-wise by median when any worker may be faulty

## What to do

Where workers can return arbitrary vectors — hardware faults, silent data
corruption, a bad shard, a bug in one worker's path, or untrusted
participants — replace the mean in the aggregation step with the
**coordinate-wise median**. Where the fraction of faulty workers `alpha` is
known or can be bounded, the **coordinate-wise trimmed mean** with
`beta = c*alpha`, `c >= 1`, achieves better statistical rates.

Prefer the median when `alpha` is unknown. That is the usual case, and the
trimmed mean's advantage is contingent on a number the deployer does not have.

## Why

**The mean's breakdown point is zero, and cluster size does not help.**
[LIT-tmpth13v](../literature.d/LIT-tmpth13v.md)'s first result is the one that matters more than the algorithm it
proposes: a single Byzantine worker can drive the average to any value it
likes, regardless of `n`, because the average is unbounded in each
contribution. The intuition that a bad worker is diluted by many good ones is
wrong — dilution works on the *direction* of a bounded vector and not on an
unbounded one.

**The two aggregators differ in what they need to know, not just in rate.**
[LIT-tmp5ev5l](../literature.d/LIT-tmp5ev5l.md) gives order-optimal rates for the trimmed mean under
sub-exponential gradients, and near-optimal rates for the median under the
weaker assumption of bounded skewness — crucially, *without* knowing `alpha`.
An aggregator parameterized by a quantity you are trying to detect is not
deployable.

**Crash-only tolerance comes free.** A crashed or hung worker is a special
case of an arbitrary one, so guarantees that hold against adversarial workers
hold a fortiori against failures — which is the regime real clusters are in.

## What this does not settle

**Cost is unmeasured here.** A coordinate-wise median is not an all-reduce.
Neither paper reports what replacing all-reduce with a robust aggregator does
to step time on a large job, and that number is what decides whether this is
worth doing when workers are trusted.

**Convex and moderate-scale settings.** The rates are for the statistical
setting these papers analyze; nothing here demonstrates a robust aggregator on
a large transformer pretraining run.

**It interacts badly with compression.** [SOTA-tmp5wyoh](SOTA-tmp5wyoh.md) keeps a local residual
and assumes the aggregate is an average. What error feedback means under a
median is not addressed by any paper in this record.
