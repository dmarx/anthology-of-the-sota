---
number: 11
status: 'Active'
title: 'visualizing eigenvalues of hessian (ratio of largest to smallest) over training can be useful diagnostics'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2017-12-01'
source:
- LIT-014
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).
---

# SOTA-011: visualizing eigenvalues of hessian (ratio of largest to smallest) over training can be useful diagnostics

## Source

Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).

## What the ratio says

The Hessian's largest eigenvalue is the curvature along the sharpest
direction, and the ratio to the smallest is the condition number of the local
quadratic approximation. A large ratio means the surface is a narrow valley:
gradient descent oscillates across the steep direction while creeping along
the shallow one, and the largest stable learning rate is set by the sharpest
direction rather than by the one that needs progress.

That connects two things the record holds separately. It is the geometry
behind why adaptive methods help ([SOTA-001](SOTA-001.md) — per-parameter scaling is an
approximation to preconditioning) and behind why the largest usable learning
rate moves when normalisation is added ([SOTA-020](SOTA-020.md)).

## The cost is why this is a diagnostic and not a monitor

The full Hessian is intractable at any interesting size. What is computed in
practice is a few extreme eigenvalues by Lanczos or power iteration on
Hessian-vector products, each of which costs roughly a forward-backward pass —
so a useful estimate is tens of extra passes, periodically, not per step.

Hence "over training" in the title should be read as *at intervals*, and the
practice is a study one runs deliberately rather than a signal on a dashboard.
<!-- inactive-ok: SOTA-021 — Rejected, and named as the contrast that explains why this practice survived and that one did not -->
That is the distinction [SOTA-021](SOTA-021.md) failed to make and was retired for; this one
survives because the quantity is at least computable and the paper actually
uses it.
