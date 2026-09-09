---
number: 89
status: 'Active'
title: 'Align tensor dimensions to hardware boundaries'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
published: '2020-06-01'
source:
- LIT-066
compared_against:
- SOTA-107
summary: >-
  Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).
---

# SOTA-089: Align tensor dimensions to hardware boundaries

## Source

Ivanov et al. (2020), [LIT-066](../literature.d/LIT-066.md) — [ARXIV-2007.00072](https://arxiv.org/abs/2007.00072).

## What alignment buys

Memory systems and tensor cores both move data in fixed units — cache lines,
128-byte transactions, matrix tiles of a fixed shape. A dimension that is not
a multiple of the unit means every access straddles a boundary or the final
tile is partly wasted, and on a memory-bound workload ([LIT-066](../literature.d/LIT-066.md)'s central
claim) that is the cost that matters rather than the arithmetic.

The familiar cases are a vocabulary size or a hidden dimension a few elements
short of a round number: padding 50,257 to 50,304 costs a rounding error's
worth of parameters and can measurably change throughput, because the padded
shape maps onto the hardware's tiles and the original does not.

## What the practice does not say, and should

Which boundary. It differs by operation and device — the tensor-core tile,
the vector width, the cache line — and the numbers that circulate (8, 64,
128) come from specific hardware generations rather than from a principle.
<!-- inactive-ok-block: SOTA-107 — Rejected in #114 for exactly this, which sharpens rather than weakens the comparison -->
This is the same gap as [SOTA-107](SOTA-107.md)'s "multiple of 128", which was retired in
[#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) once its source was read: a real effect, a constant that belongs to an
implementation, and a record stating it as though it were general. That one
turned out to be a *head dimension* restated as a sequence length, which is
the failure this practice should be checked for next.

The other half is that alignment is a *design-time* choice. Hidden sizes and
vocabulary are fixed before training starts, so unlike layout ([SOTA-090](SOTA-090.md)) or
fusion ([SOTA-088](SOTA-088.md)) this cannot be fixed by tuning afterwards — which is the
reason it is worth knowing early and the reason it rarely gets checked.
