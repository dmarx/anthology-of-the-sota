---
status: Active
formerly:
- SOTA-tmpm1xnl
title: 'Parametrize the network so its prediction target has unit variance at every noise level, and sample training noise from a log-normal'
version: 1
tags:
- training-optimization
consensus: converged
date: '2026-09-08'
source:
- LIT-075
implementations:
- EDM
- Stable Diffusion 3
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

- **Preconditioning.** Wrap the network in noise-level-dependent scalings of
  its input, output, skip connection and loss weight, chosen so the effective
  training target has unit variance at every level. The network is then
  solving the same-sized problem everywhere, rather than a problem whose
  difficulty and scale vary by orders of magnitude along the conditioning
  axis.
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

## Conditions

The specific scalings and the log-normal's parameters are derived for the
variance-exploding formulation the paper adopts. Carrying the *numbers* to a
different noise parametrization is a mistake; carrying the *principle* — make
the target unit-variance, then sample where the learning is — is the point.

Reported at image scale, on ImageNet-64 and CIFAR-10. It is not an
autoregressive-language result and nothing in the record replicates it there,
which is a reason to read it for the shape rather than the recipe.

## Known implementations

- EDM and its successors; the log-normal timestep sampling is standard in the
  rectified-flow and diffusion-transformer lines that followed
