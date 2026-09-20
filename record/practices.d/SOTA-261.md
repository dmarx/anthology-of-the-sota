---
number: 261
status: Proposed
formerly:
- SOTA-tmpuz5ea
promote_when: >-
  A second group fitting the normalized AdamW timescale against
  tokens-per-parameter and reporting an exponent, or a pretraining report
  that says it set weight decay this way. What would not move it: another
  paper reporting a better weight decay at one scale, which is the kind of
  result this replaces with a law.
consensus: unreplicated
consensus_note: >-
  One group, one architecture family, one corpus. The law is fitted over
  three orders of magnitude of compute with four held-out points on it, which
  is unusually strong for an unreplicated result, and it reproduces two
  previously published hyperparameter-scaling relations as special cases.
title: 'Set AdamW''s weight decay by targeting a timescale that follows a power law in tokens-per-parameter'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-443
introduced_by:
- LIT-443
implementations: []
summary: >-
  Bergsma et al. (2025), [LIT-443](../literature.d/LIT-443.md) — under AdamW the weights are an
  EMA of updates with timescale `1/(eta*lambda)`, and the fraction of
  training it averages, `tau = 1/(eta*lambda*S)`, is the quantity that
  scales. It follows a power law in tokens-per-parameter with exponent about
  -0.52 across three orders of magnitude of compute, so weight decay can be
  read off in advance rather than swept.
---

# SOTA-261: Set AdamW's weight decay by targeting a timescale that follows a power law in tokens-per-parameter
<!-- inactive-ok-file: SOTA-255 — Proposed, and the practice whose stated gap this one does and does not close; the distinction is the section -->

## Source

Bergsma et al. (2025), [LIT-443](../literature.d/LIT-443.md) — [ARXIV-2505.13738](https://arxiv.org/abs/2505.13738).

## Why weight decay is the wrong thing to hold constant

An AdamW update can be read as an exponential moving average over past
updates, with timescale `τ = 1/(η λ)` measured in steps. Normalized by the
total step count, `τ̃ = τ/S = 1/(η λ S)` is the *fraction* of training that
survives into the final weights.

That is the quantity with a meaning. `λ = 0.1` is not a policy held fixed
across scales; it is a policy that drifts with whatever `η` and `S` happen to
be, which is why the inherited constant keeps needing a local sweep.

## The law

Over tokens-per-parameter ratios from 20 to 1280:

    τ̃_opt ∝ TPP^(−0.52)

with `R² = 0.975` and bootstrapped 10th/90th percentiles on the exponent of
(−0.529, −0.507). Roughly 1.0 at 1 TPP, falling to 0.01 at 1000 TPP. Weight
decay follows from `τ̃`, the muP-transferred learning rate and the step count.

**The held-out points are what make this worth acting on.** Four
configurations not used in the fit, including a 3.3B model at 30 TPP
requiring about 1000× the FLOPs of the nearest fitted point, sit on the line.
A hyperparameter law that survives three orders of magnitude of compute is a
different object from one fitted where it was measured.

A secondary finding travels with it: **given muP, spend the sweep on `λ`
rather than on `η`.** Tuning `λ` at the transferred learning rate beat tuning
`η` at a default `λ = 0.1` in 6 of 8 cases — though the margins are a few
thousandths of a nat, so the reportable claim is that tuning `λ` alone is
sufficient rather than that it is much better.

## Where this does and does not meet [SOTA-255](SOTA-255.md)

[SOTA-255](SOTA-255.md) records Kim et al.'s finding that optimal weight decay under data
constraint is around 30× the inherited 0.1, and its conditions say plainly
that the paper "gives no way to predict the optimum from the
parameter-to-token ratio, so the practice is really *sweep it, and sweep
upward*". This is a law in exactly that ratio, and the temptation is to treat
it as the missing rule.

**It is not, and the record should not compose them.** This study normalizes
by `S` on the stated ground that "LLM pre-training only uses one epoch of
data", and fits from 20 to 1280 TPP — Chinchilla-optimal and above. Kim et
al. epoch a fixed corpus many times at parameter-to-token ratios *above*
Chinchilla, which is TPP below 20 and often below 1. Two disjoint regimes,
two different assumptions about repetition, and no published check that
either extrapolates into the other.

What the record holds now is two well-measured answers to "how should weight
decay move under data pressure", from opposite ends of the tokens-per-parameter
axis, and an unexamined gap between them. Naming the gap is more useful than
splitting the difference.

## Conditions, and why this is `Proposed`

**muP is a precondition, not a detail.** The claim that `λ` is the thing to
tune is made *given* that the learning rate has already been transferred from
a proxy. Without muP the learning rate is still in play and the argument does
not start.

Single-epoch only. One architecture family (GPT-2-like with ALiBi and
SwiGLU), one corpus, one schedule shape, largest model 3.3B. The exponent is
a fit; nothing claims it is a constant of nature, and the *level* of the law
has not been checked by anyone.

`τ̃` is computed at peak learning rate because it varies through decay — an
implementation detail that will silently produce the wrong answer if
overlooked.

## Known implementations

- None in the record. Every pretraining report it holds that states a weight
  decay states a constant.
