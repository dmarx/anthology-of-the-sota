---
number: 161
status: Active
formerly:
- SOTA-tmpbp6p9
consensus: unreplicated
consensus_note: >-
  One paper for the mechanism and one production run for the remedy — Kimi
  K3 at 2.8T keeps the attention output in FP32 and redesigns its kernel to
  absorb the doubled on-chip footprint, citing this. Nobody has disputed it
  and nobody has independently reproduced the analysis.
title: "Keep the attention output in FP32 during training, because flash attention's rounding bias compounds instead of cancelling"
version: 1
tags:
- model-stability
- flash-attention
date: '2026-09-08'
source:
# The paper that isolated the mechanism and tested a targeted fix. Kimi K3
# shipping the FP32 output at 2.8T is adoption and lives in consensus_note
# (ADR-017).
- LIT-198
extends:
- SOTA-085
implementations:
- 'Kimi K3'
summary: >-
  Qiu et al. (2025), [LIT-198](../literature.d/LIT-198.md) — putting flash attention in BF16 while the
  FFN goes to FP8 sometimes explodes, and the cause is two things at once:
  attention produces low-rank updates repeated across steps and tokens, and
  low-precision addition rounds with a *bias*. The biased error rides the
  repeated update and compounds into a systematic gradient bias instead of
  averaging out.
---

# SOTA-161: Keep the attention output in FP32 during training, because flash attention's rounding bias compounds instead of cancelling

## Source

Qiu et al. (2025), [LIT-198](../literature.d/LIT-198.md) — [ARXIV-2510.04212](https://arxiv.org/abs/2510.04212).

Industrial practice puts memory-bound operations like flash attention in
BF16 while pushing compute-bound ones like the FFN to FP8. That configuration
sometimes explodes, and the explosion had been treated as a random
instability to work around.

It is not random, and it takes **two** causes — neither sufficient alone:

- **Attention produces low-rank representations that repeat**, across
  training steps and across tokens. The same direction is updated again and
  again.
- **Rounding in low-precision addition is biased**, not symmetric. BF16
  addition loses precision at exponent alignment and again at
  round-to-nearest, and the residual does not average out.

Put together, the biased errors act as coefficients on the repeated low-rank
update. Instead of cancelling over steps they compound into a systematic
gradient bias, driving the spectral norm of weights and activations up until
training derails.

## What to do

Keep the attention output in FP32 during training. Kimi K3 does exactly this
at 2.8T and redesigns its kernel to absorb the doubled on-chip footprint —
which is the cost, and it is a real one.

The paper's own test is the narrower version: a minimal modification to flash
attention that removes the bias in the rounding error lets the low-rank
updates cancel again and stabilises training. If you control the kernel, that
is the cheaper fix; if you do not, the FP32 output is the one available.

## Why the isolation matters more than the remedy

The paper works down: tiling is *not* the source; the failure originates in a
single layer; it is linked to one specific computation; the numerical error
there is the source; and it is localised to particular attention heads. That
sequence turns "low precision is unstable" into a mechanism, and the
mechanism is what tells you which of several remedies is the cheap one.

This is the second instance in the record of an instability with a named
cause and a targeted fix rather than a hyperparameter workaround —
[SOTA-131](SOTA-131.md)'s QK-Clip, for attention-logit growth, is the first. The pattern
worth carrying is that a loss spike is not a flake.

## What it qualifies

<!-- inactive-ok-block: ADR-012 — Proposed, and named as the decision that
     describes the bodyless stub this qualifies -->
[SOTA-085](SOTA-085.md) says to use flash attention wherever the hardware supports it, and
says nothing about precision — it is one of the bodyless migration stubs
[ADR-012](../decisions.d/ADR-012.md) is about, so the configuration that fails is not something it
recommends so much as something it fails to rule out. This practice extends
it with the part that turned out to matter.

## Known implementations

- Kimi K3, which keeps the attention output in FP32 during training.
