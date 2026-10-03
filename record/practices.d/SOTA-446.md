---
number: 446
status: Proposed
formerly:
- SOTA-tmplxigi
promote_when: >-
  A group outside OpenAI's consistency line trains the same self-bootstrapped
  few-step model twice, with the target taken from the current weights under
  stop-gradient and from an EMA of them, everything else held, at 64 px or
  above, and reports one- and two-step FID for both. Shortcut Models' own
  choice of EMA targets is the natural test case. A further paper that just
  uses stop-gradient targets does not count. That is adoption, and there is
  already plenty of it.
consensus: unreplicated
consensus_note: >-
  One measurement, from one group: iCT (LIT-786), which proves the
  EMA-teacher objective uninformative on a point mass and shows the
  improvement as one CIFAR-10 curve per arm. Adoption is wide. sCM
  (LIT-790) from the same line, MeanFlow (LIT-784), Inductive Moment
  Matching (LIT-775) and rCM (LIT-783) all take the target from the
  current weights under stop-gradient, and none ablates it. Shortcut Models
  (LIT-787) goes the other way and takes its bootstrap targets from EMA
  weights, also without a table. Unreplicated rather than emerging because
  the adopters ran no comparison. Read as of 2026-10.
title: 'In consistency training, take the target from the current weights under stop-gradient, not from an EMA teacher'
version: 1
tags:
- generative-modeling
- few-step-generation
- model-stability
date: '2026-10-03'
source:
- LIT-786
introduced_by:
- LIT-786
implementations:
- 'iCT'
- 'sCM'
- 'MeanFlow'
- 'Inductive Moment Matching'
- 'rCM'
summary: >-
  Song and Dhariwal (2023), [LIT-786](../literature.d/LIT-786.md), §3.2. Consistency Models trained
  the student against an EMA of itself. iCT shows that on a point-mass data
  distribution the limiting objective with any teacher other than the
  student carries no information about the data (Prop. 1), and that setting
  the teacher's EMA rate to zero improves CIFAR-10 FID with both LPIPS and
  squared L2 (Fig. 2a, curves). Keep an EMA of the weights for evaluation.
  Do not use it for the target.
explained_by:
- THEORY-124
---

<!-- inactive-ok-file: SOTA-443 — Proposed, filed in the same contribution; named as one of iCT's other stabilizing changes, not as settled advice -->
<!-- inactive-ok-file: THEORY-124 — Proposed, and the account declared in `explained_by:`; cited for its untested prediction about Shortcut Models, as the test that would settle a condition -->

# SOTA-446: In consistency training, take the target from the current weights under stop-gradient, not from an EMA teacher

## Source

Song and Dhariwal (2023), [LIT-786](../literature.d/LIT-786.md) — iCT, §3.2, Prop. 1, App. A and
Fig. 2a.

## What to do

In consistency training, the loss compares the model at one noise level with
a "teacher" evaluated at the adjacent, lower one. Build that teacher from the
**current** weights with the gradient stopped (θ⁻ = stopgrad(θ)), not from an
exponential moving average of past weights.

Keep an EMA of the weights for sampling and evaluation, as iCT does. The
recommendation is about where the target comes from, not about whether to
keep an EMA at all.

The same holds for the objectives built on the same self-bootstrapped
target: continuous-time consistency, MeanFlow's average velocity, Inductive
Moment Matching. All of them already use the current weights.

## Evidence

**The argument** ([LIT-786](../literature.d/LIT-786.md), §3.2, App. A). Consistency Models
([LIT-093](../literature.d/LIT-093.md)) justified an EMA teacher with an asymptotic argument: as the step
count N grows, the consistency-training loss approaches the
consistency-model loss. iCT takes a data distribution that is a single point
and computes that limit. With θ⁻ ≠ θ the limiting objective does not depend
on the data at all (Eq. 6), so minimizing it cannot learn the consistency
function. With θ⁻ = θ, the gradient scaled by 1/Δσ converges to a regression
onto the data point (Eq. 7). The paper says this refutes the EMA argument
and is consistent with Consistency Models' second argument, which already
needed θ⁻ = θ.

**The measurement** ([LIT-786](../literature.d/LIT-786.md), Fig. 2a). On CIFAR-10, with the paper's
other fixes, a teacher EMA rate of zero "notably improves sample quality"
with both LPIPS and squared L2. It also cancels a degradation that iCT's
other changes caused under LPIPS. It is one curve per arm, at batch 512, with
no tabled values.

Together these took consistency training's ImageNet-64 one-step FID from
Consistency Models' 13.0 to iCT-deep's 3.25. That comes from all of iCT's
changes at once, and the paper does not separate this one at ImageNet scale.

## Conditions

- **The proof is a counterexample, not a general result.** It shows the
  EMA argument fails on a point mass. That zero EMA is better on real data
  rests on one CIFAR-10 figure.
- **Training, not distillation.** iCT says the teacher's EMA rate "should
  always be zero for CT, although it can be nonzero for CD" (§3.2). With a
  pretrained diffusion model supplying the ODE step, the argument does not
  apply. sCM ([LIT-790](../literature.d/LIT-790.md)) uses stop-gradient targets for its distillation
  too, but it does not compare against an EMA target in either setting.
- **Shortcut Models chose the opposite, for a stated reason.** Shortcut
  Models ([LIT-787](../literature.d/LIT-787.md), §3.1) builds the target for a step of 2d from two of
  the model's own d-steps, and takes those from EMA weights. The authors
  report that variance in the flow-matching term causes large oscillations
  at d = 1 and that EMA targets damp them. That is a step-size-conditioned
  flow, not consistency training, and neither choice has an ablation table
  behind it. [THEORY-124](../theory.d/THEORY-124.md) predicts why Shortcut can tolerate EMA
  targets: three quarters of each of its batches (k = 1/4, §3.1) is a
  plain flow-matching regression that carries the data at full strength,
  so a lagging bootstrap target only slows how that signal reaches larger
  steps. In consistency training the data enter only through the gap
  between adjacent noise levels, which a lagging target swamps. That
  prediction is the test that would settle this condition: ablate EMA
  against current-weight targets in both a shortcut model and consistency
  training, in one codebase. If the EMA rate matters much less for the
  shortcut model, Shortcut's choice is no counterexample to this practice;
  if it matters as much, the practice's reach to consistency training alone
  is the open question.
- **Stability comes from elsewhere.** Without an EMA teacher, iCT relies on
  its other changes to train stably: the step-count curriculum, the loss
  weighting, and Pseudo-Huber ([SOTA-443](SOTA-443.md)). Shortcut Models puts its
  stability on weight decay as well as EMA targets. Dropping the EMA alone,
  in a recipe that leaned on it, has not been tested.

## Known implementations

- iCT; sCM and rCM (continuous time); MeanFlow; Inductive Moment Matching,
  whose stop-gradient weights are the previous optimizer step's.
