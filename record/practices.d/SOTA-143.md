---
number: 143
status: Active
title: 'Parameterize the model with µP and tune hyperparameters on a narrow proxy, transferring them across width'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Adds a measurement of the hedge this practice already carried. The
    Conditions said transferred values are "a starting point that production
    recipes then adjust", on the evidence of production reports. LIT-501
    sweeps ten µP-coordinated learning rates across four SiT sizes with ten
    seeds each and finds the optimum is a 1.7x-wide window rather than a
    point, because seed variance blurs it into a flat region -- and that
    selecting the rate on single-seed unguided FID lands on the edge of
    training stability. The recommendation is unchanged; what changes is that
    its resolution is now measured on one family instead of described.
tags:
- training-optimization
date: '2026-09-05'
source:
- LIT-148
- LIT-501
introduced_by:
- LIT-148
summary: >-
  Yang and Hu (2022), [LIT-148](../literature.d/LIT-148.md) — under the Maximal Update Parametrization the optimal learning rate and friends are stable across width, so tune small and transfer zero-shot; GPT-3 6.7B beaten at 7% of its pretraining cost in tuning. Used by Falcon-H1, MiniCPM and the Power scheduler.
extended_by:
- SOTA-144
- SOTA-159
explained_by:
- THEORY-024
- THEORY-tmp9m644
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

**The optimum transfers as a window, not a point, and the width of that
window has now been measured.** [LIT-501](../literature.d/LIT-501.md) sweeps ten
µP-coordinated learning rates over `[5×10⁻⁵, 5×10⁻⁴]` across four SiT sizes
with ten training seeds per cell. Under a per-cell tuned FID the valleys are
flat-bottomed near `2–3×10⁻⁴` at every size, with the two rates flanking each
minimum sitting inside its seed envelope — three adjacent learning rates share
the per-size best, a **1.7× window**. µP transfers the optimum; what it
transfers is a region.

Two riders from the same sweep. Selecting the rate on *unguided* single-seed
FID gives a monotone curve whose argmin sits at the right edge, `5×10⁻⁴`,
which is also where 3 of 10 small-model seeds diverge — a confident-looking
number pointing at the edge of stability. And the seed variance does **not**
dip at the optimal rate: it is 1.7–2.3% there, inside the general floor, so
the flat region is not a low-variance region. This is one family at 100k
steps and is a measurement of this practice's resolution, not a challenge to
its claim; [SOTA-307](../practices.d/SOTA-307.md) carries the underlying variance result.

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
