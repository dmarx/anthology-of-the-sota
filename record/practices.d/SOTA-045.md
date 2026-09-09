---
number: 45
status: 'Active'
title: 'Profile data loading separate from training'
version: 1
tags:
- data-pipeline
date: '2026-08-24'
published: '2020-07-01'
source:
- LIT-050
summary: >-
  Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).
---

# SOTA-045: Profile data loading separate from training

## Source

Mohan et al. (2020), [LIT-050](../literature.d/LIT-050.md) — [ARXIV-2007.06775](https://arxiv.org/abs/2007.06775).

## This is the paper's claim, not a tip from it

[LIT-050](../literature.d/LIT-050.md) measured nine models across three tasks and four datasets on
production cluster hardware and found training time **dominated** by data
stall — the GPU waiting for items to be fetched and preprocessed — in many of
them. The input pipeline had been the unexamined half of training time, and
it was unexamined because nothing in the usual instrumentation shows it.

That is why the practice is *separate* profiling rather than profiling. A
profiler total attributes the wait to whatever kernel happens to be on the
critical path, and a well-fed step and a starved one look alike in aggregate.
DS-Analyzer establishes the stall **differentially**: run again with the data
path removed — items served from memory, preprocessing skipped — and take the
difference. Anything else measures the symptom.

## What it costs, and when it stops mattering

An extra run per configuration, which is cheap next to the thing it finds.

The condition is that the pipeline touches storage or does per-item
decoding — image or audio decode, tokenisation on the fly, augmentation. A
job reading pre-tokenised token IDs from a memory-resident shard has no
meaningful stall to find, and this measurement will correctly report nothing.

The practice ranks above the other three in this cluster for a reason worth
stating: [SOTA-042](SOTA-042.md), [SOTA-043](SOTA-043.md) and [SOTA-044](SOTA-044.md) are mitigations, and applying a
mitigation to a bottleneck nobody measured is how the pipeline got ignored in
the first place.
