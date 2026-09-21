---
status: Active
title: 'Gemini: A Family of Highly Capable Multimodal Models'
version: 1
tags:
- analysis-and-evaluation
- multimodal-learning
- in-context-learning
date: '2026-09-21'
published: '2023-12-19'
arxiv: '2312.11805'
first_author: 'Gemini Team'
keywords:
- 'multimodal'
- 'benchmark evaluation'
- 'chain-of-thought'
- 'data contamination'
- 'MMLU'
implementations: []
summary: >-
  Gemini Team, Google (2023), [ARXIV-2312.11805](https://arxiv.org/abs/2312.11805) — held for its
  evaluation methodology rather than its models. Its appendices publish three
  things the record wanted: an MMLU sweep in which the **ordering against
  GPT-4 flips** depending on the inference procedure; a measurement of how
  cheaply a benchmark can be inflated (**100 fine-tuning steps** on
  HellaSwag-adjacent web extracts take Ultra to 96.0% at 1-shot); and a
  FLEURS ablation retraining without the benchmark's own training set. Read as
  [NOTE-tmp13fue](../notes.d/NOTE-tmp13fue.md).
---

# LIT-tmpgqsmp: Gemini: A Family of Highly Capable Multimodal Models

Gemini Team, Google (2023) — [ARXIV-2312.11805](https://arxiv.org/abs/2312.11805), read as
[NOTE-tmp13fue](../notes.d/NOTE-tmp13fue.md).

## Standing

**Filed for its evaluation appendices, not for its models.** On architecture
and data it says little a reader can act on — Transformer decoders, 32k
context, multi-query attention, a pretraining set of "web documents, books,
and code" plus image, audio and video. Nothing there is isolated and nothing
is reproducible. What is filed is Appendix 10.2 and the contamination
discussion in §5.1.

**It measures three things about benchmarking that the record wanted and did
not have**, each reported voluntarily by the party they embarrass. They are in
[NOTE-tmp13fue](../notes.d/NOTE-tmp13fue.md) and they support [SOTA-tmpecji3](../practices.d/SOTA-tmpecji3.md) and a second
source for [SOTA-197](../practices.d/SOTA-197.md).

**Which version was read.** arXiv v5 (updated 2025-05-09) as served by ar5iv;
the report was first posted 2023-12-19, and the `published:` date is the
original posting per the record's convention.

**The record already used Gemini as a subject without holding it.**
[LIT-383](LIT-383.md) evidences [SOTA-233](../practices.d/SOTA-233.md) on Gemini 1.0 Pro and 1.5 Flash, and until
now the report describing those models was absent — the same trunk gap
[#243](https://github.com/dmarx/anthology-of-the-sota/issues/243) was opened about.
