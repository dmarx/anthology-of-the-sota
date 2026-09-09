---
number: 8
status: Read
formerly:
- NOTE-tmpvfccf
paper: LIT-014
title: 'Visualizing the Loss Landscape of Neural Nets'
version: 1
tags:
- model-stability
date: '2026-09-09'
summary: >-
  Filter normalization makes loss-surface plots comparable across architectures, and under it sharpness correlates with generalization error. Deep networks transition from nearly convex to chaotic; skip connections prevent that transition, which is why they are needed at depth.
---

# NOTE-008: Visualizing the Loss Landscape of Neural Nets

## Contribution

Loss-surface pictures were common and untrustworthy: because a network can be
rescaled without changing the function it computes, two plots of the same
model at different scales show different apparent sharpness. This paper
supplies **filter normalization**, a normalisation of the random plotting
directions that makes side-by-side comparison meaningful — and then uses it to
establish two things that were folklore. Sharpness correlates with
generalization error once you measure it this way; and deep networks without
skip connections transition from a nearly convex landscape to a chaotic one,
which is what makes them untrainable.

## Key insight

Before you can claim a geometric property of a loss surface, you have to fix
the fact that the surface has no canonical scale. Neural networks have
symmetries — rescale a filter's weights up and the next layer's down, and the
function is unchanged while the landscape's apparent curvature is not. Every
sharpness measure that ignores this is measuring an artefact.

Filter normalization removes the degree of freedom by scaling each filter's
plotting direction to the norm of the corresponding filter. What survives is a
comparison that means something, and under it the sharpness/generalization
relationship — which earlier work had shown was *not* invariant to those
symmetries — comes back.

## Assumptions

- **Convolutional vision architectures**: ResNet-56, ResNet-56-noshort,
  DenseNet-121, VGG-9, on CIFAR-scale data. Nothing here is a Transformer or a
  language model.
- Visualisation is over **1D and 2D random slices** of a very
  high-dimensional surface. The paper argues these are informative and is
  explicit that they are slices.
- **Filter normalization is required for the comparisons to hold.** It is not
  a presentational choice; the paper's own §3 shows unnormalised plots
  mislead.
- Loss evaluations are expensive — the reason this field had "remained
  predominantly theoretical" — so the visualisations are around minimisers,
  not exhaustive.

## Key results

- **Filter normalization.** Scale each random direction filter-wise to match
  the norm of the corresponding filter in the trained network. Without it,
  1D interpolation plots do not account for batch normalization or the
  network's invariance symmetries, and their sharpness comparisons "may be
  misleading".
- **Sharpness correlates with generalization error** *when this normalization
  is used* — "even when making comparisons across disparate network
  architectures and training methods". The conditional clause is the result.
- **The convex-to-chaotic transition.** "When networks become sufficiently
  deep, neural loss landscapes quickly transition from being nearly convex to
  being highly chaotic. This transition ... coincides with a dramatic drop in
  generalization error, and ultimately to a lack of trainability."
- **Skip connections prevent it.** They "promote flat minimizers and prevent
  the transition to chaotic behavior, which helps explain why skip connections
  are necessary for training extremely deep networks."
- **Non-convexity, quantified.** Figure 7 maps the ratio **`|λ_min/λ_max|`**
  of the Hessian across the filter-normalized surface. Blue is near-convex
  (negative eigenvalues near zero relative to positive); yellow is
  significant negative curvature. For ResNet-56 the negative eigenvalues stay
  **under 1% of the positive curvatures** over a large region.
- **It is computable.** The eigenvalues come from an **implicitly restarted
  Lanczos method** needing only Hessian-vector products via automatic
  differentiation — no explicit Hessian, no factorisation.
- **Optimization trajectories lie in an extremely low-dimensional space**,
  which the paper explains by the large nearly-convex regions its 2D
  visualisations show.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Loss-surface sharpness comparisons are meaningless without normalising for network rescaling symmetries | strong | argued from the symmetry, demonstrated against unnormalised plots, and consistent with Dinh et al. and Neyshabur et al. |
| C2 | Under filter normalization, sharpness correlates with generalization error across architectures | moderate | a visual and qualitative correlation across many models; not a fitted relationship |
| C3 | Sufficiently deep networks transition from nearly convex to chaotic landscapes | moderate | observed across a depth sweep on CIFAR-scale convnets |
| C4 | Skip connections prevent that transition and promote flat minimizers | strong | the ResNet-56 vs ResNet-56-noshort comparison, the paper's clearest result |
| C5 | `|λ_min/λ_max|` is a usable non-convexity diagnostic | strong | Figure 7, computed by Lanczos on Hessian-vector products |
| C6 | SGD trajectories occupy a very low-dimensional subspace | moderate | shown for the models studied, with a proposed explanation |

## Method

**Filter normalization.** To plot the loss along random directions `d`, scale
each filter's component of `d` to have the same norm as the corresponding
filter of the trained network. Then evaluate the loss on a 1D or 2D grid of
perturbations. For curvature, compute `λ_min` and `λ_max` of the Hessian at
each grid point by implicitly restarted Lanczos over Hessian-vector products,
and map `|λ_min/λ_max|`.

## Concepts

- **Filter normalization** — the paper's own contribution and the thing that
  makes everything else in it citable. Normalising plotting directions
  filter-wise against the trained weights.
- **Chaotic landscape** — a loss surface dominated by non-convexity, as
  distinct from "nearly convex". The paper's term for what deep networks
  without skip connections have, and it ties to trainability rather than to
  sharpness.
- **Flat minimizer** — a minimum in a wide low-loss basin. The definition
  goes back to Hochreiter and Schmidhuber; the contribution here is making it
  measurable in a scale-invariant way.
- **`|λ_min/λ_max|`** — negative curvature relative to positive, at a point.
  Near zero means locally convex.

## Connections

Responds directly to the sharpness/generalization literature — Hochreiter and
Schmidhuber's flatness, Keskar et al.'s `ε`-sharpness — and to Dinh et al. and
Neyshabur et al., who showed those measures are **not invariant to network
symmetries** and are therefore not reliable. Filter normalization is the
answer to that objection. Goodfellow et al.'s 1D interpolation plots are the
method it argues is insufficient.

## Recommendations

- **R1** — Normalise for scaling symmetries before comparing loss-surface
  sharpness. *Topic:* analysis. *Status:* standard. *Strength:* strong.
  *Applies when:* any comparison of curvature between models or checkpoints;
  without it you are measuring the parameterisation.
- **R2** — Use skip connections at depth. *Topic:* architecture. *Status:*
  standard. *Strength:* strong. *Applies when:* the network is deep enough
  that trainability is in question — which this paper is the explanation for,
  not the discovery of.
- **R3** — Track `|λ_min/λ_max|` as a non-convexity diagnostic. *Topic:*
  diagnostics. *Status:* experimental. *Strength:* moderate. *Applies when:*
  you can afford periodic Hessian-vector products; Lanczos makes it feasible
  without forming the Hessian.
- **R4** — Do not read sharpness as a causal handle. *Topic:* analysis.
  *Status:* standard. *Strength:* moderate. *Applies when:* always — C2 is a
  correlation, and the paper claims no more.

## Bearing on the record

**All three practices sourced to this note are confirmed** — the third such
cluster in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114).

| practice | disposition |
|---|---|
| [SOTA-010](../practices.d/SOTA-010.md) skip connections smooth the loss landscape | confirmed — C4, nearly verbatim |
| [SOTA-011](../practices.d/SOTA-011.md) Hessian eigenvalue ratio as a diagnostic | confirmed — C5, Figure 7 |
| [SOTA-012](../practices.d/SOTA-012.md) sharpness correlates with test error | confirmed — C2, with the filter-normalization condition its body already carries |

Two refinements the reading supplies:

`SOTA-011`'s title says "ratio of largest to smallest". The paper's quantity
is **`|λ_min/λ_max|`** — smallest over largest, and its interest is that
`λ_min` is *negative*, so the ratio measures non-convexity rather than
conditioning. Stated the other way up it reads like a condition number, which
is a different diagnostic.

<!-- inactive-ok-block: SOTA-021 — Rejected; named as the contrast that explains why SOTA-011 survived and it did not -->
`SOTA-011` also gains the reason it is affordable: **Lanczos over
Hessian-vector products**, no explicit Hessian. The record kept this practice
while retiring `SOTA-021` on the grounds that the eigenvalue ratio is at
least computable; that judgement was right and now has the method behind it.

## Limitations

- CIFAR-scale convnets throughout. Whether the convex-to-chaotic picture
  describes Transformer landscapes is untested here and untested in this
  record.
- C2 is a correlation observed across plots, not a fitted or predictive
  relationship — no number attaches to it.
- 1D and 2D slices of a millions-dimensional surface. The paper defends the
  choice; it remains a projection.
- The paper explains why skip connections work at depth; it does not compare
  them against later alternatives for the same problem.

## Open questions

- Does the convex-to-chaotic transition appear in Transformers, and if so at
  what depth and with what mitigations?
- C2 is qualitative. Is there a scale-invariant sharpness statistic that
  *predicts* generalization gap numerically?
- Optimization trajectories being low-dimensional (C6) suggests training
  could be reparameterised into that subspace. Nobody in this record has
  followed that up.
