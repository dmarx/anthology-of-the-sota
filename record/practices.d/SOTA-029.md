---
number: 29
status: 'Active'
title: 'Partition gradients and optimizer states (ZeRO-2) for larger models'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-027
introduced_by:
- LIT-027
extends:
- SOTA-028
summary: >-
  Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).
extended_by:
- SOTA-030
---

# SOTA-029: Partition gradients and optimizer states (ZeRO-2) for larger models

## Source

Rajbhandari et al. (2020), [LIT-027](../literature.d/LIT-027.md) — [ARXIV-1910.02054](https://arxiv.org/abs/1910.02054).

## The next 2×, still at no extra communication

A gradient, like an optimizer state, is only needed in full by the rank that
updates that slice. Partitioning it too takes the per-rank cost from
[SOTA-028](SOTA-028.md)'s 4Ψ + 12Ψ/N to 2Ψ + 14Ψ/N — about 8× below plain data parallelism
at large N.

Both figures are from LIT-027, which introduces gradient partitioning as
ZeRO-DP's second stage. In its worked example, a 7.5B-parameter model on
64-way data parallelism, stage 2 takes model state to 16.6 GB per GPU,
against 31.4 GB under stage 1 and 120 GB under plain data parallelism. It is
also the stage the paper ran at scale: ZeRO-100B is stage 2 plus ZeRO-R, and
trained models of up to 170B parameters on 400 GPUs.

The property that matters is the one it shares with ZeRO-1: **the
communication volume is unchanged.** The reduce-scatter that stage 1 already
performs is exactly the operation that leaves each rank holding only its own
gradient slice, so stage 2 is closer to declining to keep something than to
doing extra work. LIT-027's communication analysis is the warrant: a
reduce-scatter of the gradients and an all-gather of the updated parameters
move Ψ + Ψ = 2Ψ per step, "exactly the same as the baseline DP".

## Condition

The gradients must be reducible in slices as they are produced, which is what
lets a bucket be scattered and the rest of the tensor released. Anything that
wants the whole gradient on one rank — a custom optimizer step, gradient
clipping computed from a global norm without an extra reduction — has to be
written to work from the partition instead.

Because the cost is the same as stage 1's, "for larger models" in the title
understates it: there is little reason to stop at stage 1 except tooling
support.
