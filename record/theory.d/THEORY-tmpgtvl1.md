---
status: Proposed
promote_when: >-
  The residual barrier after alignment shown to be measurement noise rather
  than real disagreement, or the account demonstrated on a transformer. What
  would not satisfy this: a third algorithm for finding the permutation — the
  claim that is provisional is "most", not that alignment helps.
title: 'Most of the loss barrier between two independently trained networks is permutation, not disagreement'
version: 1
tags:
- model-stability
date: '2026-09-15'
source:
# LIT-tmp2m8yx states it; LIT-tmprg45v supplies the algorithms that make it
# checkable and closes the barrier on real networks.
- LIT-tmp2m8yx
- LIT-tmprg45v
explains:
- SOTA-tmpjxbss
summary: >-
  Two networks trained from different seeds land far apart in weight space and
  close together in function space, and the linear path between them crosses a
  loss barrier. The account is that the barrier is mostly an artefact of unit
  labelling: permute the hidden units of one to match the other and the
  barrier largely disappears. What looked like two different solutions was one
  solution written in two orders.
---

# THEORY-tmpgtvl1: Most of the loss barrier between two independently trained networks is permutation, not disagreement

## The claim

A network's hidden units can be relabelled without changing the function it
computes, so every solution is really an orbit of `N!` per layer. Two runs
from different seeds pick different points on the same orbit. Interpolating
between them linearly therefore walks through a region that is not on either
solution's orbit and is not a solution at all — and the loss barrier along
that path measures the mismatch in labelling rather than any disagreement
about the function.

Account for the permutation and the barrier is small. [LIT-tmp2m8yx](../literature.d/LIT-tmp2m8yx.md) conjectures
this; [LIT-tmprg45v](../literature.d/LIT-tmprg45v.md) gives three algorithms for finding the permutation and
demonstrates the barrier closing on real architectures, with activation
matching on one to four samples nearly as good as solving the weight-matching
assignment problem.

## What rests on it

<!-- inactive-ok: SOTA-tmpjxbss — Proposed, and the practice this account exists to explain -->
[SOTA-tmpjxbss](../practices.d/SOTA-tmpjxbss.md), directly: align before averaging. The wider consequence is
about the decentralized literature in this record. FedAvg, local SGD, DiLoCo
and every gossip scheme here average weights or deltas across workers, and all
of them work — because the workers share an initialization and do not drift
far enough to permute relative to each other. This theory says what that
safety is made of, and therefore where it should be expected to fail: long
local phases, heterogeneous shards, workers restarted from different
checkpoints. Several papers in this batch measure an averaging penalty in
exactly those settings without naming this as a candidate cause.

It is also the finite-width shadow of [THEORY-tmp9dr37](THEORY-tmp9dr37.md). In the mean-field
limit the permutation symmetry is quotiented away by construction — the object
is a distribution over units, which has no unit order — and the landscape is
convex. At finite width the symmetry is still there and shows up as the
barrier this explains.

## Why it is `Proposed` rather than `Active`

Two groups, and the second supplies what the first lacked, which is the
evidence pattern that would ordinarily promote. What holds it back is that the
claim as stated is stronger than what has been shown: "most of the barrier" is
demonstrated on vision architectures at moderate scale, and the residual
barrier after alignment is not zero. Whether what remains is measurement noise
or a real disagreement that permutation cannot explain is the question this
would need answered.

## What it does not cover

**Transformers.** Attention heads carry more structure than a hidden unit and
share more of it; whether the symmetry group is the one these algorithms
search over is untested here.

**Networks that did not train on the same data.** Both papers permute between
runs of the same task. Workers holding different shards, which is the case the
decentralized literature cares about, are not what was measured.

**It says nothing about why alignment should help *during* training.** The
demonstrations are between two finished networks. Applying it inside an
averaging loop is the practice's promotion condition and is not evidence this
theory currently has.
