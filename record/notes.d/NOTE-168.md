---
number: 168
status: Read
formerly:
- NOTE-tmpkr4sc
paper: LIT-380
title: 'The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits'
version: 1
date: '2026-09-17'
summary: >-
  Ternary weights trained from scratch, matching FP16 from 3B upward at equal
  size and tokens. The interesting claim is not the compression ratio but
  that the matrix multiply becomes integer addition — which is a bet on
  hardware, and the one place the paper's argument outruns its measurements.
---

# NOTE-168: The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits

Read from [LIT-380](../literature.d/LIT-380.md) — [ARXIV-2402.17764](https://arxiv.org/abs/2402.17764).

## What it does

`BitLinear` in place of `nn.Linear`, weights constrained to {-1, 0, +1} by an
absmean quantization, activations at 8 bits, trained from scratch. The name is
arithmetic: log₂3 ≈ 1.58 bits per weight.

The inclusion of **0** is not a detail. The paper attributes its advantage
over binary BitNet to "explicit support for feature filtering" — a weight can
decline to participate, which two states cannot express. That is the whole
difference between 1 bit and 1.58.

## Where the claim is strong, and where it stops

Perplexity against LLaMA at matched size and tokens:

| size | LLaMA | BitNet b1.58 |
|---|--:|--:|
| 700M | 12.33 | 12.87 |
| 1.3B | 11.25 | 11.29 |
| 3B | 10.04 | **9.91** |

Behind, level, ahead. The paper states the match "starting from a 3B size",
and the table is why that phrasing is careful rather than hedged. **Anyone
applying this below 3B is outside the evidence**, and the direction of the
error is not in their favour.

Cost side, at 3B: 2.22GB (3.55×) and 1.87ms (2.71×). At 70B on two 80GB
A100s: max batch 16 → 176 (11×), throughput 333 → 2977 tokens/s (8.9×).
Scaling in tokens is checked too — a 3B on 2T tokens following the StableLM-3B
recipe, zero-shot on Winogrande, PIQA, SciQ, LAMBADA and ARC-easy.

## The part that is a bet rather than a measurement

The energy and compute argument rests on matrix multiplication reducing to
integer addition — "the matrix multiplication of BitNet only involves integer
addition, which saves orders of energy cost". That is true of the arithmetic
and not yet true of the machines: it assumes kernels, and ultimately silicon,
built for ternary operands. The paper says so, and opens with "opens the door
for designing specific hardware".

So the practice this supports has to be split carefully. **Memory and
bandwidth savings are measured on existing hardware.** The arithmetic and
energy savings are a claim about hardware that mostly does not exist. Filing
the second as though it were the first would be recording a roadmap as a
result.

## What it does to the record

The anthology holds the post-training branch in full — [SOTA-185](../practices.d/SOTA-185.md) compensates
rounding error into the columns not yet quantized, [SOTA-163](../practices.d/SOTA-163.md) chooses the
block-scaled format — and nothing at all on training in the target format
instead.

Reading it beside [LIT-186](../literature.d/LIT-186.md) is what makes the practice worth filing rather
than noting. Scaling Laws for Precision reports post-training quantization
damage **increasing with training tokens**, far enough that additional
pretraining data becomes harmful for a model destined to be quantized.
<!-- inactive-ok: SOTA-160 — Proposed, and named as the practice this paper offers a second resolution to; the tension is the content -->
[SOTA-160](../practices.d/SOTA-160.md) already encodes that as "treat the token budget and the
quantization plan as one decision". This paper is the other resolution of the
same tension: if the format is decided in advance, there is no compression
step to be damaged by, and the token budget stops trading against it.

Not filed: anything about ternary *serving* of models trained in higher
precision, which this paper does not do and does not claim.
