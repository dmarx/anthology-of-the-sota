---
status: Active
consensus: converged
consensus_note: >-
  Standard in frontier training. DeepSeek-V4 runs Muon with QK-norm and no
  clip; the Kimi line takes the other route. The invariant is agreed, the
  instrument is not.
title: 'Normalize the queries and keys before the attention dot product'
version: 1
tags:
- model-stability
date: '2026-09-10'
source:
- LIT-088
extends:
- SOTA-050
compared_against:
- SOTA-131
implementations:
- ViT-22B
- DeepSeek-V4
---

# SOTA-tmp52hr5: Normalize the queries and keys before the attention dot product

## Source

Dehghani et al. (2023), [LIT-088](../literature.d/LIT-088.md) — ViT-22B, where the mechanism is diagnosed
rather than only fixed.

## The failure it prevents

Attention logits grow without bound as the query and key weights grow. Past some
point the softmax saturates and the failure is total: ViT-22B observed

> divergent training loss after a few thousand steps … caused by extremely large
> values in attention logits, which lead to (almost one-hot) attention weights
> with near-zero entropy

An almost-one-hot softmax has almost no gradient, so the layer stops learning
and the run diverges. The instability appeared at around **8B parameters** — it
is a scale phenomenon, absent below and fatal above.

## The fix

Apply a normalization to the queries and keys **before** the dot product:

    softmax[ (1/√d) · LN(XW_Q)(LN(XW_K))ᵀ ]

Bounding the norms of the two vectors bounds their inner product, so the logits
cannot grow with the weights. ViT-22B shows an 8B model diverging without it and
converging with it, everything else equal.

## Why `1/√d` is not enough

[SOTA-050](SOTA-050.md) already divides by `√d_head`, and that is the right correction for a
different problem: the dot product's variance grows with the **dimension**, so
the scale factor removes the dimension's contribution. It does nothing about the
**weights** growing during training. `1/√d` is a fix at initialisation;
QK-normalization is a fix that holds throughout.

## The other route to the same invariant

[SOTA-131](SOTA-131.md) (QK-Clip) rescales the query and key weights whenever the logits
exceed a threshold — the same invariant, enforced reactively on the weights
rather than structurally on the activations. The Kimi line uses the clip;
DeepSeek-V4 runs Muon with QK-norm and reports not needing it.

**Nobody has compared them.** The record now carries both, and which is
preferable — or whether the clip is only necessary when the normalization is
absent — is unresolved.

## Conditions

`LIT-088` is a **vision encoder**. The mechanism — logit growth, entropy
collapse, vanishing gradient — is architecture-independent and is the reason the
practice transfers, but the demonstration is not a decoder-only language model.
The corroboration on that side is [SOTA-131](SOTA-131.md)'s own body, which records DeepSeek-V4
using QK-norm in place of the clip.

Adds two normalization operations per attention layer. ViT-22B does not report
the cost separately.

## Known implementations

- ViT-22B; DeepSeek-V4 (with Muon, no clip)
