---
status: Proposed
consensus: unreplicated
consensus_note: >-
  One group. Other learned-forward-process methods exist (NDM, DiffEnc), but
  they use different mechanisms and nobody has re-run this one. Its margin at
  equal steps is small (0.05 bits/dim on CIFAR-10, 0.01 on ImageNet-32). Its
  step saving is large. Read as of 2026-09.
promote_when: >-
  A second group reproduces a gain in the variational bound over a scalar
  learned schedule at matched architecture and steps, or MuLAN's advantage
  survives above 32×32. The headline 2.55, an importance-weighted ODE
  likelihood, is not the number to reproduce. The comparison is VLB against
  VLB. Another model shipping a learned schedule does not count.
title: 'When the target is likelihood, learn a per-dimension noise schedule conditioned on a learned latent; a scalar or unconditioned one buys nothing'
version: 1
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
source:
- LIT-tmp1jb6n
introduced_by:
- LIT-tmp1jb6n
compared_against:
- SOTA-264
implementations:
- 'MuLAN (github.com/s-sahoo/MuLAN)'
summary: >-
  Sahoo et al. (NeurIPS 2024), [LIT-tmp1jb6n](../literature.d/LIT-tmp1jb6n.md). For density estimation with a
  pixel-space diffusion model, replace the scalar learned schedule with a
  per-dimension one conditioned on a small discrete latent that an encoder
  infers from the image. Keep the endpoints fixed. VDM's bound is reached in
  5× fewer steps on CIFAR-10 and improved at equal steps. Each component
  alone does nothing: a scalar input-conditioned schedule and a time-only
  multivariate schedule both match VDM.
---

<!-- inactive-ok-file: SOTA-264 — Proposed; named as the rival for the same objective
     in the other regime, which is what the comparison says about it -->

# SOTA-tmp61nli: When the target is likelihood, learn a per-dimension noise schedule conditioned on a learned latent; a scalar or unconditioned one buys nothing

## Source

Sahoo, Gokaslan, De Sa and Kuleshov (2023; NeurIPS 2024), [LIT-tmp1jb6n](../literature.d/LIT-tmp1jb6n.md).

## What to do

If the model is trained for likelihood (density estimation, compression),
use a **multivariate** noise schedule: a monotone polynomial in `t` for each
dimension, with endpoints fixed at the usual values. **Condition it on an
auxiliary latent** `z` inferred by an encoder from the clean input. The same
`z` conditions the denoiser, and at generation time `z` is drawn from a
learned prior. The bound gains a KL term for `z`.

Do not expect either half alone to help:

- A scalar schedule conditioned on the input "doesn't offer any advantage over
  the scalar schedule used in VDM".
- A multivariate schedule conditioned only on time "becomes comparable to that
  of VDM".
- Conditioning directly on the image or on class labels does worse than VDM.

## Why

For a scalar schedule the bound depends on the schedule only through its
endpoints ([THEORY-027](../theory.d/THEORY-027.md)). The one free degree of freedom is
then shape, and shape cannot move the bound. A per-dimension schedule turns
the bound into a line integral along a path in SNR-space, with many paths
between the same endpoints, so the schedule has something to optimize. That
this path-dependence holds in general is argued in the source and not proved.
What is measured is that the latent-conditioned version moves the bound.

## Evidence

At equal steps and architecture: 2.65 → **2.60** bits/dim on CIFAR-10 (10M
steps), and 3.72 → **3.71** on ImageNet-32 (2M). The same 2.65 comes in 2M
steps rather than 10M on CIFAR-10, and 1M rather than 2M on ImageNet-32.
Moving a trained MuLAN denoiser back onto a scalar schedule returns exactly
VDM's 2.65, which ties the gain to the schedule rather than the denoiser.

## Conditions

**Likelihood only, 32×32 only, VDM's U-Net only.** The source is explicit
that sample quality is not its aim. Its FID is mixed, and worse on
ImageNet-32 at 1M steps.

**The equal-step gain is small.** Most of the value is in steps to a given
bound, which matters to anyone whose budget is the constraint.

**It competes with [SOTA-264](SOTA-264.md) for the same objective.** [SOTA-264](SOTA-264.md)
takes the scalar setting and spends the shape on the loss estimator's
variance. This practice leaves the scalar setting and spends a multivariate
shape on the bound. MuLAN measured against VDM's learned scalar schedule,
which is [SOTA-264](SOTA-264.md)'s source setting. Choose by whether the added encoder, KL
term and roughly 10% of extra parameters are worth it for your target.

## Known implementations

- MuLAN, the source's code.
