---
status: 'Deferred'
title: '1-bit Adam: Communication Efficient Large-Scale Training with Adam''s Convergence Speed'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2021-02-01'
arxiv: '2102.02888'
first_author: 'Tang'
keywords:
- 'gradient-compression'
- 'adam'
- 'error-compensation'
- 'warmup'
implementations: []
summary: >-
  Tang et al. (2021), [ARXIV-2102.02888](https://arxiv.org/abs/2102.02888). Adam's variance term stabilizes early
  in training; freeze it after a warmup and the update becomes linear enough
  for error-compensated 1-bit compression to work.
---
# LIT-tmpvocam: 1-bit Adam: Communication Efficient Large-Scale Training with Adam's Convergence Speed

Tang et al. (2021) — [ARXIV-2102.02888](https://arxiv.org/abs/2102.02888)

## What it is

Adam's variance term stabilizes early in training; freeze it after a warmup
and the update becomes linear enough for error-compensated 1-bit compression
to work.

From the paper's own abstract:

> Scalable training of large models (like BERT and GPT-3) requires careful
> optimization rooted in model design, architecture, and system
> capabilities. From a system standpoint, communication has become a major
> bottleneck, especially on commodity systems with standard TCP
> interconnects that offer limited network bandwidth. Communication
> compression is an important technique to reduce training time on such
> systems.

## Standing in the anthology

`Deferred`, which here means what the vocabulary says: in the corpus, not
read closely enough to place. It arrived in the imported batch, which
brought in the communication-compression branch.

