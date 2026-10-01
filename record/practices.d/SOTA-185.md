---
number: 185
status: Active
formerly:
- SOTA-tmp0ttm7
title: 'Quantize weights after training by compensating each rounding error into the columns not yet quantized'
version: 1
tags:
- numerics-and-precision
- inference-optimization
consensus: converged
date: '2026-09-08'
source:
- LIT-081
introduced_by:
- LIT-081
summary: >-
  Frantar et al. (2022), [LIT-081](../literature.d/LIT-081.md) — [ARXIV-2210.17323](https://arxiv.org/abs/2210.17323). Round one column at a
  time and push the resulting error into the remaining columns using
  approximate second-order information, instead of rounding every weight
  independently to the nearest level.
compared_against:
- SOTA-356
---

# SOTA-185: Quantize weights after training by compensating each rounding error into the columns not yet quantized

## Source

Frantar et al. (2022), [LIT-081](../literature.d/LIT-081.md) — [ARXIV-2210.17323](https://arxiv.org/abs/2210.17323).

## The mechanism

Round-to-nearest treats each weight as independent, which it is not: the
layer's output error depends on the interaction between weights, and a small
rounding error in one column can be absorbed by adjusting the columns that
have not been quantized yet. GPTQ does exactly that, ordering the work
column-wise and using approximate second-order (Hessian) information from a
small calibration set to decide the compensation.

What it buys: 3- and 4-bit weight quantization of models up to 175B, with
accuracy close to the uncompressed baseline, in around four GPU-hours — a
one-shot procedure with no retraining and no gradient steps. Before this,
getting to 4 bits at that scale meant quantization-aware training.

The method and these figures are [LIT-081](../literature.d/LIT-081.md)'s, and the recommendation starts
there: Frantar et al. proposed column-wise rounding with Hessian-guided error
compensation as the replacement for round-to-nearest, and reported the 3- and
4-bit results up to 175B from a one-shot pass over a small calibration set.

## The scope worth holding onto

This is **weight-only**, and the win is memory
and bandwidth rather than arithmetic: it makes a model fit and makes decode
faster because decode is bandwidth-bound, and it does not make a
compute-bound prefill faster. It also needs a calibration set, so it is a
procedure with an input rather than a pure transformation, and a calibration
distribution unlike the serving distribution is a real failure mode.

## Filed as the approach, not the artifact

Error-compensating one-shot PTQ with a calibration set is what converged; the specific search
and ordering have been improved on repeatedly since. The record's other
quantization entries sit at different altitudes —
<!-- inactive-ok: SOTA-160 — Proposed, named as the other altitude this practice is distinguished from -->
[SOTA-160](SOTA-160.md) treats the
quantization plan and the pretraining budget as one decision, and [SOTA-163](SOTA-163.md) is
about the number format rather than the rounding procedure.

The live alternative at the same altitude is [SOTA-356](SOTA-356.md) (AWQ), which protects
activation-salient channels by scaling instead of compensating errors. Its
authors ran the head-to-head against this method on LLaMA and Llama-2 at 7B
to 70B and report lower perplexity than GPTQ with or without its reordering
trick; and on OPT-6.7B at INT3-g128, calibrating on one Pile subset and
evaluating on another cost GPTQ 2.3–4.9 perplexity against AWQ's 0.5–0.6.
That is the calibration-distribution failure mode above, measured.

## Known implementations

- the default weight-only path in most open-weight serving stacks
