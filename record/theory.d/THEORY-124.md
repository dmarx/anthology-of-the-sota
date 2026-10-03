---
number: 124
status: Proposed
formerly:
- THEORY-tmpsem9v
promote_when: >-
  Two results, of different kinds. First, the ablation SOTA-446 asks
  for, from a group outside OpenAI's consistency line: one self-bootstrapped
  model trained with the target from the current weights under
  stop-gradient and from an EMA of them, everything else held, at 64 px or
  above, with one- and two-step FID for both. Second, the account's own
  prediction, which nothing has tested. The EMA rate should matter in
  consistency training, where the data enter the update only through the
  gap between adjacent noise levels. It should matter much less in a shortcut
  model, where a full-strength flow-matching regression carries the data
  beside the bootstrap term. A run of both ablations in one codebase would
  test the mechanism rather than the recipe. Another paper that simply uses
  stop-gradient targets would not count.
title: "Consistency training is a bootstrapped fixed-point iteration, not descent on a loss, so a target that lags the student swamps a data signal that enters only at the order of the step"
version: 1
tags:
- generative-modeling
- few-step-generation
- model-stability
date: '2026-10-03'
source:
- LIT-786
- LIT-793
explains:
- SOTA-446
summary: >-
  Song and Dhariwal (2023), [LIT-786](../literature.d/LIT-786.md), Prop. 1, and Boffi, Albergo and
  Vanden-Eijnden (2024), [LIT-793](../literature.d/LIT-793.md), Prop. 3.12. Consistency training
  compares the model at one noise level with a target at the next, and the
  data enter only through that small step. With the target's weights equal
  to the student's under stop-gradient, the scaled update converges to a
  regression onto the data. With any other target, such as an EMA, the
  limiting objective does not depend on the data at all. Proved on a
  one-point distribution, where it refutes the argument that justified EMA
  targets. That it is why EMA targets hurt on real data rests on one
  CIFAR-10 curve.
---

<!-- inactive-ok-file: SOTA-446 — Proposed, and declared in `explains:`; the practice this account underwrites. Explaining a practice not yet in force is the normal case. -->
<!-- inactive-ok-file: THEORY-118 — Proposed, filed in the same contribution; named to draw the boundary between the two accounts of consistency-training instability -->

# THEORY-124: Consistency training is a bootstrapped fixed-point iteration, not descent on a loss, so a target that lags the student swamps a data signal that enters only at the order of the step

## Source

Song and Dhariwal (2023), [LIT-786](../literature.d/LIT-786.md), §3.2, Prop. 1 and App. A. Boffi,
Albergo and Vanden-Eijnden (2024), [LIT-793](../literature.d/LIT-793.md), §3.6, Prop. 3.12.

## The account

**It is not a loss.** Consistency training replaces the teacher's ODE step
with a one-sample estimate built from the data and the noise. Flow map
matching ([LIT-793](../literature.d/LIT-793.md), §3.6) shows that this substitution does not give a
loss with the same minimizer, because the squared term is quadratic in the
estimate (Eq. 3.21). Consistency models therefore put a stop-gradient on
the target, and the flow map is then a critical point of the update
(Prop. 3.12). The authors add that it is "challenging to guarantee" that
this critical point "is stable and attractive", since "the objective
function is not guaranteed to decrease". Training is a fixed-point
iteration on the network's own outputs, with no loss whose decrease
certifies progress.

**The data signal is of the order of the step.** The student is evaluated
at noise level σ_{i+1} and the target at the adjacent level σ_i, and what
the data contribute is the difference between them. iCT ([LIT-786](../literature.d/LIT-786.md),
§3.2) makes this concrete on a data distribution that is a single point ξ.
There the consistency-model and consistency-training objectives coincide.
With the uniform weighting and squared L2, Prop. 1 gives:

- if the target's weights θ⁻ differ from the student's θ, the limit as the
  step count grows is E[(1 − σ_min/σ_i)²(θ − θ⁻)²] (Eq. 6), which does not
  contain ξ;
- the gradient scaled by 1/Δσ converges to the gradient of a regression of θ
  onto ξ when θ⁻ = θ, and diverges to +∞ or −∞ otherwise (Eq. 7).

Read together, the data term vanishes with Δσ, and any gap between target
and student does not. An EMA target always differs from the student, so as
the discretization is refined the update is dominated by pulling the
student toward its own past. This refutes the argument Consistency Models
gave for EMA targets, that the training objective approaches the
consistency-model objective as Δσ → 0, whenever θ⁻ ≠ θ. iCT notes that the
second argument the original paper gave already required θ⁻ = θ.

## What it explains

**[SOTA-446](../practices.d/SOTA-446.md).** The practice says to take the consistency-training
target from the current weights under stop-gradient and keep the EMA only
for evaluation. This account is why. A lagging target adds a term that does
not shrink with the step, in an update whose data signal does. It also says
why iCT allows a nonzero EMA rate for consistency *distillation* (§3.2).
There a pretrained model supplies the ODE step, and the target carries
the teacher's information at full strength rather than through a vanishing
difference.

## What was measured

On CIFAR-10, with iCT's other changes in place, setting the target's EMA
rate to zero "notably improves sample quality" with both LPIPS and squared
L2 ([LIT-786](../literature.d/LIT-786.md), Fig. 2a). It is one curve per arm, with no tabled values.
Together with iCT's other changes it took ImageNet-64 one-step consistency
training from 13.0 to 3.25 FID, and the paper does not separate this change
at that scale.

## What this does not say

- **Not that real-data training fails with an EMA target.** The
  proposition is a counterexample on a point mass. Consistency Models
  trained with EMA targets and produced working models. The account says
  their objective lacked the justification it was given, and predicts a
  bias that grows as the step shrinks. The size of that bias on real data
  is not measured.
- **Not that current-weight targets are stable.** The fixed point is then
  correct, but Prop. 3.12 gives no guarantee that it attracts. Consistency
  training still needed iCT's curriculum, weighting and Pseudo-Huber loss.
  Inductive Moment Matching ([LIT-775](../literature.d/LIT-775.md), Fig. 5) reports that its
  one-particle case, which is consistency training, collapses on
  ImageNet-256, and reports its own re-run of iCT as prone to collapse. IMM
  gives a different account of that fragility: one particle matches only
  the first moment.
- **Shortcut models are not a counterexample, on this account.** Shortcut
  Models ([LIT-787](../literature.d/LIT-787.md), §3.1) build bootstrap targets from EMA weights and
  report that this damps oscillation. In that objective three quarters of
  each batch is an ordinary flow-matching regression, which carries the
  data at full strength. The bootstrap term only propagates it to larger
  steps. The account predicts a lagging target costs much less there. This
  is the record's reading, and nothing tests it: neither paper ablates the
  choice in the other's setting.
- **Not about the continuous-time instability.** [THEORY-118](THEORY-118.md) is about
  why continuous-time consistency models diverge even with current-weight
  targets. That is a separate mechanism, through the time derivative.
