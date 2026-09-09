---
number: 104
status: 'Active'
title: 'Monitor domain coverage during training'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2023-12-01'
source:
- LIT-117
summary: >-
  Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).
---

# SOTA-104: Monitor domain coverage during training

## Source

Albalak et al. (2023), [LIT-117](../literature.d/LIT-117.md) — [ARXIV-2312.02406](https://arxiv.org/abs/2312.02406).

## Not a recommendation, and not this paper's

"Monitor domain coverage during training" states no threshold and no
response, which is the same gap as the retired [SOTA-073](SOTA-073.md) and [SOTA-074](SOTA-074.md): nothing
a reader can do differently on reading it.

It is also in tension with its own source. Under ODM the sampling distribution
is *supposed* to move away from uniform coverage — that is what the bandit is
for. A domain being under-sampled is the method working, not a condition to
detect, so "coverage" is not even the right quantity to watch.

## What the real concern would be

There is one, and it is worth stating because it is the reason somebody wrote
this bullet: a bandit can collapse onto a few arms and starve a domain
entirely, and a domain seen almost never is a capability the model will not
have. That is a genuine failure mode of the method, and the guard is the
exploration floor in the bandit's policy rather than a dashboard.

So the useful practice is "set an exploration floor so no domain is starved",
which is a claim about the algorithm's configuration. As written, this asks
someone to watch a number that the method is deliberately moving.

Flagged for restatement or retirement, alongside [SOTA-102](SOTA-102.md) and [SOTA-103](SOTA-103.md). Three
of this cluster's four need it, which — as with [LIT-051](../literature.d/LIT-051.md) — makes it a
cluster-level problem rather than three separate ones.
