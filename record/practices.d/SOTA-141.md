---
status: Proposed
title: 'Decay the learning rate linearly all the way to zero'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2025-02-01'
source: LIT-147
summary: >-
  Bergsma et al. (2025), [LIT-147](../literature.d/LIT-147.md) — with the peak tuned, linear decay to zero beats the customary decay to 10% and other shapes at compute-optimal budgets, more so past them; Proposed because contemporary production runs in the record still decay to a floor.
---

# SOTA-141: Decay the learning rate linearly all the way to zero

## Source

Bergsma et al. (2025), [LIT-147](../literature.d/LIT-147.md) — Straight to Zero.

The customary schedule decays the learning rate to 10% of its peak. In a
large empirical study across model sizes, batch sizes, datasets and
vocabularies, with the peak tuned for each schedule, linear decay to zero
consistently beat that and the other shapes tried at compute-optimal token
budgets, and by more the further training went past compute-optimal. The
reason offered: AdamW acts as an exponential moving average of updates,
early training must move away from the initialisation while late training
must average over enough updates to cancel gradient noise, and a floor at
10% leaves noise in the final weights that a decay to zero averages out.

Why *Proposed*: one group's study, and the frontier recipes filed in the
record still decay to a floor (Falcon-H1-Tiny's ×64 exponential decay,
[LIT-119](../literature.d/LIT-119.md)). The claim is compatible with WSD ([SOTA-140](SOTA-140.md)) — it is about the
end of the decay, not its start — and [LIT-145](../literature.d/LIT-145.md)'s cooldown to zero points the
same way. Promote when a production report adopts it or a second group
replicates it.
