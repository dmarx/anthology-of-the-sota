---
number: 141
status: Proposed
promote_when: >-
  A frontier training report that decays to zero and says so, or a second
  group's schedule comparison with the peak retuned per schedule. A decay-
  to-zero result sharing one peak learning rate across schedules compares
  peaks, not schedules.
consensus: unreplicated
consensus_note: >-
  One group's large study (LIT-147). LIT-145 is a second group whose cooldown
  also decays to zero, but it recommends a shape rather than testing the
  floor, so it corroborates the endpoint and does not replicate the claim.
  Against that, every frontier recipe in this record still decays to a floor,
  DeepSeek-V4 to exactly the 10% this practice's source argues against.
  Nobody argues it is wrong and nobody has moved.
title: 'Decay the learning rate linearly all the way to zero'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-145 as well as LIT-147. The consensus_note already read
    "with LIT-145's cooldown pointing the same way", so the consensus value
    rested on a paper the source list did not name — the disconnect ADR-010
    describes. LIT-145 corroborates the endpoint, not the per-schedule
    comparison promote_when asks for, so the status is unchanged.
- version: 3
  date: '2026-09-07'
  note: >-
    Consensus re-derived from `emerging` to `unreplicated`. The note already
    ended "the field has not moved", which is the opposite of what
    `emerging` means — "several independent groups, moving toward default".
    The value was set before LIT-145 entered the source list under #58 and
    was never re-read afterwards. One group tested the claim; a second
    corroborates its endpoint incidentally; no adopter has moved. The
    recommendation and the status do not change.
tags:
- training-optimization
date: '2026-09-05'
source:
# The decay-to-zero claim is about where WSD's decay ends, not
# whether to use WSD — this practice's own Source section says so.
# LIT-145 recommends a cooldown decaying to zero with a 1-sqrt shape, and the
# consensus_note already rests on it; a consensus reading resting on a paper
# the source list does not name is the disconnect ADR-010 describes. It
# corroborates the endpoint, not the schedule comparison promote_when asks
# for, which is why this stays Proposed.
- LIT-147
- LIT-145
extends:
- SOTA-140
summary: >-
  Bergsma et al. (2025), [LIT-147](../literature.d/LIT-147.md) — with the peak tuned, linear decay to zero beats the customary decay to 10% and other shapes at compute-optimal budgets, more so past them; Proposed because contemporary production runs in the record still decay to a floor.
---

# SOTA-141: Decay the learning rate linearly all the way to zero

## Source

Bergsma et al. (2025), [LIT-147](../literature.d/LIT-147.md) — Straight to Zero.

## The finding

The customary schedule decays the learning rate to 10% of its peak. In a
large empirical study across model sizes, batch sizes, datasets and
vocabularies, with the peak tuned for each schedule, linear decay to zero
consistently beat that and the other shapes tried at compute-optimal token
budgets, and by more the further training went past compute-optimal. The
reason offered: AdamW acts as an exponential moving average of updates,
early training must move away from the initialisation while late training
must average over enough updates to cancel gradient noise, and a floor at
10% leaves noise in the final weights that a decay to zero averages out.

## Why this is Proposed

This is one group's study, and the frontier recipes filed in the
record still decay to a floor (Falcon-H1-Tiny's ×64 exponential decay,
[LIT-119](../literature.d/LIT-119.md)). The claim is compatible with WSD ([SOTA-140](SOTA-140.md)) — it is about the
end of the decay, not its start — and [LIT-145](../literature.d/LIT-145.md)'s cooldown to zero points the
same way.

## Two reports that look decisive and are not

The sharpest version of "the field has not moved" is DeepSeek-V4
([LIT-139](../literature.d/LIT-139.md)), read for [#18](https://github.com/dmarx/anthology-of-the-sota/issues/18). It decays to **exactly 10% of peak** — 2.7e-4 to
2.7e-5 for Flash, 2.0e-4 to 2.0e-5 for Pro — which is the customary floor
this practice's source names in its first sentence and argues against, at
1.6T parameters over 33T tokens. Not a report that considered decaying to
zero and declined; a report that used the default.

Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) looks at first like the second half of the promotion
condition — a schedule comparison with the hyperparameters retuned per
schedule, which is exactly what that clause asks for. It is not, and the
reason is in the same sentence of the report: the comparison is run "under a
fixed minimum learning rate". Holding the floor constant is holding *this*
practice's variable constant, so K3 settles which schedule to use and says
nothing about how far to decay it. A study can satisfy the methodology this
practice demands and still not be about it.
