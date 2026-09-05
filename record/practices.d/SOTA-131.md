---
status: Active
title: 'When training with Muon at scale, rescale query and key weights whenever attention logits exceed a threshold (QK-Clip)'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2025-07-01'
source: LIT-132
summary: >-
  Kimi Team (2025), [LIT-132](../literature.d/LIT-132.md) — MuonClip carried a 1T/32B MoE through 15.5T tokens with zero loss spikes where plain Muon let attention logits pass 1000; confirmed at 2.8T in [LIT-131](../literature.d/LIT-131.md).
---

# SOTA-131: When training with Muon at scale, rescale query and key weights whenever attention logits exceed a threshold (QK-Clip)

## Source

Kimi Team (2025), [LIT-132](../literature.d/LIT-132.md) — the Kimi K2 report.

Muon with weight decay and RMS-matched updates ([SOTA-121](SOTA-121.md)) is enough at small
scale. At a trillion parameters the K2 team found it drives the maximum
attention logit past 1000 early in training, and logits of that size bring
loss spikes and occasional divergence. QK-Clip is the addition: after each
step, for any head whose maximum logit exceeds a threshold, rescale that
head's query and key projection weights so it does not. The clip acts on
weights, so the served model is unchanged, and it fires only where needed.
With it, K2 trained on 15.5T tokens without a single loss spike; K3
([LIT-131](../literature.d/LIT-131.md)) keeps the same optimizer at 2.8T.

Conditions: the failure this prevents is a large-scale one. [LIT-119](../literature.d/LIT-119.md) trained
90M and 0.6B models with Muon and no clipping and reports stable runs, so
the clip is insurance whose premium is a per-head max-logit check per step —
cheap, but not free, and unnecessary until the logits say otherwise. The
threshold is a hyperparameter; the report's value is tuned for its model.

## Variations

DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) pretrains 1.6T and 284B MoE models with Muon and,
per secondary coverage of its report, without QK-Clip — the RMSNorm it
already applies to queries and to the compressed KV entries is said to
bound the logits on its own. If that reading holds, the clip is one of two
ways to the same invariant, and QK-normalisation is the other.

## Sequence

Muon (a 2024 blog post, not in the record) → weight decay and RMS matching
so AdamW's hyperparameters transfer ([LIT-122](../literature.d/LIT-122.md), [SOTA-121](SOTA-121.md)) → QK-Clip so the
attention logits stay bounded at scale (this practice) → [LIT-131](../literature.d/LIT-131.md) reports a
per-head variant of Muon on top. Each step keeps the one before.

## Known implementations

- Kimi K2, Kimi K3 (QK-Clip); DeepSeek-V4 (Muon with QK-norm, no clip, reported)
