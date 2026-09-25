---
number: 97
status: Proposed
formerly:
- THEORY-tmpn3rkg
promote_when: >-
  A point prediction from the SDM frame that could have come out wrong, tested
  on a model nobody chose for the purpose. The β range is not it — [10, 25]
  interpolates between three optimality criteria that themselves span a range,
  so the band was wide before the measurement was taken. The cheapest
  qualifying version: SDM's capacity result gives a predicted degradation
  curve as the number of stored patterns rises, so measure retrieval accuracy
  against context length in a trained model and compare the shape. What would
  NOT meet it: further components of the transformer reinterpreted in SDM
  terms, which extends the mapping rather than testing it.
title: 'Attention is an approximation of Kanerva''s sparse distributed memory, which is why it needs normalized vectors and a fitted temperature'
version: 1
tags:
- attention-techniques
- model-architecture
date: '2026-09-24'
source:
- LIT-641
explains:
- SOTA-192
summary: >-
  Bricken and Pehlevan (2021), [LIT-641](../literature.d/LIT-641.md) — attention's update rule is SDM's
  read operation under two conditions, `L²` normalized vectors and a fitted
  softmax temperature. Its one non-trivial consequence is a **retrodiction**:
  those two conditions are QK-norm, published a year earlier for unrelated
  reasons. Trained QK-norm heads learn β ∈ [10, 25], inside the range SDM's
  optimality criteria span.
---
<!-- inactive-ok-file: THEORY-081 — Proposed, and named as this account's
     nearest neighbour in order to say it is better evidenced than this one.
     Both are Proposed; that is the point of the comparison. -->

# THEORY-097: Attention is an approximation of Kanerva's sparse distributed memory, which is why it needs normalized vectors and a fitted temperature

## Source

Bricken and Pehlevan (2021), [LIT-641](../literature.d/LIT-641.md).

## The account

Kanerva's sparse distributed memory ([LIT-666](../literature.d/LIT-666.md)) stores patterns at binary addresses and
reads by querying an address, returning a weighted average of the pointers
whose addresses lie within a Hamming distance `d` — with the weighting given
by the intersection of two hyperspheres, which decays almost exponentially in
distance.

Attention computes `ξ^new = P_p · softmax(β P_aᵀ ξ)`. Map keys to pattern
addresses, values to pointers, the query to the read address, and the two
coincide — **provided** the vectors are `L²` normalized, so that a dot product
stands in for Hamming distance, and **provided** β is chosen to match the
circle-intersection decay.

So the claim is not that attention resembles a memory. It is that attention
*is* an SDM read with a particular temperature, and that the temperature is a
free parameter the architecture has to get right.

## What it predicts, and it is one thing

**Attention should want `L²`-normalized queries and keys and a fitted β rather
than a fixed `1/√d`.** That is QK-norm — `LIT-640`, published in 2020,
motivated by softmax saturation in low-resource translation, with no
reference to associative memory. The theory arrives at the same prescription
from a different direction and afterwards.

That prescription is `SOTA-192`, which this account is declared to explain.
The declaration is worth stating carefully: `SOTA-192` recommends the
normalization for a reason this theory does not give — bounding logits that
would otherwise saturate the softmax and kill the gradient — and that reason
is better evidenced. What this account adds is why the *temperature* is a
thing worth fitting rather than a constant to be divided out, which is the
half of `LIT-640`'s technique the record's later usage drops.

And the temperature the theory says should be chosen well is one QK-norm makes
*learnable*, so it can be read off a trained model: **β ∈ [10, 25]**, which
interpolates between SDM's critical-distance, signal-to-noise and
memory-capacity optima. The first is derived in Kanerva's book ([LIT-666](../literature.d/LIT-666.md)),
the other two in his 1992 review ([LIT-669](../literature.d/LIT-669.md)).

## Why this is `Proposed` and likely to stay there

**The measurement is a consistency check, not a test.** The three optimality
criteria give three different β and the observed range interpolates between
them — but a band spanning three criteria was wide before anything was
measured, and the authors say so: the reference values "are only a weak
reference for what β values might be reasonable". No value of β in a plausible
range would have refuted this.

**The retrodiction is genuine and cannot be repeated.** QK-norm was already
published. That the theory recovers it is a point in its favour and not
evidence in the sense the record usually means — nobody risked anything.

**A mapping that explains every component explains less than it appears to.**
The source reads LayerNorm, the feed-forward block and the residual stream
through the same frame. Each reinterpretation makes the picture more complete
and none makes it more falsifiable, which is the characteristic failure mode
of a correspondence account.

The `promote_when` therefore asks for the one thing missing: a quantity the
SDM frame fixes in advance, measured somewhere nobody chose for the purpose.

## Where it sits

<!-- inactive-ok-block: THEORY-065, THEORY-066, THEORY-061, THEORY-062 — all
     Proposed, and named as a census of the neighbourhood this account joins.
     What the paragraph claims is that all five are about dynamics or
     geometry, which is true of them whatever their standing. -->
The record holds five accounts of what self-attention does — `THEORY-065` on
clustering, `THEORY-066` on collapse, `THEORY-061` and `THEORY-062` on entropy
and spectral concentration, `THEORY-028` on circuit formation — and all five
are about *dynamics or geometry*. This is the only one about what the operation
**is**.

Its nearest neighbour is `THEORY-081`, which reads feed-forward layers as
key-value memories. That account is better evidenced: it comes from direct
measurement of what individual hidden units respond to, rather than from a
correspondence plus a temperature check. **Two halves of a transformer, two
memory accounts, and the attention side is the weaker one** — which is worth
recording precisely because the attention side is the half people assume is
understood.
