---
status: Active
title: 'Query-Key Normalization for Transformers'
version: 1
tags:
- attention-techniques
- model-stability
- training-optimization
date: '2026-09-24'
published: '2020-10-01'
arxiv: '2010.04245'
first_author: 'Henry'
keywords:
- 'qknorm'
- 'attention-normalization'
- 'softmax-saturation'
- 'low-resource-translation'
implementations: []
summary: >-
  Henry, Dachapally, Pawar and Chen (2020), [ARXIV-2010.04245](https://arxiv.org/abs/2010.04245). **The origin of
  QK-norm**, which thirty documents in this record name and `SOTA-192` recommends
  while sourcing an adopter. `ℓ₂`-normalize each query and key along the head
  dimension before the dot product, then scale by a **learnable parameter
  instead of dividing by √d** — so the temperature becomes a trained quantity
  rather than a constant. **+0.928 BLEU** averaged over five low-resource
  pairs.
compared_against:
- LIT-tmpqahee
---

# LIT-tmp5bev1: Query-Key Normalization for Transformers

Henry, Dachapally, Pawar and Chen (2020) — [ARXIV-2010.04245](https://arxiv.org/abs/2010.04245)

## Key takeaways

- **The technique, stated exactly.** Apply `ℓ₂` normalization along the head
  dimension of each query and key matrix before multiplying them, **then scale
  up by a learnable parameter instead of dividing by the square root of the
  embedding dimension.** Both halves matter and the second is the one that
  gets dropped in retellings.

- **The motivation is softmax saturation**, not stability at scale. The stated
  aim is to make the softmax "less prone to arbitrary saturation without
  sacrificing expressivity" — an expressivity argument about the attention
  distribution, arrived at from low-resource translation rather than from
  large-model training divergence.

- **The evidence is modest and clearly bounded.** +0.928 BLEU averaged over
  five low-resource translation pairs from the TED Talks corpus and IWSLT'15,
  against state-of-the-art bilingual benchmarks. Five language pairs at
  translation scale — not a claim about frontier pretraining, which is where
  the record's own practice now applies it.

- **It replaces a constant with a learned scalar**, which is the detail that
  makes `LIT-tmpqahee`'s measurement possible at all: because the temperature
  is learned by backpropagation, it can be read off a trained model and
  compared against what a theory would predict.

## Standing in the anthology

Filed as a **defect repair**. `SOTA-192`, `Active` and `converged`, recommends
normalizing queries and keys before the dot product — and carries
`source: LIT-088` and `introduced_by: LIT-088`, which is **ViT-22B**.

`LIT-088` says so itself: *"nothing in the record reads a source establishing
QK-norm. This is one of the earliest at scale."* One of the earliest **at
scale** is an adoption claim. ViT-22B did not introduce QK-norm; this paper
did, two and a half years earlier, for a different reason and at a different
scale.

**30 documents in this record name QK-norm.** `SOTA-192` recommends it,
`SOTA-131` rescales query and key weights under Muon, `SOTA-050` is what it
extends, and `LIT-449` records an independent arrival at it in diffusion
transformers. The technique is everywhere in the record and its origin was
not held.

`#290` promoted this identifier as candidate #7 with exactly that reasoning —
*"named origin of QK-norm; [LIT-088](LIT-088.md) uses it with no source for the
technique"* — and its promoted queue has not been worked: **21 of its 25
promotions are unfiled**, and this unit reached the paper through the re-read
of the same issue's *declines* rather than through the list that already
named the defect.

`introduced_by` is corrected to this paper in the same contribution. The
distinction `DP-005` draws is between evidence and adoption; this is the same
distinction applied to *origin*, and the record had the later, larger,
better-known paper in the slot.
