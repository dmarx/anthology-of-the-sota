---
status: Proposed
title: 'Attach learnable per-row and per-column multipliers to weight matrices so their norms are learned, not set by LR and WD'
version: 1
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source: LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Up to 20% relative gain on MMLU, BBH and GSM8K over a Muon baseline at 200 GT.
---

# SOTA-122: Attach learnable per-row and per-column multipliers to weight matrices so their norms are learned, not set by LR and WD

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

The claim, from [ARXIV-2601.04890](https://arxiv.org/abs/2601.04890) and validated in the blogpost at the 90M
scale: under a decoupled weight decay, a matrix layer settles into an
equilibrium norm determined by the learning rate and the weight decay
coefficient rather than by the data. Attaching a learnable scalar multiplier
to each row and each column of every weight matrix (the authors' *learnable
multipliers*, LRM) lets the norm be learned, and lets the forward multipliers
that µP would otherwise fix be learned too.

Evidence: two 200 GT runs (50 GT of decay), Muon alone against Muon with
LRMs, on the final 90M architecture. Improvements on most benchmarks, up to a
20% relative gain on MMLU, BBH and GSM8K. The authors then used LRMs for
every model in the series.

Why *Proposed* and not *Active*: one team, one architecture family, and the
larger-scale results live in the preprint rather than in this source. Promote
when an independent reproduction or a result above 1B lands in the record.

## Known implementations

- Falcon-H1-Tiny (all released checkpoints)
