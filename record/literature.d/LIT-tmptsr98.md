---
status: Active
title: 'The Truth is in There: Improving Reasoning in Language Models with Layer-Selective Rank Reduction'
version: 1
tags:
- inference-optimization
- analysis-and-evaluation
date: '2026-09-22'
published: '2023-12-21'
arxiv: '2312.13558'
first_author: 'Sharma'
keywords:
- 'rank reduction'
- 'LASER'
- 'higher-order components'
- 'reasoning'
- 'post-training intervention'
implementations: []
summary: >-
  Sharma, Ash and Misra (2023), [ARXIV-2312.13558](https://arxiv.org/abs/2312.13558) — replacing
  one weight matrix by a low-rank approximation, especially an MLP matrix in a
  later layer, can *improve* accuracy: GPT-J on CounterFact goes from 13.3% to
  **24.1%** off a single layer, with no retraining. The gains land on facts
  rare in the training corpus. Filed for the debate it anchors rather than
  read in full.
---

# LIT-tmptsr98: The Truth is in There: Improving Reasoning in Language Models with Layer-Selective Rank Reduction

Sharma, Ash and Misra (2023) —
[ARXIV-2312.13558](https://arxiv.org/abs/2312.13558).

## Key takeaways

- **Removing higher-order components can help.** LASER replaces `W` with its
  rank-`k` approximation in selected layers. GPT-J on CounterFact: 13.3% →
  **24.1%** from a single layer, no additional training or data.
- **Later-layer MLP matrices are where it works.**
- **The gains concentrate on rare facts.** Improvements fall
  disproportionately on information infrequent in the training corpus, and
  the intervention also buys robustness to paraphrase.
- **The proposed mechanism is noise cancellation.** Reconstructed from
  higher-order components alone, the matrix answers with generic
  high-frequency words or a wrong item of the right semantic type; combined
  with the low-order components these produce an "average answer" that is
  wrong.

## Standing in the anthology

**It is one pole of a disagreement that [LIT-tmpmftzj](LIT-tmpmftzj.md)
resolves.** Other work finds small singular values essential; this finds
removing them beneficial. The resolution is procedural rather than
substantive — LASER evaluates a pretrained model without fine-tuning, while
the work reporting the opposite fine-tunes first — and it reproduces both
outcomes in one experiment by varying only that order.

**Filed on a partial reading.** The abstract, introduction and the CounterFact
analysis were read; the reinforcement-learning results and the full benchmark
sweep were not. Nothing in this record cites it for more than the claim above
and its place in that debate.
