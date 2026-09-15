---
status: Rejected
status_note: the experiment that would have confirmed it was eventually run, and the benefit survived the shift being put back
title: 'Batch normalization works by reducing internal covariate shift'
version: 1
tags:
- model-stability
date: '2026-09-15'
source:
- LIT-002
summary: >-
  Ioffe and Szegedy (2015), [LIT-002](../literature.d/LIT-002.md) — the explanation batch normalization was
  named after and introduced with: that training is slowed by each layer's
  input distribution shifting as the layers below it update, and that holding
  those distributions steady is what buys the speed. Refuted in 2018;
  the technique was not.
corrected_by:
- THEORY-tmpn1kz1
---

# THEORY-tmp69thf: Batch normalization works by reducing internal covariate shift

## Source

Ioffe and Szegedy (2015), [LIT-002](../literature.d/LIT-002.md) — the paper that introduced the technique,
in which this account is not an aside but the title.

## The account, as it was stated

Each layer's input distribution moves while the layers beneath it train. The
paper names this internal covariate shift and argues it is a first-order
obstacle: a layer is forever re-adapting to a moving input, small learning
rates are what keep the movement survivable, and saturating nonlinearities
make it worse. Normalising each layer's inputs to a fixed mean and variance
holds the distributions still, so the re-adaptation stops being the
bottleneck and larger rates become usable.

It is a good explanation. It predicts the right things — faster convergence,
higher learning rates, less sensitivity to initialization, all of which
[LIT-002](../literature.d/LIT-002.md) demonstrates — and it explains them by a mechanism that is easy to
picture, which is most of why it was repeated in every subsequent treatment
for three years.

## Why this is rejected

Santurkar et al. ([THEORY-tmpn1kz1](THEORY-tmpn1kz1.md)) tested the mechanism rather than the
predictions, by putting the covariate shift back: noise injected after each
BN layer, non-zero-mean and time-varying, restoring exactly the instability
BN was supposed to be removing. The network trained anyway. Their conclusion
is flat — "distributional stability of layer inputs has little to do with the
success of BatchNorm."

What is rejected is the account, and only the account. Every effect [LIT-002](../literature.d/LIT-002.md)
reported is real and reproduces, the technique is standard, and the practices
drawn from it are `Active`. This document exists so that the record can hold
those two facts at once, which it could not while an explanation had nowhere
to live but the practice that rests on it ([DP-003](../../docs/design-principles.md#dp-3)).

## What this does not say

It does not say internal covariate shift is not a real phenomenon — layer
input distributions do move during training, and nothing here disputes that.
The rejected claim is causal: that the movement is what limits training, and
that arresting it is what BN's benefit consists of.

It also does not say the authors were careless. The explanation was the
natural reading of the evidence they had, and what unseated it was an
experiment nobody had thought to run for three years. The instructive part is
how long a plausible mechanism survives when every prediction it makes keeps
coming true for a different reason.
