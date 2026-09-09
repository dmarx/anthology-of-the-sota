---
number: 168
status: Proposed
formerly:
- SOTA-tmpvsqdg
promote_when: >-
  A pretraining report above 1B trained on SOAP, or an independent group
  running it against a per-optimizer-tuned Muon baseline at the scale the
  record's practices operate at. LIT-156 already places both in the fastest
  group at 1.2B and below, so more of that comparison at that scale is not
  the missing evidence.
consensus: unreplicated
consensus_note: >-
  One group for the algorithm, plus an independent comparison (LIT-156)
  placing it in the fastest group. Nobody disputes it and nobody ships it —
  the frontier labs in this record that left AdamW went to Muon.
title: "Run Adam in Shampoo's eigenbasis (SOAP) instead of Shampoo itself"
version: 1
tags:
- training-optimization
date: '2026-09-08'
published: '2024-09-01'
source:
# The algorithm and its derivation, plus the independent comparison that
# tuned it fairly against nine others. LIT-158 is the Shampoo implementation
# this improves on and is cited in the body.
- LIT-157
- LIT-156
compared_against:
- SOTA-121
implementations: []
summary: >-
  Vyas et al. (2024), [LIT-157](../literature.d/LIT-157.md) — Shampoo at the 1/2 power is Adafactor in the
  eigenbasis of Shampoo's preconditioner, so run the better optimizer in that
  basis. SOAP is Adam there, adding exactly one hyperparameter over Adam. Over
  40% fewer iterations and 35% less wall-clock than AdamW at 360M–660M in the
  large-batch regime.
---

# SOTA-168: Run Adam in Shampoo's eigenbasis (SOAP) instead of Shampoo itself

## Source

Vyas et al. (2024), [LIT-157](../literature.d/LIT-157.md) — [ARXIV-2409.11321](https://arxiv.org/abs/2409.11321); with the fair
comparison in Wen et al. (2025), [LIT-156](../literature.d/LIT-156.md).

The result the method falls out of is an equivalence, not an analogy:
**Shampoo implemented with the 1/2 power is exactly Adafactor run in the
eigenbasis of Shampoo's preconditioner.** Once that is established the design
question answers itself — if the basis is the useful part, run the better
optimizer in it. SOAP is Adam in that basis.

Because it is Adam in a rotated space, it adds exactly **one** hyperparameter
over Adam: how often to recompute the preconditioner.

## The failure mode it avoids, which is the practical point

The obvious way to make Shampoo affordable is to eigendecompose less often.
That degrades performance, and worse the less often you do it — so the
efficiency knob and the quality knob are the same knob, turned opposite ways.

SOAP escapes it by continuing to update the second-moment running average in
the current, slowly-rotating basis, which is what Adam does anyway. The stale
basis stops being a problem because the statistics keep moving inside it.

Reported at 360M and 660M in the large-batch regime: over **40% fewer
iterations** and over **35% less wall-clock** than AdamW, and about 20%
better than Shampoo on both.

## Against Muon, which is `compared_against` and not a rivalry

[LIT-156](../literature.d/LIT-156.md) tuned both fairly and put both in the fastest group, with matrix
preconditioning as the common factor. That is a comparison somebody ran,
which is why the relation is declared rather than argued.

The record recommends Muon ([SOTA-121](SOTA-121.md), with [SOTA-131](SOTA-131.md)'s QK-Clip riding
along) on production evidence at trillion-parameter scale that SOAP does not
have. This is the same family reached from the other direction — SOAP by
simplifying a full preconditioner until it is affordable, Muon by
orthogonalising a momentum matrix. Both are members of the trunk practice
they extend, and what SOAP supplies to that trunk is the argument that the
win belongs to the class.

## Conditions, and why this is Proposed

360M and 660M, one group for the algorithm, and no production deployment
anywhere in the record. The large-batch regime is also a condition and not a
detail: that is where the reported gains are measured.

## Known implementations

- None in the record.
