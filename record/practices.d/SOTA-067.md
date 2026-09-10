---
number: 67
status: Rejected
status_note: >-
  The cited paper contains no discussion of training instability. The record's
  sourced monitoring practices are SOTA-069 and SOTA-099, which do not depend
  on a step count
title: 'Monitor loss specifically during first ~5000 steps for instabilities'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Rejected with the rest of the LIT-052 cluster.
tags:
- model-stability
date: '2026-08-24'
source:
- LIT-052
implementations:
- vision_transformer
- bert
summary: >-
  Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686). Rejected: the source contains no discussion of instability, and the 5000 belongs to nobody.
---

# SOTA-067: Monitor loss specifically during first ~5000 steps for instabilities

## Source

Tay et al. (2021), [LIT-052](../literature.d/LIT-052.md) — [ARXIV-2109.10686](https://arxiv.org/abs/2109.10686).

## Why this is rejected

The source contains the string "instabilit" zero times. The claim came from
[LIT-052](../literature.d/LIT-052.md)'s fifth replaced takeaway, "training instability primarily occurs in
first few thousand steps", and the practice then converted "a few thousand"
into **~5000** — a number with no owner at any point in the chain.

That is the sharpest thing here and the reason this one is worth reading past
its status. The record has a recurring failure of ownerless constants: a
threshold that arrives as a round number in a summary, gets a tilde and a
practice of its own, and is thereafter quotable. `SOTA-013`'s 2000 was traced
to a real source. This 5000 was traced to a rounding.

## What replaces it

Nothing needs to. The record's monitoring practices are already sourced and
already say more than this did: [SOTA-069](SOTA-069.md) watches `exp(loss)` and [SOTA-099](SOTA-099.md)
tracks gradient-norm statistics. Neither is scoped to a step window, which is
the better shape — instabilities cluster early, but a loss spike at step 400k
is not less worth catching, and a practice that names a window invites someone
to stop looking after it.
