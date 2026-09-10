---
number: 195
status: Active
formerly:
- SOTA-tmphwawd
consensus: converged
consensus_note: >-
  v-prediction is standard in few-step diffusion and in the rectified-flow line
  that followed. The record had the derived form of the principle (SOTA-188)
  and not the parameterization everyone actually types.
title: 'Predict v rather than the noise when the model will be evaluated at low signal-to-noise'
version: 1
tags:
- training-optimization
date: '2026-09-10'
published: '2022-02-01'
source:
- LIT-067
extends:
- SOTA-188
implementations:
- Progressive Distillation
- Stable Diffusion 2
---

# SOTA-195: Predict v rather than the noise when the model will be evaluated at low signal-to-noise

## Source

Salimans and Ho (2022), [LIT-067](../literature.d/LIT-067.md) — Progressive Distillation, where
v-prediction is introduced and, more usefully, where the reason for it is
diagnosed.

## The failure

`ε`-prediction is fine for ordinary diffusion training and breaks when the model
is evaluated near zero signal-to-noise. `LIT-067` states the mechanism:

> as the signal-to-noise ratio goes to zero, the effect of small changes in the
> neural network output on the implied prediction in x-space is increasingly
> amplified

The implied `x̂` is a small number divided by a smaller one. An ordinary
diffusion model is evaluated across a wide range of SNR so this rarely dominates;
anything that concentrates evaluation at the low end — distillation, few-step
sampling — walks straight into it.

## The requirement, and three ways to meet it

The stated criterion is that **the implied `x̂` must remain stable as
`λ_t = log(α²/σ²) varies`.** Three parameterizations satisfy it:

- predict `x` directly;
- predict `x` and `ε` on separate channels and merge them,
  `x̂ = σ²·x̃ + α(z − σ·ε̃)`, interpolating between the two;
- **predict `v ≡ α_t·ε − σ_t·x`**, giving `x̂ = α_t·z_t − σ_t·v̂`.

All three work, for distillation *and* for training an original diffusion model
(§5.1) — which is how v-prediction escaped its original setting.

## The loss weighting has to change too

DDPM's implicit weighting is `exp(λ_t)`, the signal-to-noise ratio, which
**assigns weight zero to zero-SNR data** and is therefore unusable wherever you
intend to evaluate. `LIT-067` offers `max(α²/σ², 1)` ("truncated SNR") and
`(1 + α²/σ²)` — the latter being exactly `‖v − v̂‖²`, so choosing v-prediction
with an unweighted L2 loss picks the weighting for you.

**Check whether your loss weighting is zero anywhere you plan to evaluate.**
That is a cheap check and it is what would have caught this.

## Relation to [SOTA-188](SOTA-188.md)

[SOTA-188](SOTA-188.md) is the derived statement of the same problem: parametrize so the
prediction target has unit variance at every noise level, from EDM's
preconditioning. This is the empirical statement, four months earlier, and it is
what people type. `SOTA-188` says what the coefficients should satisfy; this
says what to predict.

Whether EDM's unit-variance requirement and `LIT-067`'s stability criterion are
the same condition or merely close is not written down anywhere.

## Conditions

Images, 2022. The three parameterizations are compared and **none is shown
superior** — the paper's own use of v-prediction is a preference, not a result.

Nothing here bears on autoregressive language modelling; the practice is filed
`training-optimization` because it is a statement about parameterizing a
conditioned network, and that is the form that generalises.

## Known implementations

- Progressive Distillation; Stable Diffusion 2 and successors; the
  rectified-flow line
