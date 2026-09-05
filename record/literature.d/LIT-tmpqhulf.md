---
status: Active
title: 'Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset'
version: 1
tags:
- data-pipeline
date: '2026-09-05'
published: '2024-12-01'
arxiv: '2412.02595'
first_author: 'Su'
keywords:
- 'pretraining-data'
- 'filtering'
- 'synthetic-data'
- 'long-horizon-training'
- 'common-crawl'
implementations:
- Nemotron-CC
summary: >-
  Su et al. (2024), [ARXIV-2412.02595](https://arxiv.org/abs/2412.02595). Aggressive model-based filtering
  throws away 90% of the web, which is fine at 1T tokens and ruinous at 15T;
  classifier ensembling plus synthetic rephrasing keeps four times the unique
  tokens at the same quality.
---

<!-- inactive-ok-file: SOTA-124 — the Proposed practice, named as one of three answers to a finite corpus -->
# LIT-tmpqhulf: Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset

Su et al., NVIDIA (2024) — [ARXIV-2412.02595](https://arxiv.org/abs/2412.02595)

## Key takeaways

- The critique is of a method the field had just adopted. FineWeb-Edu and
  DCLM won benchmark gains through aggressive model-based filtering, **at the
  cost of removing 90% of the data** — which is a good trade at a short token
  horizon and a bad one at 15T tokens, where you run out of corpus.
- The alternative is three things together: ensembling classifiers rather
  than trusting one, **rephrasing text synthetically** instead of discarding
  it, and leaning less on heuristic filters.
- Short horizon: a high-quality subset improves MMLU by 5.6 over DCLM when
  training 8B models for 1T tokens.
- Long horizon, which is the point: the full 6.3T-token dataset **matches**
  DCLM on MMLU while containing four times more unique real tokens. An 8B
  model trained for 15T tokens, 7.2T of them from this dataset, beats Llama
  3.1 8B by +5 MMLU, +3.1 ARC-Challenge and +0.5 averaged over ten tasks.

## Standing in the anthology

The other side of the filtering trade-off from [LIT-tmpw2sm1](LIT-tmpw2sm1.md), and the pair is
the point: how hard to filter is not a quality question with one answer but a
question about the token horizon you are training to. Aggressive filtering
wins at 1T and loses at 15T, because the thing it optimises — mean quality —
is not the thing that binds when the corpus runs out.

It also connects to a disagreement the record already holds. [SOTA-124](../practices.d/SOTA-124.md) asks
when high-quality data may be *repeated*; this asks how much data stays
high-quality if you filter less; and [LIT-tmp7fu4d](LIT-tmp7fu4d.md) prices repetition against
unique tokens. All three are answers to "the corpus is finite" and none of
them cites the others.
