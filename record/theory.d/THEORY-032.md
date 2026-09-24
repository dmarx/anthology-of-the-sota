---
number: 32
status: Proposed
formerly:
- THEORY-tmp5iwhe
promote_when: >-
  An ablation that uses THIS condition as a decision rule — spectral updates on
  the blocks whose incoming activations pass the stable-rank test, Euclidean on
  the blocks that fail — and trains faster than applying spectral updates
  everywhere. That is the experiment the inequality sets up and the paper does
  not run. Since v3 the cheapest route to it is narrower and concrete: Wang et
  al. (LIT-654) ran the per-block ablation under a DIFFERENT rule and
  found Muon on value-output plus FFN nearly recovers full Muon while Muon on
  query-key contributes little. So measure the stable rank of the incoming
  activations for QK, VO and FFN separately and see whether this condition
  orders them the same way. If it does not, this account does not explain
  where Muon's gain actually comes from and the status should fall rather than
  rise. What would still not settle it: more measurements confirming that
  transformer activations have low stable rank, which is already proved at
  initialization and observed in training; nor another per-block ablation
  selecting blocks by architectural role rather than by this inequality.
title: 'A spectral update wins where the incoming activations are low stable rank and the gradient spectrum is spread out'
version: 3
history:
- version: 2
  date: '2026-09-23'
  note: >-
    Appends `signal-structure`. A load-bearing part of this
    document is a property of the data: what turns its inequality into a
    prediction is that the stable rank of the token-indicator matrix is the
    inverse frequency of the most common token, about 20 for a Zipfian
    corpus.
- version: 3
  date: '2026-09-24'
  note: >-
    Sharpens `promote_when` into a discriminating measurement, and the account
    is unchanged. Wang et al. (LIT-654) ran the per-block ablation this
    document asked for, under a different decision rule — associative-memory
    role rather than stable rank — and found VO+FFN nearly recovers full Muon
    with QK contributing little. That establishes the half that was in doubt,
    that a per-block split is nearly costless, and leaves this account's
    specific condition untested. It also makes failure cheap to demonstrate:
    if the stable-rank ordering of QK, VO and FFN does not match the measured
    gains, this is a quantity that correlates with the regime rather than the
    mechanism, and the status should fall.
tags:
- training-optimization
- signal-structure
date: '2026-09-20'
source:
- LIT-457
explains:
- SOTA-165
- SOTA-274
summary: >-
  Davis and Drusvyatskiy (2025), [LIT-457](../literature.d/LIT-457.md) — the spectral step's
  one-step guarantee beats the Euclidean one by exactly the ratio of the
  gradient's nuclear rank to the incoming activations' stable rank, and
  transformers sit where that ratio is large. A comparison of bounds, not of
  realized training.
---

<!-- inactive-ok-file: THEORY-024 SOTA-274 THEORY-033 — THEORY-024 is Proposed and is distinguished from, not leaned on; the other two are Proposed and filed in this same contribution -->
# THEORY-032: A spectral update wins where the incoming activations are low stable rank and the gradient spectrum is spread out

## Source

Davis and Drusvyatskiy (2025), [LIT-457](../literature.d/LIT-457.md) — read as
[NOTE-209](../notes.d/NOTE-209.md).

## The account

Fix one trainable matrix `W` acting on an incoming feature matrix `X`. Bound
the loss decrease guaranteed by one Euclidean gradient step and by one
spectral step. The two bounds differ by a single ratio:

    nuclearRank(∇W) / stableRank(X)

where the nuclear rank `‖∇W‖_*² / ‖∇W‖_F²` measures how spread out the
gradient's singular values are, and the stable rank `‖X‖_F² / ‖X‖_op²`
measures how many directions the incoming features actually occupy. Spectral
wins when the first exceeds the second.

What makes this more than an inequality is that both sides are pinned down in
the case that matters. The stable rank of the token-indicator matrix is
exactly the inverse frequency of the most common token — around 20 for a
Zipfian corpus — and the paper proves that this survives RMSNorm, attention
and the MLP up to constants, giving post-activation stable ranks bounded
independently of width and sequence length. Meanwhile, in spiked
random-feature regression the gradient's nuclear rank *grows* with dimension
after a short burn-in. The predicted advantage therefore widens with scale
rather than closing, and in a NanoGPT run both quantities behave as
predicted throughout training.

The explanatory move is to locate the cause in the data flowing through the
network rather than in the norm the optimizer descends in. Transformers are
degenerate in a specific, provable way, and the spectral update is the one
that does not care.

## What was actually shown

The inequality is derived, not measured — it is a comparison of *guaranteed*
decreases from the one-step curvature bounds. The propagation results
(Lemmas 2.9, 2.10, Proposition 2.14, Corollary 2.15) are theorems at Gaussian
initialization. The dimension-scaling result is exact in the spiked
random-feature model. The claim that the structure persists through training
is a measurement in one NanoGPT run.

It could have failed in the place that matters: the stable rank of the
activations could have grown with width or sequence length, in which case the
condition would predict the advantage vanishing as models get bigger, which
is the opposite of what is observed. It does not.

## What this does not say

**A better bound is not faster training.** The comparison is between
guarantees. Nothing here establishes that realized loss reduction follows the
ratio, and the paper does not claim it does.

**It does not tell you to route updates by block.** The rule of thumb is
stated, and the ablation that would test it — spectral where the condition
holds, Euclidean elsewhere — is not run. [SOTA-274](../practices.d/SOTA-274.md) is therefore a
measurement and not a routing recipe; that restraint is [ADR-017](../decisions.d/ADR-017.md)'s
question about what a claim's source can carry.

**It is not the same claim as [THEORY-024](../theory.d/THEORY-024.md), and not a rival to it.** That
document says what the Muon update *is*: the duality map for the spectral
norm. This says *when* a spectral update pays. Both could be true. What this
does supply is the independent second account the record did not have — and
`THEORY-024` closes by noting that all three of its sources share authors.

**Nor is it [THEORY-033](../theory.d/THEORY-033.md)'s claim.** That account locates the
advantage in step-size realizability. This one locates it in rank structure.
Neither paper cites the other, and the record holds them as two hypotheses
rather than one, because nobody has shown they are the same mechanism.

**Persistence through training is measured, not proved.** Every propagation
theorem here is an initialization-time statement under Gaussian weights.
