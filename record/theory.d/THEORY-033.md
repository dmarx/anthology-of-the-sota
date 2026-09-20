---
number: 33
status: Proposed
formerly:
- THEORY-tmp6a2vb
promote_when: >-
  The `Kaon` control repeated at a scale where the record's Muon practices are
  evidenced — a billion parameters or more, on a real pretraining corpus. If
  an optimizer with random singular values still matches Muon there, the
  geometric account is finished and this one stands. What would not settle
  it: more NanoGPT runs, more members of the Schatten family, or another
  derivation showing some update is a steepest-descent step under some norm —
  the contested claim is that the geometry is what pays, and a fourth
  reformulation of the geometry does not test it.
title: 'What a spectral optimizer buys is a step size that stays optimal, not adherence to a target geometry'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-456
explains:
- SOTA-121
summary: >-
  Shumaylov et al. (2026), [LIT-456](../literature.d/LIT-456.md) — an optimizer with random
  singular values matches Muon, so the target spectrum is not what pays.
  What the controls leave standing is that the spectral update's optimal step
  size is constant where Euclidean descent's oscillates. NanoGPT scale.
---

<!-- inactive-ok-file: THEORY-024 ADR-031 ADR-034 THEORY-032 — THEORY-024 is Proposed and is what this account argues with; the ADRs are Proposed and are why arguing with it leaves its practices alone; THEORY-032 is Proposed and filed in this same contribution -->
# THEORY-033: What a spectral optimizer buys is a step size that stays optimal, not adherence to a target geometry

## Source

Shumaylov et al. (2026), [LIT-456](../literature.d/LIT-456.md) — read as [NOTE-208](../notes.d/NOTE-208.md).

## The account

Take the exact local Taylor expansion of the loss along an update direction.
Two quantities fall out with no appeal to any norm: how well the update
aligns with the stochastic gradient, and how much descent the direction
affords at second order. Every optimizer implicitly trades one against the
other, and the trade only pays at a step size tuned to exploit it.

Evaluate that trade under exact line search in a random-feature model and the
ranking everyone expects reverses: plain gradient descent extracts more loss
reduction per step than spectral descent. The catch is that its optimal step
size oscillates violently from step to step, so the schedule that would
realize the advantage cannot be run. Spectral descent's optimal step size is
essentially constant throughout training, because it is proportional to a
quantity — the inner product of the gradient with its own polar factor — that
barely moves.

So the claim is about realizability. Muon is not better because it points in
a geometrically privileged direction. It is better because its best learning
rate is a number you can find once and keep, and a schedule you can actually
implement beats an optimum you cannot.

## What was actually shown

Three controls, each of which could have come out the other way.

**`TruncatedSGD`** zeroes the largest singular values, testing the simple
story that spectral optimizers work by removing noisy directions. It improves
on SGD and does not reach Muon: the simple story is necessary and
insufficient.

**`Freon`** sweeps the Schatten family and keeps going past `p = 1`. If the
LMO account were right the optimum would sit at a value where a norm exists.
On GPT-2 it sits strictly in the quasi-norm regime, where no unitarily
invariant norm does — and Theorem 2.1 says an update there cannot be
steepest descent for any such norm.

**`Kaon`** is the one that settles it. Replace the singular values with noise
from a chaotic recurrence: no oracle, no norm, no coherent geometry at all.
It matches Muon, and retains a convergence rate (Theorem 2.5). An explanation
that cannot distinguish its object from a randomized control is not doing
explanatory work.

## What this does not say

**It does not say Muon is a bad optimizer, or that the record should stop
recommending it.** [SOTA-121](../practices.d/SOTA-121.md) and [SOTA-165](../practices.d/SOTA-165.md) are untouched: what
is contested is the account, not the technique, which is the separation
[ADR-031](../decisions.d/ADR-031.md) built this scheme for and [ADR-034](../decisions.d/ADR-034.md) restated. Read as
an argument against using Muon, this document would be a misreading of both
the paper and the scheme.

**It does not refute [THEORY-024](../theory.d/THEORY-024.md)'s derivation.** That orthogonalisation is
the duality map for the spectral norm, and that muP and Shampoo are partial
approximations of one map, are mathematical statements which no experiment
reaches. What this reaches is the sentence a reader takes away from them —
that being the duality map is *why* it works. `THEORY-024` moves to
`Proposed` on this evidence, not to `Rejected`.

**It is not established, and the scale is why.** NanoGPT and WikiText-2 at
118M tokens, three seeds, one architecture family. The practices this argues
about are evidenced from 90M to 1.6T parameters. A null result at small scale
against an effect demonstrated at large scale is a reason to look, not a
verdict — which is what `Proposed` says here and what `promote_when` asks for.

**And the positive half is weaker than the negative half.** The step-size
account is exact only in the random-feature model, which the authors show
fails as a quadratic approximation of a GPT-2 layer. Alignment and descent
potential cannot be computed during training; the framework diagnoses after
the fact. The destructive result is strong, the constructive one is a
hypothesis.

## Why this is filed separately from the rank account

[THEORY-032](../theory.d/THEORY-032.md) is also a non-geometric explanation of the same
practice, from an unrelated group, and it says something different: that the
advantage comes from the rank structure of the activations and gradients.
Neither paper cites the other. Whether they are two descriptions of one
mechanism is open, and collapsing them into one document would assert an
answer nobody has.
