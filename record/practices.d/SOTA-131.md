---
status: Active
title: 'When training with Muon at scale, rescale query and key weights whenever attention logits exceed a threshold (QK-Clip)'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2025-07-01'
source:
- LIT-132
# QK-Clip is added on top of Muon with decoupled weight decay and
# RMS-matched updates; the Sequence section below spells the same order out.
extends:
- SOTA-121
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

DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) pretrains 1.6T and 284B MoE models with Muon and
without QK-Clip, and the report says so in as many words: "The attention
architecture of DeepSeek-V4 series allows us to directly apply RMSNorm on
the attention queries and KV entries, which effectively prevents attention
logits from exploding. Consequently, we do not employ the QK-Clip technique
in our Muon optimizer." So the clip is one of two ways to the same
invariant, and QK-normalisation is the other — not a reading of secondary
coverage but the primary source's own account, under the heading "Avoiding
Exploding Attention Logits".

## Sequence

Muon ([LIT-159](../literature.d/LIT-159.md)) → weight decay and RMS matching
so AdamW's hyperparameters transfer ([LIT-122](../literature.d/LIT-122.md), [SOTA-121](SOTA-121.md)) → QK-Clip so the
attention logits stay bounded at scale (this practice) → [LIT-131](../literature.d/LIT-131.md) adds Per-Head
Muon on top, orthogonalizing each attention head's momentum block separately
so that heads with larger gradients stop dominating the shared update.
Each step keeps the one before.

## Mechanism

The failure QK-Clip answers is attention-logit growth, which
[LIT-155](../literature.d/LIT-155.md) established as a distinct instability with a normalization
remedy, and — the useful part — reproducible in small models at high
learning rate rather than only at the scale where it first cost someone a
run. That is also why [LIT-139](../literature.d/LIT-139.md) can decline QK-Clip: an RMSNorm on the queries
and compressed KV entries bounds the same quantity, so the choice is between
normalizing the input to the logit and clipping the weights after the fact.

## Known implementations

- Kimi K2, Kimi K3 (QK-Clip); DeepSeek-V4 (Muon with QK-norm, no clip)
