---
status: Active
title: 'Train sparse attention natively with a learned top-k indexer, warmed up under dense attention'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2025-12-01'
source:
- LIT-142
summary: >-
  DeepSeek-AI (2025), [LIT-142](../literature.d/LIT-142.md) — a small FP8 indexer scores past tokens and only the top-k enter attention; initialised for 2.1B tokens with dense attention on and the rest frozen; V4 repeats the pattern with a 1T-token dense warm-up.
---

# SOTA-138: Train sparse attention natively with a learned top-k indexer, warmed up under dense attention

## Source

DeepSeek-AI (2025), [LIT-142](../literature.d/LIT-142.md) — DeepSeek-V3.2.

Make the sparsity a trained part of the model, not a serving-time
approximation. A lightning indexer — few heads, FP8 — scores each query
against every preceding token; only the top-k key-value entries enter the
attention. Before switching it on, warm the indexer up with dense attention
still active and every other parameter frozen (V3.2: 1,000 steps × 16
sequences × 128K tokens, 2.1B tokens), then continue training sparse.
DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) keeps the shape at 1M tokens — compressing the KV
cache along the sequence first, running the indexer over the compressed
entries, and warming up under dense attention for the first 1T tokens
before introducing sparsity at the 64K stage.

Conditions: two production generations from one laboratory, plus the
from-scratch evidence of NSA ([LIT-143](../literature.d/LIT-143.md)) that a natively trained sparse
attention matches full attention. The warm-up matters because an
uninitialised indexer selects noise; the length of the warm-up scaled from
2.1B tokens for a retrofit to 1T for pretraining. Evaluated at 64K–1M
contexts; below that the KV cache is not the bottleneck and the indexer is
overhead.

## Sequence

NSA ([LIT-143](../literature.d/LIT-143.md), February 2025): compression, selection and a sliding window,
trained from scratch → DSA (this practice, December 2025): one learned
indexer retrofitted by continued pretraining → CSA and HCA ([LIT-139](../literature.d/LIT-139.md), 2026):
compress, then index, with a heavily compressed dense branch beside it.

## Known implementations

- DeepSeek-V3.2, DeepSeek-V4-Pro, DeepSeek-V4-Flash
