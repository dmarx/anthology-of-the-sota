---
number: 58
status: 'Active'
title: 'Use sequence parallelism for attention layers'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
# Was LIT-043 (Narayanan et al. 2021), which never mentions sequence
# parallelism; its nearest idea is the scatter/gather send optimisation
# between pipeline stages. Korthikanti et al. (2022) introduced and measured
# the scheme this body describes. Li et al. (2021) used the name earlier for
# a different scheme that replicates parameters on every device.
source:
- LIT-tmpfktcz
introduced_by:
- LIT-tmpfktcz
summary: >-
  Korthikanti et al. (2022), [LIT-tmpfktcz](../literature.d/LIT-tmpfktcz.md) — [ARXIV-2205.05198](https://arxiv.org/abs/2205.05198).
---

# SOTA-058: Use sequence parallelism for attention layers

## Source

Korthikanti et al. (2022), [LIT-tmpfktcz](../literature.d/LIT-tmpfktcz.md) — [ARXIV-2205.05198](https://arxiv.org/abs/2205.05198).

Korthikanti et al., [LIT-tmpfktcz](../literature.d/LIT-tmpfktcz.md), introduced the scheme and measured it. In
their accounting the replicated layer norms and dropouts are the `10sbh` term
of per-layer activation memory that tensor parallelism cannot divide; split
along the sequence, every term divides by the tensor-parallel degree. They
measure sequence parallelism and selective recomputation each cutting
activation memory roughly in half, about 5x together, and on one layer of a
22B model sequence parallelism alone takes the forward pass from 7.7 to
7.2 ms — a gain they note is smaller than it could be because a
reduce-scatter plus an all-gather executes slower than one all-reduce, though
it moves the same bytes. Narayanan et al. ([LIT-043](../literature.d/LIT-043.md)), cited here before, does
not mention sequence parallelism.

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
