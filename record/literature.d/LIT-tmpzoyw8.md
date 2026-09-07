---
status: Active
title: 'Why Low-Precision Transformer Training Fails: An Analysis on Flash Attention'
version: 1
tags:
- model-stability
date: '2026-09-07'
published: '2025-10-01'
arxiv: '2510.04212'
first_author: 'Qiu'
keywords:
- 'low-precision'
- 'flash-attention'
- 'training-instability'
- 'rounding-error'
- 'loss-spikes'
summary: >-
  Qiu et al. (2025), [ARXIV-2510.04212](https://arxiv.org/abs/2510.04212). The first mechanistic account of why
  training with flash attention in low precision explodes. Two things have to
  coincide: attention representations that are low-rank and similar across
  steps and tokens, and rounding error in BF16 addition that is *biased*
  rather than symmetric. The bias acts as a coefficient on the repeated
  low-rank update, so the errors accumulate instead of cancelling and the
  spectral norm of weights runs away. A minimal change to flash attention that
  de-biases the rounding stops it.
---

# LIT-tmpzoyw8: Why Low-Precision Transformer Training Fails: An Analysis on Flash Attention

Qiu et al. (2025) — [ARXIV-2510.04212](https://arxiv.org/abs/2510.04212)

## Key takeaways

- **The failure being explained.** Industrial practice puts memory-bound
  operations like flash attention in BF16 while pushing compute-bound ones
  like the FFN to FP8. That configuration sometimes explodes, and the
  explosion had been treated as a random instability to be worked around.
- **It takes two causes, and neither alone is enough.** First, the attention
  mechanism produces **low-rank representations that are similar across
  training steps and across tokens**. Second, rounding in low-precision
  addition is **biased**, not symmetric — BF16 addition loses precision at
  exponent alignment and again at the round-to-nearest step, and the residual
  does not average out. The biased errors then act as coefficients on the
  repeated low-rank update, so instead of cancelling over steps they compound
  into a systematic gradient bias, driving the spectral norm of weights and
  activations up until training derails.
- **The isolation is the convincing part.** The paper works down: tiling is
  *not* the source; the failure originates in a single layer; it is linked to
  one specific computation; the numerical error there is the source; and it is
  localised to particular attention heads. That sequence is what turns "low
  precision is unstable" into a mechanism.
- **The test.** A minimal modification to flash attention that removes the
  bias in the rounding error lets the low-rank updates cancel again and
  stabilises training — which is the experiment that makes the account causal
  rather than correlational.

## Standing in the anthology

Kimi K3's stated reason for a decision the record already carries. [LIT-131](LIT-131.md)
notes that K3 keeps the attention output in **FP32 during training** to
correct a biased rounding error in flash attention, and redesigns its kernel
to absorb the doubled on-chip footprint. This is the paper it is citing, and
without it that choice reads as caution rather than as a fix for a named
failure mode.

It also stands against a habit the record should not adopt: calling a loss
spike a flake. This is the second instance in the corpus of an instability
with a mechanism and a targeted remedy rather than a hyperparameter
workaround — [LIT-155](LIT-155.md) did it for attention-logit growth, which [SOTA-131](../practices.d/SOTA-131.md)
records. The pattern worth carrying is that these failures have causes, and
the cause tells you which of several remedies is the cheap one.

Filed via the reference pass in [#40](https://github.com/dmarx/anthology-of-the-sota/issues/40), from Kimi K3 §2.1.2.
