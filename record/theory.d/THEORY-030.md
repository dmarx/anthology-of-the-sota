---
number: 30
status: Proposed
formerly:
- THEORY-tmpmurnt
promote_when: >-
  The same analysis carried to stochastic gradients — a central flow for
  minibatch training whose predictions hold — which is the one step between
  this and every recipe the record holds. Or an optimizer designed with the
  implicit preconditioner made explicit, which is the direct test of the
  second limb. What would not settle it: more evidence that the edge of
  stability exists, which is established and is the premise rather than the
  claim.
title: 'Adaptive optimizers work by shaping the curvature they adapt to, and oscillation is how a first-order method sees curvature at all'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-453
explains:
- SOTA-001
summary: >-
  Cohen et al. (2024), [LIT-453](../literature.d/LIT-453.md) — at the edge of stability the
  effective step size is set by current sharpness, and the learning rate's
  role is to modulate an implicit curvature penalty that steers the
  trajectory toward flatter regions where larger steps are stable. Ablating
  the shaping while keeping the adaptation makes the optimizer slower.
  Separately, oscillation is how a first-order method acquires second-order
  information at no extra cost.
---

# THEORY-030: Adaptive optimizers work by shaping the curvature they adapt to, and oscillation is how a first-order method sees curvature at all

## Source

Cohen et al. (2024), [LIT-453](../literature.d/LIT-453.md) — [ARXIV-2410.24206](https://arxiv.org/abs/2410.24206).

## What was actually shown

The apparatus is a **central flow**: a differential equation modelling the
time-averaged trajectory of an optimizer that is oscillating at the edge of
stability. It earns its use empirically — integrating the flow predicts the
real long-run trajectory of generic networks to high numerical accuracy,
which is a stronger result than a qualitative account of the same regime.

Reading terms off the flow gives three findings.

**The learning rate does not set the step size.** At the edge of stability
the oscillations drive the effective step to the largest stable value at the
current weights — a quantity determined by current *sharpness*. The
hyperparameters do not appear in that expression. What the learning rate does
instead is modulate the strength of an implicit sharpness penalty,
monotonically.

**The penalty is load-bearing, and the evidence is an ablation.** Remove the
curvature regularization from the flow while keeping the identical step-size
adaptation, integrate, and the optimizer navigates into *sharper* regions,
takes smaller steps, and optimises slower. So adapting to curvature is not
what the advantage is; shaping it is. The authors name the mechanism
**acceleration via regularization** and the measured signature is that higher
learning rates optimise slower early and faster late.

**Oscillation is a free second-order channel.** A first-order method that
oscillates picks up second-order information at no additional gradient
queries, which gives RMSProp an implicit preconditioner. That is offered as a
partial answer to a standing puzzle — why no explicitly second-order
optimizer has consistently beaten the first-order adaptive ones.

Any of it could have come out otherwise. The flow could have failed to
predict the trajectories; the ablated flow could have matched the full one.

## What this makes sense of

**Why [SOTA-001](../practices.d/SOTA-001.md) is right.** The record recommends Adam as the default and
records, honestly, that this is what papers depart from rather than argue
for. The registry has never held an account of what adaptivity buys. This is
one: not a better-scaled step, but an implicit preconditioner acquired by
oscillating, plus an implicit curvature penalty that makes the landscape more
tractable as training proceeds.

**Why higher learning rates behave the way people report.** Slower at first,
faster over a run, is the direct prediction of the mechanism rather than an
anomaly to be tuned around.

## What this does not say

**It does not cover stochastic training, and that is the whole gap.** Every
result here is full-batch. Every recipe in this record uses minibatches.
Nothing in the paper bridges it, and the bridge is what `promote_when:` asks
for. This is the reason the account is `Proposed` while its measurements are
strong.

**It does not make the record's learning-rate practices wrong, and it does
not make them right either.** [SOTA-009](../practices.d/SOTA-009.md)'s warmup-then-anneal and the
warmup-stable-decay line describe the learning rate as setting how far the
optimizer moves. At the edge of stability, in full batch, it does not. The
practices stand on their own evidence; what changes is that their prose
explanation was never checked, and this is the first thing in the record that
could check it.

**It does not license reading a learning rate as a curvature penalty in a
real run.** That translation needs the stochastic case.

**The time-averaging is heuristic.** The authors say so and name making it
rigorous as future work. The justification is that the flows predict; the
conditions under which they must are unknown.

**It does not reach the architecture.** The authors flag this as the
framework's limitation: predictions live at the level of the loss landscape,
and the theory says the learning rate modulates a sharpness penalty without
saying how that penalty affects learning or which layers are implicated.

**Sharpness is expensive.** The quantity everything turns on is not something
a practitioner monitors, so this is a tool for reasoning rather than for
instrumentation.

## Against the record's other account of the same puzzle

[THEORY-024](THEORY-024.md) says orthogonalising the update is dualising it, and that muP
and Shampoo are partial approximations of one duality map. That is an account
of why second-order-flavoured methods work when they do. This is an account
of why first-order ones already are second-order, quietly.

They are addressing the same puzzle from opposite sides and neither cites the
other. Whether they are two descriptions of one mechanism or two mechanisms
is not something either paper asks, and it is the most interesting question
the record can pose from holding both.

## Why `Proposed`

The measurements are strong — a predictive flow and a clean ablation — and
the scope is narrow in exactly the way that matters. A theory about
optimization that holds only without stochastic gradients explains a setting
this record does not train in. `Proposed` is the honest status for an account
whose evidence is good and whose relevance is unestablished.
