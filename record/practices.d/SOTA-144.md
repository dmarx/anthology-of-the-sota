---
status: Proposed
title: 'Extend µP''s transfer to depth with CompleteP so one sweep serves deeper models too'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2025-05-01'
source:
- LIT-150
summary: >-
  Dey et al. (2025), [LIT-150](../literature.d/LIT-150.md) — the depth exponent α = 1 transfers the optimal learning rate across depth and keeps deep layers learning; 11.8% fewer FLOPs than µP at optimal shapes, 34.4% at 179 layers. One group so far.
---

# SOTA-144: Extend µP's transfer to depth with CompleteP so one sweep serves deeper models too

## Source

Dey et al. (2025), [LIT-150](../literature.d/LIT-150.md) — CompleteP.

µP ([SOTA-143](SOTA-143.md)) transfers hyperparameters across width; across depth, as
commonly used, it does not — the optimal base learning rate moves, and deep
layers can learn lazily, barely leaving their initialisation. CompleteP, the
parametrization with depth exponent α = 1, gives depth-wise transfer and
non-lazy learning in every layer. Against µP it saves 11.8% of FLOPs for
optimally shaped models and 34.4% for a 179-layer one, and it keeps a wider
range of width-to-depth ratios compute-efficient, so shape can follow the
hardware.

Why *Proposed*: one group and one paper, with no production report in the
record trained under it. Promote on an independent depth-transfer result.
The question it answers — how deep to go at a fixed budget — is the one
<!-- inactive-ok: SOTA-125 — a Proposed practice, named as the ablation this would replace -->
[LIT-119](../literature.d/LIT-119.md) settled by ablation ([SOTA-125](SOTA-125.md)), and the reason to want it is to
stop ablating.
