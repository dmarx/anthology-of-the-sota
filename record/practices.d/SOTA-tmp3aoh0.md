---
status: Proposed
promote_when: >-
  A second lineage reporting a scale-dependent clip value, from a run family
  that varied the clip deliberately rather than reporting the value it
  settled on. The cheapest version: one model size trained twice, at the
  small-scale clip and the tightened one, with the loss curves. What would
  NOT meet it: another large model report stating its own clip value, which
  is adoption of a number rather than evidence about the relationship.
title: 'Tighten the gradient-norm clip as the model grows rather than carrying one value across scales'
version: 1
tags:
- model-stability
- training-optimization
date: '2026-09-24'
source:
- LIT-tmpkxt2i
introduced_by:
- LIT-tmpkxt2i
consensus: unreplicated
consensus_note: >-
  One group, one run family, and the value is reported rather than ablated —
  the paper says the clip was reduced "for improved stability" at 7.1B and
  280B without showing the run that failed at 1.0. Against that: no held
  practice names a clip value at all, so the field's default here is silence
  rather than a competing number. `unreplicated` is the honest reading and
  the `promote_when` asks for the ablation nobody has published.
extends:
- SOTA-035
implementations:
- gopher
summary: >-
  Rae et al. (2021), [LIT-tmpkxt2i](../literature.d/LIT-tmpkxt2i.md) — the Gopher family clipped the global
  gradient norm at 1.0 for models up to 1.4B and at **0.25 for the 7.1B and
  280B models**, "for improved stability". Three held practices say to clip
  and none names a value; this is the first number in the record, and it is
  not a constant.
---

# SOTA-tmp3aoh0: Tighten the gradient-norm clip as the model grows rather than carrying one value across scales

## Source

Rae et al. (2021), [LIT-tmpkxt2i](../literature.d/LIT-tmpkxt2i.md), §3.2.

## When this applies

You are training a dense autoregressive transformer past a few billion
parameters, you clip the global gradient norm, and you inherited the clip
value from a smaller run or from a framework default.

## Do this

**Treat the clip value as scale-dependent.** The Gopher family used 1.0 up to
1.4B and **0.25 at 7.1B and 280B** — a 4× tightening across roughly two
orders of magnitude of parameters, introduced because the large runs needed
it for stability.

What makes this worth filing rather than noting: **three practices in this
record tell you to clip and not one of them names a value.** [SOTA-035](SOTA-035.md) says to
clip, [SOTA-071](SOTA-071.md) says to use a dynamic threshold. A reader following them has
to pick a number, and the number they will pick is a framework default set
for models much smaller than the one they are training.

## Why it is only `Proposed`

The evidence is a reported configuration, not an ablation. Rae et al. state
the value and the reason in one sentence and do not show the 1.0 run
diverging, so what is established is that **one group found 1.0 insufficient
at 7.1B and above** — not the shape of the relationship, not where the
threshold sits, and not whether 0.25 is near-optimal or merely sufficient.

The direction is corroborated indirectly by everything else in the same
paragraph moving the same way with scale — the maximum learning rate falls
from `6×10⁻⁴` to `4×10⁻⁵` across the same family — but that is a pattern
about hyperparameters generally, not evidence about clipping.

## Limitations

- **The clip and the learning rate moved together**, and the paper does not
  separate them. A reader who tightens the clip while holding the learning
  rate at a small-model value is not reproducing this configuration.
- **Dense decoder-only transformers in bfloat16**, trained with Adam. The
  same family also used stochastic rounding and later reported it cost
  performance, so the numerical setting these values were tuned inside is not
  one the record recommends.
- **It says nothing about *why*.** A tighter clip at scale is consistent with
  larger gradient-norm outliers, with a longer unstable early phase, or with
  the clip standing in for a learning-rate problem. Nothing here distinguishes
  them, and [SOTA-071](SOTA-071.md)'s dynamic threshold is a different answer to what may be
  the same question.
