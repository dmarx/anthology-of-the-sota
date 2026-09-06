---
status: Proposed
promote_when: >-
  A measurement of the memorization window at a second model scale, by
  anyone, so the linear-in-parameters assumption can be checked instead of
  assumed. The source offers one point and calls the scaling a conjecture.
title: 'Repeat high-quality data freely when its epoch size exceeds the model''s memorization window'
version: 1
tags:
- data-pipeline
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
- LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Roughly 100–500 GT for a 7B model, scaling linearly; the authors call the understanding early.
---

# SOTA-124: Repeat high-quality data freely when its epoch size exceeds the model's memorization window

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

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

Why *Proposed*: the source is explicit that this is a hypothesis with one
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
