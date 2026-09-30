---
number: 124
status: Proposed
promote_when: >-
  A measurement of the memorization window at a second model scale, by
  anyone, so the linear-in-parameters assumption can be checked instead of
  assumed. The source offers one point and calls the scaling a conjecture.
consensus: contested
consensus_note: >-
  The source calls it a hypothesis with one measurement behind it and the
  systematic study future work — and two published positions now disagree.
  LIT-166 puts the bound at four epochs from 400 runs; LIT-175 says
  repetition overfits severely and the overfitting is a property of the
  objective. The three are not measuring the same quantity, which is why the
  disagreement is live rather than settled.
contested_by:
- LIT-166
- LIT-175
title: 'Repeat high-quality data freely when its epoch size exceeds the model''s memorization window'
version: 4
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-120 as well as LIT-119. The memorization-window measurement
    the practice turns on is Figure 9 of the Falcon-H1 report, not the tiny
    blogpost. LIT-166 and LIT-175 remain in the body: they are the positions
    this argues with, and ADR-010's rule is that contrast is not support. The
    recommendation is unchanged.
- version: 3
  date: '2026-09-08'
  note: >-
    Moved from `unreplicated` to `contested`, with `contested_by` naming
    LIT-166 and LIT-175. The note said "nobody has contradicted it either"
    while the body had argued with both papers for a month — the field moved
    and the axis did not. The recommendation is unchanged.
- version: 4
  date: '2026-09-19'
  note: >-
    The linear-in-parameters conjecture is now half-checked. Morris et al.
    (LIT-440) measure transformer storage capacity at ~3.6 bits per
    parameter and find it linear in parameter count across three orders of
    magnitude. That is the scaling assumption this practice was taking on one
    figure. It is not the window itself, which is a token count, and nobody
    has done the conversion — so `promote_when:` stands as written and the
    status does not move.
tags:
- data-pipeline
- tiny-models
- model-architecture
date: '2026-09-05'
source:
# The memorization-window measurement the whole practice turns on is Figure 9
# of LIT-120, not the blogpost. LIT-166 and LIT-175 are the positions this
# argues with, so they stay in the body (ADR-010).
- LIT-119
- LIT-120
introduced_by:
- LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Roughly 100–500 GT for a 7B model, scaling linearly; the authors call the understanding early.
---

# SOTA-124: Repeat high-quality data freely when its epoch size exceeds the model's memorization window

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

## What the memorization window is

A late checkpoint of FalconMamba-7B (Figure 9 of [LIT-120](../literature.d/LIT-120.md)), shown training tokens it saw earlier,
has a loss gap against fresh tokens from the same distribution that decays
with how long ago the tokens were seen. The authors define the
*memorization window* as the delay after which that gap has closed — around
100 GT, or 500 GT as a conservative estimate, for a 7B model — and argue
that a data source whose epoch size (its size divided by its share of the
mix) is larger than the window can be repeated indefinitely without the
model overfitting to it, while one with a small epoch size will be memorised.
The window is assumed to scale linearly with parameters, giving about 5 GT
at 100M.

This decouples the ceiling on the high-quality fraction of a mix from the
total training length, which is what [SOTA-123](SOTA-123.md) relies on. Falcon-H1-Tiny is
offered as an implicit confirmation: SFT sources such as Tulu3 were repeated
100 or more times across 800 GT of SFT-pretraining, and the
memorisation sweep (0 to 100% SFT, 2 GT epoch size at the extreme) showed
no degradation during training.

## Why this is Proposed, and what it argues with

The source is explicit that this is a hypothesis with one
measurement behind it and that the systematic study is future work. It is
filed because the recipes built on it are in the record and this is the
reason they give. The standing guidance it argues with is now in the record:
[LIT-166](../literature.d/LIT-166.md) finds four epochs nearly free and the value of added compute
decaying to zero thereafter, across 400 runs. The claim here is that the
relevant quantity is not epoch *count* but epoch *size* relative to the
window — a distinction that may dissolve the conflict, since that sweep
repeats a whole corpus at fixed compute while this is about one source
inside a mixture. Nobody has run the experiment that separates them.

[LIT-175](../literature.d/LIT-175.md) is a third position worth reading against both: that
autoregressive pretraining overfits severely under heavy repetition, and
that the overfitting belongs to the objective rather than to repetition,
removable with augmentation. If that is right, a recipe repeating a source a
hundred times is either augmenting implicitly or paying an unmeasured cost.

## The linear scaling is now half-checked

`promote_when:` above asks for a measurement of the window at a second model
scale, so the linear-in-parameters assumption can be checked rather than
assumed. Morris et al., [LIT-440](../literature.d/LIT-440.md), get part of the way there.

They measure transformer storage capacity by training on uniform random
bitstrings, where generalization is impossible and the information content is
exactly computable, and find **~3.6 bits per parameter, linear in parameter
count** across models spanning three orders of magnitude. That is the scaling
shape this practice was taking from a single figure.

It is not the window. Falcon's quantity is a token count — how much unique
data must sit between repeats of a source before repetition starts being
memorized. Morris's is a bit count — how much the model can hold at all. The
two are related through the information content of the tokens, and that
conversion is the step nobody has taken. So the conjecture is half-checked,
`promote_when:` stands as written, and the status does not move.
