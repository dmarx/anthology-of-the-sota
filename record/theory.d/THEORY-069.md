---
number: 69
status: Active
formerly:
- THEORY-tmpdlyut
title: 'Grokking is a regime rather than a property of algorithmic data, and at least three knobs move it'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- model-stability
date: '2026-09-22'
source:
- LIT-538
- LIT-540
- LIT-537
- LIT-085
explains:
- SOTA-200
summary: >-
  Delayed generalization is not a fact about modular arithmetic. It is produced
  and removed by moving the training regime, and three knobs have been shown to
  move it: **training-set size** (Power et al., [LIT-538](../literature.d/LIT-538.md), and the ~60%
  threshold in [LIT-085](../literature.d/LIT-085.md)), **initialization scale relative to the generalizing
  weight norm** (Liu et al., [LIT-540](../literature.d/LIT-540.md), which uses it to induce grokking on
  MNIST, IMDb and QM9 and to eliminate it on algorithmic data), and **the
  alignment between the initial neural tangent kernel and the target** (Kumar
  et al., [LIT-537](../literature.d/LIT-537.md)). The three mechanistic accounts in this record
  contradict each other; they agree on this.
---

# THEORY-069: Grokking is a regime rather than a property of algorithmic data, and at least three knobs move it

<!-- inactive-ok-file: THEORY-071 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-070 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-072 — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->


## The account

Grokking — training accuracy saturating long before validation accuracy leaves
chance — is a *regime* a training run can be put into and taken out of. It is
not a property of algorithmic datasets, and it is not a fundamental feature of
overparameterized learning. Three separate knobs have been shown to control it,
each demonstrated in both directions.

**Training-set size.** [LIT-538](../literature.d/LIT-538.md) measures it in the paper that named the
phenomenon: converged accuracy is flat across a range of training fractions
while the *time* to reach it explodes as the fraction falls — in the vicinity
of 25–30% on `S₅`, removing 1% of the data raises median steps-to-generalize by
40–50%, while steps-to-fit stay at `10³`–`10⁴`. [LIT-085](../literature.d/LIT-085.md) puts a threshold on
it: above roughly 60% data on modular addition, grokking is gone and
generalization is immediate.

**Initialization scale relative to the generalizing weight norm.**
[LIT-540](../literature.d/LIT-540.md) induces grokking on **MNIST** (depth-3 MLP, 1k examples, Kaiming
weights scaled by `α > 1`), on **IMDb** with an LSTM at `α = 6`, and on **QM9**
with a GCNN at `α = 3`. At the standard initialization there is no grokking on
any of them. Run the other way, constraining the model to a small-weight-norm
sphere nearly eliminates grokking on algorithmic data.

**Initial kernel–task alignment.** [LIT-537](../literature.d/LIT-537.md) sweeps an output-scale
parameter `α` and shows it makes grokking more dramatic or removes it entirely,
and shows that worse alignment between the initial NTK's top eigenvectors and
the labels produces more intense grokking — and, because feature learning is
then necessary rather than optional, a *lower* final test loss. Alignment is
computable on any task as centered kernel alignment.

## Why this is `Active` when the mechanisms are not

The record holds three rival accounts of *why* — [THEORY-072](THEORY-072.md),
[THEORY-071](THEORY-071.md) and [THEORY-070](THEORY-070.md) — and none is settled; one of them exists
because it is an explicit counterexample to the other two. They disagree about
the mechanism and they do not disagree about this. A dataset-size condition
appears in all four papers, including in [LIT-537](../literature.d/LIT-537.md)'s own list of three
conditions, which is the paper arguing hardest against the others.

A claim that survives the disagreement of every account of the thing it
describes is in a different evidential position from any of them.

## What it is not

**Not "grokking is an artefact".** Ungrokking ([LIT-539](../literature.d/LIT-539.md)) is a real,
sharp, reproducible behaviour, and the representations [LIT-538](../literature.d/LIT-538.md) visualizes
are real structure. The phenomenon happens; it happens in a regime.

**Not "three knobs is the list".** Three are established. Weight decay strength
changes the *timing* in two of the accounts without being one of these axes,
and [LIT-538](../literature.d/LIT-538.md) reports operations that never generalize at any data
fraction, which no knob here explains.

**Not a licence to read across the demonstrations.** Every result outside
algorithmic data in [LIT-540](../literature.d/LIT-540.md) changes two things at once — a much smaller
training set *and* an inflated initialization — so the axes are established
jointly rather than separately, and the paper says so.

## What would change this

A demonstration of delayed generalization at standard initialization, on a
standard-sized dataset, with no knob turned — that is, grokking arriving
unbidden in an ordinary training run. Nothing in these four papers is that, and
the one setting where it occurs unbidden is the small algorithmic dataset,
which is itself a regime choice.
