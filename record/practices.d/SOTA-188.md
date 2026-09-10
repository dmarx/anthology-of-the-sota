---
number: 188
status: Active
formerly:
- SOTA-tmpm1xnl
title: 'Parametrize the network so its prediction target has unit variance at every noise level, and sample training noise from a log-normal'
version: 3
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Corrected against a full reading of the source (NOTE-019, now
    Read). The body implied all four preconditioning scalings follow
    from the unit-variance requirement; only c_in and c_out do — c_skip
    minimises error amplification and c_noise is an empirical fit. Names
    the denoiser parameterisation and the loss weight, and records that
    the log-normal's parameters are tuned rather than derived. The
    recommendation is unchanged.
- version: 3
  date: '2026-09-10'
  note: >-
    Enriched from the #123 readings. The recommendation is unchanged;
    the source list, the numbers or the neighbourhood are.
tags:
- training-optimization
consensus: converged
date: '2026-09-08'
published: '2022-06-01'
source:
- LIT-075
# LIT-067 states the same requirement four months earlier and empirically:
# the implied x-prediction must stay stable as log-SNR varies. EDM derives
# coefficients that satisfy it; Progressive Distillation finds the criterion
# by watching epsilon-prediction fail at low SNR, and supplies v-prediction.
- LIT-067
implementations:
- EDM
- Stable Diffusion 3
extended_by:
- SOTA-195
---

# SOTA-188: Parametrize the network so its prediction target has unit variance at every noise level, and sample training noise from a log-normal

## Source

Karras et al. (2022), [LIT-075](../literature.d/LIT-075.md) — [ARXIV-2206.00364](https://arxiv.org/abs/2206.00364), NeurIPS 2022.

A denoiser is asked to do a different job at every noise level: at low noise
it must pass the input through almost unchanged, at high noise it must
predict the clean signal from something close to noise. Train one network on
both ends without adjusting for it and the loss is dominated by whichever
regime happens to have the largest raw magnitudes, and the gradients are
scaled inconsistently across the conditioning variable.

The paper's answer has two parts, and both are training-time:

- **Preconditioning.** Write the denoiser as
  `D(x;σ) = c_skip(σ)·x + c_out(σ)·F(c_in(σ)·x; c_noise(σ))`, so that the raw
  network `F` is a different function from the denoiser, and then *solve for*
  the scalings instead of tuning them. Two of the four follow from the
  unit-variance requirement this practice is named for — `c_in` makes the
  network's input unit-variance, `c_out` makes its training target
  unit-variance — and the network is then solving the same-sized problem at
  every noise level rather than one whose scale varies by orders of
  magnitude. The other two do not: `c_skip` is chosen to amplify `F`'s own
  error as little as possible, and `c_noise` is, in the paper's words,
  "chosen empirically". A fifth term, the loss weight `λ(σ)`, cancels
  `c_out`'s scaling so that every noise level contributes equally to the
  loss — which is what leaves the sampling distribution below as the only
  thing deciding where training compute goes.
- **The training-noise distribution.** Sample the noise level from a
  log-normal concentrated on the middle of the range, rather than uniformly.
  The extremes teach little — the near-clean end is trivial and the near-pure-
  noise end is nearly unlearnable — so uniform sampling spends most of the
  compute where there is least to learn.

Both are recorded here as `training-optimization` rather than as diffusion
trivia because the shape generalizes: **when a network is conditioned on a
variable that changes the difficulty of its task, normalize the target so the
loss means the same thing at every value, and sample that variable where the
signal is.** The paper is also the cleanest demonstration in the corpus that
separating sampler from training objective from architecture lets each be
tuned without disturbing the others.

## The requirement has an empirical statement four months earlier

[LIT-067](../literature.d/LIT-067.md) (Progressive Distillation, February 2022) reaches the same
requirement from the other direction, by watching `ε`-prediction break. As the
signal-to-noise ratio goes to zero, "the effect of small changes in the neural
network output on the implied prediction in x-space is increasingly amplified" —
so the criterion it states is that **the implied `x̂` must remain stable as
`λ_t = log(α²/σ²)` varies.**

That is `SOTA-188`'s subject in different words: EDM derives coefficients that
satisfy a unit-variance condition, and Progressive Distillation finds a
stability condition empirically and gives three parameterizations meeting it.
Whether the two conditions are the same or merely close is not written down
anywhere.

The practical consequence is [SOTA-195](SOTA-195.md) — predict `v` — which is what people
type, and which this practice's derivation explains.

## Conditions

The specific scalings and the log-normal's parameters are derived for the
schedule the paper adopts (`σ(t) = t`, `s(t) = 1`), and every coefficient is
a function of `σ` and a single data scale `σ_data` — 0.5 for the datasets
used. Carrying the *numbers* to a different noise parametrization is a
mistake; carrying the *principle* — make the target unit-variance, then
sample where the learning is — is the point.

The log-normal's parameters are tuned, not derived: `ln σ ~ N(−1.2, 1.2²)`
for these datasets. The shape has an argument behind it and the numbers do
not.

Reported at image scale, on ImageNet-64 and CIFAR-10. It is not an
autoregressive-language result and nothing in the record replicates it there,
which is a reason to read it for the shape rather than the recipe.

## Known implementations

- EDM and its successors; the log-normal timestep sampling is standard in the
  rectified-flow and diffusion-transformer lines that followed
