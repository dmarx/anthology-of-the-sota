---
number: 234
status: 'Proposed'
formerly:
- SOTA-tmpr318t
title: 'Train in the target low-bit format from scratch rather than quantizing a finished model'
version: 1
tags:
- systems-optimization
promote_when: >-
  A second group training a model at or above 3B in a low-bit format from
  scratch and matching a full-precision baseline at equal tokens — the
  architecture need not be ternary, because the claim here is about deciding
  the format before the run rather than about {-1, 0, +1}. Stronger still:
  any frontier pretraining run that fixes its serving format in advance.
  What would NOT satisfy it: a better post-training quantization method,
  which is the other branch; a ternary model below 3B, which is outside the
  evidence; or ternary inference kernels landing, which would strengthen the
  compute argument without testing the training claim.
consensus: unreplicated
consensus_note: >-
  One group, one architecture, and no frontier model ships this way. Filed
  because the argument is measured and the alternative branch is fully
  represented here, not because the field has moved (DP-006). The strongest
  independent support is indirect: [LIT-186](../literature.d/LIT-186.md) reports the cost of the
  post-training route rising with training tokens, which is the pressure
  this route does not face.
date: '2026-09-17'
source:
- LIT-380
introduced_by:
- LIT-380
implementations:
- 'BitNet b1.58'
summary: >-
  Ma et al. (2024), [LIT-380](../literature.d/LIT-380.md) — [ARXIV-2402.17764](https://arxiv.org/abs/2402.17764). Decide the serving format
  before training and train in it, rather than training in FP16 and
  compressing afterwards. Ternary weights trained from scratch match an FP16
  model of equal size and token budget from 3B upward — but the compute
  argument assumes hardware built for the format, and only the memory saving
  is measured on machines that exist.
---

# SOTA-234: Train in the target low-bit format from scratch rather than quantizing a finished model

## Source

Ma et al. (2024), [LIT-380](../literature.d/LIT-380.md) — [ARXIV-2402.17764](https://arxiv.org/abs/2402.17764).

## The claim

The record's quantization practices all act on a finished model — [SOTA-185](SOTA-185.md)
compensates rounding error into the columns not yet quantized, [SOTA-163](SOTA-163.md)
chooses the block-scaled format to round into. This is the other branch:
constrain the weights during training and never hold a high-precision
checkpoint at all.

BitNet b1.58 does it with ternary weights, {-1, 0, +1}, 8-bit activations, and
`BitLinear` in place of `nn.Linear`. At matched size and token budget it
reaches FP16 perplexity and end-task accuracy **from 3B upward**.

## Why this is not just another compression ratio

Two arguments, and they are worth separating because only one is measured on
hardware you can buy.

**Measured.** Weight memory and bandwidth fall with the format, which is
ordinary and real: 2.22GB at 3B, a 3.55× reduction, and at 70B on two 80GB
A100s the batch ceiling goes 16 → 176 and throughput 333 → 2977 tokens/s.

**Argued.** With ternary operands the matrix multiply reduces to integer
addition and the multiplications disappear, which is where the energy claim
comes from. That is a fact about arithmetic and a bet about silicon: it
assumes kernels, and eventually hardware, built for the format. The paper says
as much. On stock GPU matmul the memory saving survives and the arithmetic
saving does not.

## Conditions

**Below 3B it does not hold, and the paper's own table says so** — 700M
perplexity 12.87 against 12.33, 1.3B 11.29 against 11.25, 3B 9.91 against
10.04. Behind, level, ahead. This is a practice for models large enough to
have been on the right side of that crossover.

**It is not available retroactively.** There is no conversion path here; the
decision has to be made before the run, which makes it the most expensive
commitment in the quantization family to get wrong. Where a model already
exists, [SOTA-185](SOTA-185.md) and [SOTA-163](SOTA-163.md) are the practices that apply.

`Proposed`, not `Active`. The measurements are real and the branch is
unrepresented in this record, which is reason enough to file it; but one
group, one architecture, and nothing at the frontier ships this way, so the
record should not yet be telling anyone to plan a pretraining run around it.

## Why it is worth watching rather than dismissing

[LIT-186](../literature.d/LIT-186.md) reports post-training quantization damage **rising with the number
of training tokens** — far enough that extra pretraining data becomes harmful
for a model that will be quantized later.
<!-- inactive-ok: SOTA-160 — Proposed, and the practice this one is the alternative resolution to; citing a live practice instead would name the wrong document -->
[SOTA-160](SOTA-160.md) already tells a reader to
treat the token budget and the quantization plan as one decision.

This practice is the other way out of that bind. If the format is fixed before
training there is no compression step to be damaged, and the token budget
stops trading against the serving precision. The two papers never cite each
other; the tension is the record's own to notice.
