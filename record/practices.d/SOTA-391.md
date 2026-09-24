---
number: 391
status: Proposed
formerly:
- SOTA-tmppogp0
promote_when: >-
  Attention resolution reported by a group that is not proposing a position
  encoding — computed for two or three existing schemes as a diagnostic,
  ideally alongside a downstream long-context measurement so the correlation
  can be checked. The cheapest version: resolution for RoPE at its training
  length and at 2x, on any model already trained, against that model's
  measured long-context behaviour. What would NOT meet it: another encoding
  paper reporting its own resolution as higher than the baselines', which is
  the metric being used as an advertisement rather than as an instrument.
title: 'Estimate attention resolution before training when choosing a position encoding, and measure it across the extrapolation boundary'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
- attention-techniques
date: '2026-09-24'
source:
- LIT-638
introduced_by:
- LIT-638
consensus: unreplicated
consensus_note: >-
  One group, one paper, and the metric has not been picked up as a diagnostic
  by anyone who is not proposing an encoding — which is the specific weakness
  a `promote_when` can ask about. What is not in doubt is that the quantity is
  cheap to compute and that the numbers it produces separate the incumbents
  sharply. What is untested is whether resolution *predicts* anything a
  practitioner cares about: the paper shows its own method scoring highest and
  performing best, which is one point, not a correlation.
implementations:
- torchscale
summary: >-
  Sun et al. (2022), [LIT-638](../literature.d/LIT-638.md) — attention resolution scores how well an
  attention pattern distinguishes token distance, and is estimable from the
  encoding **before a run**. Measured at the training length and twice it:
  **RoPE 0.91 → 0.08, ALiBi 0.81 → 0.88.** The record has four practices
  about rotary encoding and held no measure of this.
---

# SOTA-391: Estimate attention resolution before training when choosing a position encoding, and measure it across the extrapolation boundary

## Source

Sun et al. (2022), [LIT-638](../literature.d/LIT-638.md), §3.1 and §4.3.

## When this applies

You are choosing a position encoding, or you have one and want to know what it
will do past the length you trained at, and you would rather find out before
spending the run.

## Do this

**Compute the quantity.** With `s[n]` the expected pre-softmax attention score
at token distance `n`:

    R(s) = Σᵢ e^{s[i]}(e^{s[i]} − e^{s[i+1]}) / (Σᵢ e^{s[i]})²

`s[n]` comes from the encoding's own form, so `R` is available at design time;
empirically it is estimated per layer as `ŝ[n] = 1/(N−n) · E[Σᵢ e_{i(i−n)}]`
and averaged.

**Measure it at two lengths, not one.** The whole content of the measurement
is in the pair. At the 1024 training length and at 2048:

| variant | in-distribution | extrapolated |
| --- | --: | --: |
| RoPE | **0.91** | **0.08** |
| absolute sinusoidal | 0.87 | 0.28 |
| ALiBi | 0.81 | **0.88** |

**A single number tells you the wrong thing.** RoPE is the best of the three
inside the training length and the worst outside it by an order of magnitude.
Anyone who ranked encodings on in-distribution resolution would pick exactly
the one that fails.

## What this buys, put carefully

It is a **cheap diagnostic with an untested link to outcomes**, and both
halves matter.

Cheap: no training run, no long-context benchmark, no fine-tuning. It is a
property of the attention pattern that follows from the encoding.

Untested: the paper shows its own encoding scoring highest and also performing
best, which is a single coincident point. **Nobody has shown that resolution
predicts downstream long-context behaviour across schemes**, and the
`promote_when` asks for exactly that. Treat a resolution collapse as a reason
to go and measure, not as a measurement.

## Limitations

- **One model scale and one corpus.** 24 layers, 1024 hidden, a Pile subset,
  training length 1024. Whether the resolution numbers or their ordering move
  with scale is not examined.
- **The metric rewards monotonic decay of attention with distance**, which is
  a plausible proxy for position-recognisability and is also close to what
  ALiBi imposes *by construction*. That ALiBi scores stably is therefore
  partly a statement about the metric's shape, and the paper's own reading
  agrees — ALiBi's stability "comes from explicit decay, but it prevents the
  model from learning position dependency itself."
- **It measures the attention pattern, not the model.** In the same paper,
  adding blockwise causal attention at inference time raises resolution at
  2048 from 0.54 to 1.08 without touching the encoding — so a resolution
  figure is a property of a *configuration*, and the masking is part of it.
