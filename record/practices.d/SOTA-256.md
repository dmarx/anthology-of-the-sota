---
number: 256
status: Proposed
formerly:
- SOTA-tmpa2zin
promote_when: >-
  A second group adopting the asymptote as the reported figure of merit for a
  scaling comparison, or a paper showing that asymptote rankings and
  fixed-budget rankings disagree often enough to matter. What would not move
  it: another paper fitting a scaling law with an irreducible-loss term,
  which is standard and is not the same as using that term to choose between
  recipes.
consensus: unreplicated
consensus_note: >-
  One group, and the criterion is argued rather than measured — it is the
  paper's evaluation protocol, not one of its results. Filed because the
  comparisons it licenses are the substance of two other practices in this
  record, so a reader deciding whether to trust those needs it stated.
title: 'Judge a monotone scaling recipe by its asymptote, not by its loss at a compute budget'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-19'
source:
- LIT-441
introduced_by:
- LIT-441
implementations: []
summary: >-
  Kim et al. (2025), [LIT-441](../literature.d/LIT-441.md) — when compute is not the binding
  constraint, a recipe's loss at a chosen budget answers a question nobody
  asked. Fit the scaling law and compare the asymptote instead. The catch is
  that an asymptote is an extrapolation, and rankings at small scale can
  invert: the ensembling recipe wins on asymptote while losing at small
  member counts.
---

# SOTA-256: Judge a monotone scaling recipe by its asymptote, not by its loss at a compute budget
<!-- inactive-ok-file: SOTA-255 — Proposed, and filed in this same contribution from this same source -->
<!-- inactive-ok-file: SOTA-257 — Proposed, and filed in this same contribution from this same source -->

## Source

Kim et al. (2025), [LIT-441](../literature.d/LIT-441.md) — [ARXIV-2509.14786](https://arxiv.org/abs/2509.14786).

## The argument

Scaling comparisons are conventionally reported at a compute budget: recipe A
against recipe B at `10^20` FLOPs. That is the right comparison when compute
is what you are short of.

When data is the constraint and compute is not, it answers a question nobody
asked. The interesting quantity is *how good this recipe can get* — the limit
of its loss as its scaling variable goes to infinity. Fit
`L(x) = A/x^α + E` and compare `E`.

## Why it matters rather than being bookkeeping

Because the two orderings disagree. In the source, the ensembling recipe
loses to parameter scaling at small member counts and wins on asymptote; the
best hyperparameters at `K = 1` are not the best hyperparameters for the
limit. A comparison run at a budget would have reached the opposite
conclusion and would have tuned the losing configuration.

That is the whole content of the recommendation: a fixed-budget comparison of
two recipes is a statement about that budget, and reporting it as a statement
about the recipes is a category error whenever the recipes' curves have
different shapes.

## The precondition is doing real work

**Monotone.** The criterion applies only where loss decreases in the scaling
variable without turning up. The source's own standard recipe is *not*
monotone in parameter count under a data constraint — it overfits — and for
it the asymptote is undefined and the criterion says nothing. Getting a
recipe into the regime where this question can be asked is itself an
intervention ([SOTA-255](SOTA-255.md)).

## What it costs

An asymptote is an extrapolation, and it is the least well-determined
parameter of a power-law fit — small changes in the exponent move it a lot.
The source's best number is an asymptote of asymptotes, and its sensitivity
analysis covers seed variance in the individual fits rather than error
propagated through the double limit.

So the criterion buys the right question at the price of a less certain
answer, and a report using it owes the reader the fit, the range fitted over,
and the sensitivity — not just `E`.

## Conditions, and why this is `Proposed`

One group, and unlike the rest of that paper this is argued rather than
measured: it is the protocol the results are reported under, not a result.
The record files it because two other practices drawn from the same source
([SOTA-255](SOTA-255.md), [SOTA-257](SOTA-257.md)) rest their comparisons on it, and a reader
weighing those is entitled to see the criterion stated and its cost named
rather than inheriting it silently.

## Known implementations

- None in the record. Every scaling comparison it holds is reported at a
  budget.
