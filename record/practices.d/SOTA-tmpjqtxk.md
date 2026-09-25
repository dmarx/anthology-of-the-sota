---
status: Proposed
consensus: unreplicated
consensus_note: >-
  One group, two FLOP budgets up to 1.3B-equivalent, one run per
  configuration. The record holds no other byte-level or tokenizer-free
  model. BPE remains the default everywhere the record looks (SOTA-007). Read
  as of 2026-09.
promote_when: >-
  A second group reproduces the matched comparison, with bytes per batch and
  FLOPs per byte both matched, two-stage learned chunking against a modern
  BPE tokenizer (not GPT-2's), at 3B-equivalent FLOPs or more, and reports
  wall-clock. More reports that byte models are robust to typos would not
  count, because every byte model is.
title: 'To drop the tokenizer without losing to BPE, use a two-stage hierarchy with learned chunk boundaries and SSM encoder and decoder layers, not an isotropic byte model'
version: 1
tags:
- representation-and-encoding
- model-architecture
date: '2026-09-25'
source:
- LIT-tmp959vc
introduced_by:
- LIT-tmp959vc
implementations:
- 'H-Net'
summary: >-
  Hwang, Wang and Gu (2025), [LIT-tmp959vc](../literature.d/LIT-tmp959vc.md). A byte-level model that must not
  lose to a BPE Transformer at matched data and FLOPs should be hierarchical.
  Isotropic byte stacks lose by about 9 downstream points. It should use
  Mamba-2 layers for the encoder and decoder around the main network, and it
  should learn its chunk boundaries across **two** stages. One learned stage
  only ties BPE and whitespace chunking. Expect about 2× slower training.
---

# SOTA-tmpjqtxk: To drop the tokenizer without losing to BPE, use a two-stage hierarchy with learned chunk boundaries and SSM encoder and decoder layers, not an isotropic byte model

## Source

Hwang, Wang and Gu (2025), [LIT-tmp959vc](../literature.d/LIT-tmp959vc.md).

## What to do

If you want a tokenizer-free model:

1. **Do not use an isotropic byte-level stack.** At matched FLOPs, LlamaByte and
   MambaByte trail a BPE Transformer by about 9 points of downstream average.
2. **Go hierarchical.** Put a byte encoder and decoder around a main network
   that runs on chunks. Make the encoder and decoder SSM (Mamba-2) layers. The
   source finds this better than attention in a way that increases with the
   Mamba share, even on BPE inputs.
3. **Learn the boundaries, with smoothing,** and use **two stages**. One learned
   stage performs like whitespace chunking, which performs like BPE. The second
   stage is where the gain appears: 0.715 against 0.730 bits/byte at 1.3B
   FLOPs.

## Why

A fixed tokenizer commits to one segmentation before training, and it
compresses unevenly across languages and domains. Learned chunking lets the
model choose its units: whitespace-like at the first stage, multi-word units
at the second. The gain is largest where BPE's segmentation fits worst, which
is Chinese in the source.

## Conditions

- **Up to 1.3B-equivalent FLOPs, one seed per configuration.** The source says
  it "remains to validate H-Net at larger model sizes".
- **About 2× slower training in wall-clock** at matched FLOPs, and more
  parameters at matched FLOPs.
- **The English baseline is GPT-2's tokenizer.** A modern BPE vocabulary might
  close some of the gap. On code the learned chunks only tie whitespace
  chunking.
- **Stability measures are part of the recipe**: norms at sub-network ends and
  per-stage learning-rate multipliers. Without the smoothing module the
  compression ratio "fluctuate[s] severely".

## Known implementations

- H-Net, the source's code and checkpoints.
