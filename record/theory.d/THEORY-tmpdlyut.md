---
status: Active
title: 'Grokking is a regime rather than a property of algorithmic data, and at least three knobs move it'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- model-stability
date: '2026-09-22'
source:
- LIT-tmp4uno1
- LIT-tmpkn1i6
- LIT-tmp069e7
- LIT-085
explains:
- SOTA-200
summary: >-
  Delayed generalization is not a fact about modular arithmetic. It is produced
  and removed by moving the training regime, and three knobs have been shown to
  move it: **training-set size** (Power et al., [LIT-tmp4uno1](../literature.d/LIT-tmp4uno1.md), and the ~60%
  threshold in [LIT-085](../literature.d/LIT-085.md)), **initialization scale relative to the generalizing
  weight norm** (Liu et al., [LIT-tmpkn1i6](../literature.d/LIT-tmpkn1i6.md), which uses it to induce grokking on
  MNIST, IMDb and QM9 and to eliminate it on algorithmic data), and **the
  alignment between the initial neural tangent kernel and the target** (Kumar
  et al., [LIT-tmp069e7](../literature.d/LIT-tmp069e7.md)). The three mechanistic accounts in this record
  contradict each other; they agree on this.
---

# THEORY-tmpdlyut: Grokking is a regime rather than a property of algorithmic data, and at least three knobs move it

<!-- inactive-ok-file: THEORY-tmpmiiyl — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-tmplnntp — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->
<!-- inactive-ok-file: THEORY-tmpz9vjh — Proposed, and named here as one of the three rival mechanisms this cluster holds; Proposed is the record's judgement on its scope, which is the point being made when it is cited. -->


## The account

Grokking — training accuracy saturating long before validation accuracy leaves
chance — is a *regime* a training run can be put into and taken out of. It is
not a property of algorithmic datasets, and it is not a fundamental feature of
overparameterized learning. Three separate knobs have been shown to control it,
each demonstrated in both directions.

**Training-set size.** [LIT-tmp4uno1](../literature.d/LIT-tmp4uno1.md) measures it in the paper that named the
phenomenon: converged accuracy is flat across a range of training fractions
while the *time* to reach it explodes as the fraction falls — in the vicinity
of 25–30% on `S₅`, removing 1% of the data raises median steps-to-generalize by
40–50%, while steps-to-fit stay at `10³`–`10⁴`. [LIT-085](../literature.d/LIT-085.md) puts a threshold on
it: above roughly 60% data on modular addition, grokking is gone and
generalization is immediate.

**Initialization scale relative to the generalizing weight norm.**
[LIT-tmpkn1i6](../literature.d/LIT-tmpkn1i6.md) induces grokking on **MNIST** (depth-3 MLP, 1k examples, Kaiming
weights scaled by `α > 1`), on **IMDb** with an LSTM at `α = 6`, and on **QM9**
with a GCNN at `α = 3`. At the standard initialization there is no grokking on
any of them. Run the other way, constraining the model to a small-weight-norm
sphere nearly eliminates grokking on algorithmic data.

**Initial kernel–task alignment.** [LIT-tmp069e7](../literature.d/LIT-tmp069e7.md) sweeps an output-scale
parameter `α` and shows it makes grokking more dramatic or removes it entirely,
and shows that worse alignment between the initial NTK's top eigenvectors and
the labels produces more intense grokking — and, because feature learning is
then necessary rather than optional, a *lower* final test loss. Alignment is
computable on any task as centered kernel alignment.

## Why this is `Active` when the mechanisms are not

The record holds three rival accounts of *why* — [THEORY-tmpz9vjh](THEORY-tmpz9vjh.md),
[THEORY-tmpmiiyl](THEORY-tmpmiiyl.md) and [THEORY-tmplnntp](THEORY-tmplnntp.md) — and none is settled; one of them exists
because it is an explicit counterexample to the other two. They disagree about
the mechanism and they do not disagree about this. A dataset-size condition
appears in all four papers, including in [LIT-tmp069e7](../literature.d/LIT-tmp069e7.md)'s own list of three
conditions, which is the paper arguing hardest against the others.

A claim that survives the disagreement of every account of the thing it
describes is in a different evidential position from any of them.

## What it is not

**Not "grokking is an artefact".** Ungrokking ([LIT-tmp9xrey](../literature.d/LIT-tmp9xrey.md)) is a real,
sharp, reproducible behaviour, and the representations [LIT-tmp4uno1](../literature.d/LIT-tmp4uno1.md) visualizes
are real structure. The phenomenon happens; it happens in a regime.

**Not "three knobs is the list".** Three are established. Weight decay strength
changes the *timing* in two of the accounts without being one of these axes,
and [LIT-tmp4uno1](../literature.d/LIT-tmp4uno1.md) reports operations that never generalize at any data
fraction, which no knob here explains.

**Not a licence to read across the demonstrations.** Every result outside
algorithmic data in [LIT-tmpkn1i6](../literature.d/LIT-tmpkn1i6.md) changes two things at once — a much smaller
training set *and* an inflated initialization — so the axes are established
jointly rather than separately, and the paper says so.

## What would change this

A demonstration of delayed generalization at standard initialization, on a
standard-sized dataset, with no knob turned — that is, grokking arriving
unbidden in an ordinary training run. Nothing in these four papers is that, and
the one setting where it occurs unbidden is the small algorithmic dataset,
which is itself a regime choice.
