---
number: 61
status: Proposed
formerly:
- THEORY-tmp4mah6
promote_when: >-
  An intervention that separates entropy from the spectral norm: something
  that restores attention entropy WITHOUT bounding `‖W_K W_Q^T‖₂`, or bounds
  the norm without restoring entropy, with the stability comparison held
  otherwise equal. That would show whether entropy is the causal channel or a
  co-symptom. What would NOT meet it: another paper reporting that a method
  which bounds the spectral norm also stabilizes training and also raises
  entropy. Every remedy in this cluster does both at once, which is exactly
  why the question is open.
title: 'Attention entropy is bounded below by a quantity falling exponentially in the spectral norm of the query-key product'
version: 1
tags:
- model-stability
- attention-techniques
date: '2026-09-22'
source:
- LIT-523
explains:
- SOTA-319
- SOTA-192
summary: >-
  Zhai et al. (2023), [LIT-523](../literature.d/LIT-523.md) — with
  `σ = ‖W_K W_Q^T‖₂·‖XX^T‖₂`, the minimum attainable attention entropy behaves
  like `Ω(Tσe^{−σ})`, and the bound is tight. So a saturated softmax is not
  bad luck: growing weights force it. Adaptive optimizers make it worse,
  because the idealized Adam update's spectral norm grows like `√w` in the
  width. `Proposed`, because a later paper exhibits a stable network in
  precisely the collapsed state.
corrected_by:
- THEORY-062
---
<!-- inactive-ok-file: THEORY-062 — Proposed, and the account that
     corrects this one. Naming the objection that keeps this document
     `Proposed` requires it to be unsettled. -->

<!-- inactive-ok-file: SOTA-319 — Proposed, filed in this same
     contribution and named in the `explains` table, which is the relation
     itself. -->

# THEORY-061: Attention entropy is bounded below by a quantity falling exponentially in the spectral norm of the query-key product

## Source

Zhai, Likhomanenko, Littwin, Busbridge, Ramapuram, Zhang, Gu and Susskind
(2023), [LIT-523](../literature.d/LIT-523.md) — read as [NOTE-265](../notes.d/NOTE-265.md).
Theorem 3.1 and Proposition 3.2, proved in the appendix.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-192](../practices.d/SOTA-192.md) | normalize queries and keys before the dot product | bounding the two vectors bounds `σ`, and `σ` is the quantity the entropy bound decays in |
| [SOTA-319](../practices.d/SOTA-319.md) | reparameterize every linear layer by its spectral norm | the same lever, applied to the matrix rather than the activations, with the growth rate decoupled from width |

## The account

Write `σ = ‖W_K W_Q^T‖₂ · ‖XX^T‖₂`. Theorem 3.1 bounds each row's attention
entropy below by

    log(1 + (T−1)β) + σ√(T(T−1))·β / (1 + (T−1)β),   β = exp(−σ√(T/(T−1)))

and for large `σ` and sequence length the minimum attainable entropy behaves
like `Ω(Tσe^{−σ})`. The bound is **tight** — inputs and weights attaining it
exist — so this is not a loose sufficient condition. Past a certain spectral
norm, low entropy is not merely possible but unavoidable.

The consequence is the failure [SOTA-192](../practices.d/SOTA-192.md) describes. A near-one-hot
softmax passes almost no gradient, so the layer stops learning; the paper
observes that entropy collapse and loss instability appear together across
image classification, self-supervised learning, translation, speech and
language modelling.

**Proposition 3.2 says why the norm grows in the first place, and why at
scale.** Model the stochastic gradient as `g = µ + ε` and take Adam's
idealized update `Δ = E[g]/√E[g²]`. Then `σ(Δ)` is bounded below by a quantity
growing like `√w` in the matrix width. An adaptive optimizer inflates spectral
norms, and inflates them faster in wider matrices — which is the shape of an
instability that is absent in small models and fatal in large ones.

That pairing is what makes this an account rather than a restatement. The
observation is "logits grow"; this says growth is what the optimizer does, and
saturation is what growth forces.

## Why `Proposed`

**A later paper exhibits a stable network in the collapsed state.**
[THEORY-062](THEORY-062.md) distinguishes attention maps that are sparse but
not low-rank from those that are both, reports that the first trains fine, and
says so explicitly as a counterexample to the entropy criterion. If that
observation holds, low entropy is a symptom and not the cause. It is one
group's observation and it has not been answered.

**Causation is not separated from the remedy.** Every intervention here
bounds the spectral norm *and* restores entropy *and* stabilizes training.
Nothing distinguishes "entropy collapse breaks training" from "whatever else
bounding `σ` does breaks training", and the `promote_when` asks for exactly
that separation.

**Proposition 3.2 is about an idealized update.** `Δ = E[g]/√E[g²]` is Adam's
target rather than Adam's step, under assumed moments. The direction is
convincing and the magnitude is not measured against a real optimizer.

## What it does not say

**It does not say low entropy is always bad.** The bound is on the *minimum
attainable* entropy given `σ`. Attention that concentrates because the task
wants it concentrated is not what this describes, and the successor account
is built on exactly that distinction.

**It does not say spectral normalization is the remedy it implies.** Plain
spectral normalization scores 69.81% where the learned-scalar version scores
82.2%. The theory motivates bounding growth; it does not motivate removing the
degree of freedom, and the ablation shows the difference is twelve points.

**It says nothing about the input term.** `σ` has two factors and every remedy
in this cluster acts on the weights. `‖XX^T‖₂` is equally in the bound, and
nothing here asks what controls it.
