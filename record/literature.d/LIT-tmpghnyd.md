---
status: Active
title: 'MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation'
version: 1
tags:
- in-context-learning
- analysis-and-evaluation
date: '2026-09-21'
published: '2026-05-30'
arxiv: '2606.00610'
first_author: 'Wu'
keywords:
- 'graphrag'
- 'retrieval-augmented-generation'
- 'knowledge-graph-construction'
- 'recall-relevance-tradeoff'
- 'multi-agent'
- 'personalized-pagerank'
implementations: []
summary: >-
  Wu, Xiang, Tang, Chen, Zhang and Su (2026), [ARXIV-2606.00610](https://arxiv.org/abs/2606.00610). A
  multi-agent GraphRAG system, filed for its **pilot study** rather than its
  system: across three published GraphRAG pipelines, graph expansion raises
  retrieval recall (GFM-RAG **84.3%** against vanilla RAG's 71.8%) and drops
  relevance (**38.5%** against 62.9%), and end-task accuracy falls with it.
  Their own filtering probe finds **40% of extracted triples** can be deleted
  without cost.
---

# LIT-tmpghnyd: MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation

Wu, Xiang, Tang, Chen, Zhang and Su (2026) —
[ARXIV-2606.00610](https://arxiv.org/abs/2606.00610), read as [NOTE-tmp73iuw](../notes.d/NOTE-tmp73iuw.md).
KDD 2026.

## Key takeaways

- **The pilot study measures a trade-off in other people's systems**, which is
  why it is the part worth keeping. On G-Medical, GraphRAG pipelines beat
  vanilla RAG on recall (GFM-RAG 84.3% vs 71.8%) and lose badly on relevance
  (38.5% vs 62.9%), and the noisier context costs generation accuracy. The
  authors are proposing a GraphRAG system, so this is a finding against their
  own family's interest.
- **Forty per cent of a constructed graph is free to delete.** Filtering
  triples by schema frequency and dropping the bottom 40% moves accuracy from
  64.85% to 65.28%. The paper reads that as evidence of "thematically
  irrelevant noise"; the number itself supports a cost claim more strongly
  than an accuracy one — 0.43 points is small, and *nothing lost* across a 40%
  reduction is the result.
- **Three named failure modes of isolated local extraction**: thematic
  irrelevance (no global view of corpus theme), logical inconsistency
  (mutually exclusive, temporal and granularity conflicts between
  independently extracted chunks) and structural fragmentation (entities
  duplicated across disconnected subgraphs because coreference is never
  resolved globally).
- **The system:** a three-tier global memory (ontology, fact, passage) with
  three agents (extract, detect conflicts, resolve conflicts), schema
  promotion gated on frequency `Freq(s) ≥ τ`, and Personalized PageRank at
  retrieval. Headline average 59.68 against LazyGraphRAG's 44.97, and
  retrieval latency **0.061 s** against LightRAG's 11.052 s.

## Standing in the anthology

Filed for [SOTA-tmp7wp0k](../practices.d/SOTA-tmp7wp0k.md), which rests on the pilot study.
**No practice rests on MemGraphRAG itself**, and the reading says why at
length: single runs, no seeds, the authors' own system against baselines they
ran, and a transferability claim whose deltas are sub-point.

That last one is worth naming here because it is the paper's weakest passage
and its strongest verbs. §5.4 replaces four systems' graph constructors with
this one and reports HippoRAG 51.07 → 51.78 and MS-GraphRAG 43.75 → 44.21 —
under a point, one run each — as "consistent improvement" that "substantially
strengthens the effectiveness of existing retrievers". Having just filed
[SOTA-307](../practices.d/SOTA-307.md) on seed variance in a neighbouring field, the
record is not in a position to take sub-point single-run deltas at their
framing.

The corpus holds [SOTA-269](../practices.d/SOTA-269.md) — keep a knowledge base outside the
weights — and nothing about how to *build* or *evaluate* one. This is the
first document in that space, and it arrives as a caution rather than a
method.
