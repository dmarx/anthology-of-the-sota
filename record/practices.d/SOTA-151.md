---
number: 151
status: Active
formerly:
- SOTA-tmp55o8w
consensus: converged
consensus_note: >-
  Two independent groups (LIT-192, LIT-193), and the method ships in
  production: Qwen3.8-27B's own serving configuration extends 262144 to 1M
  through YaRN at factor 4.0. Nobody in the record argues the mechanism is
  wrong; the live question is whether to need it at all.
# Corrective succession (ADR-017). Entirely conditional on the model having
# used RoPE — this is the step a SOTA-063 model takes when it needs a longer
# window than it was trained on — and the defect it names as its motivation is
# that RoPE does not extrapolate, with fine-tuning at the longer length barely
# helping.
corrects:
- SOTA-063
title: "Extend a trained model's context by rescaling RoPE, not by fine-tuning at the longer length"
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Corrected. The practice claimed that a model which already exists cannot
    take the NoPE alternative, so the two could not be contested.
    LIT-209 converts an 8B RoPE model pretrained on 15T tokens by
    continued pretraining, at parity on short benchmarks. The
    recommendation is unchanged; the reason for not filing it as contested
    is now cost rather than impossibility.
tags:
- representation-and-encoding
date: '2026-09-07'
source:
- LIT-192
- LIT-193
summary: >-
  Chen et al. (2023) and Peng et al. (2023) — RoPE does not extrapolate, and
  fine-tuning at the longer length barely helps: more than 10000 batches moved
  LLaMA's effective window from 2048 to 2560. Rescaling the position indices
  so they land back in the trained range reaches 32× that in under 1000 steps.
  YaRN rescales per wavelength rather than uniformly and gets to 128k with 10×
  fewer tokens.
---

# SOTA-151: Extend a trained model's context by rescaling RoPE, not by fine-tuning at the longer length

## Source

Chen et al. (2023), [LIT-192](../literature.d/LIT-192.md) — Position Interpolation. Peng et al. (2023),
[LIT-193](../literature.d/LIT-193.md) — YaRN.

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

## Why the frequencies fail in the first place

The practice was filed on the observation that RoPE does not extrapolate and
on two remedies for it. [LIT-210](../literature.d/LIT-210.md) supplies the mechanism underneath, by
opening a trained model rather than reasoning from the encoding's definition.

RoPE's frequency band is used for two jobs. The highest frequencies build
positional attention heads — robustly, and provably so. The lowest carry
semantic content in high-norm channels, and Theorem 6.1 shows those channels
*cannot* be robust once the context is long. So the part of RoPE that breaks
at length is a specific part, and it is the part [LIT-193](../literature.d/LIT-193.md) already treats
differently: YaRN leaves the dimensions that never complete a rotation alone
and interpolates the ones that do, which is this distinction reached from the
other side.

It also explains the cheap move this practice does not cover. Raising the
base wavelength from 10,000 to 500,000 — Code Llama's, adopted by Llama 3 —
pushes the fragile low-frequency channels toward being distance-agnostic, and
the paper's own remedy is to remove them outright: keeping a fraction p of
RoPE's frequencies held perplexity and improved it at 2B, with p=1 being RoPE
and p=0 being NoPE.

Not added to `source:`. This work explains why the problem exists; it does
not evidence that rescaling is the answer, and the sources of a practice are
what its recommendation rests on.

## The alternative: not needing it

Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) reaches 1M tokens with **no** positional encoding on its
global-attention layers, and says in as many words that it therefore
extrapolates "without any positional-encoding modification, such as RoPE
rescaling or interpolation". Position sensitivity comes from the recurrence
and decay of the interleaved linear-attention layers instead.

The alternative has a source of its own now. [LIT-207](../literature.d/LIT-207.md) trained five
positional schemes from scratch under identical hyperparameters and found the
one that generalizes to unseen lengths is the absent one — and showed why a
decoder-only transformer can represent absolute and relative position without
being given either. Kimi Linear ([LIT-133](../literature.d/LIT-133.md)) cites it and repeats the comparison
at 48B, against a RoPE version of itself.

So the record holds two answers to the same problem and they are not
competing versions of one technique. This practice is what a RoPE model has
to do; [SOTA-153](SOTA-153.md) is a design that removes the need.

**This entry used to say the choice was settled at pretraining, so that a
model which already exists cannot take the other option. That is wrong.**
[LIT-209](../literature.d/LIT-209.md) converted an 8B RoPE model pretrained on 15T tokens to a
NoPE-global architecture by continued pretraining, and it came back at parity
on short benchmarks with long-context capability gained. Conversion is not
free and most readers of this practice will not do it, which is why the two
are still not filed as `contested` — but the reason is cost, not
impossibility, and the record should not have claimed the stronger one.

## Known implementations

- Qwen3.8-27B — `rope_type: yarn`, `factor: 4.0` over an
  `original_max_position_embeddings` of 262144, i.e. the documented route
  from its native window to 1M ([LIT-135](../literature.d/LIT-135.md))
- Falcon-H1 ([LIT-120](../literature.d/LIT-120.md)) and Olmo 3 ([LIT-130](../literature.d/LIT-130.md)) both cite Position Interpolation;
  Olmo 3 and Kimi K3 both cite YaRN
