---
number: 202
status: Active
formerly:
- SOTA-tmpyfvex
consensus: converged
consensus_note: >-
  Dynamic thresholding is standard in guided diffusion samplers. The general
  form — bound what a model feeds back to itself — is not stated anywhere the
  record can find.
title: "Clamp the prediction to the training range at every step when sampling from a model's own output"
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Adds the precondition this practice had without stating: the clamp needs the
    sampler to be carrying `x̂₀`. LIT-676 arrives at the same boundedness
    mechanism from the solver side and draws the consequence — a high-order solver
    written on the noise prediction has no data prediction to clamp at its
    intermediate stages, so this practice is unavailable exactly where guidance
    makes it most necessary. Recommendation, status and consensus unchanged.
tags:
- training-optimization
- generative-modeling
date: '2026-09-10'
source:
- LIT-073
- LIT-676
introduced_by:
- LIT-073
compared_against:
- SOTA-035
implementations:
- Imagen
---

# SOTA-202: Clamp the prediction to the training range at every step when sampling from a model's own output

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

## The precondition: the sampler has to be carrying `x̂₀`

This practice says to clamp the `x̂₀` prediction at every step, which assumes
there is an `x̂₀` to clamp. A diffusion ODE solver can be written on the **noise**
prediction `ε̂` instead, and a high-order one then has intermediate stages where
no data prediction exists — so the clamp has nowhere to attach.

[LIT-676](../literature.d/LIT-676.md) reaches this mechanism independently, from the solver side rather
than from Imagen's, and draws the design consequence: it solves the ODE for the
data prediction model specifically because "thresholding methods are further
available to keep the samples bounded". [SOTA-410](SOTA-410.md) is that recommendation.

The practical form: **this practice and a noise-prediction high-order sampler are
not compatible**, and the incompatibility bites hardest at the large guidance
weights where this practice was needed in the first place. Two documents in this
record found the same mechanism from opposite directions, which is the strongest
support either of them has.

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
