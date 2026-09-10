---
number: 58
status: 'Active'
title: 'Use sequence parallelism for attention layers'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
source:
- LIT-043
summary: >-
  Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).
---

# SOTA-058: Use sequence parallelism for attention layers

## Source

Narayanan et al. (2021), [LIT-043](../literature.d/LIT-043.md) — [ARXIV-2104.04473](https://arxiv.org/abs/2104.04473).

## What it is that gets parallelised

Tensor parallelism splits the attention and MLP matmuls across devices, but
leaves the operations *between* them — layer norm, dropout, the residual add
— replicated on every rank, each holding a full copy of the activation. At
long sequence length those replicated activations are a large share of the
memory, and they are pure duplication.

Sequence parallelism splits those regions along the sequence dimension
instead, so each rank holds 1/*t* of them. The two schemes interlock: the
boundaries between a sequence-parallel region and a tensor-parallel one
become all-gather and reduce-scatter, which together cost the same traffic as
the all-reduce they replace.

That last property is what makes the practice nearly free, and it is the
reason to state it as a default rather than a trade.

## Condition

It only pays where the replicated activations are big, which means long
sequences and a tensor-parallel degree above one. On a job that is not using
tensor parallelism there is nothing to interlock with.

Like ZeRO's stages ([SOTA-028](SOTA-028.md)), the saving scales with the degree, so the
question is never "is this worth it" in isolation but "is it worth it at the
degree already chosen for other reasons".
