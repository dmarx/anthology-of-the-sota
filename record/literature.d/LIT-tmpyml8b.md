---
status: 'Deferred'
title: 'Bayesian Learning via Stochastic Gradient Langevin Dynamics'
version: 1
tags:
- training-optimization
date: '2026-09-15'
published: '2011-06-01'
url: 'https://icml.cc/2011/papers/398_icmlpaper.pdf'
first_author: 'Welling'
keywords:
- 'langevin'
- 'posterior-sampling'
- 'stochastic-gradient'
- 'uncertainty'
implementations: []
summary: >-
  Welling and Teh (2011), [Bayesian Learning via Stochastic Gradient Langevin
  Dynamics](https://icml.cc/2011/papers/398_icmlpaper.pdf). Adding correctly
  scaled Gaussian noise to a decaying-step-size SGD update turns the optimizer
  into a posterior sampler, with no accept-reject step.
---
# LIT-tmpyml8b: Bayesian Learning via Stochastic Gradient Langevin Dynamics

Welling and Teh (2011) — [Bayesian Learning via Stochastic Gradient Langevin Dynamics](https://icml.cc/2011/papers/398_icmlpaper.pdf)

## What it is

Adding correctly scaled Gaussian noise to a decaying-step-size SGD update
turns the optimizer into a posterior sampler, with no accept-reject step.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the Langevin branch, where the training noise is the sampler.

