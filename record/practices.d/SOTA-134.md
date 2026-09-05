---
status: Active
title: 'Gate each attention head''s output with a sigmoid after the scaled dot-product'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2025-05-01'
source:
- LIT-138
summary: >-
  Qiu et al. (2025), [LIT-138](../literature.d/LIT-138.md) — the best of 30 gating variants at 15B MoE and 1.7B dense over 3.5T tokens: better quality, more stable training, larger tolerable learning rates, no attention sinks; shipped in every Qwen full-attention layer since Qwen3-Next.
---

# SOTA-134: Gate each attention head's output with a sigmoid after the scaled dot-product

## Source

Qiu et al. (2025), [LIT-138](../literature.d/LIT-138.md) — Gated Attention.

Multiply each head's attention output by a learned, input-dependent sigmoid
gate before the output projection. In a controlled comparison of 30 ways to
gate softmax attention — on 15B mixture-of-experts and 1.7B dense models,
each trained for 3.5T tokens — this head-specific output gate was the
variant that consistently improved quality. It also made training more
stable, let it tolerate larger learning rates, improved scaling behaviour,
and removed the attention-sink pattern and the massive activations that
accompany it. The paper credits the non-linearity it inserts between the
value and output projections and the sparsity it induces in the output.

Conditions: the ablation is one group's, but a large one, and the practice
has since shipped in production at several scales — Qwen3-Next's 80B-A3B
([LIT-136](../literature.d/LIT-136.md)), the Qwen3.5, 3.6 and 3.8 generations ([LIT-135](../literature.d/LIT-135.md)), and, on a
latent-attention base, apparently Kimi K3's gated MLA layers ([LIT-131](../literature.d/LIT-131.md)). The
cost is one sigmoid per head per token. Not to be confused with gating the
attention *scores*, which is among the variants that did not help.

## Known implementations

- Qwen3-Next, Qwen3.5, Qwen3.6-27B, Qwen3.8-27B; Kimi K3 (gated MLA)
