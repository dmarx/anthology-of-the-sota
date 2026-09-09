---
number: 163
status: Active
formerly:
- SOTA-tmphbtjn
consensus: emerging
consensus_note: >-
  Two frontier labs cite it and ship it — DeepSeek-V4's FP4 quantization-aware
  training on MoE expert weights and the indexer QK path, and Kimi K3's MXFP4
  quantization-aware post-training. Not `converged`: most released models
  still quantize per-tensor or not at all, and the format is young enough that
  hardware support is the reason it is spreading.
title: 'Quantize with block-scaled microscaling formats rather than one scale per tensor'
version: 1
tags:
- inference-optimization
date: '2026-09-08'
published: '2023-10-01'
source:
# The specification and the ablations across regimes. The two frontier
# reports that ship it cite it without re-measuring, so they are adoption
# and live in consensus_note (ADR-017).
- LIT-197
implementations:
- 'DeepSeek-V4'
- 'Kimi K3'
summary: >-
  Rouhani et al. (2023), [LIT-197](../literature.d/LIT-197.md) — an MX block is 32 elements sharing one
  E8M0 scale, so applying the scale is an exponent adjustment rather than a
  multiply. Shrinking the scope of the scale contains outliers locally
  instead of letting a few large values cost every small one its precision.
  6-bit MX trains large transformers to FP32 accuracy with no recipe change.
---

# SOTA-163: Quantize with block-scaled microscaling formats rather than one scale per tensor

## Source

Rouhani et al. (2023), [LIT-197](../literature.d/LIT-197.md) — [ARXIV-2310.10537](https://arxiv.org/abs/2310.10537).

An MX block is a vector of k elements sharing one scale. The shipped formats
use **block size 32** and an **E8M0** scale — eight bits of exponent, no
mantissa — so the scale is a power of two and applying it is an exponent
adjustment rather than a multiply. The element type is independent: MXFP8
(E4M3 or E5M2), MXFP6 (E2M3 or E3M2), MXFP4 (E2M1), MXINT8.

**Why block scaling and not per-tensor.** A single scale for a whole tensor
has to cover its whole dynamic range, so a few large values cost every small
one its precision. Thirty-two elements is a small enough neighbourhood that
outliers are contained locally. That is the same problem massive activations
and quantization outliers pose, met by shrinking the scope of the scale
rather than by changing the model — which is why it composes with everything
else instead of competing with it.

## What each width can bear, which is the part to read before choosing one

| Width | Regime |
|---|---|
| 8-bit MX | **Direct-cast** inference on FP32 pretrained models, minimal loss, no calibration or fine-tuning |
| 6-bit MX | Close to FP32 after quantization-aware fine-tuning or a PTQ method |
| 6-bit MX | **Training** — weights, activations *and* gradients — to FP32 accuracy with no recipe change |
| 4-bit weights | A minor drop |

The 6-bit training result is the headline and the paper claims it as the
first sub-8-bit instance. The clause that matters operationally is **"without
modifications to the training recipe"**: the paper is explicit that user
friction is a third axis alongside accuracy and efficiency, and that a format
nobody can adopt without rewriting their recipe does not count as practical.
That is stated as a result rather than an aside, and it should be read as one.

## What "FP4" means in the record's other notes

DeepSeek-V4 and Kimi K3 both say FP4 and MXFP4, and both mean this: a 4-bit
element inside a 32-element block with a shared power-of-two scale, not a
bare 4-bit float. Reading those reports without this practice makes their
precision decisions look like implementation details rather than choices.

## The decision this does not make for you

<!-- inactive-ok-block: SOTA-160 — Proposed, and named as the other half
     of the same decision -->
Which width goes *where in the pipeline* is a separate question, and
[SOTA-160](SOTA-160.md) is the practice about it: quantization damage grows with how
much data the model was trained on, so the pretraining budget and the
quantization plan are coupled. This practice says what the format can bear in
each position; that one says the position is not free to choose late.

## Known implementations

- DeepSeek-V4 — FP4 quantization-aware training on MoE expert weights and the
  indexer QK path, applied in post-training.
- Kimi K3 — MXFP4 quantization-aware post-training; the release is in MXFP4.
