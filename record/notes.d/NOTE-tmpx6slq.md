---
status: Read
paper: LIT-tmp4xjcz
title: 'Variational Diffusion Models'
version: 1
date: '2026-09-20'
summary: >-
  Integrating the diffusion VLB over signal-to-noise ratio rather than time
  collapses the schedule out of the expression: in continuous time the bound
  depends on it only through the endpoint SNRs. VP and VE specifications are
  therefore equivalent, and the freed schedule shape is spent on minimizing
  the loss estimator's variance.
---

# NOTE-tmpx6slq: Variational Diffusion Models

## Contribution

Establishes that the noise schedule of a continuous-time diffusion model is
not part of the model. Rewriting the variational bound as an integral over
signal-to-noise ratio rather than over time removes the schedule from the
integrand and leaves it only in the limits, so the bound and the generative
distribution both depend on it through two numbers. Several diffusion
specifications the literature had treated as different model classes fall out
as equivalent. Having freed the shape, the paper spends it: learning the
schedule to minimize the variance of the loss estimator speeds optimization
at no cost to the bound, and with Fourier features on the input channels the
result is state-of-the-art likelihood on image density estimation, taking
benchmarks autoregressive models had held for years.

## Key insight

**A change of variables can tell you which of your design choices were
choices.** The noise schedule looked like modelling — every diffusion paper
proposed one and argued for it — because the loss was written as an integral
over time, where the schedule appears throughout. Integrate over SNR instead,
which is legitimate because the schedule is monotone and hence invertible,
and the schedule vanishes from the integrand. What remains is where you start
and where you stop. Everything in between was free the whole time, and the
years of schedule proposals were an argument about an optimization
convenience conducted in the vocabulary of a model class.

## Assumptions

- **Continuous time.** The invariance is a statement about the infinite-depth
  limit. In discrete time the loss is an upper Riemann sum of the same
  integral, so the schedule's shape does matter — it determines how good the
  approximation is — and more steps is always at least as good.
- **A monotone SNR function**, which makes the change of variables valid. The
  paper states this as a mild regularity condition satisfied by the
  variance-preserving and variance-exploding specifications alike.
- **The unweighted VLB** for the headline invariance. The equivalence between
  specifications is shown to survive a weighted diffusion loss; the
  indifference to schedule shape is a statement about the bound.
- The generative distribution's invariance holds **up to a trivial rescaling
  of the latents**, not exactly.
- Gaussian diffusion with the marginal's mean and variance parameterized
  directly, rather than the individual steps — which is what allows the
  schedule to be optimized jointly with the model at all.

## Key results

- **The continuous-time VLB, in SNR coordinates**, is an integral of a
  weighted MSE with respect to SNR between the two endpoint values. *Holds
  when:* continuous time, monotone SNR.
- **Invariance**: given the endpoints, the bound does not depend on the
  schedule between them. *Holds when:* as above.
- **Equivalence**: two specifications with equal endpoint SNRs define the same
  generative distribution up to a rescaling — so VE and VP, presented as
  distinct classes, are the same model in continuous time.
- **Discrete-time loss is an upper bound** on the continuous-time integral,
  improving monotonically as steps are added.
- **Variance-minimizing learned schedule**: with the endpoints fixed by the
  VLB and the shape learned to minimize estimator variance, optimization is
  markedly faster at the same bound. A low-discrepancy sampler for the time
  variable cuts variance further.
- **Fourier features, conditionally.** Appending high-frequency periodic
  channels of the input improves likelihood substantially — but only with a
  learned schedule. Ho et al.'s fixed schedule pins maximum log-SNR near 8
  and likelihood stalls above 4 bits/dim; the learned endpoints reach about
  13.3 and the features become usable. No benefit in a PixelCNN++.
- **State-of-the-art likelihoods** on CIFAR-10 and ImageNet 64×64, over the
  autoregressive models that had led those benchmarks.
- A bits-back compression scheme with lossless rates near the theoretical
  optimum.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | In continuous time the diffusion VLB depends on the noise schedule only through its endpoint SNRs | strong | derivation; the change of variables is exact under a stated monotonicity condition |
| C2 | Diffusion specifications with matching endpoints are equivalent up to a rescaling of latents | strong | proved in the appendix, with VE and VP named as instances |
| C3 | Learning the schedule to minimize estimator variance speeds optimization without changing the bound | moderate | follows from C1 plus measured variance reductions and training curves on CIFAR-10 |
| C4 | Fourier features on colour channels improve likelihood, and require a learned schedule to do so | moderate | ablation on CIFAR-10, with a negative control in PixelCNN++ |
| C5 | Diffusion models can beat autoregressive models on density estimation | strong | benchmark results on two datasets |

## Method

Define the forward process by its marginal's mean and variance directly,
rather than step by step, so that the schedule is a differentiable object
that can be optimized with the model. Write the VLB, then substitute SNR for
time. Read off the invariance.

Parameterize the log-SNR as a monotone network. Optimize its endpoints
against the VLB. Optimize its shape against the *variance* of the Monte Carlo
estimate of the loss — a target that exists only because the bound itself is
indifferent to it. Sample the time variable with a low-discrepancy sequence
rather than i.i.d. uniformly.

Append Fourier features of the input's colour channels to the denoiser's
input, so the network can represent fine-scale structure that likelihood, as
against perceptual quality, is sensitive to.

## Concepts

- **SNR, `α_t²/σ_t²`** — the signal-to-noise ratio of the diffused data. The
  natural coordinate for the whole problem, on this account.
- **Endpoint SNRs** — the values at `t=0` and `t=1`. The only part of the
  schedule the continuous-time bound sees.
- **Variance-preserving / variance-exploding** — two families of forward
  process, shown here to be the same object in continuous time.
- **Variance of the VLB estimator** — the quantity the freed schedule shape is
  optimized against; not the bound, which is fixed.

## Connections

Generalizes DDPM ([LIT-036](../literature.d/LIT-036.md)) to continuous time by way of a variational
derivation rather than an SDE one. Concurrent with the score-SDE line, which
reached continuous-time bounds through stochastic differential equations; the
paper's stated advantage over those is the SNR expression, which is what
makes the invariance visible at all.

Forward to EDM ([LIT-075](../literature.d/LIT-075.md)), whose design-space study takes the freedom this
paper establishes and spends it on a different objective — where training
compute goes along the noise axis — reaching the log-normal sampling
distribution that [SOTA-188](../practices.d/SOTA-188.md) records.

The Fourier-feature result connects to the positional-encoding literature,
applied here to colour channels of a single pixel rather than to spatial
coordinates.

## Recommendations

- **R1** — Fix the noise schedule's endpoints against the bound and choose its
  shape to minimize the variance of the loss estimator. *Topic:* noise
  schedule. *Status:* experimental. *Strength:* strong. *Applies when:*
  continuous-time diffusion training with a differentiable schedule.
- **R2** — Do not argue about schedule *shape* as though it were a modelling
  choice in continuous time; it is not. *Topic:* modelling. *Status:*
  standard. *Strength:* strong. *Applies when:* continuous time, unweighted
  bound.
- **R3** — Prefer continuous-time training where the bound is what you care
  about; the discrete loss is an upper bound that only converges to it.
  *Topic:* training. *Status:* experimental. *Strength:* moderate.
  *Applies when:* likelihood is the objective.
- **R4** — When optimizing for likelihood rather than perceptual quality, give
  the denoiser high-frequency features of its input, and learn the schedule
  so it can use them. *Topic:* architecture. *Status:* experimental.
  *Strength:* moderate. *Applies when:* density estimation.

## Bearing on the record

- **Should produce a theory document** for C1 and C2, and it has a real
  target: it explains why [SOTA-188](../practices.d/SOTA-188.md)'s choice of training-noise distribution
  is an optimization decision rather than a change of model. The record has
  carried that practice without an answer to that objection.
- **Should produce a practice** for R1. Nothing in the record learns a noise
  schedule.
- **Explains a compatibility the record assumes silently.** [LIT-036](../literature.d/LIT-036.md),
  [LIT-038](../literature.d/LIT-038.md), [LIT-075](../literature.d/LIT-075.md) and the practices drawn from them are discussed as
  being about one model class. C2 is why that is allowed.
- **R4 has no home** and probably should not get one on this evidence: it is
  one architecture on two small datasets, and the record's diffusion
  practices are all about perceptual generation where likelihood is not the
  objective.

## Limitations

- The invariance is continuous-time and unweighted. Every practical recipe the
  record holds uses a weighted loss and a finite number of steps, so the
  clean statement is about a limit that nobody trains in exactly.
- "Equivalent up to a trivial rescaling" is doing work: the models are the
  same object under a transformation, which does not make two implementations
  interchangeable in a codebase.
- Results are CIFAR-10 and ImageNet 64×64 — small, and likelihood-oriented.
  Nothing here is about text-to-image or about sample quality.
- The variance-minimizing schedule is optimized for *this* estimator; the
  paper does not characterize how much of the gain survives a different
  sampling strategy for the time variable.
- Fourier features help here and not in an autoregressive model, and no
  account of the asymmetry is offered.

## Open questions

- How far does the invariance degrade at realistic step counts? The Riemann
  argument says the gap closes monotonically and does not say how fast, and
  that rate is what a practitioner needs.
- Under a weighted loss, the schedule shape and the weighting are two handles
  on one thing. Which parameterization is better conditioned is unexamined,
  and the record now holds practices that reach for each.
- Does the variance-minimizing schedule coincide with the compute-allocating
  one that EDM and [SOTA-188](../practices.d/SOTA-188.md) reach on perceptual grounds? Two different
  arguments for concentrating effort in the middle of the range, and nobody
  has checked whether they land in the same place.
