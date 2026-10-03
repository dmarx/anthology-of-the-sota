---
status: Active
promote_when: >-
  Active for the identifications, each of which is a line or two of algebra
  from the source papers' own definitions. What the account does not settle,
  and holds no position on, is which identity makes the best estimator. One
  controlled comparison exists, Lagrangian against Eulerian distillation on
  CIFAR-10 with small models. It would be extended by a run that trains the
  semigroup, Eulerian and Lagrangian forms from one teacher, or from
  scratch, in one codebase at 256 px or above, at matched budget, and reports
  FID at one, two, four and eight steps for each. Rows copied between
  papers, which is what every current cross-method table holds, would not.
title: "Consistency, shortcut, MeanFlow and progressive-distillation models all estimate the two-time flow map of the probability-flow ODE, and differ in which identity of that map they train on"
version: 1
tags:
- generative-modeling
- few-step-generation
- flows-and-transport
date: '2026-10-03'
source:
- LIT-tmpuz24v
- LIT-tmpkkjv3
- LIT-tmpo7np5
- LIT-093
- LIT-tmpkegvh
explains:
- SOTA-206
summary: >-
  Boffi, Albergo and Vanden-Eijnden (2024), [LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md). The object a
  few-step model learns is X_{s,t}, which carries any point of the ODE from
  time s to time t. It satisfies three identities: a Lagrangian equation in
  the end time, an Eulerian equation in the start time, and composition.
  Progressive distillation and shortcut models train on composition,
  consistency models and MeanFlow on the Eulerian equation, and flow map
  matching's Lagrangian loss on the first. Consistency models are the
  one-time case. Inductive Moment Matching is the exception: it matches
  marginals, and its minimizer need not be the ODE's map. Which identity
  trains best is measured once, on CIFAR-10, where the Lagrangian form won
  by a wide margin.
---

<!-- inactive-ok-file: SOTA-tmpqagel — Proposed; named to say this account does not explain its ranking of MeanFlow over the other from-scratch objectives -->
<!-- inactive-ok-file: THEORY-tmpsem9v — Proposed, filed in the same contribution; named for what it says about the stop-gradient form of the Eulerian identity -->

# THEORY-tmpjf41h: Consistency, shortcut, MeanFlow and progressive-distillation models all estimate the two-time flow map of the probability-flow ODE, and differ in which identity of that map they train on

## Source

Boffi, Albergo and Vanden-Eijnden (2024), [LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md), §3.2–3.7 and
App. C. Geng, Deng, Bai, Kolter and He (2025), [LIT-tmpkkjv3](../literature.d/LIT-tmpkkjv3.md), §4.1,
Eqs. 3–6. Frans, Hafner, Levine and Abbeel (2024), [LIT-tmpo7np5](../literature.d/LIT-tmpo7np5.md), §3,
Eqs. 3–4. Song, Dhariwal, Chen and Sutskever (2023), [LIT-093](../literature.d/LIT-093.md). Zheng et al.
(2025), [LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md), App. F.1.

## The account

**One object.** Write X_{s,t}(x) for the point the probability-flow ODE
reaches at time t from x at time s. Flow map matching ([LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md))
proves it is the unique solution of two equations (Props. 3.5–3.6). In the
end time it is Lagrangian: ∂_t X_{s,t}(x) = b_t(X_{s,t}(x)), with b the
velocity. In the start time it is Eulerian: ∂_s X_{s,t} + b_s·∇X_{s,t} = 0,
so the output does not change as the start point slides along its own
trajectory. And it composes: X_{t,τ}∘X_{s,t} = X_{s,τ}, "the consistency
property, here stated over two times". A sample in n steps is n
applications of the map over a partition of the interval. At the true map
every partition gives the same endpoint.

**Each named method trains one of these identities.**

| Method | What the network outputs | Identity trained on |
|---|---|---|
| Progressive distillation | one step of the new sampler | composition, against two steps of the previous one ([LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md), App. C.4, Eq. C.23) |
| Shortcut models | s(x, t, d), with x + d·s = X_{t,t+d}(x) | composition at binary steps, s(x, t, 2d) = ½s(x, t, d) + ½s(x′, t+d, d) ([LIT-tmpo7np5](../literature.d/LIT-tmpo7np5.md), Eqs. 3–4), with the velocity as the d = 0 base case |
| Consistency models | the one-time map X_{t,0} | Eulerian; consistency distillation is its discretization, and its continuous-time limit is the Eulerian loss ([LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md), App. C.2, Eqs. C.12, C.18) |
| MeanFlow | the average velocity u(z, r, t) | Eulerian, written for the displacement |
| Flow map matching, Lagrangian | the two-time map | Lagrangian, against the teacher's velocity (§3.3) |

**MeanFlow in these terms.** MeanFlow ([LIT-tmpkkjv3](../literature.d/LIT-tmpkkjv3.md)) defines u(z_t, r, t)
as the displacement from t to r divided by t − r (Eq. 3). Its own text
says that, in flow map matching's language, "the Flow Map corresponds to
displacement". So X_{t,r}(z_t) = z_t − (t − r)·u(z_t, r, t). Differentiate
that along the trajectory in t, with r held fixed. It vanishes exactly
when u = v − (t − r)·du/dt, which is the MeanFlow identity. The identity is
the Eulerian equation for the map from t to r. This is the record's algebra
on the paper's definitions, and rCM ([LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md), App. F.1) reaches the
same place from the other side: adding a second time to continuous-time
consistency gives a continuous-time consistency trajectory model, "which
MeanFlow is under the rectified-flow schedule". MeanFlow's additivity
remark, that one step over [r, t] equals two over [r, s] and [s, t], is
composition, holding automatically for the true field.

**Consistency models are the one-time case.** A consistency model
([LIT-093](../literature.d/LIT-093.md)) maps every point of a trajectory to its data end, X_{t,0} only.
Flow map matching places it as that special case (App. C.2). That is why
its multistep sampling has to re-noise and denoise again rather than stop
at an intermediate time. [LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md)'s §2 overstates this as consistency
models "do not benefit from multistep sampling". [LIT-093](../literature.d/LIT-093.md) and its successors
report that they do, by re-noising.

## What it explains

**[SOTA-206](../practices.d/SOTA-206.md)'s dial.** The practice says to keep a multi-step option in a
few-step model, and its evidence is one set of weights sampled at several
step counts. On this account the dial is not a feature added to some
models. It is what a two-time map is. Composition makes every partition of
[0, 1] reach the same endpoint at the optimum, so the step count is chosen
at sampling time, and a learned map's error is what makes more steps
help. Shortcut models ([LIT-tmpo7np5](../literature.d/LIT-tmpo7np5.md)) show it most plainly: the step size is
an input, the network is trained so that one step of 2d equals two of d,
and one set of weights scores 6.9, 13.8 and 20.5 FID at 128, 4 and 1 steps
on CelebA-HQ (Table 1). Inductive Moment Matching and MeanFlow also
condition on two times and expose the dial directly. Consistency models, with one time,
keep it only through re-noising. Progressive distillation trains the map at
a single step size per stage and keeps no dial, which is the counter-case
in [SOTA-206](../practices.d/SOTA-206.md)'s Conditions.

## What was measured

- **The identities are not interchangeable as losses.** With a 5.53-FID
  teacher on CIFAR-10, the Lagrangian loss distils to 7.13 FID at two steps
  and 6.04 at four. The Eulerian loss reaches 48.32 and 44.35
  ([LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md), Table 1). The authors attribute the gap to the Eulerian
  loss's spatial Jacobian of a nearly singular map (§3.4). The record's
  view: small models, one dataset, one run each.
- **The second time is what does the work in MeanFlow.** With r = t on
  every sample the objective is flow matching, and one-step FID is 328.91.
  With r ≠ t on 25% of samples it is 61.06 ([LIT-tmpkkjv3](../literature.d/LIT-tmpkkjv3.md), Table 1a).

## What it does not say

- **Not which estimator wins.** [SOTA-tmpqagel](../practices.d/SOTA-tmpqagel.md) ranks MeanFlow above
  consistency training and shortcut models from scratch, on rows copied
  between papers at different budgets. This account says the three aim at
  the same object, so their differences are differences of estimator:
  identity, discretization, weighting and budget. It does not say which,
  and it does not explain that ranking. rCM's one figure has the MeanFlow
  form distilling a large model worse than plain continuous-time
  consistency ([LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md), App. F.1).
- **Not that the training dynamics agree.** The Eulerian form is trained
  with a stop-gradient on the target. Flow map matching shows the flow map is
  then a critical point of the update, not the minimizer of a loss
  (Prop. 3.12). [THEORY-tmpsem9v](THEORY-tmpsem9v.md) is about what follows from that.
- **Not Inductive Moment Matching.** IMM ([LIT-tmp7ppws](../literature.d/LIT-tmp7ppws.md)) also learns a
  two-time sampler from scratch, but matches the *distributions* reached
  from t and from a nearby r. Its own §3.1 notes that the minimizer "is not
  unique and, under mild assumptions, a deterministic minimizer exists". So
  it learns a marginal-preserving map, which need not be the ODE's flow map.
  Consistency models are its one-particle case (Lemma 1), and there the
  two accounts meet.
- **Not distribution-matching distillers.** DMD and its successors train a
  one-step generator on a divergence to the teacher's marginals, with no
  identity of the ODE's map in the loss. Their one-step generator need not
  be X_{1,0}.
