---
status: Proposed
promote_when: >-
  A second group reporting the ordering swap on a pretrained diffusion model,
  with the objective **and** a feasibility or execution measure both reported
  — the two-number comparison is the point, since the standard method's
  advantage on the objective alone is what this argues is misleading. A
  learned-denoiser setting would be worth more than a synthetic one. What
  would not move it: a paper proposing a new guidance scheme that beats PDG
  on a task score; guidance schemes are numerous and the content here is the
  ordering and what it costs on the geometry.
consensus: unreplicated
consensus_note: >-
  One group, one paper. The ingredients — Tweedie's identity, DDIM,
  projected gradient — are all standard, so the assembly is what is new and
  nobody has re-run it. The strongest experiments are in the appendix and the
  benchmark most likely to be cited, D4RL, is the weakest arm.
title: 'Apply the objective gradient before the denoiser, not after it, when guiding diffusion toward a task objective'
version: 1
tags:
- generative-modeling
date: '2026-09-21'
source:
- LIT-tmpzcf35
introduced_by:
- LIT-tmpzcf35
implementations: []
explained_by:
- THEORY-tmphpdiq
summary: >-
  Zhang et al. (2026), [LIT-tmpzcf35](../literature.d/LIT-tmpzcf35.md) — the usual recipe adds `−η∇f`
  after the denoising step, which walks the sample off the geometry the model
  learned with nothing left to pull it back. Apply the gradient to the noisy
  iterate first and let the denoiser follow: it acts as an approximate
  projection, and the sampler becomes an inexact projected-gradient method.
  Same cost, one line, and in trajectory planning it is the difference
  between a plan that looks good and one that survives execution.
---

<!-- inactive-ok-file: THEORY-tmphpdiq — Proposed, filed in this same
     contribution, and the sentence citing it says so and says the practice
     does not rest on it: the empirical failure of the other ordering is
     direct, the proofs are the account of why -->

# SOTA-tmprcn0m: Apply the objective gradient before the denoiser, not after it, when guiding diffusion toward a task objective

## Source

Zhang, Zhang, Zardini, Amin and Ozdaglar (2026), [LIT-tmpzcf35](../literature.d/LIT-tmpzcf35.md) —
[ARXIV-2608.29507](https://arxiv.org/abs/2608.29507) — read as [NOTE-tmpyuelo](../notes.d/NOTE-tmpyuelo.md).

## What to do

At each reverse step you have a noisy iterate, a pretrained denoiser, and a
differentiable objective. The standard implementation denoises, then adds the
gradient correction outside. **Reverse that:** apply `−η∇f` to the noisy
iterate, then call the denoiser on the result, then take the usual DDIM step.

One gradient evaluation, one denoiser call, one trajectory. No score
Jacobians, no fine-tuning, no auxiliary model, no repeated batch generation —
which is what the nearest optimization-oriented alternatives require.

## Why the order is not a detail

If the data lie on a structured feasible set — a manifold, a convex region, a
family of dynamically admissible trajectories — the objective gradient need
not point along it. Added **after** denoising, the gradient is the last thing
that happens: you end the step off the geometry, and nothing corrects it.
Added **before**, the denoiser is the correction, because it maps noisy
points back toward the data support.

[THEORY-tmphpdiq](../theory.d/THEORY-tmphpdiq.md) is the account — the Stein denoiser as an approximate
projection — and with it the reverse process is an inexact projected-gradient
method with finite-time guarantees on linear subspaces, compact convex sets
and compact Riemannian submanifolds. It is `Proposed`, and the practice does
not depend on the proofs: the empirical failure of the other ordering is
direct.

## What it buys, and where the evidence actually is

**The trajectory-planning experiments are the informative ones, and the
result is about measurement as much as optimization.** In double-integrator
and unicycle reference tracking, the standard ordering produces plans that
track the reference closely — and **much of that advantage disappears once
the controls are rolled out through the true dynamics**. The plans were not
dynamically consistent; they were fitted to the reference. With the gradient
inside the denoiser, planned and executed trajectories nearly coincide, and
it reports the lowest rollout cost and dynamic-feasibility error among guided
methods on both random references.

So the honest statement of the benefit is not "better objective values". It
is that the standard ordering **optimizes the plan and this one optimizes
something you can act on** — and a practitioner comparing the two on planned
cost alone would pick the wrong one.

## Conditions

**The guarantees describe an idealization.** The proofs assume an *exact*
Stein posterior-mean denoiser and that the learned support faithfully
represents the feasible set. What you run is a trained network approximating
that denoiser, on a model whose support may include infeasible regions. The
authors name misspecification as future work, and that gap is the whole
distance between the theorem and the deployment.

**The setting is narrow.** Deterministic DDIM, variance-exploding diffusion,
an exponentially decaying noise schedule. Other samplers and schedules
"require tracking their time-varying relaxation and denoising errors" — the
theory does not transfer as written, though the ordering argument is cheap
enough to test wherever you are.

**The reinforcement-learning result is the weakest arm and the most citable
one.** On Hopper, Walker and HalfCheetah (medium-v2) under a Diffuser-style
pipeline, this achieves **"slightly higher"** normalized returns — the
authors' own word — against one baseline on three tasks, with guidance scale
tuned separately per method. D4RL numbers travel further than a unicycle
study; here the unicycle study is the better evidence.

**It is not free of the tuning problem.** A guidance stepsize still has to be
chosen, and the comparison tunes it separately for each method, which is
correct practice and means the reported gap is between two tuned systems
rather than a drop-in improvement.

**Your feasible set is whatever the training data said it was.** Projection
onto the learned support is a feasibility guarantee only insofar as the
training trajectories were themselves feasible.
