---
number: 25
status: 'Active'
title: 'Initialize LayerNorm weight close to 1 (0.97-1.0)'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2019-11-01'
source:
- LIT-025
summary: >-
  Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — [ARXIV-1911.07013](https://arxiv.org/abs/1911.07013).
compared_against:
- SOTA-051
---

# SOTA-025: Initialize LayerNorm weight close to 1 (0.97-1.0)

## Source

Xu et al. (2019), [LIT-025](../literature.d/LIT-025.md) — [ARXIV-1911.07013](https://arxiv.org/abs/1911.07013).

## What the initialisation controls

LayerNorm's learned scale multiplies the normalised activation, so its
initial value sets how much of the block's output reaches the residual
stream at step one. Starting at 1 is the identity: the normalised signal
passes through unchanged, and the network begins as the architecture without
the learned adjustment rather than with an arbitrary one.

The narrower range in the title — 0.97 to 1.0 — is a slight shrink below the
identity, which damps the residual contribution at initialisation in the same
direction as [SOTA-060](SOTA-060.md)'s scaled output projections and [SOTA-051](SOTA-051.md)'s near-zero
final layer. All three are the same instinct: start the residual branches
quiet and let training turn them up.

## Condition, and what the record cannot say

Whether the shrink is worth anything is not established here. Weight 1 is what
every framework initialises to and what almost every large run uses; the
record has no comparison showing 0.97 beats it, and [LIT-025](../literature.d/LIT-025.md)'s contribution is
an analysis of LayerNorm's gradients rather than a sweep over this constant.

So the safe reading is: **initialise to 1**, and treat the lower end of the
range as an untested variation rather than a recommendation. That is a
narrowing of the practice, and it is the honest one — the same shape as
[SOTA-078](SOTA-078.md)'s buffer and [SOTA-089](SOTA-089.md)'s alignment, where a real principle carries a
constant nobody in the record has grounds for.

RMSNorm, now the more common choice ([SOTA-006](SOTA-006.md)), keeps this scale and drops the
bias entirely, which makes [SOTA-026](SOTA-026.md) moot in most current models.
