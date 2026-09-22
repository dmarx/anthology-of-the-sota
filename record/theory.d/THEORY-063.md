---
number: 63
status: Proposed
formerly:
- THEORY-tmphj2w6
promote_when: >-
  A consequence demonstrated: an intervention that exploits the placement —
  steering, editing or probing restricted to the low-variance subspace —
  beating the same intervention without that restriction, on more than the
  four-of-five models and seven-of-thirteen configurations the source already
  reports as partial. Placement with no consequence is a description of
  geometry; what would make it an account is something that works because of
  it. What would NOT meet it: the anti-concentration measurement repeated on
  more models, which is the part already robust.
title: 'Contextual concept directions sit in the low-variance tail of the unembedding spectrum while vocabulary contrasts sit at the top'
version: 1
tags:
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-22'
source:
- LIT-526
summary: >-
  Acharya, Rimal and Dhakal (2026), [LIT-526](../literature.d/LIT-526.md) — concept
  directions read out of the residual stream anti-concentrate in the
  low-eigenvalue directions of the unembedding second moment, in 17 of 17
  models and by three independent extraction methods. Static unembedding-row
  contrasts do the opposite. So the same model carries semantic content at
  both ends of one spectrum, depending on whether the representation is
  contextual.
---
<!-- inactive-ok-file: THEORY-034 — Proposed, named under "what it does not
     say" to record that this account does not contradict it. -->

# THEORY-063: Contextual concept directions sit in the low-variance tail of the unembedding spectrum while vocabulary contrasts sit at the top

## Source

Acharya, Rimal and Dhakal (2026), [LIT-526](../literature.d/LIT-526.md) — read as
[NOTE-270](../notes.d/NOTE-270.md).

## The account

Take the unembedding rows `γ(w)` and form their regularized uncentered second
moment `Σ`. Its eigenbasis orders directions by how much of the vocabulary's
variance they carry. Now ask where a concept direction sits in that order.

**Contextual directions sit at the quiet end.** Difference-of-means vectors
computed from the residual stream over 22 semantic categories anti-concentrate
— their mass accumulates in the low-eigenvalue directions, in 17 of 17 models
against a uniform baseline and 13 of 17 against a norm-matched random-direction
null. Sparse-autoencoder features and linear probes find the same thing, which
matters because those three extractions share no machinery.

**Static directions sit at the loud end.** Contrasts computed from the
unembedding rows themselves concentrate in high-variance directions. Same
model, same spectrum, opposite end.

**And the placement is not inherited from the ambient spectrum.** Correlation
between random-direction placement and concept placement is `r = 0.019`. So
concepts are not merely landing wherever the spectrum happens to put things.

The reading the source offers is that transformers rotate semantic content
*into* spectrally quiet regions during contextualized processing — the static
vocabulary geometry and the geometry of what the model actually computes are
different geometries, and the difference is the contextualization.

## Why `Proposed`

**Placement is not yet consequence.** Everything robust here is a measurement
of where directions lie. The one attempt at a consequence — that steering in
the quiet subspace interferes less than steering in the loud one — is graded
*partial* by the authors themselves: 4 of 5 models, 7 of 13 configurations,
uncorrected sweep, one model undetermined, magnitude dependent on steering
strength.

**The syntax half may be about English.** The companion claim — that syntax
sits preferentially in the high-variance subspace — holds in 6 of 8 models on
English and **reverses** in the Qwen 2.5 family and in both models tested on
Chinese. That is either a language effect or a tokenizer effect and the source
does not separate them.

**Correlational, on 17 checkpoints.** Breadth in models rather than in
architecture families, and no intervention establishes direction of any
relationship.

## What it does not say

**It does not say low-variance directions are unimportant or important in
general.** It says concept directions are found there. This record now holds
three unrelated results in which the small end of some spectrum carries more
than its magnitude suggests — weight matrices, quantization residuals, and
this — across three different matrices and three literatures. Counted in the
reading, joined nowhere, because no mechanism connecting them survives being
written down. [DP-009](../../docs/design-principles.md#dp-9).

**It does not settle the causal inner product it set out to test.** The
paper's null is specific: whitened alignment adds nothing over spectral
regularization for cross-lingual transport, across 17 models and four language
pairs. That is a result about one proposed use, not a refutation of the
underlying geometry.

**It does not contradict [THEORY-034](THEORY-034.md).** That account is about the shape
of a concept region — intersections of half-spaces. This is about where the
direction lies in a covariance spectrum. They answer different questions about
the same object and the record has not joined them.
