---
number: 27
status: Active
formerly:
- THEORY-tmp962qd
title: 'In continuous time the diffusion bound depends on the noise schedule only through its endpoints'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Scoped to scalar schedules. LIT-677 (MuLAN) shows the invariance
    follows because a scalar schedule confines the bound's path in SNR-space
    to one line. Its own scalar ablation and schedule-swap test reproduce
    this document's result exactly (2.65 bits/dim either way). A per-dimension
    schedule conditioned on a learned latent moves the bound (2.65 → 2.60 at
    equal steps). The account is unchanged within its scope, and it stays
    Active.
tags:
- generative-modeling
date: '2026-09-20'
source:
- LIT-446
- LIT-677
explains:
- SOTA-188
- SOTA-264
summary: >-
  Kingma et al. (2021), [LIT-446](../literature.d/LIT-446.md) — integrate the diffusion
  variational bound over signal-to-noise ratio instead of over time and the
  schedule leaves the integrand, remaining only in the limits. The bound and
  the generative distribution therefore depend on the schedule through two
  numbers, and variance-preserving and variance-exploding specifications are
  the same model up to a rescaling of the latents.
extended_by:
- THEORY-106
---

# THEORY-027: In continuous time the diffusion bound depends on the noise schedule only through its endpoints
<!-- inactive-ok-file: SOTA-264 — Proposed, and filed in this same contribution as the practice this account licenses; it is also named in `explains:` -->

## Source

Kingma et al. (2021), [LIT-446](../literature.d/LIT-446.md) — [ARXIV-2107.00630](https://arxiv.org/abs/2107.00630).

## What was actually shown

The diffusion variational bound is conventionally written as an integral over
time, where the noise schedule appears throughout the integrand. Because the
signal-to-noise ratio is a monotone function of time, it is invertible, and
the integral can be rewritten with SNR as the variable of integration.

After the substitution the schedule is gone from the integrand. It survives
only in the limits of integration — the SNR at `t=0` and at `t=1`. So:

- **The continuous-time bound is invariant to the schedule's shape** given
  those two endpoint values.
- **So is the generative distribution**, up to a trivial rescaling of the
  latents.
- Therefore **variance-preserving and variance-exploding specifications,
  presented in the literature as different model classes, are equivalent in
  continuous time.**

This is a derivation, not a fit, and it could have failed in an identifiable
way: if the SNR function were not monotone the substitution would be invalid,
which is the regularity condition the result is stated under.

A second result travels with it and is useful in its own right: the
discrete-time loss is an **upper Riemann sum** of the continuous-time
integral, so adding timesteps can only improve the bound — a question the
literature had been settling empirically.

## What this makes possible

A free parameter is only interesting once somebody spends it. The source
spends the freed schedule shape on minimizing the variance of the loss
estimator, which is [SOTA-264](../practices.d/SOTA-264.md). The field spent it differently — EDM
and its successors concentrate training noise where the model has something
to learn, which is [SOTA-188](../practices.d/SOTA-188.md).

**That second connection is why this document exists.** [SOTA-188](../practices.d/SOTA-188.md) tells a
reader to change where along the noise axis they train, and the obvious
objection is *have you then changed the model?* The record has carried that
practice without an answer. In continuous time the answer is no: the shape is
not part of the model, so choosing it is an optimization decision and nothing
more.

## What this does not say

**It does not say the schedule never matters.** In discrete time it does —
the loss is an approximation to the integral and the schedule determines how
good it is. Every recipe the record holds trains with finitely many steps.

**It does not say the weighting never matters.** The clean statement is about
the *unweighted* bound. The equivalence between specifications is shown to
survive a weighted loss, but under a weighting the schedule shape and the
weight function are two handles on the same thing, and what is optimized is
no longer the bound. [SOTA-188](../practices.d/SOTA-188.md)'s recommendation lives in that regime.

**"Equivalent up to a trivial rescaling" is doing work.** Two specifications
being one object under a transformation does not make two implementations
interchangeable in a codebase, or their numerics equally well-conditioned.

**It does not say how fast the discrete case approaches the continuous one.**
The Riemann argument gives monotone improvement and no rate, and the rate is
what a practitioner with a step budget needs.

**It is about scalar schedules: one SNR function shared by every dimension.**
That is the only kind [LIT-446](../literature.d/LIT-446.md) considers, and the substitution
that removes the schedule from the integrand relies on it. With a
per-dimension schedule the bound becomes a line integral along a path in
SNR-space, and many paths connect the same endpoints.
[LIT-677](../literature.d/LIT-677.md) (MuLAN) reports that such a schedule, conditioned on a
learned auxiliary latent, improves the bound at equal steps (2.65 → 2.60 on
CIFAR-10). It also re-measures this account inside its scope. A scalar
schedule conditioned on the input gives no advantage, and a trained MuLAN
denoiser moved onto a scalar or linear schedule "reduces to the same value as
that of the VDM: 2.65". That path-dependence holds in general for
multivariate schedules is argued by analogy in that paper, not proved. Its
own time-only multivariate arm matched VDM.

**It says nothing about sample quality.** The bound is a likelihood, the
source's benchmarks are density estimation, and the record's diffusion
practices are mostly about perceptual generation where likelihood is a known
poor proxy.

## Why `Active`

The core claim is a derivation from a stated and mild regularity condition,
not an empirical fit, and the record believes it. Its limits are limits of
*scope* — continuous time, unweighted bound — rather than open questions
about whether it holds.

What remains genuinely open is the bridge in the other direction: whether the
variance-minimizing schedule this licenses and the compute-allocating one
[SOTA-188](../practices.d/SOTA-188.md) recommends land in the same place. Two arguments from different
premises both conclude "spend effort in the middle of the range", and nobody
has checked whether they agree on where the middle is.
