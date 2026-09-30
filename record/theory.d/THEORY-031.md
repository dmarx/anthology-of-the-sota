---
number: 31
status: Active
formerly:
- THEORY-tmpq5g15
title: 'The aggregate loss curve is a lossy projection of training, in at least three measured ways'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-20'
source:
- LIT-455
- LIT-453
- LIT-454
explains:
- SOTA-270
summary: >-
  Three independent measurements of what the loss curve discards. It
  time-averages oscillation the optimizer is actually doing
  ([LIT-453](../literature.d/LIT-453.md)); it sums over transitions that are individually abrupt
  and differently timed, so smoothness is what many breakthroughs look like
  added up ([LIT-455](../literature.d/LIT-455.md)); and it reads flat while the weights keep
  travelling ([LIT-454](../literature.d/LIT-454.md)).
---

# THEORY-031: The aggregate loss curve is a lossy projection of training, in at least three measured ways
<!-- inactive-ok-file: THEORY-030 — Proposed, and filed in this same contribution; named to contrast its narrower scope with this account's -->

## Source

Kangaslahti et al. (2025), [LIT-455](../literature.d/LIT-455.md) — [ARXIV-2506.15872](https://arxiv.org/abs/2506.15872).

Cohen et al. (2024), [LIT-453](../literature.d/LIT-453.md) — [ARXIV-2410.24206](https://arxiv.org/abs/2410.24206).

Kunin et al. (2021), [LIT-454](../literature.d/LIT-454.md) — [ARXIV-2107.09133](https://arxiv.org/abs/2107.09133).

**No one of these states the claim; the record does, from holding all three.**
That is the kind of synthesis [DP-007](../principles.d/DP-007.md) says has no author and therefore no
arrival event — filed here so it has one.

## What was actually shown

A loss curve is one number per step. Three collapses go into producing it,
and each has been measured independently.

**It averages over time.** At the edge of stability the optimizer oscillates;
the path that gets plotted is the time-average of a path that is not smooth.
This is not a rendering artifact — the oscillations do real work, implicitly
triggering the curvature reduction that lets later steps be larger, and the
time-average is a different curve from the one gradient flow would take.

**It averages over data and over directions.** Conceptual transitions are
frequent, individually abrupt, and differently timed; their sum is smooth.
The negative control is what makes this more than a story: on synthetic
arithmetic, clustering exact per-example loss curves recovers digit position
and *not* the carrying skill, at chance; decomposing the loss per example and
along a curvature-derived basis recovers both. **Smoothness is what many
breakthroughs look like when added up.**

**It saturates before the weights do.** Long after the curve flattens,
networks keep travelling, distance growing as a power law in updates with a
non-trivial exponent. What drives that motion is not the plotted loss but a
modified objective with a velocity term, and the motion is incoherent
oscillation in the Hessian's top eigensubspace rather than a random walk.

## What follows

**A flat stretch and a smooth descent are the same kind of non-evidence.**
Neither licenses the conclusion that nothing structural is happening, and the
record has a worked instance: [THEORY-028](THEORY-028.md) shows one plateau to be an attention
recall circuit under construction, demonstrated by patching the circuit in
and watching the plateau disappear. That was one transition made visible by
an intervention. The first collapse above says the population is large.

[SOTA-270](../practices.d/SOTA-270.md) is the practice: do not read the curve as evidence about
the training, and decompose it when the answer matters.

## What this does not say

**It does not say the loss curve is useless.** It is the right instrument for
the thing it measures — whether the number is going down. The claim is about
what it cannot be used to conclude, and the failure is specifically inference
from *smoothness* to *uniformity*.

**The three legs have different scopes and do not compose into one
mechanism.** The first is full-batch and at the edge of stability. The second
is a 9M-parameter model chosen for measurement feasibility. The third is the
limiting regime after convergence, from 2021, at small scale. They agree on
the conclusion and they are not three views of one experiment.

**It does not say how often**, and that is the weakest part. "Breakthroughs
occur frequently" is the headline of the second paper and its least
quantified claim: how many, at what scale, in a real pretraining run, is
exactly what the method's cost prevents measuring.

**It does not supply an affordable instrument.** POLCA needs checkpoints,
Hessian-vector products at each and per-example forward passes at every
interval; sharpness is expensive; diffusion exponents need long tails. The
caution is free and the measurement is not, which is why the practice drawn
from this is mostly about what not to conclude.

**It does not license reading a smooth curve as *hiding* anything in
particular.** Absence of visible structure is not evidence of hidden
structure either. What the account establishes is that the curve cannot
settle the question, in both directions.

## Why `Active`

Three independent measurements, from three groups across four years, in three
different regimes, none citing the others, agreeing that the aggregate
discards structure that matters. Each leg has its own evidence — a predictive
flow with an ablation, a negative control against a chance baseline, a fitted
exponent with closed-form hyperparameter predictions.

What is `Proposed` elsewhere in this contribution is the *mechanism* of any
one leg ([THEORY-030](THEORY-030.md), whose scope is full-batch). The claim here is
weaker and better supported: not why the curve is lossy in each case, but
that it is, in ways that have been separately measured.
