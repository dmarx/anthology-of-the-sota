---
number: 147
status: Active
formerly:
- SOTA-tmpjolsp
consensus: emerging
consensus_note: >-
  Two labs, four generations, no third adopter yet. DeepSeek has shipped it in
  every model since V2 (LIT-174, LIT-160, LIT-139) and Moonshot builds on it
  in both Kimi K3 and Kimi Linear (LIT-131, LIT-133). Llama, Qwen and Mistral
  still ship GQA, so this is spreading rather than arrived — and the record is
  recommending it slightly ahead of the field on the strength of the
  production numbers.
title: 'Compress the KV cache into one shared latent vector instead of sharing key and value heads'
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to the one work that ran the comparison. The Evidence section
    says it in as many words — "four generations of adoption rather than one
    result" — and then the field listed all four as support anyway. Under
    ADR-017 they are evidence about the field, and the consensus_note
    already carried them, so nothing is lost and the `emerging` reading is
    now countable against a list that means one thing. Neither the status
    nor the recommendation moves.
tags:
- attention-techniques
date: '2026-09-07'
published: '2024-05-01'
source:
# One comparison: LIT-174 ran MLA against the same team's dense 67B and
# reports a 93.3% smaller KV cache at 5.76x generation throughput. The four
# generations after it ship MLA without comparing it to anything, which this
# practice's own Evidence section calls "four generations of adoption rather
# than one result" — so they are consensus data (ADR-017), and the
# consensus_note already names every one of them.
- LIT-174
compared_against:
- SOTA-109
implementations:
- DeepSeek-V2
- DeepSeek-V3
- DeepSeek-V4
- Kimi K3
- Kimi Linear
summary: >-
  DeepSeek-AI (2024), [LIT-174](../literature.d/LIT-174.md) — Multi-head Latent Attention projects keys and
  values into a single low-rank latent and caches that, cutting the KV cache
  93.3% and raising maximum generation throughput 5.76× against the same
  team's dense 67B. Every DeepSeek model since is built on it.
---

# SOTA-147: Compress the KV cache into one shared latent vector instead of sharing key and value heads

The KV cache is what makes long-context serving expensive, and the field has
two answers to it.

[SOTA-109](SOTA-109.md) is the first: **share** key and value heads across
groups of query heads, so there are fewer of them to store. MLA is the second:
**compress** keys and values into one low-rank latent vector, cache that, and
project back up when attention runs. The cache stops scaling with head count
at all.

The distinction worth holding is what each gives up. GQA gives up head
diversity in the keys and values. MLA keeps every head distinct and gives up
storing them uncompressed. Neither gives up exact attention over all
positions — which is what separates both of them from the linear-attention
line ([SOTA-132](SOTA-132.md), [SOTA-135](SOTA-135.md)), where a fixed-size
recurrent state gives up exactness itself.

## The evidence

Against the same team's dense 67B ([LIT-174](../literature.d/LIT-174.md)):
**93.3% smaller KV cache**, 5.76× maximum generation throughput, 42.5% lower
training cost.

Then four generations of adoption rather than one result:

- [LIT-160](../literature.d/LIT-160.md) — DeepSeek-V3 at 671B.
- [LIT-139](../literature.d/LIT-139.md) — V4, with the sparse-attention indexer built on top of it.
- [LIT-131](../literature.d/LIT-131.md) — Kimi K3 gates it.
- [LIT-133](../literature.d/LIT-133.md) — Kimi Linear keeps MLA for the one layer in four that stays
  global, which is the layout [SOTA-132](SOTA-132.md) recommends.

That last one is the reason this practice was overdue: the record already
recommends a layout **defined in terms of MLA layers** while never having said
what an MLA layer is.

## Why `Active` but only `emerging`

`Active` because the production evidence is unusually strong for an
architecture choice — not one result but four models across two labs, at
scales from 236B to 1.6T, each of which could have dropped it and did not.

`emerging` because two labs is not the field. Llama, Qwen and Mistral ship
GQA, and no third group has adopted MLA. The record is recommending this
slightly ahead of consensus and the second axis is where it says so
([ADR-015](../decisions.d/ADR-015.md)).

## What this does not say

It does not retire [SOTA-109](SOTA-109.md). GQA remains the right default for
a model that is not paying MLA's implementation cost, which is most models —
the two are `compared_against` rather than one superseding the other.
