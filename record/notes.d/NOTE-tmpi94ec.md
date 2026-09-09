---
status: Read
paper: LIT-067
title: 'Progressive Distillation for Fast Sampling of Diffusion Models'
version: 1
tags:
- generative-modeling
date: '2026-09-09'
summary: >-
  Repeatedly halves a diffusion sampler's step count by distilling two teacher steps into one student step, from 8192 down to 4 at FID 3.0 on CIFAR-10, for no more total compute than training the original model. Also where v-prediction comes from — and the reason for it is that ε-prediction's implied x̂ blows up as signal-to-noise goes to zero.
---

# NOTE-tmpi94ec: Progressive Distillation for Fast Sampling of Diffusion Models

## Contribution

Two contributions, and the record cares more about the second.

**Progressive distillation:** distil an `N`-step DDIM sampler into a student
taking `N/2` steps, where the student's target is what two teacher steps
produce. Then make that student the teacher and repeat. From 8192 steps down to
**4**, at **FID 3.0 on CIFAR-10**, and the whole cascade costs no more than
training the original model.

**New parameterisations for stability at few steps**, including
**v-prediction** — and the reason they are needed is a precise diagnosis.

## Key insight

The standard ε-parameterisation is fine for training and breaks under
distillation, for a stated reason:

> as the signal-to-noise ratio goes to zero, the effect of small changes in the
> neural network output on the implied prediction in x-space is increasingly
> amplified

An ordinary diffusion model is evaluated across a wide range of signal-to-noise
ratios, so this rarely dominates. As distillation halves the step count, the
model is increasingly evaluated **at the low-SNR end**, where ε-prediction's
implied `x̂` is a small number divided by a smaller one.

The requirement that follows is stated exactly: parameterise so that **the
implied `x̂` remains stable as `λ_t = log(α²/σ²)` varies.** Three
parameterisations satisfy it:

- predict `x` directly;
- predict both `x` and `ε` on separate channels and merge them,
  `x̂ = σ²·x̃ + α(z − σ·ε̃)`, smoothly interpolating between the two;
- **predict `v ≡ α_t·ε − σ_t·x`**, giving `x̂ = α_t·z_t − σ_t·v̂`.

The loss weighting has to change too, because DDPM's implicit weighting is
`exp(λ_t)` — the signal-to-noise ratio — which **gives weight zero to
zero-SNR data** and is therefore unusable for distillation. Two replacements:
`max(α²/σ², 1)` ("truncated SNR") and `(1 + α²/σ²)`, the latter being exactly
`‖v − v̂‖²` ("SNR+1").

## Assumptions

- The teacher's two-step behaviour is the right target — deterministic DDIM
  sampling makes it well-defined.
- The student can be initialised from the teacher, which is why each halving is
  cheap.
- Images; CIFAR-10, ImageNet, LSUN.

## Key results

- **8192 → 4 steps**, FID 3.0 on CIFAR-10 at 4 steps.
- **Total distillation cost ≤ the cost of training the original model.**
- **Halving beats quartering.** Training each student on 4× fewer steps than
  its teacher works worse than 2×, even though the denoising target is still
  two teacher steps: "if the computational budget is limited, it's better to
  take fewer parameter updates per halving than to skip distillation
  iterations altogether." The schedule matters more than the budget.
- All three parameterisations also work well for training an *original*
  diffusion model, not only for distillation (§5.1) — which is why
  v-prediction escaped into general use.
- Both alternative loss weightings are good choices for ordinary training too.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Step count can be halved repeatedly by distillation with little quality loss | strong | 8192→4, three datasets |
| C2 | ε-prediction is unstable as SNR → 0 | strong | argued from the algebra, and it is why C1 needs C3 |
| C3 | x-, joint- and v-parameterisations all keep `x̂` stable across SNR | strong | all three tried, all work |
| C4 | DDPM's implicit SNR weighting is unusable for distillation | strong | it assigns weight zero at zero SNR |
| C5 | Gradual halving beats aggressive step reduction at fixed budget | strong | ablated, Figure 12 |
| C6 | The whole procedure costs no more than the original training run | strong | measured |

## Method

Train normally with a stable parameterisation. Then repeatedly: freeze the
teacher, initialise the student from it, train the student so one of its steps
matches two of the teacher's, halve `N`, promote the student.

## Concepts

- **v-prediction** — `v = α_t·ε − σ_t·x`, and the record should know it
  originates here rather than in the flow-matching literature that popularised
  it.
- **Stability of the implied prediction across the conditioning variable** —
  the criterion, stated four months before EDM derives coefficients from a
  closely related one.
- **Distil the sampler, not the model** — the student learns a *procedure*.

## Connections

Takes `LIT-038`'s deterministic sampler as its teacher; solves the failure mode
`LIT-038` left unexamined (deterministic trajectories at low SNR).
`LIT-076` and `LIT-093` are the training-free and one-step alternatives to the
same goal.

**The important one is `LIT-075` and `SOTA-188`.** `SOTA-188` says: parametrise
the network so its prediction target has unit variance at every noise level.
This paper, four months earlier, states the requirement as *keep the implied
`x̂` stable as log-SNR varies*, gives three parameterisations that do, and
replaces the SNR loss weighting for the same reason EDM later replaces it with
`λ(σ)`. It reaches the criterion empirically; EDM derives it. **The record
carries the derivation and not the antecedent.**

## Recommendations

- **R1** — Choose a parameterisation whose implied prediction is stable across
  the whole conditioning range, not just the range you usually train at.
  *Topic:* training optimization. *Strength:* strong; the general form of
  `SOTA-188`, arrived at from a different direction.
- **R2** — Check whether your loss weighting assigns zero weight anywhere you
  intend to evaluate. *Strength:* strong, and a cheap check that would have
  caught this.
- **R3** — Reduce gradually. C5 says a schedule of small halvings beats fewer,
  larger reductions at equal compute. *Strength:* moderate.
- **R4** — Use v-prediction. *Strength:* strong; standard now.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice** — but
it identifies the antecedent of one.

`SOTA-188` is sourced to `LIT-075` (EDM), correctly: EDM derives the
preconditioning coefficients. But the *problem* `SOTA-188` solves — that a
network conditioned on noise level is asked a differently-scaled question at
each level, and the parameterisation must absorb that — is stated here first,
with a concrete failure (low-SNR amplification), a concrete criterion (stable
implied `x̂`), and three concrete solutions. **v-prediction, which the record
does not mention anywhere, is one of them.**

That is a gap worth naming and not one this pass should close: adding
`LIT-067` as a second source for `SOTA-188`, or filing v-prediction as its own
practice, is a registry decision.

The document's takeaways — "faster sampling through distillation",
"student-teacher framework", "quality-speed tradeoff analysis", "practical
implementation guide" — describe the first contribution generically and omit
the second entirely.

## Limitations

- Images, 2022, and 4-step quality is "not much" degraded rather than equal.
- The three parameterisations are compared and none is shown superior; the
  paper's own use of v-prediction is a preference.
- C5 is one ablation on one budget.
- Distillation requires a teacher, so it does not help anyone training from
  scratch — which is what `LIT-093`'s isolation mode addresses.

## Open questions

- Is the stability criterion here the same as EDM's unit-variance requirement,
  or merely close? Both produce workable coefficients; nobody has written down
  whether they agree.
