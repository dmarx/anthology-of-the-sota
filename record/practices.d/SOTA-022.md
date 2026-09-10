---
number: 22
status: Superseded
superseded_by: SOTA-004
status_note: >-
  a duplicate of SOTA-004, which states the same placement rule from batch
  normalization's own paper. The two arrived in the same import from
  different notes and have coexisted since; SOTA-004 is the one with the
  originating source
title: 'Place BN after linear/conv layers but before activation functions'
version: 1
tags:
- model-stability
date: '2026-08-24'
source:
- LIT-015
summary: >-
  Santurkar et al. (2018), [LIT-015](../literature.d/LIT-015.md) — [ARXIV-1806.02375](https://arxiv.org/abs/1806.02375).
---

# SOTA-022: Place BN after linear/conv layers but before activation functions

## Source

Santurkar et al. (2018), [LIT-015](../literature.d/LIT-015.md) — [ARXIV-1806.02375](https://arxiv.org/abs/1806.02375).

## The same practice as [SOTA-004](SOTA-004.md)

Same recommendation, same words, different citation: [SOTA-004](SOTA-004.md) carries it from
[LIT-002](../literature.d/LIT-002.md), the paper that introduced batch normalization and stated the
placement; this one carries it from [LIT-015](../literature.d/LIT-015.md), which is about learning rates and
does not argue placement at all.

Superseded rather than rejected, because the recommendation is correct and
still in force — it is held by [SOTA-004](SOTA-004.md), and a reader arriving here should go
there. Retiring it as wrong would misrepresent what happened, which was a
duplicate import rather than a mistaken belief.

Worth recording how it survived: two practices with near-identical titles, in
a registry with no check for that, cited to two different papers so nothing
about their sources looked alike either.
