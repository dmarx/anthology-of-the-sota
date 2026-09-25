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
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Bounds a recommendation that was `universal` and silent about the regime it
    fails in. LIT-676 measures the fast solvers under classifier guidance at
    scale 8.0: at 10 function evaluations FID is 13.04 for first-order DDIM,
    114.62 for DPM-Solver-2 and 164.74 for DPM-Solver-3. Higher order is
    monotonically worse, so this document's own framing — DDIM as "the
    *first-order* case, the least accurate member of the family" — inverts in the
    regime its implementations line describes, since guidance is on by default in
    every serving stack. The recommendation stands for unguided sampling and the
    guided case is now SOTA-410. Status and consensus unchanged: the claim
    was never wrong, its scope was never written.
tags:
- generative-modeling
date: '2026-09-10'
source:
- LIT-076
- LIT-038
- LIT-676
introduced_by:
- LIT-076
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

<!-- inactive-ok-file: THEORY-104 — Proposed, and cited as the account of why this practice's recommendation inverts under guidance.
     The bound on the practice rests on the measured table, not on the account being settled. -->

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
  *first-order* case — the least accurate member of the family **without
  guidance**. This is the reason to state the practice as "higher-order" rather
  than as a product name, and the qualifier is load-bearing: under guidance the
  ordering reverses and DDIM becomes the *most* accurate of them at a small
  budget. See the condition below.

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

## The condition this practice was missing: guidance

Everything above is measured **without** guidance. Guided sampling at a large
scale is how conditional models are actually run — 7.5 is the recommended setting
for Stable Diffusion — and there the recommendation inverts. [LIT-676](../literature.d/LIT-676.md),
ImageNet 256×256 at classifier guidance 8.0, FID:

| sampler | 10 NFE | 15 | 20 | 25 |
| --- | --- | --- | --- | --- |
| DDIM — order 1 | **13.04** | 11.27 | 10.21 | 9.87 |
| DPM-Solver-2 | 114.62 | 44.05 | 20.33 | 9.84 |
| DPM-Solver-3 | 164.74 | 91.59 | 64.11 | 29.40 |

Monotone in the wrong direction, and two other solver families fail the same way.
[THEORY-104](../theory.d/THEORY-104.md) is the account: guidance amplifies the model's derivatives, a
`k`-th order method is built from `k`-th order derivatives, and the convergence
radius narrows fastest for the largest `k`.

So this practice applies to **unguided sampling**, and [SOTA-410](SOTA-410.md) is the
guided case — second order, multistep, on the data prediction. The two are one
recommendation split by regime rather than rivals.

**Why the gap survived here.** This document's `implementations` line reads
"default or selectable sampler in essentially every diffusion serving stack",
which is precisely where guidance is on by default. A practice can name its
deployment setting and still not have checked the setting's own defaults.

## What this does not cover

Distillation and few-step *training* are a different route to the same goal and
are not compared here: this practice costs a solver, that one costs a run.
[LIT-067](../literature.d/LIT-067.md) and [LIT-093](../literature.d/LIT-093.md) are the record's holdings on the other route.

## Known implementations

- Default or selectable sampler in essentially every diffusion serving stack.
