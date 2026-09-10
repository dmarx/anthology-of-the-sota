---
number: 53
status: Read
formerly:
- NOTE-tmpmizcq
paper: LIT-093
title: 'Consistency Models'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    The
tags:
- generative-modeling
date: '2026-09-09'
published: '2023-03-01'
summary: >-
  Trains a model to map any point on a diffusion trajectory directly to its origin, so one network evaluation generates a sample — FID 3.55 on CIFAR-10 and 6.20 on ImageNet-64 in one step. Trainable either by distilling a diffusion model or from scratch, and the from-scratch mode is what makes it a model family rather than a distillation trick.
---

# NOTE-053: Consistency Models

## Contribution

A generative model family whose defining property is **self-consistency along a
diffusion trajectory**: every point on a trajectory maps to the same origin. If
the model has that property, generation is one function evaluation — map noise
straight to data.

Two training modes, and the second is the contribution that matters:

- **Consistency distillation** — from a pretrained diffusion model.
- **Consistency training** — in isolation, with **no diffusion model at all**,
  which makes consistency models an independent class rather than an
  acceleration technique.

Multistep sampling remains available, so compute can still be traded for
quality; and zero-shot editing — inpainting, colorization, super-resolution —
works without task-specific training.

## Key insight

The trajectory is the training signal. A diffusion model learns a *local* step;
a consistency model learns the *whole map to the origin*, and the constraint
that makes that learnable without simulating the trajectory is that adjacent
points must agree about where they came from.

The second insight is a bias/variance schedule, and it is the practical heart
of the isolation mode. With `N` discretisation steps, the consistency training
loss "has less variance but more bias" with respect to the distillation loss
when `N` is small, and the reverse when `N` is large. So they **increase `N`
during training** on a schedule `N(·)`, with the EMA decay `μ` scheduled
alongside it: fast, biased progress early; accurate, noisier refinement late.

That is a general pattern — anneal a discretisation from coarse to fine to move
along the bias/variance tradeoff during a single run — and it is stated here
with the reasoning explicit.

## Assumptions

- **A well-defined probability-flow ODE trajectory exists** to be consistent
  along. Distillation inherits one; isolation mode constructs it from the
  noise schedule.
- The consistency constraint is enough to pin the map — a boundary condition at
  the data end does the rest.
- `ℓ₁` and other metrics are usable, though the theory is weaker for some:
  Theorem 3 is **vacuous for `ℓ₁`**, since its Hessian is zero, and the paper
  says so and proves a separate non-vacuous statement.

## Key results

- **One-step FID 3.55 on CIFAR-10 and 6.20 on ImageNet-64** — state of the art
  for one-step generation at the time, beating existing distillation methods.
- **Trained in isolation**, they beat existing one-step **non-adversarial**
  generative models on CIFAR-10, ImageNet-64 and LSUN-256.
- **Multistep sampling trades compute for quality** without retraining.
- **Zero-shot inpainting, colorization and super-resolution**, no task-specific
  training.
- The `N(·)` and `μ(·)` schedules are necessary for good isolation-mode
  performance, with the bias/variance reasoning given (Fig. 3d, Appendix C).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Self-consistency along a trajectory suffices for one-step generation | strong | the results |
| C2 | Consistency models beat prior diffusion distillation at one and few steps | strong | measured |
| C3 | They can be trained without any diffusion model | strong | the isolation-mode results |
| C4 | Progressive `N` moves along a bias/variance tradeoff within one run | moderate | reasoned and used; the tradeoff is argued rather than measured directly |
| C5 | Zero-shot editing comes for free | moderate | demonstrated on three tasks |
| C6 | The theory covers the metrics used | **qualified by the authors** | Theorem 3 is vacuous for `ℓ₁`; a separate proof is given |

## Method

Train a network `f(x_t, t)` with a boundary condition at the data end, penalising
disagreement between its outputs at adjacent points on a trajectory — the
adjacent point coming from a teacher (distillation) or from the noise process
(isolation). Increase `N` and adjust `μ` on a schedule. Sample by evaluating
once from noise, or a few times with re-noising.

## Concepts

- **Self-consistency as an objective** — learning a map by constraining its
  agreement with itself, rather than by matching a target.
- **Scheduled discretisation** — C4, and the transferable one.
- **One-step by design, multi-step by option** — the compute/quality dial
  survives, which is what separates this from a distilled point solution.

## Connections

The third route to few-step sampling in this batch: `LIT-067` distils a
*sampler*, `LIT-076` replaces the *solver*, this replaces the *model*. Built on
the EDM formulation — `LIT-075` — whose σ-parameterisation and trajectory it
adopts.

Its isolation mode is the one that escapes the `LIT-038` lineage entirely: no
pretrained network, so none of `LIT-038`'s sampler/objective separation is
being exploited. That makes it the only paper in this batch whose result does
not depend on a diffusion model existing.

## Recommendations

- **R1** — When distilling a procedure, consider learning the whole map rather
  than a shorter version of the procedure. *Topic:* generative modelling.
  *Strength:* strong.
- **R2** — Anneal a discretisation from coarse to fine within a run to trade
  bias for variance over training. *Strength:* moderate, and general.
- **R3** — Keep the multi-step option; a one-step model that cannot spend more
  compute has no quality dial. *Strength:* strong.
- **R4** — State when a theorem is vacuous for a setting you actually use.
  *Topic:* analysis and evaluation. *Strength:* strong — the paper does this
  and it is worth copying.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

<!-- inactive-ok: SOTA-204 — Proposed, and named here as Proposed: this is the practice filed from R2, and its status is the point being made -->
> **Overtaken by the [#121](https://github.com/dmarx/anthology-of-the-sota/issues/121) audit.** R2 is now [SOTA-204](../practices.d/SOTA-204.md)
> (`Proposed`, on the grounds this reading gives — one instance of a general
> mechanism) and R3 is [SOTA-206](../practices.d/SOTA-206.md). The rest of this reading stands as
> written.

R2 is the reading's transferable finding and the record has nothing like it.
<!-- inactive-ok-block: SOTA-141, SOTA-156 — both Proposed, named as the record's schedule neighbourhood rather than relied on -->
The corpus's schedule practices are about learning rates (`SOTA-140`,
`SOTA-141`, `SOTA-156`) and batch sizes; this is a schedule on a
**discretisation**, justified by an explicit bias/variance argument, and the
same shape would apply anywhere a training loss approximates a target through a
step count.

The document's takeaways — "single-step generation", "distillation of diffusion
models", "faster sampling", "theoretical guarantees" — get the emphasis
backwards. **"Distillation of diffusion models" is the mode the paper is at
pains to say it does not require**; the isolation mode is what makes this a new
model family, and it is the claim in the title's spirit.

## Limitations

- Images, 2023, and one-step FID 3.55 still trails multi-step diffusion.
- C4's tradeoff is argued from the loss's structure; the schedules themselves
  are in an appendix and are tuned.
- The theory has a hole the authors flag for `ℓ₁`.
- Isolation mode's sample quality, while beating one-step non-adversarial
  baselines, is not compared against the full diffusion models it would have to
  replace.

## Open questions

- What is the general form of C4? "Increase the discretisation as training
  proceeds" is stated for this loss and looks like it should apply to any
  approximation with a step-count knob.
