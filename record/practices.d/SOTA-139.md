---
status: Active
title: 'Extend the context length in stages during pretraining rather than training at the target length from the start'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2026-06-01'
source: LIT-139
summary: >-
  DeepSeek-AI (2026), [LIT-139](../literature.d/LIT-139.md) — 4K, then 16K, 64K and 1M over 32–33T tokens, with sparse attention introduced at the 64K stage; Kimi K3 ([LIT-131](../literature.d/LIT-131.md)) reaches 1M the same way.
---

# SOTA-139: Extend the context length in stages during pretraining rather than training at the target length from the start

## Source

DeepSeek-AI (2026), [LIT-139](../literature.d/LIT-139.md) — DeepSeek-V4.

Start pretraining at a short sequence length and lengthen it in stages:
V4 trains at 4K, then 16K, 64K and finally 1M tokens, and schedules its
architectural switch — sparse attention on — at the 64K stage. Kimi K3
([LIT-131](../literature.d/LIT-131.md)) reports the same shape of schedule to its own 1M window, adding
synthetic tasks that can only be solved by attending across the whole
window. The short stages are where most tokens are cheapest to process; the
long stages teach the position-dependent behaviour the target length needs.

Conditions: both sources are frontier-scale reports rather than controlled
comparisons against training at the target length throughout, and neither
publishes the token split per stage in the material read here. The
practice is stated because two independent laboratories converged on it
for million-token contexts; the stage boundaries and what to switch on at
each are the parts to tune.

## Known implementations

- DeepSeek-V4, Kimi K3
