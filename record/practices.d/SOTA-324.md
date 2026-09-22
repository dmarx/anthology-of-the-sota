---
number: 324
status: Proposed
formerly:
- SOTA-tmpxlbv7
title: 'Separate rival accounts of an internal algorithm by convergence rate and conditioning, not by how well each fits the output'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
- training-optimization
date: '2026-09-22'
source:
- LIT-535
introduced_by:
- LIT-535
contested_by: []
explained_by:
- THEORY-067
promote_when: >-
  The layer-to-iteration measurement is run on a model pretrained on a general
  objective rather than on the task family, and reports a rate — of any order —
  against a candidate algorithm. That is the test the whole in-context-learning
  dispute lacks, and a method that only works on purpose-trained models is
  worth less than this one claims.
summary: >-
  Fu, Chen, Jia and Sharan (2023), [LIT-535](../literature.d/LIT-535.md) — output similarity cannot tell
  gradient descent from Newton's method, because both converge to the same
  answer. Matching each layer to the best-fitting step count of each candidate
  gives a linear trend for the right rate and an exponential one for the wrong
  one; a regime where the rivals must differ — here, condition number 100 —
  separates them again. Two measurements, both cheap, both decisive where a fit
  was not.
---

# SOTA-324: Separate rival accounts of an internal algorithm by convergence rate and conditioning, not by how well each fits the output

<!-- inactive-ok-file: SOTA-323 — Proposed, the sibling practice filed in this same contribution and named as its counterpart; it is new, not retired. -->

## Source

Fu, Chen, Jia and Sharan (2023), [LIT-535](../literature.d/LIT-535.md) — NeurIPS 2024. Read as
[NOTE-278](../notes.d/NOTE-278.md).

## The practice

When two candidate algorithms are proposed for what a network computes
internally, do not compare each one's output to the network's. Both
candidates converge to the same answer on the task, so both will fit — and
[LIT-535](../literature.d/LIT-535.md) reports exactly that: gradient descent shows high output
similarity with the trained model at later layers, and it is still the wrong
description.

Two measurements do separate them.

**A rate.** If depth is iteration, then matching layer `ℓ` to the
best-fitting step count `k(ℓ)` of a candidate gives a relation whose *shape*
is the diagnosis. The candidate with the model's own convergence rate gives a
straight line; one that is exponentially slower gives an exponential curve.
Here: roughly 3 Iterative Newton iterations per middle layer between layers 3
and 9, against an exponential correspondence with gradient descent, and single
layers advancing as far as hundreds of GD steps.

**A regime where the rivals must differ.** Pick a setting the candidates
respond to differently on theoretical grounds, and put the model in it. Here:
conditioning, because second-order methods depend on `κ` logarithmically and
first-order methods polynomially. At `κ(Σ) = 100` with a per-sequence random
eigenbasis, the model still matched Newton at 21 iterations while gradient
descent needed about 2,000 steps — more than the twelve layers available, and
not rescuable by a preconditioner, because the eigenbasis is resampled.

Two independent separations pointing the same way is what "the model is doing
`A` and not `B`" needs. One fit is not.

## Claim the result at the strength the method supports

[LIT-535](../literature.d/LIT-535.md)'s own discipline is part of the practice: BFGS shows the same
linear trend as Iterative Newton, so the paper claims *a* second-order method
rather than a named one. A rate identifies an algorithm's *class*. Naming a
specific member requires evidence the rate does not carry, and the record
files the paper's restraint as part of what it is recommending.

## Why it is `Proposed`

**One source and one problem class.** Both measurements need a task whose
optimal algorithm is known in closed form and whose candidate solvers have
established rates — linear regression obliges, most things do not. Whether
the method extends to a setting without an answer key is untested.

**And it has only been run on purpose-trained models**, which is the gap
[SOTA-323](SOTA-323.md) names. That is what `promote_when` asks for: the same
measurement on a model pretrained on a general objective. It is also the
experiment this record could not find anybody having done, on either side of
the dispute.

## Relation to the other half

[SOTA-323](SOTA-323.md) says to check what family of models your evidence comes from.
This says how to tell two mechanisms apart once you have the right models.
They came out of different papers on the same dispute and neither subsumes the
other: [LIT-535](../literature.d/LIT-535.md) applies this method inside the purpose-trained setting
[SOTA-323](SOTA-323.md) warns about, and reaches a sound conclusion about that setting.
