---
status: Proposed
promote_when: >-
  A learning-curve study on more than one system, from a group other than
  MACE's authors, over at least two decades of training-set size with
  several seeds, that holds body order fixed while varying equivariance and
  the reverse, and reports fitted slopes with intervals. What would not
  settle it: another equivariant model with a steeper curve than a two-body
  invariant one, which is the confounded comparison this account
  re-explains.
title: 'The steeper learning curves of equivariant interatomic potentials come from the higher body order of their local features, not from equivariance as such'
version: 1
tags:
- physical-sciences
- graphs-and-networks
- model-architecture
date: '2026-10-22'
source:
- LIT-tmpj25em
- LIT-tmpm07pb
explains: []
summary: >-
  Batatia et al. (2022), [LIT-tmpj25em](../literature.d/LIT-tmpj25em.md) — NequIP ([LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md)) found that
  turning on l ≥ 1 features steepened the log-log learning curve and
  credited equivariance. MACE re-ran the aspirin experiment: invariant
  models with body order 2, 3 and 4 have slopes −0.33, −0.51 and −0.64, and
  at body order 4 adding equivariant features leaves the slope at −0.63 to
  −0.64 and only shifts the curve. Equivariance is one route to higher body
  order, and body order is what sets the slope.
---

# THEORY-tmpghjc1: The steeper learning curves of equivariant interatomic potentials come from the higher body order of their local features, not from equivariance as such

## Source

Batatia et al. (2022), [LIT-tmpj25em](../literature.d/LIT-tmpj25em.md). Read as [NOTE-tmpbbjt7](../notes.d/NOTE-tmpbbjt7.md). Batzner et al.
(2021), [LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md). Read as [NOTE-tmp6evsh](../notes.d/NOTE-tmp6evsh.md).

## The account

NequIP ([LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md)) observed that its equivariant networks (l = 1, 2, 3)
learn faster with data than the same network restricted to l = 0, on bulk
water from 10 to 1,000 structures and on aspirin from 150 to 950, and that
the l = 0 network keeps its shallow slope even when matched to l = 1 in
weights or in features. It concluded that "it is indeed the equivariant
nature of NequIP" that changes the learning behaviour.

The l = 0 network there is a two-body model: each message depends on one
neighbor's state and one distance. Turning on l = 1 does two things at once.
It makes the features equivariant, and it lets angular information between
pairs of neighbors survive into the next layer, which raises the effective
body order. NequIP's control matched size, not body order.

MACE ([LIT-tmpj25em](../literature.d/LIT-tmpj25em.md), Figure 2) separates the two on the same aspirin task,
rMD17 force MAE against training-set size, two-layer models:

- **Body order, invariant features only.** Correlation order ν = 1, 2, 3
  (two-, three- and four-body messages) gives slopes −0.33, −0.51, −0.64
- **Equivariance at high body order.** At ν = 3, symmetry order L = 0, 1, 2
  gives −0.64, −0.63, −0.64. The curves shift down; the slope does not move
- **Equivariance at low body order.** At ν = 1, L = 0, 1, 2 gives −0.33,
  −0.44, −0.45. Here equivariance does steepen the curve, which is the
  NequIP shape, since L = 1 messages carry angular information a two-body
  invariant message cannot

So equivariant features steepen the curve when they are the only route to
higher body order, and stop doing so once body order is supplied another
way. An invariant four-body model reaches the slope of the equivariant ones.

## What it explains

- Why NequIP's l = 0 → 1 step changed the slope and l = 1 → 3 only shifted
  it: the first step adds angular correlation, the later ones refine it
- Why NequIP's weight- and feature-matched l = 0 controls did not recover
  the slope: neither raises body order
- Partly, why invariant MACE (L = 0), a four-body model, sits among the
  two-body equivariant models on 3BPA at 1200 K (forces 81.6 against
  76.2–86.4 meV/Å, energy 37.1 against 38.5–42.6 meV) at a tenth of their
  latency (Table 2). At 300 K it is behind them (forces 14.6 against
  10.8–13.0), which this account does not explain

## Why `Proposed`

**One molecule, one group, a figure.** The slopes come from aspirin alone,
over roughly one decade of training size, with no error bars on the fitted
exponents. Without intervals, the −0.63 against −0.64 that carries the
central claim cannot be told apart from a real but small effect.

**The reverse control is partial.** Body order was raised with equivariance
held at L = 0, and equivariance raised at fixed ν. Nobody has raised body
order in a model of the NequIP family and checked that the slope moves the
same way there.

## What it does not say

**It does not say equivariance is useless.** At every body order, adding L
shifts the curve down, which at fixed data is lower error, and MACE's best
models use L = 2. The claim is about the exponent, not the error.

**It does not say anything at large data.** Both papers stop below about
1,000 configurations. Erwin ([LIT-763](../literature.d/LIT-763.md)) found equivariant graph models,
NequIP among them, leading at small training sets and overtaken as data
grew, on a different task; this account neither predicts nor contradicts
that.
