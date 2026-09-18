---
status: Active
title: 'Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning'
version: 1
tags:
- model-stability
date: '2026-09-18'
published: '2015-06-01'
arxiv: '1506.02142'
first_author: 'Gal'
keywords:
- 'dropout'
- 'bayesian-deep-learning'
- 'gaussian-processes'
- 'variational-inference'
- 'uncertainty'
implementations: []
summary: >-
  Gal and Ghahramani (2015), [ARXIV-1506.02142](https://arxiv.org/abs/1506.02142), ICML 2016. Casts dropout
  training as approximate variational inference in a deep Gaussian process,
  which makes an already-trained dropout network a Bayesian model whose
  uncertainty can be read out by sampling at test time — information the
  standard procedure discards. Improved predictive log-likelihood and RMSE
  over the then-standard methods, plus a deep-RL application. The derivation
  is the contribution; whether the uncertainty it yields is *good* uncertainty
  is a separate question this paper does not settle.
---

# LIT-tmpffawr: Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning

Gal and Ghahramani (2015) — [ARXIV-1506.02142](https://arxiv.org/abs/1506.02142), ICML 2016

## Key takeaways

- **The framework.** Dropout training in a deep network is cast as
  approximate Bayesian inference in a **deep Gaussian process**. The
  objective a dropout network already minimizes is, up to scaling, the
  variational objective for a particular approximating distribution over the
  weights.

- **The consequence that made it famous.** If dropout training *is*
  approximate variational inference, then a network trained with dropout is
  already a Bayesian model and nothing extra needs training. Keeping dropout
  **on at test time** and sampling gives draws from an approximate posterior
  predictive — the practice later known as MC dropout. The paper's own
  framing: this extracts "information from existing models that has been
  thrown away so far."

- **What it costs: nothing structural.** No change to the architecture, the
  training procedure, or the loss. The price is `T` forward passes at
  inference instead of one.

- **What was measured.** Regression and classification across various
  architectures and non-linearities, with MNIST as the worked example, plus a
  deep reinforcement-learning application. Reported as a considerable
  improvement in predictive log-likelihood and RMSE against the
  then-state-of-the-art.

## Standing in the anthology

The third account of dropout the record holds, and the one whose standing is
least settled — which is why it is filed with its scope stated rather than
with its reputation.

**It answers a different question from the other two.**
[THEORY-016](../theory.d/THEORY-016.md) explains why one scaled forward pass
substitutes for an ensemble, and [THEORY-015](../theory.d/THEORY-015.md)
explains what dropout does to the objective. This explains what the *stochastic
procedure* is, probabilistically, and it is the only one of the three that
turns into a test-time capability rather than a training-time account.

**The three are not independent**, and the pattern the record already recorded
for the first two applies here too from a different direction: the
ensemble-averaging reading and the Bayesian reading are both ways of saying
that the dropout network stands in for a distribution over networks. What
differs is what each licenses.

The critical literature on whether MC-dropout uncertainty is well-calibrated —
and on whether the implied posterior behaves like a posterior as data grows —
is real and **the record holds none of it**. That is the reason
[THEORY-tmpre9uh](../theory.d/THEORY-tmpre9uh.md) states the derivation and
declines the application.
