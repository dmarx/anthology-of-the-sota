---
number: 23
status: 'Superseded'
title: 'Use multi-query attention for decoder-only models to reduce memory bandwidth'
version: 2
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Superseded by SOTA-109. Use multi-query attention had stood Active beside
    "Prefer GQA to MQA or MHA", so the record advised both at once; grouped-
    query attention keeps most of the cache saving without the quality cost.
    Attribution corrected in the same pass: the source is Shazeer (2019),
    not "Dao et al." as the migrated stub said.
superseded_by:
- SOTA-109
tags:
- inference-optimization
date: '2026-08-24'
published: '2019-11-01'
source:
- LIT-024
summary: >-
  Shazeer (2019), [LIT-024](../literature.d/LIT-024.md) — [ARXIV-1911.02150](https://arxiv.org/abs/1911.02150).
---

# SOTA-023: Use multi-query attention for decoder-only models to reduce memory bandwidth

## Source

Shazeer (2019), [LIT-024](../literature.d/LIT-024.md) — [ARXIV-1911.02150](https://arxiv.org/abs/1911.02150).

## Superseded

Grouped-query attention ([SOTA-109](SOTA-109.md)) replaced this. GQA gives each
*group* of query heads its own key/value head rather than sharing one across
all of them, which keeps most of multi-query attention's cache saving without its quality
cost, and can be uptrained from a multi-head checkpoint.

This stood as `Active` alongside [SOTA-109](SOTA-109.md)'s "prefer GQA to MQA
or MHA", so the record advised both at once. The body stays; only the status
moved.
