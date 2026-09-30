---
number: 41
status: Proposed
formerly:
- THEORY-tmp99061
title: 'Left unconstrained, a transformer''s matrices drift into a badly conditioned, rank-deficient shape, and the norms are the part nothing was managing'
version: 1
promote_when: >-
  An intervention that separates conditioning from norm constraint — a model
  whose matrices are well conditioned without being normalized, or normalized
  without being well conditioned — with the training-speed comparison held
  otherwise equal. A further measurement that unconstrained matrices are badly
  conditioned is not it; that is the observation this account already rests on.
tags:
- model-stability
- model-architecture
date: '2026-09-21'
source:
- LIT-472
explains:
- SOTA-282
summary: >-
  Loshchilov et al. (2024), [LIT-472](../literature.d/LIT-472.md) — trained GPT embeddings
  form a hyper-ellipsoid with a high condition number and attention matrices
  whose singular values suggest rank deficiency; renormalizing after training
  narrows the gap without closing it. `Proposed`, because the evidence is
  correlational: these models are worse conditioned and they also train
  slower, and nothing yet connects the two.
---

<!-- inactive-ok-file: SOTA-122 — Proposed, named as the intervention that would
     come closest to settling this account, which is a use that requires it to
     be untested rather than one that leans on it -->

<!-- inactive-ok-file: SOTA-282 — Proposed, and the practice this account
     explains; naming it in the `explains` table is the relation, not a claim
     that either is settled -->

# THEORY-041: Left unconstrained, a transformer's matrices drift into a badly conditioned, rank-deficient shape, and the norms are the part nothing was managing

## Source

Loshchilov, Hsieh, Sun and Ginsburg (2024), [LIT-472](../literature.d/LIT-472.md) — read as
[NOTE-221](../notes.d/NOTE-221.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-282](../practices.d/SOTA-282.md) | put every matrix and hidden state on the unit hypersphere | removing a degree of freedom nothing was steering, which had been drifting somewhere bad |

## The account

In an ordinary transformer, the *direction* of every weight vector is trained
and its *magnitude* is not — not directly. Magnitude is a residue of
initialization, the learning rate, and weight decay pulling against the
gradient. Nobody chose it; it is where the tug-of-war settled.

The claim is that where it settles is not benign. Measured on trained models:

- **Input embeddings spread into a hyper-ellipsoid.** Norms vary widely,
  and the covariance eigenvalue spectrum has a high condition number —
  markedly worse at 1B than at 0.5B, so it worsens with scale.
- **Attention matrices lose rank.** Singular-value distributions in the third
  and fourth layers are consistent with degeneration toward lower-rank
  matrices, which bounds what those blocks can compute.
- **It is not only the norms.** Renormalizing a trained GPT's matrices after
  the fact *reduces* the condition numbers without bringing them down to the
  constrained model's. Some of the ill-conditioning is in the directions, and
  fixing the norms during training is what prevents it — after the fact is
  too late.

That last point is what makes this an account rather than a tautology. If
normalizing afterwards fixed the numbers, the constraint would just be
changing what you measure. It does not, so the constraint is changing what
gets learned.

The accompanying reading — that a normalized transformer is a variable-metric
optimizer on the sphere, each block proposing a direction and its learned
`α` supplying the step size — is a frame rather than part of this account. It
is why the paper's parameters have the names they do, and it carries no
evidence of its own.

## Why `Proposed`

Because the evidence is correlational and the paper does not pretend
otherwise. Unconstrained models are worse conditioned. Unconstrained models
also take more tokens to reach a given loss. Nothing measured connects the
two — no intervention isolates conditioning, and no result shows that a
badly conditioned model is slow *because* it is badly conditioned.

What would settle it: an architecture that fixes the conditioning without
fixing the norms, or the reverse, with the training-speed comparison held
otherwise equal. [SOTA-122](../practices.d/SOTA-122.md)'s learnable multipliers are close to such a
probe — they manage norms explicitly without constraining them to one — and
nobody has reported conditioning numbers for a model trained that way.

## What this does not say

**It does not say normalization layers were doing nothing.** They keep
activations in range; this is about the *weights*, and the two are different
quantities with a confusingly shared word.

**It does not say weight decay is harmful.** It says that in an architecture
where norms are fixed by construction there is nothing left for weight decay
to do. On an unconstrained architecture [SOTA-120](../practices.d/SOTA-120.md) stands unaffected.

**It is measured at 0.5B and 1B, at layers 3 and 4, on OpenWebText.** The
scale-worsening observation rests on two points — 0.5B and 1B — which is a
direction rather than a trend.
