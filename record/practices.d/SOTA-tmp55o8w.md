---
status: Active
consensus: converged
consensus_note: >-
  Two independent groups (LIT-tmp9rps9, LIT-tmpsei2t), and the method ships in
  production: Qwen3.8-27B's own serving configuration extends 262144 to 1M
  through YaRN at factor 4.0. Nobody in the record argues the mechanism is
  wrong; the live question is whether to need it at all.
title: "Extend a trained model's context by rescaling RoPE, not by fine-tuning at the longer length"
version: 1
tags:
- attention-techniques
date: '2026-09-07'
published: '2023-06-01'
source:
- LIT-tmp9rps9
- LIT-tmpsei2t
summary: >-
  Chen et al. (2023) and Peng et al. (2023) — RoPE does not extrapolate, and
  fine-tuning at the longer length barely helps: more than 10000 batches moved
  LLaMA's effective window from 2048 to 2560. Rescaling the position indices
  so they land back in the trained range reaches 32× that in under 1000 steps.
  YaRN rescales per wavelength rather than uniformly and gets to 128k with 10×
  fewer tokens.
---

# SOTA-tmp55o8w: Extend a trained model's context by rescaling RoPE, not by fine-tuning at the longer length

## Source

Chen et al. (2023), [LIT-tmp9rps9](../literature.d/LIT-tmp9rps9.md) — Position Interpolation. Peng et al. (2023),
[LIT-tmpsei2t](../literature.d/LIT-tmpsei2t.md) — YaRN.

The problem is not that a longer window is expensive to train. It is that
training it directly barely works: fine-tuning a pretrained LLaMA at the
longer length moved its *effective* context from 2048 to 2560 after more than
10000 batches. Meanwhile pushing the model past its trained window without
adaptation does not degrade gracefully — perplexity goes to numbers
comparable to an untrained model, and a question at position 3000 becomes
unanswerable even from evidence at position 2900.

The remedy is to change the position indices rather than the weights. Scale
them so the longest relative distance the model is asked about is one it
already saw in pretraining, then fine-tune briefly to settle. Under 1000
steps takes LLaMA 7B–65B to 32768 tokens, a 16× extension, at a cost
negligible against pretraining.

**Scale by wavelength, not uniformly.** Stretching every RoPE dimension
equally destroys the high-frequency components, and the effect compounds:
uniform interpolation stalls around a scale factor of 8 even with
fine-tuning. YaRN's diagnosis is that RoPE is not purely relative — in
dimensions whose wavelength exceeds the pretraining context, the rotation
never completes and absolute position survives — so those dimensions should
be left alone while the fully-rotating ones are interpolated. With a
temperature on the pre-softmax logits, folded into the rotary tables so it
costs nothing at run time, that reaches 128k with 10× fewer tokens and 2.5×
fewer steps.

Conditions: this is for RoPE models, and it is a *post-hoc* extension of a
finished model, which is a different question from how to train for a long
window in the first place ([SOTA-139](SOTA-139.md)). A short fine-tune is still required —
the scaling alone is not free of adaptation, except under Dynamic Scaling at
inference, which works without fine-tuning but is a graceful-degradation
measure rather than a way to reach a target length.

## Variations

**Dynamic Scaling** recomputes the scale factor per forward pass from the
current sequence length instead of pinning it at the target. A fixed factor
costs quality below the target and breaks abruptly above it; the dynamic form
degrades gracefully and, notably, works on unmodified pretrained models.

## The alternative: not needing it

Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) reaches 1M tokens with **no** positional encoding on its
global-attention layers, and says in as many words that it therefore
extrapolates "without any positional-encoding modification, such as RoPE
rescaling or interpolation". Position sensitivity comes from the recurrence
and decay of the interleaved linear-attention layers instead.

So the record holds two answers to the same problem and they are not
competing versions of one technique. This practice is what a RoPE model has
to do; NoPE-plus-linear-attention is a design that removes the need. Which is
available to you is decided at pretraining, which is why this is not filed as
`contested` — a model that already exists cannot take the other option.

## Known implementations

- Qwen3.8-27B — `rope_type: yarn`, `factor: 4.0` over an
  `original_max_position_embeddings` of 262144, i.e. the documented route
  from its native window to 1M ([LIT-135](../literature.d/LIT-135.md))
- Falcon-H1 ([LIT-120](../literature.d/LIT-120.md)) and Olmo 3 ([LIT-130](../literature.d/LIT-130.md)) both cite Position Interpolation;
  Olmo 3 and Kimi K3 both cite YaRN
