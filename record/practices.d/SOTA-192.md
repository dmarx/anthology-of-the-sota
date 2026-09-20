---
number: 192
status: Active
formerly:
- SOTA-tmp52hr5
consensus: converged
consensus_note: >-
  Standard in frontier training. DeepSeek-V4 runs Muon with QK-norm and no
  clip; the Kimi line takes the other route. The invariant is agreed, the
  instrument is not.
title: 'Normalize the queries and keys before the attention dot product'
version: 4
history:
- version: 2
  date: '2026-09-18'
  note: >-
    Adds `attention-techniques`. The practice normalizes queries and keys before the dot product; its relation to SOTA-131 joins two interventions on the same matrices (ADR-049).
- version: 3
  date: '2026-09-18'
  # inactive-ok-block: SOTA-168 — Proposed, and named only as a member of
  # the line this tag binds; nothing here rests on its standing
  note: >-
    Adds `training-optimization`. Normalizing queries and keys is a training-dynamics intervention, and it is the value shared by the line running through SOTA-121, SOTA-165 and SOTA-168 (ADR-049).
- version: 4
  date: '2026-09-20'
  note: >-
    Records an independent arrival. Esser et al. (LIT-449) adopt QK-norm
    for a high-resolution diffusion transformer after mixed-precision
    training diverged, diagnosing it through the discriminative ViT
    literature's attention-entropy result rather than through anything in the
    language-model line this practice was filed from. Neither line cites the
    other. The recommendation is unchanged; what is added is that the
    invariant now has two arrival events from two different failures.
tags:
- model-stability
- attention-techniques
- training-optimization
date: '2026-09-10'
source:
- LIT-088
introduced_by:
- LIT-088
extends:
- SOTA-050
compared_against:
- SOTA-131
implementations:
- LIT-088
- LIT-139
---

# SOTA-192: Normalize the queries and keys before the attention dot product

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

## A third arrival, from generative modelling

The two routes above are both from language-model training. A third arrives
from image synthesis and does not cite either: Esser et al., [LIT-449](../literature.d/LIT-449.md),
found that mixed-precision training of an 8B diffusion transformer **diverged
when moving to high resolution**, took the diagnosis from the discriminative
ViT literature — attention entropy growing without bound — and fixed it with
RMSNorm on Q and K in both streams of their architecture.

Same intervention, same invariant, a failure mode the language-model line
never reports, and no citation in either direction.

[DP-007](../principles.d/DP-007.md) says agreement has no author and therefore no arrival event.
This is the interesting variant: there are two arrival events, in different
literatures, and the record can see both only because it files by the kind of
claim rather than by the domain the claim was found in ([ADR-026](../decisions.d/ADR-026.md)).

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
