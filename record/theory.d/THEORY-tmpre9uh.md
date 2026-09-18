---
status: Active
title: 'Dropout training minimizes the same objective as variational inference in a deep Gaussian process'
version: 1
tags:
- model-stability
date: '2026-09-18'
source:
- LIT-tmpffawr
explains: []
summary: >-
  Gal and Ghahramani (2015), [LIT-tmpffawr](../literature.d/LIT-tmpffawr.md) — the objective a dropout network
  already minimizes is, up to scaling, the variational objective for a
  particular approximating distribution in a deep Gaussian process. The
  derivation is the claim and it is `Active`; what the record declines is the
  step most citations take next, that sampling such a network at test time
  therefore yields trustworthy uncertainty. That is an empirical question about
  calibration, the approximating family is chosen rather than fitted, and the
  record holds none of the literature that argued about it.
---

# THEORY-tmpre9uh: Dropout training minimizes the same objective as variational inference in a deep Gaussian process

## Source

Gal and Ghahramani (2015), [LIT-tmpffawr](../literature.d/LIT-tmpffawr.md) —
[ARXIV-1506.02142](https://arxiv.org/abs/1506.02142), ICML 2016.

## What was actually shown

**An identification between two objectives.** Fix a deep Gaussian process and
an approximating distribution over its weights of a particular Bernoulli form.
The variational objective for that pair is, up to scaling, the objective a
network trained with dropout and L2 weight decay already minimizes. Nothing
about the training procedure changes; the claim is that the procedure was
always doing this.

**What that buys, which is the reason the result travelled.** A network
already trained with dropout is, on this reading, an approximate posterior —
so uncertainty can be extracted from it with no retraining, by leaving dropout
**on** at test time and sampling `T` forward passes. The paper's framing is
that this recovers "information from existing models that has been thrown away
so far", and the cost is `T` passes rather than one.

**What was measured.** Regression and classification over several
architectures and non-linearities with MNIST as the worked example, reporting
improved predictive log-likelihood and RMSE against the then-standard methods,
plus a deep reinforcement-learning application.

## The third account, and how it sits with the other two

The record now holds three explanations of dropout and this is the one that
answers a different question.
[THEORY-016](THEORY-016.md) says why one scaled forward pass substitutes for
an ensemble; [THEORY-015](THEORY-015.md) says what dropout does to the
objective; this says what the stochastic procedure *is*, probabilistically.

They are not rivals and they are also not independent evidence. All three
amount to saying that a dropout network stands in for a distribution over
networks — an ensemble in [THEORY-016](THEORY-016.md), an approximate
posterior here. What differs is what each licenses, and this is the only one
of the three that turns into a capability at inference rather than an account
of training.

## What this does not say

**It does not establish that the uncertainty is good uncertainty**, and that
is the step nearly every citation of this paper takes. Sharing an objective
with a variational method makes the network *an* approximate posterior; it
says nothing about how close the approximation is, and calibration is an
empirical property that has to be measured on the task at hand. The record
holds **none** of the literature that argued this out — which is a gap worth
knowing about before relying on MC dropout, not a reason to treat the question
as settled in either direction.

**The approximating family is chosen, not derived.** The identification holds
for a Bernoulli approximating distribution matched to the dropout mask. A
different family gives a different variational problem, and nothing here says
this one is the right one; it is the one that makes the objectives line up.

**It licenses no practice, deliberately.** `explains:` is empty. "Keep dropout
on at test time and average `T` samples" is a real recommendation and it is
not filed, because what would justify filing it is a calibration result, which
is exactly what this paper does not provide and what the record cannot
currently cite.

**And it says nothing about whether to train with dropout at all**, which is
[SOTA-240](../practices.d/SOTA-240.md)'s question. This is an account of a
network that already has it.
