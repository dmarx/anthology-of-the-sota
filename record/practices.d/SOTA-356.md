---
number: 356
status: Active
formerly:
- SOTA-tmpt7jr1
title: 'Protect the salient weight channels by scaling them before rounding, choosing them from the activations rather than the weights'
version: 1
tags:
- numerics-and-precision
- inference-optimization
consensus: converged
consensus_note: >-
  Served by both `vllm` and `transformers` as of 2026-09, which is what
  surfaced it (#289) — one of three items in 91 that two independent
  adoption indexes both carried. That is a statement about adoption and not
  about evidence (DP-005), and it sits beside GPTQ rather than above it:
  the field runs both, and the comparison between them is live.
date: '2026-09-23'
source:
- LIT-585
introduced_by:
- LIT-585
compared_against:
- SOTA-185
summary: >-
  Lin et al. (2023), [ARXIV-2306.00978](https://arxiv.org/abs/2306.00978). Identify the ~1% of weight channels
  whose activations are largest, scale them up by an equivalent
  transformation before rounding, and quantize everything uniformly — rather
  than keeping the important channels in higher precision.
---

# SOTA-356: Protect the salient weight channels by scaling them before rounding, choosing them from the activations rather than the weights

## Source

Lin et al. (2023), [LIT-585](../literature.d/LIT-585.md) — [ARXIV-2306.00978](https://arxiv.org/abs/2306.00978).

## What to do

Before quantizing a linear layer's weights to 4 bits:

1. Run a small calibration set forward and collect **activation** statistics
   per input channel.
2. Take the channels with the largest activations — about 1% — as salient.
3. Scale those weight channels up, and scale the corresponding activations
   down by the same factor, so the layer computes the same function.
4. Round everything to the target width uniformly.

There is no backward pass and nothing is fitted to a reconstruction
objective.

## The two choices that carry it

**Salience is read from activations, not from weights.** This is the part
the name states and the part that is easy to get backwards. A weight channel
is worth protecting because the activations flowing through it are large,
and weight magnitude is a poor proxy for that. Choosing by weight magnitude
is a different and worse method.

**The protection is a scaling, not a precision carve-out.** Keeping 1% of
channels in 16 bits is the obvious implementation and it makes the kernel
irregular, which costs more than the quantization saves. Scaling instead
leaves every weight at the same width, so the matrix multiply stays dense
and uniform.

## When this is the wrong tool

This is **weight-only** quantization: the weights shrink, the activations
stay in 16-bit. It buys memory and the bandwidth that follows from it, and
it does not buy int8 arithmetic. A deployment that is compute-bound rather
than bandwidth-bound gets much less from it than the memory figures suggest.

## Against GPTQ

`SOTA-185` solves the same problem by compensating each rounding error into
the columns not yet quantized, using second-order information from a
calibration set. Both are one-shot post-training methods at similar bit
widths, and the record carries both because the field runs both.

The distinguishing claim is **generalization**, not accuracy at a bit width.
GPTQ fits a calibration objective; AWQ deliberately does not, and its
argument for itself is that this is why it holds on instruction-tuned and
multi-modal models rather than only on the calibration distribution. A
reader choosing between them should be checking that claim, not the headline
perplexity — and the record does not hold an independent test of it.
