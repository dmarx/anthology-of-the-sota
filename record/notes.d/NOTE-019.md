---
number: 19
status: Read
formerly:
- NOTE-tmpvjumo
paper: LIT-075
title: 'Elucidating the Design Space of Diffusion-Based Generative Models'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Re-read from the full text, which was not available at v1. Upgraded
    from `Skimmed` to `Read`: the claims table, assumptions, the
    derivation of the preconditioning coefficients and the method are
    new, and SOTA-188 is confirmed against Section 5 and Appendix B.6
    rather than left unverified.
tags:
- generative-modeling
date: '2026-09-09'
published: '2022-06-01'
summary: >-
  Pulls diffusion's tangled formulations apart into independent axes — sampler, training noise distribution, and preconditioning — and derives the preconditioning coefficients from a unit-variance requirement rather than choosing them. FID 1.79 on class-conditional CIFAR-10 at 35 network evaluations; a pretrained ImageNet-64 model improves 2.07 to 1.55 from the sampler alone.
---

# NOTE-019: Elucidating the Design Space of Diffusion-Based Generative Models

## Contribution

Not a new model. The paper argues that "the theory and practice of
diffusion-based generative models are currently unnecessarily convoluted",
and remedies that by casting the existing formulations — variance-preserving,
variance-exploding, DDIM, score-matching — into **one common framework whose
design choices are separable**. Having separated them it improves three:
the **sampler**, the **preconditioning** of the score network, and the
**distribution of training noise levels**.

The preconditioning section is the one that matters for this record: it is,
in the paper's own words, "the first principled analysis of the
preconditioning of the networks' inputs, outputs, and loss functions in a
diffusion model setting".

## Key insight

Two, and they are independent, which is itself the paper's point.

**The choices were entangled by presentation, not by necessity.** Prior
formulations bundled the noise schedule, the network parameterisation, the
loss weighting and the sampler into a single derivation, so a change to one
implied changes to the others. Written in a common notation they turn out to
be free parameters. The evidence for the framing is **modularity**: the
improved sampler works on *already-trained* networks from previous work, with
no retraining, which it could not do if the axes were genuinely coupled.

**Preconditioning is derived, not chosen.** The denoiser is written as

    D_θ(x; σ) = c_skip(σ)·x + c_out(σ)·F_θ(c_in(σ)·x; c_noise(σ))          (Eq. 7)

so that F_θ — the raw network — is a different function from D_θ, the
denoiser. The four scalings are then *solved for* rather than picked: the
paper "derive[s] our choices shown in Table 1 by requiring network inputs and
training targets to have unit variance (c_in, c_out), and amplifying errors
in F_θ as little as possible (c_skip). The formula for c_noise is chosen
empirically."

That sentence is the whole of `SOTA-188`'s first half, stated by the paper
about itself.

## Assumptions

- **σ_data is a known scalar** — the standard deviation of the data
  distribution, taken as 0.5 for the datasets used. Every coefficient below
  is a function of σ and σ_data, so the derivation assumes the data has a
  single meaningful scale.
- **The signal is x + n with n ~ N(0, σ²I)** — additive Gaussian noise at a
  known level, and x independent of n. The variance algebra in Appendix B.6
  is this and nothing more.
- **σ(t) = t, s(t) = 1** — the paper's preferred schedule, chosen so that the
  ODE's tangent points at the denoiser output. The preconditioning derivation
  does not depend on it; the sampler's step sizes do.
- Images, at 2022 scales: CIFAR-10 (32×32) and ImageNet-64. NeurIPS 2022.

## Key results

- **FID 1.79** class-conditional and **1.97** unconditional on CIFAR-10, at
  **35 network evaluations per image**.
- **ImageNet-64: 2.07 → 1.55 → 1.36.** The first step is the improved sampler
  applied to a *previously trained* network with no retraining; the second is
  retraining with the paper's preconditioning and noise distribution. Most of
  the first gain costs nothing.
- **The preconditioning coefficients, derived** (Appendix B.6):

  | coefficient | value | derived from |
  |---|---|---|
  | c_in(σ) | 1/√(σ² + σ²_data) | unit-variance network **input** (Eq. 117) |
  | c_out(σ) | σ·σ_data/√(σ² + σ²_data) | unit-variance training **target** (Eq. 138) |
  | c_skip(σ) | σ²_data/(σ² + σ²_data) | minimal amplification of F_θ's error (Eq. 131) |
  | λ(σ) | (σ² + σ²_data)/(σ·σ_data)² | makes the effective loss weight w(σ) = 1 (Eq. 144) |
  | c_noise(σ) | ¼·ln(σ) | empirical — the one that is not derived |

  The division of labour matters: **two of the four come from unit variance,
  one from error amplification, one is a curve fit.**
- **Training noise distribution:** ln(σ) ~ N(P_mean, P²_std) with
  P_mean = −1.2, P_std = 1.2 — a log-normal, concentrating samples away from
  both extremes, where the denoising task is respectively trivial and
  hopeless.
- **Sampler:** Heun's second-order method with time steps
  σ_i spaced by ρ = 7 between σ_min = 0.002 and σ_max = 80.
- **Stochasticity's usefulness shrinks as the model improves.** Adding noise
  during sampling helps the ImageNet-64 model but is *harmful* on CIFAR-10
  once the network is trained under the paper's own improvements — the
  authors read this as stochasticity correcting errors that better training
  removes.
- **Table 2's A→F ablation** attributes the CIFAR-10 gains to the individual
  changes rather than to the recipe as a whole.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The existing diffusion formulations differ only in choices that are independently settable | strong | the common framework, plus the sampler transferring to pretrained networks |
| C2 | c_in and c_out follow from requiring unit-variance inputs and targets | strong | derived in Appendix B.6 (Eqs. 117, 138) |
| C3 | c_skip follows from minimising the amplification of the network's own error | strong | derived (Eq. 131), a different criterion from C2 |
| C4 | c_noise has no derivation | strong | stated: "chosen empirically" |
| C5 | Sampling training σ from a log-normal beats sampling it uniformly | moderate | ablated; P_mean and P_std are tuned, not derived |
| C6 | Higher-order (Heun) sampling reduces NFE at equal quality | strong | measured, with the truncation-error argument |
| C7 | Stochastic sampling compensates for model error, and matters less as the model improves | moderate | inferred from the CIFAR-10/ImageNet-64 split, not isolated |

## Method

Write every prior diffusion formulation in a common notation (σ(t), s(t),
plus the four preconditioning scalings). Fix the schedule to σ(t) = t,
s(t) = 1. Solve for c_in, c_out, c_skip, λ under the stated criteria; fit
c_noise. Replace ancestral/Euler sampling with Heun's method on a ρ-spaced σ
grid. Sample training noise log-normally. Ablate each change separately
(Table 2, configs A–F), and separately apply the sampler alone to networks
trained by others.

## Concepts

- **Preconditioning** — the noise-level-dependent scalings that sit between
  the raw network F_θ and the denoiser D_θ. The paper's framing is that these
  are *not* part of the model: they are a change of variables, and the right
  one can be computed.
- **Effective loss weight** — what the training loss actually weights each σ
  by, once c_out and λ are folded in. Setting it to 1 uniformly is what makes
  the log-normal σ distribution the *only* thing deciding where compute goes.
- **Design space** — the paper's framing device, and the reason its results
  transferred: separable axes are separately improvable.

## Connections

Descends from the score-based and DDPM lines it unifies; its immediate
consequence is that later systems quote its σ-parameterisation directly. The
log-normal timestep sampling and the unit-variance target survive into the
rectified-flow and diffusion-transformer work that followed, which is where
most readers meet them.

## Recommendations

- **R1** — Derive a network's input/output scalings from a variance
  requirement rather than tuning them. *Topic:* training optimization.
  *Status:* standard. *Strength:* strong. *Applies when:* a network is
  conditioned on a variable that changes the scale of its task.
- **R2** — Sample the conditioning variable where the learning signal is, not
  uniformly. *Topic:* training optimization. *Status:* standard.
  *Strength:* moderate — the shape is principled, the parameters are tuned.
- **R3** — Keep sampler, objective and architecture separable, and check that
  a change to one transfers to models trained without it. *Topic:*
  methodology. *Strength:* strong. This is the paper's method as much as its
  result.

## Bearing on the record

**The one practice sourced to this note is confirmed** — and the gap this
note previously recorded is closed.

| practice | disposition |
|---|---|
| [SOTA-188](../practices.d/SOTA-188.md) parametrize the network so its prediction target has unit variance, and sample training noise from a log-normal | **confirmed** — C2 and C5 |

Both halves check out, and the reading sharpens the first one. `SOTA-188`
says the scalings are "chosen so the effective training target has unit
variance at every level", which reads as though all four came from that
requirement. They did not: **c_in and c_out come from unit variance, c_skip
comes from a separate error-amplification criterion, λ comes from flattening
the effective loss weight, and c_noise is a curve fit.** The practice is
right about what it recommends and loose about how much of the recipe the
principle covers, so the body has been corrected at v2 rather than the
practice re-sourced.

The conditions the practice already states survive the reading: the numbers
are specific to σ_data and to this schedule, and the result is an image
result with nothing in the record replicating it for language.

## Limitations

- Images at 2022 scales; no language or audio evidence.
- **c_noise is unexplained**, and the paper says so. One of the four
  coefficients in a section titled as a principled analysis is a fit.
- P_mean and P_std are tuned per dataset. The *shape* of the training-noise
  distribution is argued for; the parameters are not.
- C7 is the weakest claim here: the stochasticity finding comes from two
  datasets behaving differently, and the explanation — that noise corrects
  model error — is the authors' reading rather than an isolated measurement.
- σ_data as a single scalar is an assumption the paper never stresses, and it
  is doing real work in every coefficient.

## Open questions

- Does the unit-variance derivation survive when the data has no single
  scale? Every coefficient is a function of one σ_data.
- Why ¼·ln(σ)? A derivation for c_noise would complete the section.
- The modularity result — a sampler improving networks trained by other
  people — is the transferable finding here, and the record has no practice
  that states it as a methodological expectation.
