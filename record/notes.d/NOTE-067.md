---
number: 67
status: Read
formerly:
- NOTE-tmptmi2d
paper: LIT-038
title: 'Denoising Diffusion Implicit Models'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    The
tags:
- generative-modeling
date: '2026-09-09'
published: '2020-10-01'
summary: >-
  Generalises DDPM to a family of *non-Markovian* forward processes that share DDPM's exact training objective, so the sampler can be replaced without retraining. Picking the deterministic member gives 10–50× fewer steps, plus latent interpolation and encoding that a stochastic sampler cannot do. Not a continuous-time or SDE paper — that is a different one.
---

# NOTE-067: Denoising Diffusion Implicit Models

## Contribution

Separates the sampler from the training objective. DDPM's generative process is
the reverse of a *Markovian* diffusion; this paper constructs a family of
**non-Markovian** forward processes and shows they all "have a shared surrogate
objective, which is exactly the objective used to train DDPM."

The consequence is the point: **you can choose a different generative process
for an already-trained network, with no retraining.** Choosing the
deterministic member gives DDIM.

## Key insight

The training objective does not determine the sampler. That sounds obvious and
was not — DDPM presents them as one derivation, and the reason a whole family
of samplers is available is that the objective is invariant to a choice the
derivation appeared to fix.

Once the sampler is deterministic, two things become possible that a stochastic
one cannot do:

- **Fixed `x_T` determines high-level image features regardless of trajectory
  length**, so `x_T` behaves as a latent code and interpolating in it produces
  semantically meaningful interpolation.
- **Samples can be encoded back to a latent and reconstructed** with very low
  error. DDPM cannot, because its sampling injects fresh noise at every step.

## Assumptions

- **The surrogate objective is genuinely shared.** The whole result rests on
  this and it is derived, not assumed.
- The trained noise-prediction network is accurate enough that a deterministic
  trajectory does not accumulate error — which is what later few-step work
  (`LIT-067`) finds is *not* true at the low signal-to-noise end.
- Images, 2020, DDPM-scale models.

## Key results

- **10–50× wall-clock speedup**: quality comparable to a 1000-step model within
  **20–100 steps**. On CelebA, a 100-step DDPM matches a **20-step** DDIM.
- Speedups of 10–100× over the original DDPM generation process when few
  iterations are considered.
- **Sampling time scales linearly with trajectory length** (Figure 4) — so step
  count is the whole cost, which is what makes it the thing to attack.
- **No training changes at all.** "Only slight changes to the updates" produce
  the faster processes, and they apply to DDPM, DDIM and the whole family.
- Section 4.3 relates the deterministic sampler to **neural ODEs** — an ODE
  connection, in a subsection.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A family of non-Markovian forward processes share DDPM's training objective | strong | derived |
| C2 | The sampler can therefore be changed without retraining | strong | demonstrated on pretrained models |
| C3 | 10–50× fewer steps at comparable quality | strong | measured, several datasets |
| C4 | A deterministic sampler makes `x_T` a usable latent code | strong | interpolation and reconstruction both shown |
| C5 | DDPM cannot do C4 | strong | structural — its sampling is stochastic |

## Method

Define a non-Markovian forward process with the same marginals; derive the
corresponding reverse process; set its stochasticity parameter to zero. Use the
existing trained network unchanged, on a subsequence of timesteps.

## Concepts

- **Sampler/objective separation** — the contribution, and the reason the
  diffusion literature could then iterate on samplers alone.
- **The trained network as a fixed asset** — every later fast-sampling paper
  inherits the assumption that you improve sampling *on somebody else's
  weights*.
- **Determinism as invertibility** — the latent code exists because nothing
  random is added, not because anything was designed for it.

## Connections

Directly downstream of `LIT-036`; directly upstream of `LIT-067` (which
distils a DDIM sampler), `LIT-076` (**"DDIM as DPM-Solver-1"** — DDIM is
literally the first-order case of an exponential-integrator solver) and
`LIT-093`.

**This is where EDM's modularity comes from.** `LIT-075`'s reading records that
the strongest evidence for EDM's design-space framing is that its sampler
improvements transfer to *pretrained* networks — a previously trained
ImageNet-64 model going from FID 2.07 to 1.55 with no retraining. That
transfer is possible because of C1 and C2, established here. The record
carried the consequence without the cause.

## Recommendations

- **R1** — Check whether a training objective actually constrains the inference
  procedure before treating them as one design. *Topic:* generative modelling.
  *Strength:* strong; the whole paper is one instance and it was worth 10–50×.
- **R2** — Prefer a deterministic sampler when you want the latent to mean
  something. *Strength:* strong.
- **R3** — Report sampler improvements on someone else's trained weights; it is
  a stronger claim and a cheaper experiment. *Topic:* analysis and evaluation.
  *Strength:* strong.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

> **Overtaken by the [#121](https://github.com/dmarx/anthology-of-the-sota/issues/121) audit.** That sentence was this pass's policy, not a
> judgement about the paper. R2 is now [SOTA-207](../practices.d/SOTA-207.md) and the
> sampler/objective separation is corroborating source on
> [SOTA-203](../practices.d/SOTA-203.md). The rest of this reading stands as written.

The reading fixes the document, which was substantially about a **different
paper**. Two of its four takeaways — *"continuous-time formulation of diffusion
models"* and *"connection to SDE theory"* — describe Song et al.'s *Score-Based
Generative Modeling through Stochastic Differential Equations*, a separate 2020
paper. DDIM is a **discrete-time, non-Markovian** reformulation whose sampler
is deterministic; its only continuous connection is a subsection relating it to
neural **ODEs**, not SDEs.

That is the `#114` failure mode — takeaways describing a neighbouring paper —
appearing in this population, where the first fifteen readings had found only
vagueness. It matters for what this pass is: the population is not uniformly
"true but empty".

It also supplies the cause behind an effect the record already carries.
`LIT-075`'s reading treats sampler-transfer-without-retraining as EDM's
evidence for its framing; C1 and C2 here are why that transfer is available at
all.

## Limitations

- 2020, images, and quality at 20 steps is *comparable*, not equal.
- The deterministic trajectory's error accumulation at low signal-to-noise is
  not examined and is exactly what `LIT-067` has to fix.
- No theory for *which* member of the family is best — DDIM is one choice, and
  `LIT-076` later shows the space is much larger.

## Open questions

- The family is parameterised by a stochasticity level, and the paper takes the
  two ends. `LIT-075` later finds the useful amount of stochasticity depends on
  how good the model is — which is a question posed here and answered elsewhere.
