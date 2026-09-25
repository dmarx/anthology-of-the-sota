---
number: 35
status: Active
formerly:
- THEORY-tmpp47kd
title: 'Gradient descent drives the sharpness up to the largest value its own step size tolerates, and then trains there'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Adds a section from Islamov et al. (LIT-tmp87rqx): the equilibrium
    replicates for steepest descent under the spectral, l-infinity and block
    norms, but only when sharpness is measured in the update's own norm.
    The account's quantity, the top Hessian eigenvalue, is the right one for
    Euclidean gradient descent only. Nothing removed; status unchanged.
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-461
explains:
- SOTA-272
summary: >-
  Cohen et al. (2021), [LIT-461](../literature.d/LIT-461.md) — the top Hessian eigenvalue rises
  until it reaches `2/eta` and then stops, so the step size sets the
  curvature rather than responding to it. Full-batch gradient descent only:
  under SGD the sharpness settles nowhere predictable.
---

<!-- inactive-ok-file: THEORY-030 THEORY-013 — THEORY-030 is Proposed and is cited for the premise its promote_when names; THEORY-013 is Rejected, and is named for exactly what it was rejected for, which is the misreading this section warns against -->
# THEORY-035: Gradient descent drives the sharpness up to the largest value its own step size tolerates, and then trains there

## Source

Cohen et al. (2021), [LIT-461](../literature.d/LIT-461.md) — read as [NOTE-205](../notes.d/NOTE-205.md).

## The account

Two forces, one equilibrium. **Progressive sharpening**: while the maximum
eigenvalue of the training-loss Hessian is below `2/eta`, gradient descent
raises it. **Instability**: above `2/eta`, gradient descent on the local
quadratic diverges, and the iterates begin oscillating along the direction of
greatest curvature. The two meet at `2/eta` and training stays there —
sharpness hovering at or just above the threshold, loss non-monotone over
short timescales and steadily falling over long ones.

The direction of causation is the part worth holding. The step size is not
chosen to suit the curvature; the curvature arrives at whatever the step size
will tolerate. A practitioner who halves the learning rate does not get the
same landscape traversed more carefully — they get a different, sharper
landscape, traversed at the new threshold.

## What was actually shown

Full-batch gradient descent, run at a range of step sizes across several
architectures and tasks, with the sharpness measured throughout. It could
have come out otherwise in two visible ways and did not: the sharpness could
have risen past `2/eta` and diverged, and it could have settled at a value
with no relation to `eta`. Instead the resting value tracks the hyperparameter
across the whole sweep.

The sharper test is Appendix F, which is a prediction rather than an
observation. If sharpness is something the step size *sets*, then the
classical rule that anneals `eta` to `1/sharpness` is chasing a quantity it
is itself producing, and should lose to a fixed step size that the rule calls
impermissible. It does.

## What this does not say

**It says nothing about generalization.** The paper adds a footnote
specifically to disclaim it: "sharpness" here is the top Hessian eigenvalue
and no connection to test error is asserted. The flat-minima literature uses
the same word for a quantity it does claim relates to generalization, and
importing that reading here is the failure this section exists to prevent. It
is also, exactly, the error [THEORY-013](../theory.d/THEORY-013.md) was rejected for — a claim about
optimization dynamics read as a claim about what generalizes.

**It is not about SGD.** §6 is explicit: under stochastic gradients the
sharpness does not settle at any fixed value, let alone one computable from
the hyperparameters. Large steps and small batches steer it lower, which is
a weaker and older statement. Everything the record recommends is trained
stochastically, so this account sits one step away from every practice it
neighbours — and five years on, [THEORY-030](../theory.d/THEORY-030.md) still names that step as the
open one.

**It does not explain progressive sharpening.** Why curvature rises at all is
reported, not accounted for. Half the equilibrium is a mechanism and half is
an observation.

## Which sharpness: the account in other geometries

*(Added at v2.)* Islamov et al., [LIT-tmp87rqx](../literature.d/LIT-tmp87rqx.md) — read as [NOTE-tmpf0zmh](../notes.d/NOTE-tmpf0zmh.md), and
with Cohen among the authors — run the same test on steepest descent under
other norms: Spectral GD (the update underneath Muon), ℓ∞-descent, block
coordinate descent, and the normalized forms SignGD and normalized Spectral
GD. The two forces and the one equilibrium reappear in every case, full-batch,
on small networks. But the curvature that rises to `2/eta` and stays is
`max_{‖d‖=1} dᵀ∇²L d` **in the norm the update is steepest in**, and on
ResNet20 and VGG11 under Spectral GD and ℓ∞-descent the ordinary top Hessian
eigenvalue stays well below `2/eta` throughout.

So "the maximum eigenvalue of the training-loss Hessian" above is the
Euclidean case of the account, not the account. For the spectral update the
record recommends, the step size sets the curvature in the spectral geometry,
and a reader who checked the Euclidean eigenvalue would conclude, wrongly,
that the run is not at the edge.

What this does not add: it is still full-batch, so the stochastic gap above
is untouched; the non-Euclidean sharpness is a heuristic lower estimate of an
NP-hard maximum; and its identity — the loss falls on a step iff the
curvature along that step is at most `2/eta` — does not explain progressive
sharpening either, since it constrains the curvature *along the step* once
the loss oscillates rather than saying why the Hessian's curvature rises.

## Why `Active` on small-scale evidence

Because the claim is about a regime, not about a number, and the regime was
tested where it could have failed: across architectures, tasks and a sweep of
step sizes, with a prediction derived from it and confirmed. It has been
built on since — [LIT-453](../literature.d/LIT-453.md) turns the oscillation into a quantitative
model of the averaged trajectory, and [LIT-tmp87rqx](../literature.d/LIT-tmp87rqx.md) carries it to
non-Euclidean optimizers — and nothing in the record contests it.
What is *not* established, and is marked above rather than smoothed over, is
that any of it survives the move to stochastic gradients.
