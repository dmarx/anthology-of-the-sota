---
status: 'Active'
title: 'Prefer GQA to MQA or MHA'
version: 2
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
tags:
- attention-techniques
date: '2026-08-24'
published: '2023-05-01'
source:
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

Grouped-query attention interpolates: partition the query heads into groups
and give each group its own key/value head. The cache shrinks by the group
factor rather than by the head count, and the quality loss largely goes away.
It can also be *uptrained* from an existing multi-head checkpoint, which is
why it spread as fast as it did — adopting it did not require pretraining
from scratch.

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
