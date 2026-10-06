---
number: 109
status: 'Active'
title: 'Prefer GQA to MQA or MHA'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Body written and the attribution corrected: the migrated stub credited
    "Yang et al."; GQA is Ainslie et al., verified against arXiv. The claim is
    unchanged — GQA over MQA or MHA — but it now says why, and it is placed in
    the line rather than standing alone. SOTA-023 and SOTA-024 recommended the
    multi-query attention this replaced and had been Active beside it; they are
    Superseded here. MLA is named as the other live answer to the same problem,
    not as a successor.
- version: 3
  date: '2026-10-06'
  note: >-
    Adds a condition for models that will be context-extended. In 26
    controlled 7B runs (LIT-tmpnww11), fewer KV heads was monotonically worse
    for long-context extension, and GQA combined with sliding-window layers
    cost about 9 HELMET points where windows alone cost 1.1. The
    recommendation, status and consensus are unchanged.
tags:
- attention-techniques
date: '2026-08-24'
source:
- LIT-100
introduced_by:
- LIT-100
implementations:
- llama2
summary: >-
  Ainslie et al. (2023), [LIT-100](../literature.d/LIT-100.md) — group the query heads and give each group
  one key/value head: multi-query's cache saving without multi-query's quality
  loss, and uptrainable from an existing multi-head checkpoint. Still the
  default for a model not paying MLA's implementation cost.
compared_against:
- SOTA-147
---

# SOTA-109: Prefer GQA to MQA or MHA

Multi-head attention stores a key and a value per head, and that cache is what
makes long-context serving expensive. Multi-query attention
([LIT-024](../literature.d/LIT-024.md)) collapses it to one key/value head
shared by every query head — cheap, and it costs quality.

Grouped-query attention (Ainslie et al., 2023, [LIT-100](../literature.d/LIT-100.md)) interpolates:
partition the query heads into groups and give each group its own key/value
head. The cache shrinks by the group factor rather than by the head count, and
the quality loss largely goes away. It can also be *uptrained* from an existing
multi-head checkpoint — the paper's own subtitle, and the reason the design
spread as fast as it did, since adopting it did not require pretraining from
scratch.

## What this replaced

<!-- inactive-ok-block: SOTA-023, SOTA-024 — Superseded by this practice, and
     naming them is how the retirement is legible from the successor -->

[SOTA-023](SOTA-023.md) and [SOTA-024](SOTA-024.md) recommended multi-query
attention, from the same 2019 paper, and both are `Superseded` by this. They
had stood as `Active` beside this practice, so the record simultaneously
advised using MQA and preferring GQA to it. That is the contradiction this
version resolves; the bodies stay where they are, which is the point of
retiring by status.

## What this is not the end of

[SOTA-147](SOTA-147.md) is the other live answer to the same
problem — compress the cache into a latent instead of sharing heads. It is not
a successor: GQA stays the default for a model that is not paying MLA's
implementation cost, which is most of them. The two are `compared_against`,
and the record recommends both, for different situations.

## Condition: long-context extension

"The quality loss largely goes away" was measured at the training length.
Bertsch et al. ([LIT-tmpnww11](../literature.d/LIT-tmpnww11.md)) pretrained 26 7–8B models on identical data
and extended each to 64K with one recipe. Fewer KV heads was worse at 32K,
and more than Llama 3's eight was better, with the MLP widened to keep
parameters level. The interaction is the larger effect. Adding three-in-four
sliding-window layers cost 1.1 HELMET points without GQA and about 9 with
it, and the worst model in the pool combined GQA, windows and headwise QK
norm.

It is not a reason to drop GQA. The Llama 3 architecture uses eight KV
heads and was still among the best in that pool. The 16-head model at the
top also had the most parameters. The GQA rows are the one axis the paper
could not control for initialization, which by itself moves these scores by
about 2 points on average. What it changes is the combination. **GQA and
sliding-window layers each save KV cache, and together they cost long
context more than the sum of their parts.** A model meant to be extended
should not take both without measuring the cost early, and the paper finds
it shows up in a short extension run early in pretraining.
