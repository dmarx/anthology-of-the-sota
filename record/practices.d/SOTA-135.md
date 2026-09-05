---
status: Active
title: 'Give linear-attention layers a gated delta rule: a decay gate for erasure plus a delta update for targeted writes'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2024-12-01'
source:
- LIT-137
summary: >-
  Yang et al. (2024), [LIT-137](../literature.d/LIT-137.md) — beats Mamba2 and DeltaNet across language modelling, retrieval and long context at 1.3B/100B; the recurrence the Qwen hybrids use for three layers in four, and the one Kimi Delta Attention extends.
---

# SOTA-135: Give linear-attention layers a gated delta rule: a decay gate for erasure plus a delta update for targeted writes

## Source

Yang et al. (2024), [LIT-137](../literature.d/LIT-137.md) — Gated DeltaNet.

A linear-attention layer keeps a fixed-size state and has to manage it. A
decay gate, as in Mamba2, lets the state forget fast; the delta rule, as in
DeltaNet, overwrites one key's association without disturbing the others.
The gated delta rule does both in one recurrence, and a chunkwise parallel
algorithm keeps it hardware-efficient. At 1.3B parameters on 100B tokens
it consistently beat both parents on language modelling, commonsense
reasoning, in-context retrieval, length extrapolation and long-context
understanding, and the paper's own hybrids with sliding-window attention or
Mamba2 layers did better still.

Conditions: on its own the layer still trails full attention on exact
retrieval, which is why every production use interleaves it with global
attention ([SOTA-132](SOTA-132.md)). The paper's evidence is at 1.3B; the production
evidence is the Qwen line from Qwen3-Next's 80B-A3B ([LIT-136](../literature.d/LIT-136.md)) to the dense
Qwen3.8-27B ([LIT-135](../literature.d/LIT-135.md)).

## Sequence

DeltaNet and Mamba2 → the gated delta rule (this practice) → Kimi Delta
Attention ([LIT-133](../literature.d/LIT-133.md)), which replaces the scalar decay with a channel-wise
one and is what Kimi K3 uses. Each keeps the delta update; the variation is
in how the state forgets.

## Known implementations

- Qwen3-Next, Qwen3.5, Qwen3.6-27B, Qwen3.8-27B (Gated DeltaNet); Kimi Linear, Kimi K3 (as KDA)
