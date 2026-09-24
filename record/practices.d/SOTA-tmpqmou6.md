---
status: Proposed
promote_when: >-
  A second group reporting the same direction on models they trained, or a
  frontier model report stating that its weight decay, dropout or training
  dtype was set with post-training quantization in view and reporting the
  quantized result. What would NOT move it: another INT8 result on a model
  trained for other reasons, which cannot separate the recipe from everything
  else about that model.
consensus: unreplicated
consensus_note: >-
  One group, one controlled study, validated to 52B. bf16 over fp16 is already
  near-universal at frontier scale for unrelated reasons, so that leg is
  common practice arrived at independently; the weight decay, dropout and
  clipping legs are not chosen for quantization anywhere the record can see.
  Nobody has disputed it and nobody has repeated it.
title: 'Choose pre-training weight decay, dropout, clipping and precision for the quantization you intend to ship'
version: 1
tags:
- numerics-and-precision
- training-optimization
date: '2026-09-24'
source:
- LIT-tmp7791d
introduced_by:
- LIT-tmp7791d
implementations: []
explained_by:
- THEORY-tmp3s87v
---

# SOTA-tmpqmou6: Choose pre-training weight decay, dropout, clipping and precision for the quantization you intend to ship

## Source

Ahmadian et al. (2023), `LIT-tmp7791d`.

## What to do

If the model will be served quantized, four pre-training choices move
post-training quantization degradation by more than an order of magnitude, at
comparable pre-quantization quality:

| choice | set it to | measured effect |
| --- | --- | --- |
| weight decay | **0.1**, not 0.001 | 0.09% degradation vs 1.36% |
| dropout | **0** | degradation rises monotonically with it |
| gradient clipping | **on**, threshold 1.0 | helps, and offsets a low weight decay |
| half precision | **bf16**, not fp16 | fp16 with low weight decay: 1.73% |

At 52B with all four, plain INT8 costs nothing measurable — a 0.08% *gain* on
the eight-task zero-shot average and 0.01% loss on LAMBADA, HellaSwag and PIQA
— against about 42% degradation reported for OPT-66B.

## Why this is a recommendation and not a curiosity

**The alternative is more expensive.** Every other quantization practice in
this record repairs the problem after the fact: isolate the outlier dimensions
([SOTA-355](SOTA-355.md)), scale the salient channels before rounding ([SOTA-356](SOTA-356.md)), absorb
the outliers into a high-precision branch ([SOTA-314](SOTA-314.md)). Those are real and they
cost kernel complexity, mixed-precision paths, or rank. This one costs a
hyperparameter you were setting anyway.

**The two halves of the trade are measurable at different times**, which is
the awkward part. The cost of a higher weight decay or no dropout is paid
during pre-training and shows up in the model you get; the benefit is paid at
serving time, months later. `LIT-tmp7791d` reports comparable pre-quantization
quality across its variants on its evaluations, which is the evidence that the
cost is small — on one architecture family, on those evaluations.

## Conditions

**It is one group's controlled study.** The design is good — same
architecture, one axis at a time, every variant from scratch, comparable
pre-quantization quality — and it is still one architecture family and one set
of runs. The `unreplicated` reading is about that, not about the design.

**bf16 is the leg you are probably already on.** Frontier training moved to
bf16 for stability reasons that have nothing to do with quantization, so that
row mostly explains an existing choice rather than changing one. The weight
decay, dropout and clipping rows are the ones that ask for something.

**This does not obviate outlier handling.** It reduces the outliers you have
to handle. Models trained by someone else, or before this was known, still
have them, and [SOTA-355](SOTA-355.md) is what to do then.

**The knobs have other jobs.** Weight decay and dropout are regularizers and
clipping is a stability measure. This practice says what they do to
quantization; it does not say they should be set for that reason alone, and
nothing here measures what the recommended settings cost on a task where
dropout was earning its place — see [SOTA-240](SOTA-240.md), which says where dropout is
worth having.

## Known implementations

- None the record can name. `LIT-tmp7791d`'s own 410M–52B models are the only
  ones trained this way on purpose; BLOOM-176B's relative robustness is
  consistent with it (bf16) and was not a quantization decision.
