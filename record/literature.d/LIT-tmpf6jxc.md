---
status: Active
title: 'What Can Transformers Learn In-Context? A Case Study of Simple Function Classes'
version: 1
tags:
- in-context-learning
- analysis-and-evaluation
- model-architecture
date: '2026-09-22'
published: '2022-08-01'
arxiv: '2208.01066'
first_author: 'Garg'
keywords:
- 'in-context learning'
- 'function classes'
- 'linear regression'
- 'least squares'
- 'distribution shift'
implementations: []
summary: >-
  Garg, Tsipras, Liang and Valiant (2022), [ARXIV-2208.01066](https://arxiv.org/abs/2208.01066), NeurIPS 2022 —
  the setup that turned "how does in-context learning work" into a question
  with a checkable answer. A 9.5M-parameter GPT-2 trained from scratch on
  sequences of `(x, f(x))` pairs in-context-learns unseen linear functions at
  the accuracy of the optimal least-squares estimator, and sparse linear
  functions, two-layer ReLU networks and depth-4 decision trees at or above
  their task-specific algorithms. Read as [NOTE-tmptsb58](../notes.d/NOTE-tmptsb58.md).
---

# LIT-tmpf6jxc: What Can Transformers Learn In-Context? A Case Study of Simple Function Classes

Garg, Tsipras, Liang and Valiant (2022) — [ARXIV-2208.01066](https://arxiv.org/abs/2208.01066), NeurIPS 2022.
Read as [NOTE-tmptsb58](../notes.d/NOTE-tmptsb58.md).

## Key takeaways

- **A transformer can be trained from scratch to in-context learn a function
  class.** 12 layers, 8 heads, 256-dimensional embeddings, 9.5M parameters,
  500k steps at batch 64, trained only on sampled `(x, f(x))` sequences — no
  text, no pretrained initialization.
- **On linear functions in `d = 20` it matches ordinary least squares**, the
  optimal estimator for the problem, and keeps doing so under two kinds of
  distribution shift: between training prompts and inference prompts, and
  between the in-context examples and the query.
- **On harder classes it matches the algorithm built for each.** 3-sparse
  linear functions: 0.58 and 0.09 squared error at `k = 5` and `k = 10`
  against Lasso's 0.62 and 0.08 — and Lasso has no closed form, so the
  transformer is matching an iterative minimization in one forward pass.
  Also two-layer ReLU networks and depth-4 decision trees.
- **Curriculum learning is load-bearing for training cost**, starting on
  functions restricted to a low-dimensional subspace.

## Standing in the anthology

**It is the substrate the mechanism papers are built on.** Every later claim
in this cluster — [ARXIV-2212.07677](https://arxiv.org/abs/2212.07677), [ARXIV-2211.15661](https://arxiv.org/abs/2211.15661), [ARXIV-2310.17086](https://arxiv.org/abs/2310.17086) — trains
in this setup, on this task, in most cases on this exact architecture, and
measures against these baselines. The record held the claims' descendants
([SOTA-037](../practices.d/SOTA-037.md), [SOTA-038](../practices.d/SOTA-038.md)) and none of the substrate.

**It also supplies the objection to itself.** The model here is trained on the
ICL objective — the same restricted task family it is then tested on — which
is precisely the gap [ARXIV-2310.08540](https://arxiv.org/abs/2310.08540) later argues makes these results say
little about in-context learning in a model pretrained on text. That is an
argument about what the setup licenses, not a defect in the setup, and the
paper is careful about what it claims.
