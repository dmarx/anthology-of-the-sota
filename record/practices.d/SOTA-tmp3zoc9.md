---
status: Proposed
consensus: unassessed
consensus_note: >-
  Nobody has surveyed what practitioners believe about short-timescale loss
  non-monotonicity, and the honest answer is that the record has not looked.
  The negative half — that curvature-based step-size rules are not used — is
  true of the field by observation, but nobody has written down why, and
  `DP-005` is exactly the reason not to count that as agreement.
promote_when: >-
  The same head-to-head in the stochastic setting at a scale the record's
  other optimization practices are evidenced at: a curvature-annealed step
  size against a fixed or fixed-schedule one, on a decoder-only transformer
  at a billion parameters or more, with the sharpness measured. What would
  not settle it: another full-batch demonstration of the edge of stability,
  which is the premise here rather than the claim.
title: 'Expect the loss to be non-monotone at the step size that trains fastest, and do not set the step size from a curvature bound'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmpnqv3x
introduced_by:
- LIT-tmpnqv3x
implementations: []
summary: >-
  Cohen et al. (2021), [LIT-tmpnqv3x](../literature.d/LIT-tmpnqv3x.md) — gradient descent raises the
  sharpness until its own step size cannot tolerate more, so a rule that
  anneals the step size to the measured curvature is chasing a number it is
  producing, and loses to the fixed step it forbids. Demonstrated full-batch.
explained_by:
- THEORY-tmpp47kd
---

# SOTA-tmp3zoc9: Expect the loss to be non-monotone at the step size that trains fastest, and do not set the step size from a curvature bound

## Source

Cohen et al. (2021), [LIT-tmpnqv3x](../literature.d/LIT-tmpnqv3x.md) — [ARXIV-2103.00065](https://arxiv.org/abs/2103.00065),
read as [NOTE-tmp72c2z](../notes.d/NOTE-tmp72c2z.md). Accounted for by
[THEORY-tmpp47kd](../theory.d/THEORY-tmpp47kd.md).

## What to do

Two things, one negative and one interpretive.

**Do not set the step size from a measurement of local curvature.** The
classical rule — `eta ≤ 2/sharpness`, optimally `1/sharpness` — treats
curvature as a property of the landscape that the step size must respect.
It is not: gradient descent raises the sharpness until it reaches `2/eta`
and then stops, so the quantity being measured is downstream of the
quantity being set. Run the rule and it anneals forever, chasing its own
output. In a direct comparison it is beaten by a fixed step size that the
rule itself calls impermissible.

**When the loss bounces over short timescales while falling over long ones,
that is not an instability to correct.** At any step size worth using,
training sits where oscillation along the highest-curvature direction is
the mechanism keeping a fixed step size viable. Lowering the learning rate
because the curve looks rough buys a smoother curve and a sharper
landscape, not a healthier run. The signal that something is wrong is the
long-timescale trend, not the short-timescale texture.

## Conditions

This is `Proposed`, and the gap between what was shown and what a reader
will want to do with it is wide enough to state plainly.

- **Full-batch gradient descent.** The `2/eta` equilibrium is a full-batch
  result and the paper says so in §6: under SGD the sharpness settles
  nowhere predictable from the hyperparameters. Nothing this record
  recommends is trained full-batch.
- **Small scale.** CIFAR-10-class vision architectures and a Transformer on
  WikiText-2.
- **One head-to-head.** The `1/sharpness` comparison is a single experiment
  in an appendix, not a study.
- **The interpretive half is a caution, not a diagnostic.** "Non-monotone is
  normal" does not tell you which non-monotonicity is normal. Loss spikes
  that do not recover, in large-batch transformer training, are a separate
  and real failure mode, and nothing here licenses ignoring them.
- **Sharpness here means the top Hessian eigenvalue and nothing about
  generalization.** The paper disclaims that connection explicitly.

## Why file it at all, given those conditions

Because the field's behaviour and the field's stated reasons have come
apart, and that is the gap an anthology is for. Nobody sets learning rates
from a curvature bound in practice — but the textbook account of why you
*could* is still what a reader meets first, and there is a published
experiment showing the rule loses to what it prohibits. [DP-005](../principles.d/DP-005.md) says
adoption is not evidence; the converse holds too, and a recommendation
everybody already follows for no recorded reason is worth the paper it
finally has.

## Relation to the neighbours

[SOTA-270](../practices.d/SOTA-270.md) warns against reading a smooth loss curve as evidence of
smooth training. This warns against reading a rough one as evidence of
broken training. They are the same caution about the same instrument, filed
from different directions, and a reader who has one should be handed the
other.
