---
number: 10
status: Proposed
formerly:
- THEORY-tmpgtvl1
promote_when: >-
  The residual barrier after alignment at standard (1×) width and on
  ImageNet shown to be permutation that a stronger search can remove, rather
  than a difference no permutation accounts for; or the account demonstrated
  on a transformer. The candidate that it is measurement noise is gone: LIT-333
  measures that barrier falling to zero as width grows and staying put at 1×,
  which is a real effect and not a noise floor. A third algorithm that only
  repeats the wide-network result would not satisfy this — the claim that is
  provisional is "most", not that alignment helps.
title: 'Most of the loss barrier between two independently trained networks is permutation, not disagreement'
version: 2
history:
- version: 2
  date: '2026-10-03'
  note: >-
    Corrected after LIT-251 and LIT-333 were re-read against their texts.
    Activation matching is not a one-to-four-sample method "nearly as good"
    as weight matching. It uses activations over the training data (LIT-333
    §3.1), and weight matching is the fast, data-free method: the two
    "perform similarly, although weight matching is orders of magnitude
    faster and does not rely on the input data distribution" (Figure 2). The
    barrier closing is now stated with its width condition. It is zero on
    MNIST and on wide ResNet20 on CIFAR-10, and 1× models "did not seem to
    exhibit linear mode connectivity" (§5.3, Figure 4). On ImageNet a barrier
    remains after a 67% reduction (§5.1). "Not what was measured" was wrong
    for networks trained on different data: LIT-333 §5.4 merges two ResNet20s
    trained on disjoint, biased CIFAR-100 subsets. The residual-barrier
    sentence and promote_when are reworded to match. The width dependence
    rules out measurement noise as the explanation of the residual, so
    promote_when no longer offers it. The status is unchanged.
tags:
- model-stability
date: '2026-09-15'
source:
# LIT-251 conjectures it; LIT-333 supplies the algorithms that make it
# checkable and closes the barrier on real networks when they are wide enough.
- LIT-251
- LIT-333
explains:
- SOTA-217
summary: >-
  Two networks trained from different seeds land far apart in weight space and
  close together in function space, and the linear path between them crosses a
  loss barrier. The account is that the barrier is mostly an artefact of unit
  labelling: permute the hidden units of one to match the other and the
  barrier largely disappears — entirely, for wide enough networks, but not at
  standard width or on ImageNet. What looked like two different solutions was
  one solution written in two orders.
---

# THEORY-010: Most of the loss barrier between two independently trained networks is permutation, not disagreement

## The claim

A network's hidden units can be relabelled without changing the function it
computes, so every solution is really an orbit of `N!` per layer. Two runs
from different seeds pick different points on the same orbit. Interpolating
between them linearly therefore walks through a region that is not on either
solution's orbit and is not a solution at all — and the loss barrier along
that path measures the mismatch in labelling rather than any disagreement
about the function.

Account for the permutation and the barrier is small. [LIT-251](../literature.d/LIT-251.md) conjectures
this. Its evidence is indirect: barriers between independently trained
networks look like barriers between random permutations of one network. Its
own permutation search did not reduce the barrier for VGG or ResNet.
[LIT-333](../literature.d/LIT-333.md) gives three algorithms for finding the permutation and
demonstrates the barrier closing on real architectures. Weight matching uses
no data and runs in seconds to minutes. Activation matching, on activations
over the training data, performs about as well and is orders of magnitude
slower (Figure 2). The closing depends on width. The barrier is zero on
MNIST and for wide ResNet20 on CIFAR-10. There is no LMC at 1× width (§5.3),
and a barrier remains on ImageNet ResNet50 after a 67% reduction (§5.1).

## What rests on it

<!-- inactive-ok: SOTA-217 — Proposed, and the practice this account exists to explain -->
[SOTA-217](../practices.d/SOTA-217.md), directly: align before averaging. The wider consequence is
about the decentralized literature in this record. FedAvg, local SGD, DiLoCo
and every gossip scheme here average weights or deltas across workers, and all
of them work — because the workers share an initialization and do not drift
far enough to permute relative to each other. This theory says what that
safety is made of, and therefore where it should be expected to fail: long
local phases, heterogeneous shards, workers restarted from different
checkpoints. Several papers in this batch measure an averaging penalty in
exactly those settings without naming this as a candidate cause.

It is also the finite-width shadow of [THEORY-009](THEORY-009.md). In the mean-field
limit the permutation symmetry is quotiented away by construction — the object
is a distribution over units, which has no unit order — and the landscape is
convex. At finite width the symmetry is still there and shows up as the
barrier this explains.

## Why it is `Proposed` rather than `Active`

Two groups, and the second supplies what the first lacked, which is the
evidence pattern that would ordinarily promote. What holds it back is that the
claim as stated is stronger than what has been shown. "Most of the barrier" is
demonstrated on vision architectures at moderate scale. The barrier after
alignment is zero on MNIST and for wide ResNet20, but not zero at standard
(1×) width or on ImageNet ([LIT-333](../literature.d/LIT-333.md) §5.1, §5.3).

The width dependence rules out measurement noise as the explanation of what
remains. The barrier falls to zero as width grows and stays put at 1×, which
is a real effect. [LIT-333](../literature.d/LIT-333.md) itself names the two live readings: "either our
permutation selection methods are failing to find satisfactory permutations
on thinner models or that some form of invariance other than permutation
symmetries must be at play" (§5.3). The first keeps this account whole. The
second means permutation is not "most" of the barrier for the networks people
actually train at standard width. Telling them apart is the question this
would need answered, and `promote_when` now asks it in those terms.

## What it does not cover

**Transformers.** Attention heads carry more structure than a hidden unit and
share more of it; whether the symmetry group is the one these algorithms
search over is untested here.

**Networks that did not train on the same data — measured once, at small
scale.** [LIT-251](../literature.d/LIT-251.md) permutes only between runs on the same data.
[LIT-333](../literature.d/LIT-333.md) §5.4 does merge two ResNet20s trained on disjoint, biased CIFAR-100
subsets: 20% of labels 0–49 and 80% of labels 50–99, and the reverse. The
merged model has lower test loss than either input but is "not competitive
in terms of top-1 accuracy". It falls short of an ensemble and of full-data
training. Its MergeMany calibration result uses 32 MNIST MLPs, each on a
random 50% of the data (A.10). So the heterogeneous-shard case the
decentralized literature cares about has been measured, but only in one
two-model experiment, where alignment beats naive averaging and does not
recover what the data split cost.

**It says nothing about why alignment should help *during* training.** The
demonstrations are between two finished networks. Applying it inside an
averaging loop is the practice's promotion condition and is not evidence this
theory currently has.
