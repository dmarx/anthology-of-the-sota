---
status: Proposed
promote_when: >-
  The spectral claim measured outside diffusion transformers: singular value
  distributions of `W`, of the smoothed `Ŵ`, and of the quantization residual
  `W − Q(W)`, reported for a model family this record already holds — a
  language transformer, a convolutional vision model — with the rank needed to
  capture a fixed fraction of each. That would separate "weight matrices have
  steep spectra" from "diffusion transformer weight matrices do". What would
  NOT meet it: another method that puts a low-rank branch beside a quantized
  one and reports better images. That is the practice, and the record already
  holds it.
title: 'A low-rank branch corrects quantization because weight spectra are steep and quantization-error spectra are flat'
version: 1
tags:
- numerics-and-precision
- inference-optimization
date: '2026-09-21'
source:
- LIT-tmpglyct
explains:
- SOTA-tmp0iki2
summary: >-
  Li et al. (2024), [LIT-tmpglyct](../literature.d/LIT-tmpglyct.md) — two propositions bound the
  output error by the *magnitude* of weights and activations, not only by
  their rounding errors. So a rank-`r` branch helps exactly when the thing it
  subtracts has a few dominant singular values. A weight matrix does; a
  quantization error does not, which is why the same trick applied to the
  error rather than the weights underperforms.
---

<!-- inactive-ok-file: SOTA-tmp0iki2 — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself. -->

# THEORY-tmpo44nu: A low-rank branch corrects quantization because weight spectra are steep and quantization-error spectra are flat

## Source

Li, Lin, Zhang, Cai, Li, Guo, Xie, Meng, Zhu and Han (2024),
[LIT-tmpglyct](../literature.d/LIT-tmpglyct.md) — read as [NOTE-tmpujtdw](../notes.d/NOTE-tmpujtdw.md). Propositions 4.1
and 4.2, with proofs in the appendix.

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-tmp0iki2](../practices.d/SOTA-tmp0iki2.md) | absorb outliers into a high-precision low-rank branch taken from the weights, and fuse its kernels | the branch pays off because the weight matrix is nearly low-rank in its largest directions, and it would not pay off if applied one step later |

## The account

The usual mental model of post-training quantization is that the thing to
minimize is the **rounding error** — how far `Q(W)` is from `W`. On that
model, the natural way to use a spare high-precision branch is to have it
approximate the error: compute `W − Q(W)`, take its truncated SVD, add it
back. That is what LoRC does.

Proposition 4.1 says the model is incomplete. The error in the layer's output
is bounded by four quantities, not two: the rounding errors
`‖W − Q(W)‖_F` and `‖X − Q(X)‖_F`, **and the magnitudes** `‖W‖_F` and
`‖X‖_F`. Magnitude is a lever in its own right. Proposition 4.2 closes the
loop: the rounding error of a matrix is itself bounded by that matrix's
magnitude. So shrinking what you hand to the quantizer shrinks both terms at
once.

That makes the question spectral. Subtracting a rank-`r` matrix `L₁L₂` from
`M` reduces `‖M‖_F` by exactly as much as the first `r` singular values
contain — Eckart-Young gives the optimum as the truncated SVD. So the
manoeuvre is worth doing on a matrix whose spectrum is **steep**, and close to
worthless on one whose spectrum is **flat**.

A weight matrix is the steep case. The paper's Figure 5 shows the singular
values of `W` are highly imbalanced, and that after smoothing the first 32 of
`Ŵ` drop steeply while the rest decay gradually — so rank 32 removes a large
share of the magnitude.

A quantization error is the flat case. Rounding is close to independent across
entries, so `W − Q(W)` behaves like a matrix with no preferred directions and
its singular values are well spread. A rank-32 approximation of it captures
almost nothing, which is why applying the low-rank branch to the error
underperforms applying it to the weights.

**So the ordering matters more than the ingredient.** Decompose first and
quantize the residual; do not quantize first and try to patch what is left.
The same components in the other order do not work, and the spectrum is why.

## Why `Proposed`

**The spectral claim is measured on one model family.** Figure 5 is diffusion
transformer weights. "Weight matrices have steep singular spectra" is
plausible far beyond that and is not shown beyond it here, which is what the
`promote_when` asks for.

**The flatness of the error spectrum is argued, not plotted.** The paper
states that quantization errors "exhibit a well-spread distribution of
singular values" and infers the consequence for LoRC; this record did not find
the spectrum of `W − Q(W)` plotted beside the others. The inference is sound
and the measurement is one line of code, and the difference between those two
is exactly what `Proposed` is for.

**Smoothing and decomposition are not separated spectrally.** Smoothing shifts
outliers from activations into weights and changes `Ŵ`'s spectrum; the
ablation shows the combination beats either, but nothing reports how much of
the steepness rank-32 exploits was already in `W` and how much smoothing put
there.

## What it does not say

**It does not say low-rank adapters and this are the same thing.** The
arrangement resembles [SOTA-230](../practices.d/SOTA-230.md) — a 4-bit base with a 16-bit low-rank
side — and the purpose is opposite. There the branch carries *new* task
information and the base is frozen; here it carries *existing* weight
magnitude away from the quantizer and nothing is learned. The source is
explicit that the prior work in that line targets compression or fine-tuning,
uses weight-only quantization, and so yields no speedup.

**It does not say magnitude is the only lever.** Proposition 4.1 has four
terms. Block scaling ([SOTA-163](../practices.d/SOTA-163.md)) and error compensation
([SOTA-185](../practices.d/SOTA-185.md)) act on the other ones, and the source uses GPTQ on the
residual weights, so these compose rather than compete.

**It says nothing about activations beyond the smoothing step.** The account
of why the residual quantizes well is about `W`. The activation side is
handled by moving outliers out of it, and this theory does not explain what
makes that transfer safe.
