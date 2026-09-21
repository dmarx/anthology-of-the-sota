---
number: 277
status: Proposed
formerly:
- SOTA-tmphvq7d
consensus: unassessed
consensus_note: >-
  Depth-versus-width is settled as a scaling question and not as a
  task-conditional one. Nobody has surveyed whether practitioners shape
  models differently for compositional workloads, and this recommendation is
  a theorem plus two empirical papers it was written to explain.
promote_when: >-
  A controlled comparison at matched parameter count — deeper and narrower
  against shallower and wider — on a task with a tunable composition depth,
  showing the deep model's advantage growing with that depth. The prediction
  is specifically about the *interaction* with composition depth, so a result
  that deep models are better overall would not settle it: that is a known
  scaling fact with other explanations. What would also not settle it:
  another lower bound, which strengthens the theory and not the
  recommendation.
title: 'For a task that is a sequential composition, buy depth rather than width'
version: 1
tags:
- model-architecture
date: '2026-09-21'
source:
- LIT-464
introduced_by:
- LIT-464
implementations: []
summary: >-
  Chen et al. (2024), [LIT-464](../literature.d/LIT-464.md) — composing `k` functions costs a
  constant-depth decoder polynomially many parameters and a `log k`-layer one
  polylogarithmically. An exponential separation, proved unconditionally, and
  about what a shape can express rather than what a run will learn.
explained_by:
- THEORY-038
---

<!-- inactive-ok-file: SOTA-125 SOTA-144 SOTA-tmpnjlal — SOTA-125 is Proposed and is the tiny-model neighbour this is compared with rather than derived from; SOTA-144 and SOTA-tmpnjlal are Proposed and are named to say that the cost of depth is an open question, which is a caveat rather than a claim -->
# SOTA-277: For a task that is a sequential composition, buy depth rather than width

## Source

Chen et al. (2024), [LIT-464](../literature.d/LIT-464.md) — [ARXIV-2412.02975](https://arxiv.org/abs/2412.02975),
read as [NOTE-214](../notes.d/NOTE-214.md). Accounted for by [THEORY-038](../theory.d/THEORY-038.md).

## What to do

When the workload is *sequential composition* — apply a step, feed the result
to the next step, repeat — and you are choosing how to spend a fixed
parameter budget on a decoder-only model, spend it on layers rather than on
width.

The separation behind this is not a constant factor. Composing `k` functions
over a long context needs **polynomially many** parameters at constant depth
and **polylogarithmically many** at `log k` depth. Width can substitute for
depth here, and the exchange rate is exponentially bad.

The reason is specific to decoders and worth knowing, because it tells you
when the advice does not apply: causal masking means a position cannot see
what follows it, and a position does not retain what it forwarded. Each layer
buys one round of information movement. Composition needs `k` rounds or
enough bits per position to shortcut them. [THEORY-038](../theory.d/THEORY-038.md) has the
argument.

## Conditions

This is `Proposed`, and the distance between the theorem and the
recommendation is the reason.

- **The theorem is about representability, not learnability.** It says no
  parameter setting of a shallow narrow decoder computes the function. It
  does not say training finds the composing solution when one exists, and it
  does not say a model below the bound fails on inputs anyone uses.
- **It is asymptotic in context length.** No constant in it is small enough
  to tell you anything about a specific model at a specific context length.
  "Buy depth" is a direction, not a ratio.
- **The hard task is constructed** against this model class. That composition
  is hard for decoders is a real fact; that your compositional workload is
  hard for the same reason is an extrapolation.
- **It is a decoder-only result.** An encoder solves the same task
  exponentially smaller, which is the paper's second corollary — so this says
  nothing about encoder architectures, and nothing here argues against
  decoder-only, which won on generation and efficiency grounds this does not
  touch.
- **Depth is not free.** Deeper models are harder to train and to scale;
  the depth parameterization is its own open question — see
  [SOTA-144](../practices.d/SOTA-144.md) and [SOTA-tmpnjlal](../practices.d/SOTA-tmpnjlal.md) — and none of that cost
  appears in a representability bound.

## Relation to the neighbours

[SOTA-125](../practices.d/SOTA-125.md) recommends depth over MLP width at a fixed *tiny* parameter
budget, filed from experiments. This is the general-scale theoretical
counterpart, from an unconditional bound, and the two were reached
independently — which is worth more than either alone, and is not the same as
either confirming the other, since one is measured and one is proved.

## Known implementations

- None recorded as having been chosen for this reason. Deep-and-narrow models
  exist; nobody in the record shaped one because of a composition argument.
