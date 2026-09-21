---
number: 134
status: Active
title: 'Gate each attention head''s output with a sigmoid after the scaled dot-product'
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-191 and LIT-190 as well as LIT-138. The practice was
    filed claiming the gate removes the attention-sink pattern and the
    massive activations with it, while the record described neither; the
    notes arrived under #42 and the body says reading them changed what the
    claim means. Production shipments stay adoption. The recommendation is
    unchanged.
tags:
- attention-techniques
- numerics-and-precision
date: '2026-09-05'
source:
# LIT-138 ran the ablation. LIT-191 and LIT-190 are what the gate is claimed
# to remove — this practice was filed asserting it without the record holding
# either, and reading them changed what the claim means, which makes them
# evidence about it rather than background (ADR-017). The Qwen and Kimi
# shipments are adoption and stay in the conditions.
- LIT-138
- LIT-191
- LIT-190
# Added with the origin correction below: this paper did not only propose the
# gate, it measured it — BERT-base, OPT-125M and ViT-S/16, with the outlier
# metrics and the INT8 result. Small models, so it corroborates rather than
# leads, but it is evidence about the claim and belongs here (ADR-017).
- LIT-414
# CORRECTED. This practice was filed with `introduced_by: LIT-138`, which is
# where the evidence at scale is and NOT where the recommendation was first
# stated. Bondarenko et al. (2023) equation 5 is this gate, per-head, two
# years earlier — and Qiu et al. say so themselves: "The work most closely
# related to ours is Quantizable Transformers (Bondarenko et al., 2023) ...
# Building on these insights, we scale up gated attention models." ADR-017's
# split, applied: origin here, evidence in `source:`.
introduced_by:
- LIT-414
summary: >-
  Qiu et al. (2025), [LIT-138](../literature.d/LIT-138.md) — the best of 30 gating variants at 15B MoE and 1.7B dense over 3.5T tokens: better quality, more stable training, larger tolerable learning rates, no attention sinks; shipped in every Qwen full-attention layer since Qwen3-Next.
explained_by:
- THEORY-019
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
latent-attention base, Kimi K3's gated MLA layers ([LIT-131](../literature.d/LIT-131.md)) — at a different
granularity, which the K3 report is explicit about: "an input-dependent,
channel-wise full-rank output gate", where this paper's sweep settles on a
head-specific sigmoid. Same position in the block, same justification,
different width, and neither group has swept its choice against the other's.
The cost is one sigmoid per head per token. Not to be confused with gating the
attention *scores*, which is among the variants that did not help.

## Where this came from, corrected

This practice was filed crediting Qiu et al. (2025) with the recommendation.
That is where the evidence at scale is and it is not where the recommendation
was first stated. **Bondarenko et al. (2023), [LIT-414](../literature.d/LIT-414.md), equation 5, is this
gate** — `sigmoid(G(x)) ⊙ softmax(QKᵀ/√d)V`, with `G` defined per head and
parameterized by a single linear layer — proposed two years earlier, for the
same reason, and measured on BERT, OPT and ViT.

Qiu et al. are explicit about it:

> The work most closely related to ours is Quantizable Transformers
> (Bondarenko et al., 2023), which also finds that applying gating in softmax
> attention alleviates extreme attention concentration and outliers in hidden
> states ... Building on these insights, we scale up gated attention models.

So the correction is not a dispute with either paper; it is the record
catching up to what both of them say. `introduced_by:` now names the 2023
paper and `source:` keeps Qiu et al. first, because the 30-variant ablation at
15B over 3.5T tokens is what makes this an `Active` practice rather than a
`Proposed` one. That is precisely the split [ADR-017](../decisions.d/ADR-017.md) exists to record, and the
error it existed to prevent: with one field, every practice reads as though it
began with the paper it cites.

It also relocates the claim. The gate was not invented to improve quality; it
was invented to let a head do nothing so it would stop producing activation
outliers that break INT8 quantization. The quality gain Qiu et al. measured is
a *later* discovery about a mechanism introduced for quantizability, which is
a more interesting history than the one this practice previously told.

## What the sinks are, and why removing them is a benefit

This practice was filed claiming the gate removes "the attention-sink
pattern and the massive activations that come with it", and the record
described neither. Both now have notes, and read together they change what
the claim means.

An **attention sink** ([LIT-191](../literature.d/LIT-191.md)) is the consequence of a softmax that
cannot output zeros. Its scores are normalised to sum to one, so a head with
nothing it needs to attend to must still put its mass somewhere, and models
learn to dump the surplus on whatever every query can see — under causal
masking, the first few tokens, regardless of content. Replacing the first
four tokens with linebreaks barely moves perplexity; it is the position that
is doing the work. A **massive activation** ([LIT-190](../literature.d/LIT-190.md)) is how that gets
implemented: a handful of scalars running ~100,000× the median, at fixed
feature dimensions, behaving as constants rather than features — pin them at
their mean and the model is fine, zero them and it collapses. They ride
through the QKV projections and impose an implicit bias on an attention
mechanism that has no bias term.

So the sink is not a defect to be deleted. In an ungated model it is
**load-bearing**: evict those four KV entries and Llama-2-13B goes from 5.40
perplexity to 5158. What the gate does is make the pressure go away rather
than redirect it. A head that can scale its own output down has nothing to
shed, so there is no surplus mass to park.

That puts three findings in one line, which is the useful part. An explicit
learnable attention bias ([LIT-190](../literature.d/LIT-190.md)), a learnable sink token
([LIT-191](../literature.d/LIT-191.md)) and this output gate all eliminate the same phenomenon, and
all three work by giving the model a way to *not attend* that softmax alone
does not provide. Two of the three cost nothing in quality; this one
improves it, which is why it is the practice and they are the explanation.

The practical corollary: a model **without** this gate needs its sinks
protected. Anything that evicts early tokens — window attention, a rolling
KV cache, aggressive cache trimming — has to keep the first few entries or
retrain with a sink token.

## Known implementations

- Qwen3-Next, Qwen3.5, Qwen3.6-27B, Qwen3.8-27B; Kimi K3 (gated MLA)
