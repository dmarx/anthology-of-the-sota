---
number: 276
status: Proposed
formerly:
- SOTA-tmpr10ct
consensus: unassessed
consensus_note: >-
  One paper old, and stated as a simplification rather than adopted by
  anybody the record knows of. Nothing to assess yet.
promote_when: >-
  A group implementing width-depth muP this way for an optimizer the paper
  did not derive — taking their existing width-muP setup, adding the `1/L`
  hidden residual multiplier and nothing else — and reporting that depth
  transfer holds. The claim is about a class, and every confirmation so far
  comes from inside the nine derivations that produced it. What would not
  settle it: another of those nine being run, which tests the derivation
  rather than the generalization.
title: 'For a normalized or preconditioned optimizer, width-depth muP is width muP plus a hidden residual multiplier of order 1/L'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-462
introduced_by:
- LIT-462
implementations: []
summary: >-
  Zheng et al. (2026), [LIT-462](../literature.d/LIT-462.md) — a normalized or preconditioned
  update has a norm that does not depend on the residual multiplier, so the
  depth factor the raw gradient carries is removed and the optimizer's own
  muP rule is unchanged. SGD is the exception and needs more.
explained_by:
- THEORY-037
---

<!-- inactive-ok-file: SOTA-275 — Proposed, and filed in this same contribution as what fixes the multiplier this practice says to add -->
# SOTA-276: For a normalized or preconditioned optimizer, width-depth muP is width muP plus a hidden residual multiplier of order 1/L

## Source

Zheng et al. (2026), [LIT-462](../literature.d/LIT-462.md) — [ARXIV-2603.00541](https://arxiv.org/abs/2603.00541),
read as [NOTE-211](../notes.d/NOTE-211.md), Takeaway 2. Accounted for by
[THEORY-037](../theory.d/THEORY-037.md).

## What to do

If you already have a width-scaling muP setup and now want to scale depth as
well, and your optimizer normalizes or preconditions its update — Muon,
Muon-Kimi, Shampoo, SOAP, AdamW, Sophia, Lion — then:

1. Keep your width-muP initialization and learning-rate rules exactly as they
   are.
2. Set the hidden residual multiplier `α_l = Θ(1/L)`.
3. Change nothing else.

**SGD is the exception and needs a further step.** Its update is proportional
to the raw gradient, which carries the residual multiplier, so after setting
`α_l` the hidden learning rate needs an additional `α_l`-dependent rescaling.

## Why the depth correction collapses to one number

A hidden layer's raw gradient inherits the residual multiplier `α_l` as a
factor. An optimizer that normalizes or preconditions its update divides that
factor out, so the *norm* of the update it produces does not depend on `α_l`
at all. The spectral condition constrains that norm — which means the
optimizer-specific part of the rule is the same as it was under width-only
scaling, and the only thing depth changes is the multiplier itself. SGD does
not divide anything out, so for SGD the factor survives into the update and
has to be compensated.

The practical consequence is that adopting depth scaling is a one-line change
for most of the optimizers the record recommends, rather than a re-derivation.

## Conditions

- **`Proposed`.** The rule is derived for nine named optimizers and four were
  run. It is stated as a property of a class — "normalized or preconditioned"
  — and the evidence for the class is the nine instances that produced it.
  Whether some other preconditioned optimizer has an update norm that *does*
  depend on `α_l` is a thing to check, not a thing the paper rules out.
- **SGD is genuinely different**, and an optimizer that is partly raw-gradient
  should be treated as SGD-like rather than assumed to simplify.
- **Hybrid setups need care.** The experiments run Muon on hidden matrices
  and AdamW on embeddings, LM head and biases; both are in the simplifying
  class, so the hybrid inherits the simplification. A hybrid with an
  SGD-like component would not.
- **300M tokens per run**, GPT-2-style models, widths to 4096 and depths to
  256.
- **The experiments implement the simplification rather than testing it.**
  No run compares the simplified rule against a non-simplified derivation of
  the same condition, because for these optimizers the two coincide by the
  argument. The check is the argument.

## Relation to the neighbours

[SOTA-143](../practices.d/SOTA-143.md) is the width-muP setup this takes as given.
[SOTA-275](../practices.d/SOTA-275.md) is what fixes `Θ(1/L)` rather than `Θ(1/√L)` as the
multiplier to add. The record recommends Muon ([SOTA-121](../practices.d/SOTA-121.md)) and matrix
preconditioning ([SOTA-165](../practices.d/SOTA-165.md)) and has never said how to muP either; this
is the answer, and it is short because of what preconditioning does.

## Known implementations

- None reported. The paper's own runs implement it; no production report in
  the record trains this way.
