---
number: 11
status: 'Active'
title: 'Map the Hessian ratio |lambda_min / lambda_max| to find where the loss surface is non-convex'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Two corrections from reading the source (#114). The paper's quantity is
    |lambda_min / lambda_max| — smallest over largest — and the title had it
    the other way up, which reads as a condition number rather than a
    non-convexity measure. And the method that makes it affordable, an
    implicitly restarted Lanczos over Hessian-vector products, is now in the
    body. The recommendation is unchanged.
tags:
- training-optimization
date: '2026-08-24'
published: '2017-12-01'
source:
- LIT-014
compared_against:
- SOTA-010
- SOTA-012
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).
---

# SOTA-011: Map the Hessian ratio |lambda_min / lambda_max| to find where the loss surface is non-convex

## Source

Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).

## What the source actually computes

Figure 7 of [LIT-014](../literature.d/LIT-014.md) maps **`|λ_min/λ_max|`** — smallest over largest — at
each point of a filter-normalized loss surface. The quantity is interesting
because `λ_min` is *negative*: the ratio measures how much **negative
curvature** there is relative to positive, so it is a non-convexity measure,
not a conditioning one. Blue means near-convex; yellow means significant
negative curvature. For ResNet-56 the negative eigenvalues stay under **1% of
the positive curvatures** across a large region — which is the quantitative
form of "skip connections keep the landscape nearly convex" ([SOTA-010](SOTA-010.md)).

The plot only means anything under filter normalization, because a network can
be rescaled without changing its function and unnormalised curvature moves
with the rescaling. That condition travels with this practice.

## The condition number is a different diagnostic, and is not from here

This practice's body used to describe the ratio the other way up — `λ_max`
over `λ_min`, the condition number of the local quadratic approximation — and
reason from it: a large ratio means a narrow valley, gradient descent
oscillates across the steep direction, the largest stable learning rate is set
by the sharpest direction. That is all true, and it connects to why adaptive
methods help ([SOTA-001](SOTA-001.md)) and why the usable learning rate moves when
normalisation is added ([SOTA-020](SOTA-020.md)).

It is also not what [LIT-014](../literature.d/LIT-014.md) computes, and the two answer different
questions: the condition number asks *how hard is this to optimise*, while
`|λ_min/λ_max|` asks *is this even locally convex*. Stated the wrong way up
the practice reads as the first while citing the paper that did the second.

The conditioning material is kept because it is worth knowing and is signposted
as unsourced, which is the honest treatment. If the record wants it as a
recommendation it needs a paper that makes it.

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
