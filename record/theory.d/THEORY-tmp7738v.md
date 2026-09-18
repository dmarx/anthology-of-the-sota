---
status: Rejected
status_note: >-
  correct where it was validated, which was the convex case; for neural
  networks the three largest terms of the discrepancy turn out not to be
  approximation error at all
title: 'An influence-function estimate predicts the effect of removing a training point and retraining'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-17'
source:
- LIT-tmpz6v6v
explains: []
corrected_by:
- THEORY-tmpz2g03
summary: >-
  Koh and Liang (2017), [LIT-tmpz6v6v](../literature.d/LIT-tmpz6v6v.md) — the account the method was derived
  from and named for: the estimate approximates leave-one-out retraining, so
  a large influence means the model would have been meaningfully different
  without that point. True for convex models, where it was checked. Corrected
  for neural networks in 2022; the method was not.
---

# THEORY-tmp7738v: An influence-function estimate predicts the effect of removing a training point and retraining

## Source

Koh and Liang (2017), [LIT-tmpz6v6v](../literature.d/LIT-tmpz6v6v.md). This is not an aside in that paper — the
counterfactual is how the quantity is *defined*, and matching it against
retraining is the experiment that validates the method.

## The account, as it was stated

Removing a training point and refitting gives a new minimizer. That is the
quantity of interest and it is unaffordable, so approximate it: upweight the
point by `ε` instead of deleting it, differentiate the minimizer with respect
to `ε` via the implicit function theorem, and evaluate at the removal
direction. What comes out is a gradient alignment warped by the inverse
Hessian, and it is an approximation *to retraining*.

The paper checks this. On 10-class MNIST, for the 500 most influential
training points, the predicted change in test loss tracks the change actually
measured by removing the point and refitting.

It is a good explanation, and the validation is the right one to have run. It
makes the method mean something — a large influence is a claim about a
counterfactual world — and that meaning is why the four use cases sounded
like use cases rather than like coincidences.

## Where it holds, and where it stopped

The derivation assumes a twice-differentiable, strictly convex empirical risk
minimized exactly. MNIST logistic regression satisfies this. A trained neural
network satisfies none of it: the objective is non-convex, training stops
before any minimum, and it stops *warm* — at parameters reached from a
particular trajectory rather than at the global optimum of anything.

The paper knew the assumptions were violated and argued, reasonably, that a
damped quadratic approximation around the obtained parameters would still be
informative. The part that was not anticipated is that the residual would not
behave like error. [LIT-tmpyirk2](../literature.d/LIT-tmpyirk2.md) decomposes the discrepancy into five terms and
finds the three largest are **structural differences in what is being asked**,
not failures to ask it accurately — see [THEORY-tmpz2g03](THEORY-tmpz2g03.md).

## The reading it invites and does not support

That a large influence score means *this example made the model what it is,
and without it the model would be different.* On a neural network that reading
is unsupported, and it is the one every intuitive presentation of the method
produces, including this one's.

<!-- inactive-ok-block: SOTA-tmp8ornu — Proposed, named as the practice that outlives this
     explanation. The pointer is the section's whole argument and holds at any status. -->
There is a second reading that is safe and is easy to lose along with the
first: **the ranking is still informative.** The practice built on this
account — finding mislabelled data by self-influence, [SOTA-tmp8ornu](../practices.d/SOTA-tmp8ornu.md) —
survives, because what it needs is an ordering over training points and not a
counterfactual about any of them. Rejecting an explanation is not rejecting
what it explained, which is the whole reason this record keeps the two apart.
