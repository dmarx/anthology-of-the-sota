---
status: Proposed
consensus: unassessed
consensus_note: >-
  The choice between the two depth parameterizations is not something the
  field has been posed as a choice — the two were published separately and
  used by whoever adopted one. Nobody has surveyed which is used where, and
  this claim about how to pick is one paper old.
promote_when: >-
  A depth sweep by another group, on an architecture whose residual branch
  holds one transformation, in which the `k = 1` rule transfers and the
  `k ≥ 2` rule does not. That is the prediction with a side that has not been
  tested: the paper shows `k ≥ 2` beating `k = 1` on Transformers, and the
  claim is that branch depth is the index rather than that the tighter rule
  is always better. What would not settle it: another Transformer sweep
  confirming CompleteP-style scaling, which is the half already shown.
title: 'Pick the depth parameterization from the residual branch: a Transformer branch has more than one transformation, so it needs the stricter rule'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmpfv7vs
introduced_by:
- LIT-tmpfv7vs
extends:
- SOTA-144
implementations: []
summary: >-
  Zheng et al. (2026), [LIT-tmpfv7vs](../literature.d/LIT-tmpfv7vs.md) — Depth-muP's `α = Θ(1/√L)` is
  the rule for a one-transformation residual branch. Attention and FFN
  branches hold more than one, so Transformers need CompleteP's
  `α = Θ(1/L)`, and the looser rule measurably fails to transfer on them.
explained_by:
- THEORY-tmpmnsb5
---

<!-- inactive-ok-file: SOTA-144 — Proposed, and the practice this one extends: it says use CompleteP, this says which architectures need it -->
# SOTA-tmpnjlal: Pick the depth parameterization from the residual branch: a Transformer branch has more than one transformation, so it needs the stricter rule

## Source

Zheng et al. (2026), [LIT-tmpfv7vs](../literature.d/LIT-tmpfv7vs.md) — [ARXIV-2603.00541](https://arxiv.org/abs/2603.00541),
read as [NOTE-tmpepjgm](../notes.d/NOTE-tmpepjgm.md). Accounted for by [THEORY-tmpmnsb5](../theory.d/THEORY-tmpmnsb5.md).

## What to do

Count the linear transformations inside one residual branch of your
architecture. That number, called `k`, picks the depth rule:

| `k` | residual multiplier | published name |
|---|---|---|
| 1 | `α_l = Θ(1/√L)` | Depth-muP |
| ≥ 2 | `α_l = Θ(1/L)` | CompleteP |

A Transformer's attention and FFN branches each hold more than one
transformation, so a Transformer is always the second row. Nothing changes
again past `k = 2`, so there is no further case to work out for a deeper
branch.

This is not a preference between two competing proposals. The two rules are
the same condition evaluated at different branch depths, and applying the
`k = 1` rule to a `k ≥ 2` architecture is a mismatch rather than a
conservative choice: in a depth sweep from 4 to 256 layers the optimal base
learning rate drifts under `k = 1` and holds under `k ≥ 2`, for
Muon-Kimi-AdamW, Muon-AdamW, Shampoo-AdamW and Sophia alike.

## Why it is a structural question and not an empirical one

Under muP each update is deliberately as large as stability allows, so when a
branch holds two weights the term in which *both* moved in one step is the
same order as the terms in which one did. Constraining that cross term is
what tightens the multiplier. A branch with one weight has no such term, so
its constraint set is genuinely looser. [THEORY-tmpmnsb5](../theory.d/THEORY-tmpmnsb5.md) holds the
derivation.

## Conditions

- **`Proposed`, and at 300M tokens per run.** The depth sweep is deep and
  short. Nothing here speaks to whether the choice still pays over a
  realistic token budget.
- **The margin at realistic depth is smaller than the theory suggests, and
  the authors say so.** In their §5.4, standard parameterization *appears* to
  transfer across depth for Muon-Kimi-AdamW; they attribute it to moderate
  depths and to LayerNorm and QKNorm masking the scaling pathology, and
  removing LayerNorm makes SP break. Modern normalization is already
  absorbing some of what the parameterization is for.
- **Only one side of the prediction is tested.** The claim is that branch
  depth is the index. What is shown is `k ≥ 2` beating `k = 1` on
  Transformers. Nobody has shown `k = 1` beating `k ≥ 2` on a
  one-transformation architecture, which is what would make this a rule
  rather than a preference for the tighter option.
- **Branch depth must be well defined.** An architecture with parallel
  attention and FFN, or with different branch depths at different blocks, is
  not covered.
- **The derivation is a deep linear residual MLP, one step, one example**,
  generalized under assumptions stated in an appendix.

## Relation to the neighbours

[SOTA-144](../practices.d/SOTA-144.md) says to use CompleteP so one sweep serves deeper models.
This says *which architectures need it and why*, and that the alternative
fails on Transformers specifically — which `SOTA-144` does not claim, because
[LIT-150](../literature.d/LIT-150.md) compared CompleteP against muP rather than against Depth-muP.
Declared as `extends`.
