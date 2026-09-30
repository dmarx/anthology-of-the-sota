---
number: 265
status: Active
formerly:
- SOTA-tmpf60k7
consensus: emerging
consensus_note: >-
  One group states and demonstrates it (the stochastic-interpolants
  framework and SiT share authors), but the claim rests on an identity
  rather than on a sweep: the coefficient does not enter the velocity or the score, so
  it cannot be downstream of training. Nothing in the record contests it.
  `emerging` because no second group has reported tuning it, and because the
  measured gain is on one dataset — the framework paper itself reports no
  image metric.
title: 'Tune the stochastic sampler''s diffusion coefficient after training; it is not fixed by the forward process'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    introduced_by moved from SiT to the stochastic-interpolants framework
    (ARXIV-2303.08797), now filed: its v1 abstract already says the noise
    strength can be tuned after training, and SiT takes the result from it.
    SiT stays as a source, for the measurement. The recommendation is
    unchanged.
tags:
- generative-modeling
date: '2026-09-20'
source:
- LIT-447
- LIT-645
introduced_by:
- LIT-645
implementations:
- 'SiT-XL'
summary: >-
  Albergo, Boffi and Vanden-Eijnden (2023), LIT-645, state it and Ma
  et al. (2024), [LIT-447](../literature.d/LIT-447.md), measure it — score-based diffusion conventionally
  takes the reverse SDE's diffusion coefficient from the forward process, and
  presents the two as intrinsically tied. They are not: the coefficient
  affects neither the velocity nor the score, only the integration. So it is
  a sampler hyperparameter, tunable on a frozen model, and tuning it tightens
  the KL divergence to the target.
---

# SOTA-265: Tune the stochastic sampler's diffusion coefficient after training; it is not fixed by the forward process

## Source

Albergo, Boffi and Vanden-Eijnden (2023), [LIT-645](../literature.d/LIT-645.md) — [ARXIV-2303.08797](https://arxiv.org/abs/2303.08797).
The framework paper introduces it: one learned velocity and score give a
family of SDEs sharing the interpolant's marginals, and its v1 abstract says
the noise strength "can be tuned as model hyper-parameter after training".
Its evidence is a 2-D checkerboard and a 128-D Gaussian mixture.

Ma et al. (2024), [LIT-447](../literature.d/LIT-447.md) — [ARXIV-2401.08740](https://arxiv.org/abs/2401.08740). Shares three
authors with the framework, takes its KL bound to derive a computable
coefficient, and supplies the ImageNet measurement.

## The claim is structural before it is empirical

In score-based diffusion the reverse-time SDE's diffusion coefficient is
taken from the forward SDE that generated the training distribution, and the
literature presents this inheritance as intrinsic to the method.

It is not. The coefficient enters the integration of the reverse process and
appears in neither the velocity field nor the score — the two things training
estimates. So it is a knob on the sampler, not on the model, and it can be
chosen **after training with no retraining**, by whatever criterion you like.

That is why this is `Active` on one group's evidence: the load-bearing part
is an identity, not a sweep. The sweep confirms the identity buys something.

## What it buys

Tuning it tightens control of the KL divergence between the model
distribution and the target, and the empirical gain is a step in SiT's
transition from DiT — measured with the model frozen, at matched function
evaluations.

**The free-lunch framing is the useful one.** Most practitioners with a
trained diffusion model have an unexploited tuning dimension that costs
sampling passes rather than training runs.

## The precondition nobody states

The freedom is usable because training is in **continuous time**. Continuous
time is the step in SiT's transition whose direct gain is marginal, and this
is what it is actually for: it decouples the sampling discretization from the
training discretization, so the integration can be re-chosen after the fact.
A discrete-time model has already committed.

That makes [SOTA-266](SOTA-266.md)'s and this practice's cases interlock — a
marginal-looking choice earns its place by what it leaves open.

## Against the record's assumption about samplers

Every sampler practice the record holds treats sampling as downstream of
training: [SOTA-203](SOTA-203.md) picks a higher-order ODE solver for the weights you have,
[SOTA-207](SOTA-207.md) picks the deterministic sampler when the noise input has to mean
something. Both are about choosing among samplers given a trained model. This
says one *parameter* of the stochastic sampler was never determined by
training at all, which is a different kind of freedom than choosing a solver.

## Conditions

Measured on class-conditional ImageNet at 256×256 and 512×512, with FID as
the only quality metric. The identity generalizes; the size of the gain is
one dataset's.

The coefficient may need regularizing near an endpoint for some interpolants
— the linear and GVP interpolants carry a term that makes the SDE hard to
integrate there — so "free to choose" is free within a range that the
interpolant sets.

Requires a stochastic sampler. A deterministic ODE sampler has no diffusion
coefficient to tune, so this and [SOTA-207](SOTA-207.md) apply in different cases rather
than competing.

## Known implementations

- SiT-XL, which reports its FID with the coefficient tuned.
