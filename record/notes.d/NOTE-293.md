---
number: 293
status: Read
formerly:
- NOTE-tmpsgjrr
paper: LIT-545
title: 'Gemma 3n'
version: 1
date: '2026-09-22'
summary: >-
  Per-Layer Embeddings: every token id indexes a table with one 256-d vector
  per layer, gated into the residual at each layer, about 2.35B parameters
  held off the accelerator. No measurements are published. Read from the
  model overview, the developer guide, and the Hugging Face `transformers`
  implementation, which is the only place the mechanism is fully specified.
---

<!-- inactive-ok-file: SOTA-326 — Proposed, filed in this same contribution from this paper's own ablations; new, not retired, and cited as the practice this document feeds -->

# NOTE-293: Gemma 3n

## Contribution

A deployment design, not a result. It moves a large, sparsely read block of
parameters out of accelerator memory and says the model is better for having
them. Before it, extra parameters kept outside the accelerator were a
serving trick applied to finished models. Here the architecture is built so
that a third or more of its parameters never need to be on the accelerator.

## Key insight

**A table indexed by token id can be fetched before the network runs.**
Attention and MLP weights are needed for every token. A row of an embedding
table is needed only for the tokens present, and which rows those are is
known from the input ids alone. So the table can sit in slow memory and be
prefetched, and its size adds almost nothing to per-token compute.

## Assumptions

- **On-device inference is the target.** The accelerator memory budget is
  the binding constraint, and host memory or flash is comparatively plentiful
- **The per-layer signal is worth having.** Every layer receives a
  token-identity signal, not only the first. Nothing published tests this
- Sources read: the model overview (`ai.google.dev/gemma/docs/gemma-3n`), the
  developer guide (Google Developers Blog, 2025-06-26), and
  `transformers/models/gemma3n/modeling_gemma3n.py` with its configuration
  file

## Key results

There are none in the measured sense. The published figures are:

- **E2B:** "over 5 billion parameters", runnable at "an effective memory
  load of approximately 1.91 billion" with PLE caching and parameter skipping
- **Accelerator-resident weights:** "approximately 2B for E2B and 4B for E4B"
- **Table size**, from the implementation defaults: `262,144 × (35 × 256)`,
  about 2.35B. The Gemma 4 report lists E2B's embedder at 400M plus 2,340M,
  consistent with the same design

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | PLE parameters can be held off the accelerator and fetched per token | strong | follows from the mechanism, and the documented memory figures are consistent with it |
| C2 | PLE "dramatically improves model quality" | weak | asserted in a blog post, no number or baseline |

## Method

From the implementation. Take token id `t` and layer `l`:

1. `e_t = PLE_table[t]`, reshaped to `(L, 256)`, scaled by `√256`
2. Add a projection of the ordinary input embedding, reshaped the same way
   and RMS-normalized, and multiply the sum by `1/√2`. Call the result `p_{t,l}`
3. Inside layer `l`, after attention and MLP:
   `r += RMSNorm(W_up · (act(W_gate · h) ⊙ p_{t,l}))`, with `W_gate` of
   shape `d → 256` and `W_up` of shape `256 → d`

The `+=` goes onto the AltUp side streams, not the one AltUp routes through
attention. That detail is specific to Gemma 3n's other components.

## Concepts

- **Effective parameters (E2B, E4B)** — the parameter count that has to be
  on the accelerator, not the total. "E2B" loads over 5B parameters in total

## Connections

It is one of several designs that add capacity as lookup tables rather than
as layers. The Qwen3.8-Flash-Next report ([LIT-152](../literature.d/LIT-152.md)) cites it with RWKV-8's
DeepEmbed, STEM and L3 for unigram lookup, and generalizes the key from a
token to an n-gram. It ships alongside MatFormer ([LIT-546](../literature.d/LIT-546.md)). Gemma 4 carries PLE forward in its two smallest models.

## Bearing on the record

- **[SOTA-326](../practices.d/SOTA-326.md)** counts this as adoption of off-accelerator embedding
  memory, not as evidence for it
- **`#163`'s description of PLE as the source of Qwen's n-gram embedding is
  too strong.** Qwen cites it for unigram memory and for offloading, and
  cites other work for n-grams

## Limitations

- **No paper and no ablation.** Nothing says how much of the quality comes
  from PLE and not from the other new components shipped with it (AltUp,
  LAuReL, MatFormer, activation sparsity)
- **The per-layer design is untested against the alternatives.** No
  comparison is published against one table at one layer, or against putting
  the same parameters into the backbone

## Open questions

- What a same-budget comparison of per-layer against single-layer tables
  would show. [LIT-152](../literature.d/LIT-152.md) shows two n-gram layers are no better than one, but
  that is n-gram tables at a fixed budget, not PLE
