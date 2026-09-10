---
status: Active
consensus: converged
consensus_note: >-
  Dynamic thresholding is standard in guided diffusion samplers. The general
  form — bound what a model feeds back to itself — is not stated anywhere the
  record can find.
title: "Clamp the prediction to the training range at every step when sampling from a model's own output"
version: 1
tags:
- training-optimization
date: '2026-09-10'
source:
- LIT-073
compared_against:
- SOTA-035
implementations:
- Imagen
---

# SOTA-tmpyfvex: Clamp the prediction to the training range at every step when sampling from a model's own output

## Source

Saharia et al. (2022), [LIT-073](../literature.d/LIT-073.md) — Imagen, where high classifier-free guidance
weights were destroying images and the cause turned out to be arithmetic rather
than aesthetic.

## The mechanism

Training data lies in `[−1, 1]`, so the model's `x̂₀` prediction should too.
High guidance weights push it outside. On its own that would be a bounded
error — but the model is applied **iteratively to its own output**, so the
out-of-range prediction is fed back in as input, and the excursion compounds
step over step. `LIT-073`'s description: the sampling process "produces unnatural
images and sometimes even diverges".

**A small out-of-distribution excursion is not small when it is the next step's
input.**

## The fix

**Dynamic thresholding.** At each sampling step, set `s` to a percentile of
`|x̂₀|`; if `s > 1`, clip `x̂₀` to `[−s, s]` and divide by `s`. Saturated pixels
are pushed inward at every step rather than accumulating.

The percentile matters: static clipping to `[−1, 1]` also bounds the range and
flattens everything that was already near the edges. The dynamic version rescales
instead, so the distribution is compressed rather than truncated.

Reported to improve **both** photorealism and image-text alignment, especially at
very large guidance weights — so it is not a quality-for-safety trade.

## The general form

The record already holds this instrument twice, in two other places:

- [SOTA-035](SOTA-035.md) and [SOTA-071](SOTA-071.md) clip the **gradient**, because an optimizer accumulates
  its own updates.
<!-- inactive-ok-block: SOTA-158 — Proposed, named as a parallel instance of the same instrument rather than relied on -->
- [SOTA-158](SOTA-158.md) bounds the **activation range** in low precision, because error
  accumulates through a network's depth.

This is the third: bound the **output**, because a sampler consumes its own
predictions. The common structure is a quantity that is fed back into the
process that produced it, where an excursion is not corrected but compounded.

Where else this structure appears and the record says nothing: autoregressive
decoding, and agent loops that consume their own outputs.

## Conditions

Diffusion sampling with classifier-free guidance, images, 2022. The percentile
is a hyperparameter with no principle behind it.

Requires a known training range — `[−1, 1]` here — so "the training range" has
to be a thing you can name. That is easy for pixels and not obvious for a latent.

The generalisation to other iterative self-application is the shape of the
argument, not something `LIT-073` establishes.

## Known implementations

- Imagen; standard in guided diffusion samplers since
