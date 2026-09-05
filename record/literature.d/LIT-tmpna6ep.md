---
status: Active
title: 'Small-scale proxies for large-scale Transformer training instabilities'
version: 1
tags:
- model-stability
date: '2026-09-05'
published: '2023-09-01'
arxiv: '2309.14322'
first_author: 'Wortsman'
keywords:
- 'training-stability'
- 'attention-logits'
- 'qk-norm'
- 'z-loss'
- 'learning-rate-sensitivity'
summary: >-
  Wortsman et al. (2023), [ARXIV-2309.14322](https://arxiv.org/abs/2309.14322). Instabilities reported only at
  frontier scale reappear in small models trained at high learning rate, and
  the large-scale mitigations work there too — which makes instability
  something a small budget can study.
---

# LIT-tmpna6ep: Small-scale proxies for large-scale Transformer training instabilities

Wortsman et al. (2023) — [ARXIV-2309.14322](https://arxiv.org/abs/2309.14322)

## Key takeaways

- The methodological move that makes the rest possible: instabilities that
  teams report at large scale, and that do not appear at small scale with the
  same hyperparameters, **do** appear at small scale when the learning rate
  is pushed. Sweeping learning rate against loss across model sizes turns a
  phenomenon that cost a frontier run to observe into one a small budget can
  reproduce.
- Two known instabilities are studied this way: growth of the logits in
  attention layers, and divergence of the output logits from the log
  probabilities. The mitigations used at scale — QK-norm for the first, a
  z-loss for the second — are equally effective in the small-scale regime,
  which is the evidence that the proxy is measuring the same thing.
- With that proxy, other interventions can be asked the same question: how
  much does warm-up, weight decay, or µP change the *sensitivity of the final
  loss to the learning rate*? Combining them trains small models that hold
  their loss across orders of magnitude of learning-rate variation.
- Two instabilities are shown to be predictable **before** they emerge, by
  extrapolating the scaling behaviour of activation and gradient norms — the
  case for tracking norms as an early-warning signal rather than as
  post-mortem evidence.

## Standing in the anthology

The mechanism under the record's attention-logit practices. [SOTA-131](../practices.d/SOTA-131.md) records
QK-Clip, which rescales query and key weights when a head's logits exceed a
threshold; this is the paper establishing that attention-logit growth is a
distinct failure mode with a normalization remedy, and that the remedy is
testable without a frontier budget. It is also the background for
DeepSeek-V4 declining QK-Clip on the grounds that an RMSNorm on queries and
compressed KV entries already bounds the logits ([LIT-139](LIT-139.md)) — same diagnosis,
normalization instead of clipping.

It also supports [SOTA-070](../practices.d/SOTA-070.md) and [SOTA-099](../practices.d/SOTA-099.md), which ask for gradient-norm statistics
to be tracked: this is where the claim that those norms are *predictive*
rather than merely diagnostic comes from.
