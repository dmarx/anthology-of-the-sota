---
status: Active
title: 'Parameterize the model with µP and tune hyperparameters on a narrow proxy, transferring them across width'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2022-03-01'
source:
- LIT-148
summary: >-
  Yang and Hu (2022), [LIT-148](../literature.d/LIT-148.md) — under the Maximal Update Parametrization the optimal learning rate and friends are stable across width, so tune small and transfer zero-shot; GPT-3 6.7B beaten at 7% of its pretraining cost in tuning. Used by Falcon-H1, MiniCPM and the Power scheduler.
---

# SOTA-143: Parameterize the model with µP and tune hyperparameters on a narrow proxy, transferring them across width

## Source

Yang and Hu (2022), [LIT-148](../literature.d/LIT-148.md) — Tensor Programs V.

Scale initialisation variances and per-layer learning rates with width the
way the Maximal Update Parametrization prescribes, and the optimal
learning rate — along with several other hyperparameters — stops moving as
the model gets wider. Then tune on a narrow proxy and transfer the values
to the full model without tuning it: the paper beats the published
BERT-large from a 13M-parameter sweep, and the published GPT-3 6.7B from a
40M-parameter sweep at about 7% of the large model's pretraining cost.

Conditions: transfer is across *width*. Depth, batch size and training
<!-- inactive-ok: SOTA-144 — a Proposed extension of µP transfer, named as part of the chain -->
duration are not covered by the original result — [LIT-150](../literature.d/LIT-150.md) ([SOTA-144](SOTA-144.md))
extends it to depth, and [LIT-146](../literature.d/LIT-146.md) ([SOTA-142](SOTA-142.md)) handles tokens and batch size
by a separate law. The multipliers µP fixes are what Learnable Multipliers
<!-- inactive-ok: SOTA-122 — a Proposed practice, named as the variation that learns the multipliers -->
([LIT-121](../literature.d/LIT-121.md), [SOTA-122](SOTA-122.md)) proposes to learn instead. In practice the transferred
values are a starting point that production recipes then adjust: Falcon-H1
tuned 35 multipliers and Falcon-H1-Tiny carried them to 90M through the
forward multipliers with learning rate and weight decay held fixed ([LIT-119](../literature.d/LIT-119.md)).

## Sequence and variations

µP (this) → u-µP ([LIT-149](../literature.d/LIT-149.md)): add Unit Scaling so the sweep becomes
<!-- inactive-ok: SOTA-144 — a Proposed extension of µP transfer, named as part of the chain -->
one-dimensional and FP8 works out of the box → CompleteP ([SOTA-144](SOTA-144.md)): the
depth exponent that makes transfer hold across depth as well.

## Known implementations

- Falcon-H1, Falcon-H1-Tiny; MiniCPM; PowerLM; Cerebras-GPT
