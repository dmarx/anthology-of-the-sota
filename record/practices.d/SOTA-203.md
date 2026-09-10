---
number: 203
status: Active
formerly:
- SOTA-tmp2a5h0
consensus: universal
consensus_note: >-
  Every production diffusion pipeline ships a solver of this family as its
  default, and the successor DPM-Solver++ is what the names in the tooling
  refer to. The record holds no paper arguing for first-order sampling on
  quality grounds after 2022.
title: 'Sample a diffusion model with a higher-order ODE solver on the weights you already trained'
version: 1
tags:
- generative-modeling
date: '2026-09-10'
published: '2022-06-01'
source:
- LIT-076
- LIT-038
implementations:
- Stable Diffusion
- diffusers
summary: >-
  Lu et al. (2022), [LIT-076](../literature.d/LIT-076.md) — the diffusion ODE is semi-linear, so
  solve the linear part exactly and approximate only the neural integral.
  10-20 function evaluations, no retraining. Rests on [LIT-038](../literature.d/LIT-038.md), which
  established that the sampler is not fixed by the training objective.
---

# SOTA-203: Sample a diffusion model with a higher-order ODE solver on the weights you already trained

## Source

Lu et al. (2022), [LIT-076](../literature.d/LIT-076.md) — DPM-Solver, which supplies the solver; and
Song et al. (2020), [LIT-038](../literature.d/LIT-038.md) — DDIM, which supplies the permission to
change the sampler at all.

## Why this is available

The enabling fact is not about solvers. [LIT-038](../literature.d/LIT-038.md) derived a family of
non-Markovian forward processes that **share DDPM's training objective**, so the
generative process is a choice made *after* training rather than a consequence
of it. Sampling is therefore a separate design problem, attackable on weights
somebody else trained.

That separation is what the record was already relying on without holding it.
[SOTA-188](SOTA-188.md)'s source treats sampler improvements transferring to a pretrained
network — ImageNet-64 from FID 2.07 to 1.55, no retraining — as its evidence
for the design-space framing. That transfer is available because of [LIT-038](../literature.d/LIT-038.md).

## The claim

The diffusion ODE is **semi-linear**: an analytically solvable linear term plus
an integral of the neural network. A general-purpose solver approximates both.
Solving the linear part exactly and approximating only the neural integral is
what buys the step count.

- **10-20 NFE**, training-free: 4.70 FID at 10 NFE and 2.87 at 20 on CIFAR-10.
- **4-16x faster** than the previous best training-free samplers.
- Beats Runge-Kutta of comparable order, which is the direct test of the
  argument rather than a benchmark win.
- **DDIM is exactly DPM-Solver-1.** The widely used sampler is the
  *first-order* case — the least accurate member of the family. This is the
  reason to state the practice as "higher-order" rather than as a product name.

## Conditions

- Works on continuous- and discrete-time pretrained models, under linear and
  cosine noise schedules. Discrete-time models accepting continuous time inputs
  is a **stated hypothesis** that works empirically; the explanation offered is
  a guess.
- The exact solution does not depend on the noise schedule *between* endpoints
  (Proposition 3.1). A schedule choice is choosing where the approximation
  error lands, not which solution you converge to — which is a sharper reading
  of EDM's tuned `rho` than EDM offers.
- Quality at 10 NFE is comparable, not equal, to a long run. Where fidelity
  matters more than latency, spend the steps.

## What this does not cover

Distillation and few-step *training* are a different route to the same goal and
are not compared here: this practice costs a solver, that one costs a run.
[LIT-067](../literature.d/LIT-067.md) and [LIT-093](../literature.d/LIT-093.md) are the record's holdings on the other route.

## Known implementations

- Default or selectable sampler in essentially every diffusion serving stack.
