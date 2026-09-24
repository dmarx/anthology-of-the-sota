---
number: 98
status: Active
formerly:
- THEORY-tmp4t3x7
title: 'Softmax attention coefficients must disperse as the number of items grows, so no learned attention circuit stays sharp out of distribution'
version: 1
tags:
- attention-techniques
- model-architecture
date: '2026-09-24'
source:
- LIT-653
summary: >-
  Veličković et al. (2024), [LIT-653](../literature.d/LIT-653.md). With logits bounded and temperature
  non-zero, every softmax coefficient is at most `(1/n)·exp(δ/θ)` — and in a
  Transformer over a finite vocabulary the logits are *always* bounded, so the
  bound applies in every attention head. A head that looks sharp
  in-distribution is not a robust circuit; it is a circuit whose input size
  has not grown yet.
---

# THEORY-098: Softmax attention coefficients must disperse as the number of items grows, so no learned attention circuit stays sharp out of distribution

## Source

Veličković, Perivolaropoulos, Barbero and Pascanu (2024), `LIT-653`.

## The claim

Two steps, and the second is the one that makes it bite.

**Dispersion follows from bounded logits.** For `n` logits with spread
`δ = max e − min e` and temperature `θ > 0`, no coefficient can exceed
`(1/n)·exp(δ/θ)`. As `n` grows with `δ` and `θ` fixed, every coefficient is
driven towards zero, and for any threshold `ε` this happens once
`n > exp(δ/θ)/ε`.

**In a Transformer the logits are always bounded.** If the input vocabulary is
finite, the embeddings sit in a compact set; feedforward layers are continuous
and map compact sets to compact sets; a self-attention layer outputs convex
combinations and so stays inside the same set. The query-key dot products are
therefore bounded in **every** layer, whatever `n` is. The premise of the
first step is not an assumption about a particular model — it is a
consequence of tokenisation plus global attention.

What follows is a statement about circuits rather than about accuracy. A head
that has learned to place most of its mass on one item, and which looks sharp
under inspection on in-distribution inputs, **cannot be doing that robustly**:
the mass it can place anywhere is capped and the cap shrinks with `n`. So any
function depending on a fixed number of inputs — `max`, `min`, a
random-access lookup — degrades with input size by construction.

## Why it is `Active`

It is a proof, its assumptions are stated and checkable, and the phenomenon it
explains was already being observed empirically by people who could not
account for it (Yan et al. 2020; Ebrahimi et al. 2024 both report dispersion
patterns). Nothing in this record contradicts it.

The status is about the account, and the account is narrow in a way worth
being explicit about: it says a particular architectural choice has a
particular limit. It does **not** say models cannot generalise to longer
inputs, and it does not explain any specific observed failure without further
argument about which heads mattered.

## What it does not license

**It is a bound, not a rate for any given model.** `δ` is what sets the
constant, and the paper says that naively bounding `δ` from floating-point
ranges gives *"fairly loose bounds which are not particularly informative"*.
The theorem says dispersion is inevitable; it does not say it has happened yet
at the sequence length you are running.

**Local attention is outside it.** The argument is about heads attending over
all items. A head with a bounded window has bounded `n` by construction.

**Three families escape it**, per the source: unnormalised attention (linear,
sigmoidal, stick-breaking), which pays for it in how hard it becomes to rank
items; selective attention, which removes excess mass explicitly; and
possibly not the Differential Transformer, whose subtraction happens after
each softmax and so cannot undo dispersion that already occurred inside them.

**The proposed mitigation does not repair it.** Adaptive temperature buys 1.6
points at 16,384 items against a fall from 98.6% to 12.4%. That the fix is
marginal is part of the evidence for the account, not an argument against it.

## What it joins

<!-- inactive-ok-block: THEORY-061, THEORY-062 — both Proposed, and cited to
     say this account bounds the same quantity from the opposite side. The
     paragraph's claim is about which variable each one ranges over, which
     holds whatever their standing. -->
The record holds two accounts of attention sharpness and both run the other
way. `THEORY-061` bounds attention entropy **below** by a quantity falling
exponentially in the spectral norm of the query-key product — how sharp a head
*can* get as its weights grow. `THEORY-062` says spectral energy concentrating
in `W_q^T W_k` is what predicts a crashed run. Both are about weights at fixed
input size.

This one bounds entropy **above**, as a function of input size at fixed
weights. Together they say the sharpness of a head is squeezed by two
different variables, and `SOTA-192` — which bounds the logits structurally to
stop the first failure — sits on the boundary. The source's Proposition 3.1
makes the connection its own: normalisation applied right before the
query-key mechanism clamps the activation norms, leaving `δ` governed by the
singular values of `Q` and `K`.

Whether that trade is worth anything at real sequence lengths is unmeasured,
and is written down in the source's note as a reading rather than a result.
