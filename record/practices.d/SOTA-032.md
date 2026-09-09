---
number: 32
status: Active
title: 'Put the layer normalization inside the residual block, before the sublayer'
version: 2
history:
# inactive-ok: LIT-029 — the retired duplicate, named as what this practice used to cite
- version: 1
  date: '2026-08-24'
  note: >-
    Filed by the migration as "Use pre-norm (RMSNorm) for transformer
    layers", sourced to LIT-029 — a duplicate note whose one-line summary
    attributed RMSNorm to Xiong et al. The practice inherited that
    conflation: it recommended two independent choices and cited a paper
    that supports one of them.
# inactive-ok: LIT-029 — the retired duplicate, named as what the split repointed away from
- version: 2
  date: '2026-09-08'
  note: >-
    Split. This practice is now the placement claim alone, sourced to the
    paper that argues it; the statistic is SOTA-182, sourced to
    Zhang and Sennrich. LIT-029 retired as a duplicate of LIT-114.
tags:
- model-stability
consensus: universal
date: '2026-08-24'
source:
- LIT-114
implementations:
- llama2
summary: >-
  Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745). Pre-LN: normalize the
  input to each sublayer rather than the sum after it, so the gradients near
  the output are well behaved at initialization.
---

# SOTA-032: Put the layer normalization inside the residual block, before the sublayer

## Source

Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745).

The original Transformer normalizes *after* the residual addition (Post-LN).
Xiong et al.'s mean-field analysis shows that this leaves the expected
gradients of parameters near the output layer large at initialization, which
is what makes early training fragile under a large learning rate. Moving the
normalization inside the residual branch, applied to the sublayer's input
(Pre-LN), removes that.

The condition worth carrying: the paper's argument is about *initialization*,
and its headline consequence is that Pre-LN models can be trained with no
warmup stage at all and reach comparable results in less time. The record
still recommends warmup in [SOTA-100](SOTA-100.md), which was written against a different
account of why warmup exists. [LIT-114](../literature.d/LIT-114.md) flags that tension; this practice does
not resolve it.

The trade Pre-LN makes is representational rather than numerical: the
residual stream is never renormalized, so later layers see a stream whose
magnitude grows with depth. That is the cost people cite when they revisit
Post-LN or hybrid placements, and it is why this is a placement recommendation
rather than a law.

Independent of the *statistic* — see [SOTA-182](SOTA-182.md). Pre-LN with centered
LayerNorm is what GPT-2 does.

## Known implementations

- llama2
