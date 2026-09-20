---
number: 144
status: Proposed
promote_when: >-
  A run at a realistic token budget — not 300M tokens — under CompleteP-style
  depth scaling, reporting that the transferred learning rate is still the
  right one at the end of training. The independence question is now answered
  (LIT-tmpfv7vs); what `Proposed` means here is that validation at scale is
  missing, and every depth sweep in the record so far is deep and short. What
  would not settle it: another short depth sweep, or a result reaching depth
  transfer by a different mechanism — LIT-153 did that, and two routes to one
  property is evidence the property is reachable, not that this route works.
consensus: emerging
consensus_note: >-
  A second, independent group (LIT-tmpfv7vs) derives the same depth scaling
  from its own spectral framework and reports depth transfer to 256 layers
  across four optimizers. Not `converged`: still no production report in the
  record trained under it, and no run at a realistic token budget.
title: 'Extend µP''s transfer to depth with CompleteP so one sweep serves deeper models too'
version: 2
history:
- version: 2
  date: '2026-09-20'
  note: >-
    Consensus from `unreplicated` to `emerging`, and `promote_when` rewritten
    to name what is actually left. Zheng et al. (LIT-tmpfv7vs) are an
    independent group — Renmin University and ByteDance Seed, no overlap with
    the CompleteP authors — who derive the same depth scaling from an
    independent spectral framework and report learning-rate transfer to 256
    layers. Status stays `Proposed`. The old `promote_when` asked for a group
    "training under CompleteP itself"; what arrived trains Muon-Kimi-AdamW,
    Muon-AdamW, Shampoo-AdamW and Sophia under a condition the paper says
    "recovers CompleteP-style results", the hedge being its own word, and
    explicitly not AdamW. That is corroboration of the route by a wider set of
    optimizers rather than the literal test, and the letter of the old field
    is not counted as met. A section below records the difference.
tags:
- training-optimization
date: '2026-09-05'
source:
- LIT-150
introduced_by:
- LIT-150
# CompleteP is the depth exponent that makes µP's transfer hold
# across depth as well; the title says extend and the Source says how.
extends:
- SOTA-143
summary: >-
  Dey et al. (2025), [LIT-150](../literature.d/LIT-150.md) — the depth exponent α = 1 transfers the optimal learning rate across depth and keeps deep layers learning; 11.8% fewer FLOPs than µP at optimal shapes, 34.4% at 179 layers. One group so far.
explained_by:
- THEORY-tmpmnsb5
extended_by:
- SOTA-tmpnjlal
---

# SOTA-144: Extend µP's transfer to depth with CompleteP so one sweep serves deeper models too

## Source

Dey et al. (2025), [LIT-150](../literature.d/LIT-150.md) — CompleteP.

## What CompleteP changes

µP ([SOTA-143](SOTA-143.md)) transfers hyperparameters across width; across depth, as
commonly used, it does not — the optimal base learning rate moves, and deep
layers can learn lazily, barely leaving their initialisation. CompleteP, the
parametrization with depth exponent α = 1, gives depth-wise transfer and
non-lazy learning in every layer. Against µP it saves 11.8% of FLOPs for
optimally shaped models and 34.4% for a 179-layer one, and it keeps a wider
range of width-to-depth ratios compute-efficient, so shape can follow the
hardware.

## Why this is Proposed

One group and one paper, and no production report in the
record is trained under it.

## A result that does not count

One result has already arrived that does not count, and is worth naming so
the next reader does not count it either. [LIT-153](../literature.d/LIT-153.md) reports improved learning-rate transfer across widths
*and depths* from an independent group — the same property this practice
claims, by an unrelated mechanism (pinning weight-matrix norms rather than
a depth exponent). Two routes to one property is evidence the property is
reachable, not evidence that this route works.
The question it answers — how deep to go at a fixed budget — is the one
<!-- inactive-ok: SOTA-125 — a Proposed practice, named as the ablation this would replace -->
[LIT-119](../literature.d/LIT-119.md) settled by ablation ([SOTA-125](SOTA-125.md)), and the reason to want it is to
stop ablating.

## The independent derivation, and what it does and does not settle

*(Added at v2.)* Zheng et al., [LIT-tmpfv7vs](../literature.d/LIT-tmpfv7vs.md), reach this
parameterization from a different direction: a spectral condition on RMS
operator norms under joint width-depth scaling, derived with elementary
linear algebra rather than the machinery [LIT-150](../literature.d/LIT-150.md) used. CompleteP-style
scaling comes out as the case where a residual branch holds two or more
transformations. They sweep depth from 4 to 256 on GPT-2-style models under
Muon-Kimi-AdamW, Muon-AdamW, Shampoo-AdamW and Sophia, and the optimal base
learning rate holds.

**Settled**: that this is not one group's result. The derivation is
independent, the optimizers are different, and the depth range is larger than
[LIT-150](../literature.d/LIT-150.md)'s. `consensus` moves to `emerging` on that.

**Not settled**: the scale. Every run is 300M tokens. The original
`promote_when` was written about independence because that was the visible
weakness; the weakness that remains is that no depth sweep in the record,
from either group, runs long enough to say the transferred value is still
right at the end of a real training run. That is now what `promote_when`
asks for.

**Not claimed**: that CompleteP itself was replicated. The paper's own word is
"recovers CompleteP-style results", and it does not run AdamW — the optimizer
[LIT-150](../literature.d/LIT-150.md) defined the exponent for — on the grounds that prior work
covered it. The record counts this as corroboration of the route and not as
the literal test, and says so here rather than quietly treating the field as
discharged.
