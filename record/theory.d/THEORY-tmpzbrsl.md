---
status: Proposed
promote_when: >-
  A measurement of critical batch size at fixed token budget across model
  sizes well beyond 1.2B — the scale at which the muP argument predicts the
  flatness should continue and at which a width effect would be most likely
  to reappear; or a derivation of the data exponent for an adaptive optimizer
  on a transformer rather than for SGD on least squares. What would not
  settle it: another Chinchilla-line sweep reporting critical batch size
  growing with scale, which cannot distinguish the two variables and is the
  measurement this account explains away.
title: 'Critical batch size is set by how much data has been seen, not by how large the model is'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmphgpkf
- LIT-tmp5olz5
explains:
- SOTA-tmp0cq3b
summary: >-
  Zhang et al. (2024), [LIT-tmphgpkf](../literature.d/LIT-tmphgpkf.md) — under maximal update
  parameterization there is a width past which more width does not raise the
  batch a step can usefully absorb, while for mini-batch SGD on least squares
  under power-law source and capacity conditions the useful batch grows as a
  power of the sample count. Two arguments, one for each half of the split
  the measurements show.
---

# THEORY-tmpzbrsl: Critical batch size is set by how much data has been seen, not by how large the model is
<!-- inactive-ok-file: SOTA-tmpbfftm — Proposed, and named to say this account does NOT bear on where to operate below the ceiling -->

## Source

Zhang et al. (2024), [LIT-tmphgpkf](../literature.d/LIT-tmphgpkf.md) — [ARXIV-2410.21676](https://arxiv.org/abs/2410.21676).

Bergsma et al. (2025), [LIT-tmp5olz5](../literature.d/LIT-tmp5olz5.md) — [ARXIV-2505.13738](https://arxiv.org/abs/2505.13738), for the
independent measurement of the exponent.

## What was actually shown

**The empirical half is a decoupling.** Every previous measurement of
critical batch size was made along the Chinchilla line, where model size and
token budget grow together, so "it grows with scale" could not name which one
was responsible. Holding each fixed in turn: models of different sizes trained
on the *same* token count have nearly the same critical batch size, and at
fixed model size it rises with tokens. The fitted law in model size at fixed
data is nearly flat; the law in data is not.

This could have come out otherwise, and the confounded version of the
experiment had been reported for years as though it had. It is also confirmed
from the other direction: Bergsma et al. fit `D^0.47` where this gets
`D^0.462`, from a different architecture, corpus, context length,
parameterization and schedule.

**The theoretical half is two arguments doing different jobs.** Under maximal
update parameterization, past some width, increasing width at fixed data does
not further increase critical batch size — which accounts for the flatness in
model size. For mini-batch SGD on least squares under power-law source and
capacity conditions, the batch size that reaches minimal excess risk at
fastest serial runtime grows as `n^a` in the sample count, with `a` explicit
in the variance-dominated regime — which accounts for the growth in data.

## The picture it installs

The quantity that sets how much parallelism a step can absorb is the
signal-to-noise of the gradient estimate, and that is a property of how much
the model has already learned from data rather than of how much capacity it
has. A larger model does not average its gradient over more samples. It fits
the same samples better, and in practice it is given more of them — which is
where the appearance of a model-size effect comes from.

## What this does not say

**It does not say model size is irrelevant, only that it is nearly flat over
85M to 1.2B at fixed data.** "Weakly dependent" is the measured statement.
The muP argument predicts flatness past a width without saying where that
width is, and nothing tests whether the flatness survives an order of
magnitude further up.

**The theory is not about the systems the experiments run.** The `n^a` result
is for mini-batch SGD on least squares under power-law source and capacity
conditions. The experiments are Adam on transformers. The two are offered as
consistent, which they are; neither derives the other, and the measured
exponent is not predicted by the analysis.

**It does not overturn the gradient-noise-scale account, it relocates it.**
[SOTA-198](../practices.d/SOTA-198.md) says to measure the noise scale and expect it to grow during a
run. A noise scale rising through training is exactly what "critical batch
size grows with tokens seen" looks like from inside a run — so that
observation is evidence *for* this account, and what changes is the variable a
practitioner should plan from, not the instrument.

**It says nothing about where to operate below the ceiling.** Critical batch
size is a speed-against-efficiency boundary. [SOTA-tmpbfftm](../practices.d/SOTA-tmpbfftm.md) argues from a
different source that the useful operating point is far below it, and nothing
in this account bears on that.

**The absolute level is convention.** Critical batch size is defined against a
chosen overhead threshold, so two studies agreeing on the exponent can
prescribe different batch sizes. The exponent is the part two groups have
checked.

## Why `Proposed`

The measurement is strong and the account is partial. What is established is
that the split falls on the data side over the range tested, by a controlled
experiment whose design was aimed at exactly this question, corroborated
independently. What is offered as explanation is one asymptotic argument about
width that does not say where "past a certain width" begins, and one exact
result in a setting several steps removed from the one measured.

That is enough to explain [SOTA-tmp0cq3b](../practices.d/SOTA-tmp0cq3b.md) and to say why the old compute
exponent fitted a projection. It is not yet enough to predict the exponent,
which is what would make this `Active`.
