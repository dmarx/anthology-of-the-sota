---
number: 104
status: Rejected
status_note: >-
  Names no signal and no response, and is in tension with its own source:
  under ODM the sampling distribution is supposed to move away from
  uniform coverage. The string "domain coverage" does not appear in the
  paper
title: 'Monitor domain coverage during training'
version: 2
history:
- version: 2
  date: '2026-09-09'
  # inactive-ok-block: SOTA-073, SOTA-074 — Rejected earlier, named as the same
  # no-signal-no-action shape
  note: >-
    Rejected on reading the source (#114). The body had already placed it
    with SOTA-073 and SOTA-074 as a practice naming no threshold and no
    response; the paper contains "domain coverage" zero times, which
    settles the attribution as well.
tags:
- data-pipeline
date: '2026-08-24'
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
<!-- inactive-ok-block: SOTA-073, SOTA-074 — Rejected, named as the same no-signal-no-action gap -->
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

<!-- inactive-ok-block: SOTA-102, SOTA-101 — Superseded and Rejected in this same change; the paragraph is the cluster's disposition -->
The cluster is resolved as of [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114). [SOTA-103](SOTA-103.md) survives, restated as what ODM
actually does; [SOTA-102](SOTA-102.md) is superseded into it; [SOTA-101](SOTA-101.md) and this one are
retired. Four practices, one method, and none of the four described it.
