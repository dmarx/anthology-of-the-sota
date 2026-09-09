---
number: 41
status: Rejected
status_note: >-
  States the opposite of its source. Kaplan reports that larger models
  require a *smaller* learning rate to prevent divergence, and carries an
  explicit size-dependent rule LR(N) because the right rate is not
  size-independent
title: 'lr tuning less important for larger models'
version: 2
history:
- version: 2
  date: '2026-09-09'
  note: >-
    Rejected on reading the source (#114). Kaplan says larger models
    require a SMALLER learning rate to prevent divergence, and
    implements LR(N) = 0.003239 - 0.0001395*log(N) for exactly that
    reason. The practice conflated schedule-insensitivity — measured on
    a 3M-parameter model — with rate-insensitivity, and reversed the
    direction.
tags:
- training-optimization
date: '2026-08-24'
published: '2020-01-01'
source:
- LIT-028
compared_against:
- SOTA-040
summary: >-
  Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).
---

# SOTA-041: lr tuning less important for larger models

## Source

Kaplan et al. (2020), [LIT-028](../literature.d/LIT-028.md) — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).

## Why this is rejected: the source says the reverse

[LIT-028](../literature.d/LIT-028.md), Appendix D.6:

> We found that **larger models require a smaller learning rate to prevent
> divergence**, while smaller models can tolerate a larger learning rate.

And it carries an explicit size-dependent rule, used for most of its runs
(Eq. D.1):

    LR(N) ≈ 0.003239 − 0.0001395·log(N)

A paper that computes the learning rate from the parameter count is not a
paper saying the learning rate matters less as the parameter count grows. It
also notes the rule "breaks down for `N > 10¹⁰` parameters" — below every
frontier model in this record — and separately that "the optimal choice of
learning rate is sensitive to the target loss". The word `insensitive` does
not occur in it.

## Two conflations produced the practice

**Schedule for rate.** What Kaplan calls "mostly irrelevant" is the *shape* of
the decay, given a warmup and a final decay to near-vanishing rate — not the
peak value. That scan is Figure 22, on a **3 million parameter model**, with
run-to-run variation at 0.05 loss.

**Direction.** "Less important for larger models" reverses the finding. Larger
models have *less* headroom before divergence, not more.

## What survives, and where it lives

The idea below — that hyperparameter transfer across scale is what makes
large-model practice tractable — is real, and the record holds it properly
<!-- inactive-ok-block: SOTA-144, SOTA-159 — Proposed, cited as where the transfer claim actually lives with a source -->
sourced elsewhere: µP ([SOTA-144](SOTA-144.md), [SOTA-159](SOTA-159.md)) makes transfer a property of the
parameterisation rather than a hoped-for flatness. `LR(N)` is the hand-fitted
ancestor of that, and the honest lineage runs from this paper's rule of thumb
to µP — not from a flatness claim the paper never made.

## The superseded reasoning

### The original argument, unsourced

The power-law fits in [LIT-028](../literature.d/LIT-028.md) flatten near the optimum as model size grows:
the loss penalty for being some factor away from the best learning rate is
smaller for a larger model than for a smaller one. So a rate tuned at one
scale is less wrong at the next, and the sweep that a small model needs is
worth less on a large one.

This is the observation that made large-model hyperparameter practice
tractable at all, and it is the empirical ancestor of a stronger idea the
<!-- inactive-ok-block: SOTA-144, SOTA-159 — Proposed, cited as the µP line this observation is the empirical ancestor of -->
record holds elsewhere: µP ([SOTA-144](SOTA-144.md), [SOTA-159](SOTA-159.md)) makes transfer a property of
the parameterisation rather than a lucky flatness, so the rate is measured on
a small proxy and carried over by construction.

## What it should not be read as

Not "large models do not need tuning". The penalty for a badly wrong rate is
still large, and the cost of a wrong choice is far higher at scale because
there is no second run. Less sensitive is not insensitive.

And the claim is about the *learning rate*, not about hyperparameters
generally. Batch size ([SOTA-062](SOTA-062.md)), weight decay and the schedule shape
([SOTA-140](SOTA-140.md)) do not obviously inherit it, and the record has no source saying
they do.
