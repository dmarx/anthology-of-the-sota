---
number: 37
status: Active
formerly:
- THEORY-tmpmnsb5
title: 'Residual-branch depth sets the depth scaling rule, because a branch with two transformations has a second-order update term that a branch with one does not'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-462
extends:
- THEORY-076
explains:
- SOTA-144
- SOTA-275
- SOTA-276
summary: >-
  Zheng et al. (2026), [LIT-462](../literature.d/LIT-462.md) — Depth-muP and CompleteP are
  `k = 1` and `k ≥ 2` of one condition. The cross term where both weights in
  a branch move in the same step is what tightens the residual multiplier
  from `1/√L` to `1/L`, and it does not exist when the branch holds one
  weight.
---

<!-- inactive-ok-file: SOTA-144 SOTA-275 SOTA-276 THEORY-024 — the three practices this account explains, all Proposed, two of them filed in this same contribution; THEORY-024 is Proposed and is distinguished from rather than leaned on -->
# THEORY-037: Residual-branch depth sets the depth scaling rule, because a branch with two transformations has a second-order update term that a branch with one does not

## Source

Zheng et al. (2026), [LIT-462](../literature.d/LIT-462.md) — read as [NOTE-211](../notes.d/NOTE-211.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-144](../practices.d/SOTA-144.md) | use CompleteP to transfer across depth | the `k ≥ 2` member of one family, not a rival parameterization |
| [SOTA-275](../practices.d/SOTA-275.md) | pick the rule from the residual branch | the family is indexed by branch depth, and that is the whole index |
| [SOTA-276](../practices.d/SOTA-276.md) | add one `1/L` multiplier to width muP | preconditioning removes the depth factor, so nothing else moves |

## The account

Write the change in a residual block's output after one step. For a branch
holding a single weight, every term has exactly one `ΔW` in it. For a branch
holding two, there is also the term where *both* moved: the product
`ΔW⁽²⁾ΔW⁽¹⁾`.

In ordinary analysis that cross term is second order and negligible. Under
muP it is not, and the reason is what muP is for. The maximal-update
principle deliberately makes each update as large as stability permits, so
`ΔW` is not small — it is exactly as large as the constraint allows. A
product of two such terms is therefore the same order as the terms
themselves, and it needs its own constraint.

Adding that constraint is the entire difference between the two published
depth parameterizations. Without it the residual multiplier can be
`Θ(1/√L)`, which is Depth-muP. With it the multiplier must be `Θ(1/L)`,
which is CompleteP. Carry the expansion to a branch of depth `k` and all
orders up to `k` get the same `Θ(1/L)` constraint — and the resulting
parameterization stops changing after `k = 2`, so there is no third regime
to discover.

The consequence for practice is structural rather than empirical. An
architecture does not get to choose which depth rule it wants; the number of
transformations in its residual branch chooses. Every Transformer has more
than one, so every Transformer is in the tighter regime.

## What was actually shown

The derivation is the argument, and the experiment is a prediction test
rather than a demonstration. The theory says the `k = 1` rule should fail to
transfer on architectures whose branches hold more than one transformation.
Figure 2 sweeps depth from 4 to 256 on GPT-2-style models under both rules:
the `k = 1` optimum drifts with depth, the `k ≥ 2` optimum does not. It
could have come out with both transferring, or with neither, and it did not.

## What this does not say

**It does not say the two rules differ much at the depths people train
today.** The paper's own §5.4 is the check that matters here: for
Muon-Kimi-AdamW even *standard* parameterization appears to transfer across
depth reasonably well, and the authors attribute it to moderate depths and to
LayerNorm and QKNorm masking the pathology. Remove LayerNorm and SP breaks.
That is a finding about how much modern normalization is already absorbing,
and it means the practical margin at realistic depth is smaller than the
asymptotic argument suggests.

**It does not establish CompleteP at scale.** 300M tokens per run. The
account explains why a parameterization is right; how much it is worth is a
separate question that these runs cannot answer, which is why
[SOTA-144](../practices.d/SOTA-144.md) stays `Proposed`.

**It is not a duality claim and does not need one.** [THEORY-024](../theory.d/THEORY-024.md) holds
that muP is a partial approximation of a duality map. This derives muP —
including for Shampoo and Muon, the other objects in that account — from norm
bookkeeping alone, with no dual space anywhere. The two frames describe the
same objects and neither requires the other, which is worth recording now
that the duality frame is itself `Proposed`.

**And the scale estimates are estimates.** The derivation tracks typical
magnitudes using subadditivity and submultiplicativity, and their tightness
rests on non-cancellation and alignment behaviour that the paper argues for
rather than proves.

## Why `Active`

The claim is a decomposition, it is checkable by hand, and the one place it
makes a falsifiable prediction about training — that `k = 1` scaling fails on
multi-transformation branches — was tested against the alternative and held
across four optimizers. It also unifies two published results the record
carried separately without saying how they relate.
