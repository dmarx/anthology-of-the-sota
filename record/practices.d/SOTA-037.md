---
number: 37
status: 'Active'
title: 'LM in-context learning emerges at scale'
version: 1
tags:
- model-architecture
date: '2026-08-24'
published: '2020-05-01'
source:
- LIT-035
extends:
- SOTA-036
summary: >-
  Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).
---

# SOTA-037: LM in-context learning emerges at scale

## Source

Brown et al. (2020), [LIT-035](../literature.d/LIT-035.md) — [ARXIV-2005.14165](https://arxiv.org/abs/2005.14165).

## The claim, and the word "emerges"

[LIT-035](../literature.d/LIT-035.md)'s headline finding is that a model trained only to predict the next
token becomes able to perform tasks it was never trained on, given a few
examples in its prompt — and that this ability is weak or absent at smaller
scales and substantial at 175B. Nothing in the objective asks for it.

That is what makes it a *finding about scale* rather than about architecture
or data. It is also the observation that made pretraining scale worth its
cost: a larger model was not just better at the objective, it acquired a
capability the objective does not name.

## What has been contested since

"Emerges" invites a reading — a sharp phase transition at some size — that
subsequent work disputes: several apparently emergent curves flatten into
smooth ones when the metric is continuous rather than thresholded, so the
discontinuity is partly a property of how the ability was measured.

The record has no source for that critique, which is worth flagging rather
than leaving the stronger reading unqualified. What is not in dispute is the
direction: in-context ability increases with scale, and the increase is steep
enough that small-model results do not predict it.

The practical consequence is a negative one, and it is the reason this belongs
in a registry of practice: **capability evaluations on a small proxy model do
not transfer.** A pipeline validated at 1B can be silently wrong about what
the 100B run will be able to do, and this is the finding that says so.
