---
number: 230
status: 'Active'
formerly:
- SOTA-tmpasvp1
title: 'Quantize the frozen base to 4-bit and keep the adapters in 16-bit'
version: 1
tags:
- adaptation-and-tuning
- systems-optimization
- numerics-and-precision
consensus: converged
consensus_note: >-
  The default path for fine-tuning a model too large for the GPU in front of
  you, shipped as the 4-bit branch of the major PEFT tooling rather than
  argued about in the literature. No paper in this record contests it; none
  replicates it either, so the agreement is adoption rather than
  measurement (DP-005).
date: '2026-09-17'
source:
- LIT-378
introduced_by:
- LIT-378
implementations:
- 'bitsandbytes'
- 'the 4-bit path in the major PEFT libraries'
- 'Guanaco'
summary: >-
  Dettmers et al. (2023), [LIT-378](../literature.d/LIT-378.md) — [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314). Store the frozen base
  weights in 4-bit NormalFloat and dequantize to BFloat16 for every matrix
  multiply, training only 16-bit LoRA adapters. Fine-tuning a 65B model falls
  from >780GB to <48GB with no measured loss against a 16-bit fully
  fine-tuned baseline, because the arithmetic never happens in 4 bits.
---

# SOTA-230: Quantize the frozen base to 4-bit and keep the adapters in 16-bit

## Source

Dettmers et al. (2023), [LIT-378](../literature.d/LIT-378.md) — [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314).

## The method

One storage type and one computation type. The frozen base is held in 4-bit
NormalFloat; whenever a weight is used it is dequantized to BFloat16 and the
multiply happens in 16 bits. Gradients pass through that dequantized base but
are computed only for the adapter parameters, which are BFloat16 throughout.

**Nothing is multiplied in 4 bits**, and that is why the accuracy holds. The
quantization buys resident memory for weights that are never updated; the
arithmetic is identical to 16-bit LoRA. Treating it as a precision decision
rather than a storage one is what makes people expect a quality cost that the
measurements do not show.

Two refinements carry their weight. **Double quantization** quantizes the
per-block quantization constants, worth about 0.37 bits per parameter — some
3GB on a 65B model, which is often the difference between fitting and not.
**Paged optimizers** page optimizer state to CPU on unified memory so that
gradient-checkpointing spikes do not OOM; that one is an engineering answer to
a crash rather than a claim about learning.

## Why NF4 rather than any 4-bit type

The data type is matched to the distribution: weights are approximately
normal, so the quantiles are placed for a normal rather than uniformly. The
paper checks this empirically instead of resting on the optimality argument —
mean Pile Common Crawl perplexity across 125M–13B OPT, BLOOM, LLaMA and
Pythia:

| type | mean PPL |
|---|--:|
| Int4 | 34.34 |
| Float4 (E2M1) | 31.07 |
| Float4 (E3M0) | 29.48 |
| **NF4 + double quantization** | **27.41** |

## Conditions

The saving is in **resident weight memory**, so it helps exactly when the
frozen base is what does not fit. It does nothing for activation memory, and
the dequantize-per-multiply costs bandwidth — the paper reports no runtime
degradation at its scales, which is a claim about those scales rather than a
general guarantee.

It also inherits every condition of the adapter method underneath it: this
practice is a way of *holding the base*, not a way of adapting. In particular
it inherits [SOTA-231](SOTA-231.md) — quantizing the base does not excuse leaving the
adapters on the query and value projections alone, and the same paper is the
source of both.

## Known implementations

- `bitsandbytes`, and the 4-bit path in the major PEFT libraries
- Guanaco, the paper's own model family — 65B fine-tuned in 24 hours on one GPU
