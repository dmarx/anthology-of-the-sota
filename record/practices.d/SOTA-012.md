---
number: 12
status: 'Active'
title: 'sharpness in the loss landscape correlates with test error'
version: 3
history:
- version: 1
  note: >-
    Titled "sharpness in loss landscape corerlates with test error" — a typo in
    the claim itself, carried since the migration.
- version: 2
  note: >-
    Spelling corrected. The claim is unchanged; this is not a restatement, and
    is recorded only because a title is the thing citations resolve against.
- version: 3
  date: '2026-09-22'
  note: >-
    Adds a condition, not a correction. The correlation stands and so does the
    advice. What is new is LIT-tmp63rr1's argument that curvature is not the
    load-bearing quantity at all: neural networks are singular models, the
    theorems contain the exponent of the volume law and curvature is its
    prefactor. Filter normalisation fixes the rescaling artefact; it does not
    make the Hessian the right object. SOTA-tmpnp2m8 is the alternative
    measurement, and no compared_against is declared between them because
    nobody has run the comparison.
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-014
- LIT-tmp63rr1
introduced_by:
- LIT-014
# `SOTA-010` is Superseded because it moved to the THEORY scheme, not
# because the claim failed (ADR-034). The link stays: it records that
# three readings of one figure were filed together.
compared_against:
- SOTA-010
- SOTA-011
summary: >-
  Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).
---

<!-- inactive-ok-file: SOTA-010, ADR-034 — the sibling link is kept
     deliberately and the frontmatter says why; see the decision. -->

# SOTA-012: sharpness in the loss landscape correlates with test error

<!-- inactive-ok-file: SOTA-tmpnp2m8 — Proposed, filed in this same contribution as the alternative measurement, filed today; new, not retired. -->

## Source

Li et al. (2017), [LIT-014](../literature.d/LIT-014.md) — [ARXIV-1712.09913](https://arxiv.org/abs/1712.09913).

## The correlation, and what it is not

[LIT-014](../literature.d/LIT-014.md) visualises the loss surface around trained minima by filter-normalised
random directions, and the visible regularity is that solutions sitting in
wide, flat basins generalise better than solutions in sharp ones. The
filter normalisation is what makes the comparison meaningful — without it,
rescaling a network's weights changes the apparent sharpness without changing
the function at all, which is how earlier sharpness claims were shown to be
artefacts.

So the practice is a diagnostic reading rather than an objective: sharpness is
*correlated* with test error across the architectures and training
configurations examined, and the paper does not establish that flattening a
minimum causes better generalisation.

## Why the distinction matters here

Methods that optimise for flatness directly — sharpness-aware minimisation and
its relatives — exist and sometimes help, and they are a different claim with
their own evidence, which this record does not currently hold.

## A deeper objection than the rescaling one

Filter normalisation answers the objection that sharpness is not
reparameterisation-invariant. There is a second objection it does not answer,
and the record now holds it: **curvature may be the wrong quantity even when
measured perfectly.**

`LIT-tmp63rr1` makes the case. Neural networks are *singular* statistical
models — many parameters give the same function, so the set of optima is a
variety rather than a point and the loss is not locally quadratic. In
Watanabe's volume law `V(ε) ∝ ε^λ`, the quantity that enters the model-selection
criterion (`n L_n(w_0) + λ log n`) and the Bayes generalisation rate (`λ/n`) is
the **exponent** `λ` — the number of directions that change the function.
Curvature is the prefactor, and the prefactor appears in neither. In the source's
own words, the RLCT "matters more than the curvature of those directions (as
measured for example by eigenvalues of the Hessian) laying bare some of the
confusion over 'flat' minima".

This does not retire the practice. `LIT-014`'s correlation is a measurement and
it holds; the advice below — treat a visibly sharp basin as worth suspecting —
costs nothing and is still good. What it does is bound the explanation: the
correlation is evidence that something about the local geometry tracks
generalisation, and the geometry a visualisation displays may not be the part
doing the tracking. `SOTA-tmpnp2m8` is the practice that measures the exponent
instead, and `THEORY-tmpzuan6` is the account behind it.

Reading this practice as "make the minimum flatter and the model generalises"
is the failure it invites. What it supports is narrower and still useful: a
model whose basin is visibly sharp is worth suspecting, and a change that
sharpens the landscape (removing skip connections, per [THEORY-011](../theory.d/THEORY-011.md),
or raising
depth without them) has a known cost that shows up in the surface before it
shows up in the metric.
